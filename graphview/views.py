from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from graphview.models import Recipe, Ingredient
from django.core.urlresolvers import reverse
from django.utils import timezone
import xml.etree.cElementTree as ET
import random

def get_data(request):
    limit = 5
    if ('requestID' in request.session):
        request.session['requestID'] += 1
    else:
        request.session['requestID'] = 1
    reqID = request.session['requestID']
    reqID = str(reqID) + '-'

    fields = ['color', 'country_of_origin']
    recipe = get_object_or_404(Recipe, recipe_name=request.META['HTTP_RECIPE'])
    suggestions = Recipe.objects.none()
    qs = Recipe.objects.exclude(id=recipe.id) 

    for field in fields:
        val = getattr(recipe, field)
        if val:
            d = {field: val}
            qs_ = qs.filter(**d)
            if qs_:
                suggestions = qs_

    count = suggestions.count()
    if count == 0:
        suggestions = qs.order_by('?')
    elif count < limit:
        suggestions = suggestions | qs.exclude(id__in=suggestions.values_list('id', flat=True)).order_by('?')[:limit-count]
    print suggestions

    cwidth = "60"
    cheight = "40"

    return HttpResponse("testText")

def add_recipe(request):
    error_text = ""
    return render(request, 'graphview/add_recipe.html', {
        'error_text': error_text
        })

def add_recipe_to_database(request):
    recipe_name = request.POST['recipe_name']
    color = request.POST['color']
    country_of_origin = request.POST['country_of_origin']
    ingredient1 = request.POST['ingredient1']
    new_recipe = Recipe(recipe_name=recipe_name, color=color, country_of_origin=country_of_origin)
    #new_recipe.save()
    #if ingredient already exists add to recipe
    #else add ingredient in database
    #possible needs some extra user input :/
    return HttpResponseRedirect(reverse(request, 'graphview:add_recipe'))

def all_recipes(request):
    recipe_list = get_list_or_404(Recipe.objects.all().values_list('recipe_name'))
    recipe_str_list = []
    for recipe in recipe_list:
        recipe_str_list.append(''.join(recipe[0]).encode("ascii"))
    return render(request, 'graphview/list_all.html', {
        'recipe_list': recipe_str_list,
        })

def random_recipe(request):
    recipe_list = get_list_or_404(Recipe.objects.all())
    recipe = ''.join(random.choice(recipe_list).recipe_name).encode("ascii")
    return HttpResponseRedirect(reverse('graphview:view', args=(recipe,)))

def view(request, recipe):
    return render(request, 'graphview/view.html', {
        'focusedNode': recipe,
        })
    
def question(request, question_num):
    if int(question_num) == 1:
        color_list = get_list_or_404(Recipe.objects.order_by('color').values_list('color').distinct())
        color_str_list = []
        for color in color_list:
            color_str_list.append(''.join(color[0]).encode("ascii"))
        return render(request, 'graphview/question.html', {
            'question': "What color is your food?",
            'question_num': question_num,
            'option_list': color_str_list,
            })
    if int(question_num) == 2:
        recipe_list = Recipe.objects.filter(color=request.session['color'])
        country_list = get_list_or_404(recipe_list.order_by('country_of_origin').values_list('country_of_origin').distinct())
        country_str_list = []
        for country in country_list:
            country_str_list.append(''.join(country[0]).encode("ascii"))
        return render(request, 'graphview/question.html', {
            'question': "What country is your food from?",
            'question_num': question_num,
            'option_list': country_str_list,
            })
    if int(question_num) == 3:
        recipe_list = Recipe.objects.filter(color=request.session['color'])
        recipe_list = recipe_list.filter(country_of_origin=request.session['country_of_origin'])
        ingredient_list = get_list_or_404(Ingredient.objects.filter(recipe=recipe_list).distinct())
        return render(request, 'graphview/question.html', {
            'question': "Which of these ingredients is in your food?",
            'question_num': question_num,
            'option_list': ingredient_list,
            })
    if int(question_num) == 4:
        recipe_list = Recipe.objects.filter(color=request.session['color'])
        recipe_list = recipe_list.filter(country_of_origin=request.session['country_of_origin'])
        recipe_list = recipe_list.filter(ingredients=Ingredient.objects.filter(ingredient_name=request.session['ingredient1']))
        ingredient_list = get_list_or_404(Ingredient.objects.filter(recipe=recipe_list).distinct())
        return render(request, 'graphview/question.html', {
            'question': "Which of these ingredients is in your food?",
            'question_num': question_num,
            'option_list': ingredient_list,
            })
    if int(question_num) == 5:
        recipe_list = Recipe.objects.filter(color=request.session['color'])
        recipe_list = recipe_list.filter(country_of_origin=request.session['country_of_origin'])
        recipe_list = recipe_list.filter(ingredients=Ingredient.objects.filter(ingredient_name=request.session['ingredient1']))
        recipe_list = recipe_list.filter(ingredients=Ingredient.objects.filter(ingredient_name=request.session['ingredient2']))
        recipe = ''.join(random.choice(recipe_list).recipe_name).encode("ascii")
        return HttpResponseRedirect(reverse('graphview:view', args=(recipe,)))

def answer(request, question_num):
    if (request.POST.get('answer', False) == False):
        return HttpResponseRedirect(reverse('graphview:question', args=(int(question_num),)))
    else:
        if int(question_num) == 1:
            request.session['color'] = request.POST.get('answer', False)
        if int(question_num) == 2: 
            request.session['country_of_origin'] = request.POST.get('answer', False)
        if int(question_num) == 3:
            request.session['ingredient1'] = request.POST.get('answer', False)
        if int(question_num) == 4:
            request.session['ingredient2'] = request.POST.get('answer', False)
        return HttpResponseRedirect(reverse('graphview:question', args=(int(question_num)+1,)))
