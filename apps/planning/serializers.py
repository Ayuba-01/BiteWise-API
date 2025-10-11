from rest_framework import serializers
from .models import MealPlan, PlanDay, PlanItem
from nutrition.serializers import RecipeListSerializer

class PlanItemSerializer(serializers.ModelSerializer):
    recipe = RecipeListSerializer()
    class Meta:
        model = PlanItem
        fields = ("id","meal_type","servings","recipe","eaten_servings","marked_eaten_at")

class PlanDaySerializer(serializers.ModelSerializer):
    items = PlanItemSerializer(many=True, read_only=True)
    class Meta:
        model = PlanDay
        fields = ("id","date","kcal_target","protein_target_g","fat_target_g","carb_target_g","items")

class MealPlanSerializer(serializers.ModelSerializer):
    days = PlanDaySerializer(many=True, read_only=True)
    class Meta:
        model = MealPlan
        fields = ("id","start_date","end_date","daily_kcal","protein_target_g","fat_target_g","carb_target_g","days")
