from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from graphview.models import Recipe, Ingredient
from django.core.urlresolvers import reverse
import random


def random_recipe(request):
    recipe_list = get_list_or_404(Recipe.objects.all())
    recipe = ''.join(random.choice(recipe_list).recipe_name).encode("ascii")
    return HttpResponseRedirect(reverse('graphview:view', args=(recipe,)))

def view(request, recipe):
    return render(request, 'graphview/view.html')

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
