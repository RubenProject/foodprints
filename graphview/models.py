import datetime

from django.db import models
from django.utils import timezone

class Ingredient(models.Model):
    INGREDIENT_TYPE_CHOICES = (
        ('VE', 'Vegetable'),
        ('CA', 'Carbs'),
        ('BE', 'Beef'),
        ('CH', 'Chicken'),
        ('PO', 'Pork'),
        ('FI', 'Fish'),
        ('MO', 'Meat_other'),
        ('HE', 'Herb'),
        ('SP', 'Spice'),
        ('DI', 'Diary'),
        ('OI', 'Oil'),
        ('AL', 'Alcohol'),
        ('NU', 'Nuts'),
        ('FR', 'Fruit'),
    )
    ingredient_name = models.CharField(max_length = 200)
    ingredient_type = models.CharField(
        max_length = 2,
        choices = INGREDIENT_TYPE_CHOICES,
    )
    
    def __str__(self):
        return self.ingredient_name

    class Meta:
        ordering = ('ingredient_name',)

class Recipe(models.Model):
    RECIPE_COLOR_CHOICES = (
        ('YELLOW', 'Yellow'),
        ('RED', 'Red'),
        ('BROWN', 'Brown'),
        ('BLACK', 'Black'),
        ('WHITE', 'White'),
        ('GREEN', 'Green'),
        ('Pink', 'Pink'),
        ('Orange', 'Orange'),
        ('OTHER', 'Other'),
    )
    recipe_name = models.CharField(max_length = 200)
    country_of_origin = models.CharField(max_length = 30)
    date_added = models.DateTimeField('date added') 
    color = models.CharField(
        max_length = 10, 
        choices = RECIPE_COLOR_CHOICES,
    )
    ingredients = models.ManyToManyField(Ingredient)
    
    def __str__(self):
        return self.recipe_name

    class Meta:
        ordering = ('recipe_name',)

