from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from graphview.models import Recipe, Ingredient
from django.core.urlresolvers import reverse
from django.utils import timezone
import random
from random import randint, shuffle
import json
import urllib
import urllib2
import itertools

def get_image(recipeName):
    fields = ['', 'picture of ']
    for field in fields:
        query = urllib.urlencode(dict(q=field + recipeName, format='json', t='Foodprints'))
        response = urllib2.urlopen('https://api.duckduckgo.com?' + query)
        d = json.load(response)
        if (d['Image'] != ''):
            return d['Image']
    
    country = Recipe.objects.get(recipe_name=recipeName).country_of_origin
    query = urllib.urlencode(dict(q='flag of ' + country, format='json', t='Foodprints'))
    response = urllib2.urlopen('https://api.duckduckgo.com?' + query)
    d = json.load(response)
    if (d['Image'] != ''):
        return d['Image']
    else:
        return '/static/graphview/img/broken.png'

def get_info(request):
    recipe = get_object_or_404(Recipe, recipe_name=request.META['HTTP_RECIPE'])
    info = {}
    info['image'] = get_image(recipe.recipe_name)
    info['recipe'] = recipe.recipe_name
    info['color'] = recipe.color
    info['country_of_origin'] = recipe.country_of_origin
    info['link'] = 'http://www.bbcgoodfood.com'
    info['ingredients'] = []
    ingredient_obj_list = recipe.ingredients.all()
    for ingredient in ingredient_obj_list:
        info['ingredients'].append(ingredient.ingredient_name)
    return HttpResponse(json.dumps(info))

