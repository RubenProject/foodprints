from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from graphview.models import Recipe, Ingredient


_color = ''
_country_of_origin = ''
_ingredient_1 = ''
_ingredient_2 = ''



def index(request):
    return render(request, 'graphview/index.html')

def question(request, question_num):
    if int(question_num) == 1:
        color_list = get_list_or_404(Recipe.objects.order_by('color').values_list('color').distinct())
        color_str_list = []
        for color in color_list:
            color_str_list.append(''.join(color[0]).encode("ascii"))
        return render(request, 'graphview/question.html', {
            'question': "What color is your food?",
            'question_num': question_num,
            'recipe_list': color_str_list,
            })
    if int(question_num) == 2:
        return HttpResponse(question_num)
    if int(question_num) == 3:
        return HttpResponse(question_num)


def answer(request, question_num):
    if int(question_num) == 1:
        try:
            _color = request.POST['answer']
        except (KeyError, Recipe.DoesNotExist):
            return(request, 'graphview/question.html', {
                'question': "What color is your food?",
                'question_num': question_num,
                'recipe_list': color_str_list,
                })
    if int(question_num) == 2:
        return HttpResponse(question_num)
    if int(question_num) == 3:
        return HttpResponse(question_num)
