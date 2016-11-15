from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from graphview.models import Recipe, Ingredient


_user_color = ''
_country_of_origin = ''
_ingredient_1 = ''
_ingredient_2 = ''



def index(request):
    return render(request, 'graphview/index.html')

def question(request, question_num):
    if int(question_num) == 1:
        recipe_list = get_list_or_404(Recipe.objects.order_by('color').values_list('color').distinct())
        recipe_str_list = []
        for recipe in recipe_list:
            recipe_str_list.append(''.join(recipe[0]).encode("ascii"))
        return render(request, 'graphview/question.html', {
            'question': "What color is your food?",
            'question_num': question_num,
            'recipe_list': recipe_str_list,
            })
    if int(question_num) == 2:
        return HttpResponse(question_num)
    if int(question_num) == 3:
        return HttpResponse(question_num)


def answer(request, question_num):
    return HttpResponse(question_num)