def get_recipes(request):
    limit = 5
    target_recipe = get_object_or_404(Recipe, recipe_name=request.META['HTTP_RECIPE'])
    recipe_list = Recipe.objects.all().exclude(id=target_recipe.id)

    fields = get_list_or_404(target_recipe.ingredients.all())
    suggestion_list = []
    spare_list = []
    shuffle(fields)
    refinement = 0
    for idx, field in enumerate(fields):
        temp_list = recipe_list.filter(ingredients=field)
        if temp_list.count() <= limit and temp_list.count() >= limit / 2 and refinement > 1:
            suggestion_list = get_list_or_404(temp_list)
            break
        elif temp_list.count() <= limit / 2:
            if temp_list.count() > 0:
                spare_list.append(get_list_or_404(temp_list))
            elif len(spare_list) >= limit and idx > 3:
                suggestion_list = spare_list
                break
            continue
        print field
        recipe_list = temp_list
        refinement += 1

    print suggestion_list

    data = {}
    data['nodes'] = [{"id" : "0", "label": target_recipe.recipe_name, "image": get_image(target_recipe.recipe_name)}]
    data['edges'] = []

    for idx, suggestion in enumerate(suggestion_list):
        data['nodes'].append({"id" : str(idx + 1), "label": suggestion.recipe_name, "image": get_image(suggestion.recipe_name)})
        data['edges'].append({"id" : str(idx), "from": "0", "to": str(idx + 1)})

    return HttpResponse(json.dumps(data))  

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
    #TODO: if number of choices is down to 1, pick randomly
    PIC_DIR = "/static/graphview/img/ingredient_type/"
    if int(question_num) == 1:
        color_list = get_list_or_404(Recipe.objects.order_by('color').values_list('color').distinct())
        color_str_list = []
        for color in color_list:
            color_str_list.append(''.join(color[0]).encode("ascii"))
        url_list = []
        for color in color_str_list:
            query = urllib.urlencode(dict(q='color ' + color, format='json', t='Foodprints'))
            response = urllib2.urlopen('https://api.duckduckgo.com?' + query)
            d = json.load(response)
            url_list.append(d['Answer'][5:12])
        option_list = zip(color_str_list, url_list)
        return render(request, 'graphview/question.html', {
            'question': "What color is your food?",
            'question_num': question_num,
            'option_list': option_list,
            })
    elif int(question_num) == 2:
        recipe_list = Recipe.objects.filter(color=request.session['color'])
        country_list = get_list_or_404(recipe_list.order_by('country_of_origin').values_list('country_of_origin').distinct())
        country_str_list = []
        for country in country_list:
            country_str_list.append(''.join(country[0]).encode("ascii"))
        url_list = []
        for country in country_str_list:
            query = urllib.urlencode(dict(q='flag of ' + country, format='json', t='Foodprints'))
            response = urllib2.urlopen('https://api.duckduckgo.com?' + query)
            d = json.load(response)
            if d['Image'] != '':
                url_list.append(d['Image'])
            else:
                url_list.append('/staticgraphview/img/broken.png')
        option_list = zip(country_str_list, url_list)
        return render(request, 'graphview/question.html', {
            'question': "What country is your food from?",
            'question_num': question_num,
            'option_list': option_list,
            })
    elif int(question_num) == 3:
        recipe_list = Recipe.objects.filter(color=request.session['color'])
        recipe_list = recipe_list.filter(country_of_origin=request.session['country_of_origin'])
        ingredient_list = get_list_or_404(Ingredient.objects.filter(recipe=recipe_list).distinct())
        ingredient_str_list = []
        for ingredient in ingredient_list:
            ingredient_str_list.append(''.join(ingredient.ingredient_name).encode("ascii"))
        url_list = []
        fields = ['', 'picture of '] 
        for idx in ingredient_str_list:
            for field in fields:
                query = urllib.urlencode(dict(q=field + idx, format='json', t='Foodprints'))
                response = urllib2.urlopen('https://api.duckduckgo.com?' + query)
                d = json.load(response)
                if d['Image'] != '':
                    url_list.append(d['Image'])
                    break
            if d['Image'] == '':
                ingredient_type = Ingredient.objects.get(ingredient_name=idx).ingredient_type
                url_list.append(PIC_DIR + ingredient_type + ".png")
        option_list = zip(ingredient_str_list, url_list)
        return render(request, 'graphview/question.html', {
            'question': "Which of these ingredients is in your food?",
            'question_num': question_num,
            'option_list': option_list,
            })
    elif int(question_num) == 4:
        recipe_list = Recipe.objects.filter(color=request.session['color'])
        recipe_list = recipe_list.filter(country_of_origin=request.session['country_of_origin'])
        recipe_list = recipe_list.filter(ingredients=Ingredient.objects.filter(ingredient_name=request.session['ingredient1']))
        ingredient_list = get_list_or_404(Ingredient.objects.filter(recipe=recipe_list).distinct())
        ingredient_str_list = []
        for ingredient in ingredient_list:
            ingredient_str_list.append(''.join(ingredient.ingredient_name).encode("ascii"))
        url_list = []
        fields = ['', 'picture of ']
        for idx in ingredient_str_list:
            for field in fields:
                query = urllib.urlencode(dict(q=field + idx, format='json', t='Foodprints'))
                response = urllib2.urlopen('https://api.duckduckgo.com?' + query)
                d = json.load(response)
                if d['Image'] != '':
                    url_list.append(d['Image'])
                    break
            if d['Image'] == '':
                ingredient_type = Ingredient.objects.get(ingredient_name=idx).ingredient_type
                url_list.append(PIC_DIR + ingredient_type + ".png")
        option_list = zip(ingredient_str_list, url_list)
        return render(request, 'graphview/question.html', {
            'question': "Which of these ingredients is in your food?",
            'question_num': question_num,
            'option_list': option_list,
            })
    elif int(question_num) == 5:
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
        elif int(question_num) == 2: 
            request.session['country_of_origin'] = request.POST.get('answer', False)
        elif int(question_num) == 3:
            request.session['ingredient1'] = request.POST.get('answer', False)
        elif int(question_num) == 4:
            request.session['ingredient2'] = request.POST.get('answer', False)
        return HttpResponseRedirect(reverse('graphview:question', args=(int(question_num)+1,)))
