from django.db import models
from django.utils import timezone
from ..planning.models import MealPlan
from ..nutrition.models import Ingredient

class GroceryList(models.Model):
    meal_plan = models.OneToOneField(MealPlan, on_delete=models.CASCADE, related_name="grocery_list")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"GroceryList<plan={self.meal_plan_id}>"

class GroceryItem(models.Model):
    grocery_list = models.ForeignKey(GroceryList, on_delete=models.CASCADE, related_name="items")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=24)
    aisle_hint = models.CharField(max_length=64, blank=True)

    class Meta:
        unique_together = (("grocery_list", "ingredient", "unit"),)

    def __str__(self):
        return f"{self.ingredient.name} {self.quantity}{self.unit}"
