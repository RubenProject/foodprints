from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_data/$', views.get_data, name='get_data'),
    url(r'^add_recipe/$', views.add_recipe, name='add_recipe'),
    url(r'^add_recipe_to_database/$', views.add_recipe, name='add_recipe_to_database'),
    url(r'^all_recipes/$', views.all_recipes, name='all_recipes'),
    url(r'^random_recipe/$', views.random_recipe, name='random_recipe'),
    url(r'^view/(?P<recipe>[A-Z a-z]+)$', views.view, name='view'),
    url(r'^question/(?P<question_num>[0-9]+)/$', views.question, name='question'),
    url(r'^answer/(?P<question_num>[0-9]+)/$', views.answer, name='answer'),
]
