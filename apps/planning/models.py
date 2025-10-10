from django.db import models
from django.conf import settings
from django.utils import timezone
from ..nutrition.models import Recipe


User = settings.AUTH_USER_MODEL

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_plans")
    start_date = models.DateField()
    end_date = models.DateField()
    daily_kcal = models.PositiveIntegerField()
    protein_target_g = models.DecimalField(max_digits=6, decimal_places=2)
    fat_target_g = models.DecimalField(max_digits=6, decimal_places=2)
    carb_target_g = models.DecimalField(max_digits=6, decimal_places=2)
    created_from_goal_id = models.PositiveIntegerField(null=True, blank=True)  # store pk for traceability
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"MealPlan<{self.user_id} {self.start_date}..{self.end_date}>"

class PlanDay(models.Model):
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="days")
    date = models.DateField()
    kcal_target = models.PositiveIntegerField()
    protein_target_g = models.DecimalField(max_digits=6, decimal_places=2)
    fat_target_g = models.DecimalField(max_digits=6, decimal_places=2)
    carb_target_g = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = (("meal_plan", "date"),)
        ordering = ["date"]

    def __str__(self):
        return f"PlanDay<{self.meal_plan_id} {self.date}>"

class PlanItem(models.Model):
    MEAL_TYPES = (("breakfast","breakfast"),("lunch","lunch"),("dinner","dinner"))
    plan_day = models.ForeignKey(PlanDay, on_delete=models.CASCADE, related_name="items")
    meal_type = models.CharField(max_length=16, choices=MEAL_TYPES)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    servings = models.DecimalField(max_digits=6, decimal_places=2, default=1)
    eaten_servings = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    marked_eaten_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["meal_type", "id"]

    def __str__(self):
        return f"{self.meal_type}: {self.recipe.title} x{self.servings}"
