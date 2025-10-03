from rest_framework import serializers
from .models import Tag, Ingredient, Recipe, RecipeIngredient

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id","name")

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id","name","category","is_halal")

class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    class Meta:
        model = RecipeIngredient
        fields = ("ingredient","quantity","unit")

class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Recipe
        fields = ("id","title","per_serving_kcal","protein_g","carbs_g","fat_g",
                  "is_vegan","is_vegetarian","is_halal","tags")

class RecipeDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    items = serializers.SerializerMethodField(source="recipeingredient_set")

    class Meta:
        model = Recipe
        fields = ("id","title","description","instructions","serving_size",
                  "per_serving_kcal","protein_g","carbs_g","fat_g",
                  "is_vegan","is_vegetarian","is_halal","tags","items")

    def get_items(self, obj):
        qs = RecipeIngredient.objects.filter(recipe=obj).select_related("ingredient")
        return RecipeIngredientReadSerializer(qs, many=True).data
