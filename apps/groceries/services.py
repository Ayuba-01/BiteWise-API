from collections import defaultdict
from django.db import transaction
from ..planning.models import MealPlan
from ..nutrition.models import RecipeIngredient
from .models import GroceryList, GroceryItem

@transaction.atomic
def build_grocery_list(meal_plan: MealPlan) -> GroceryList:
    gl, _ = GroceryList.objects.get_or_create(meal_plan=meal_plan)
    gl.items.all().delete()

    totals = defaultdict(lambda: defaultdict(float))  # ingredient_id -> unit -> qty
    for day in meal_plan.days.all():
        for item in day.items.all():
            for ri in RecipeIngredient.objects.filter(recipe=item.recipe).select_related("ingredient"):
                qty = float(ri.quantity) * float(item.servings)
                totals[ri.ingredient_id][ri.unit] += qty

    rows = []
    for ingredient_id, per_unit in totals.items():
        for unit, qty in per_unit.items():
            rows.append(GroceryItem(
                grocery_list=gl,
                ingredient_id=ingredient_id,
                unit=unit,
                quantity=round(qty, 3),
            ))
    GroceryItem.objects.bulk_create(rows)
    return gl
