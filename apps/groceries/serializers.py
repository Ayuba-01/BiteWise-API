from rest_framework import serializers
from .models import GroceryList, GroceryItem
from ..nutrition.serializers import IngredientSerializer

class GroceryItemSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    class Meta:
        model = GroceryItem
        fields = ("ingredient","quantity","unit","aisle_hint")

class GroceryListSerializer(serializers.ModelSerializer):
    items = GroceryItemSerializer(many=True, read_only=True)
    class Meta:
        model = GroceryList
        fields = ("meal_plan","created_at","items")
