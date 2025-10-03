from django.contrib import admin
from .models import Tag, Ingredient, Recipe, RecipeIngredient

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name","category","is_halal")

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title","per_serving_kcal","is_vegan","is_vegetarian","is_halal","created_at")
    list_filter = ("is_vegan","is_vegetarian","is_halal","tags")
    search_fields = ("title","description")
    inlines = [RecipeIngredientInline]
