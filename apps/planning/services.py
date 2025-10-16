from __future__ import annotations

from datetime import timedelta, date
from typing import TYPE_CHECKING

from django.db import transaction
from django.contrib.auth.models import AbstractBaseUser 
from ..accounts.models import Goal, UserPreference
from ..nutrition.models import Recipe, RecipeIngredient
from .models import MealPlan, PlanDay, PlanItem

if TYPE_CHECKING:
    from accounts.models import User as UserModel

# --- Calculations ---
def calc_bmr(sex: str, weight_kg: float, height_cm: float, age_years: int) -> float:
    if sex and sex.lower().startswith("m"):
        return 10 * weight_kg + 6.25 * height_cm - 5 * age_years + 5
    return 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 161

def activity_factor(level: str) -> float:
    mapping = {
        "sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725, "very_active": 1.9
    }
    return mapping.get(level or "moderate", 1.55)

def tdee_for_user(user: AbstractBaseUser, current_weight_kg: float) -> float:
    # compute age safely
    today = date.today()
    if getattr(user, "dob", None):
        years = today.year - user.dob.year - ((today.month, today.day) < (user.dob.month, user.dob.day))
        age = max(18, years)
    else:
        age = 30  # default
    bmr = calc_bmr(getattr(user, "sex", "") or "", current_weight_kg, float(getattr(user, "height_cm", 170) or 170), age)
    return bmr * activity_factor(getattr(user, "activity_level", "moderate") or "moderate")

def daily_targets(goal: Goal, user: AbstractBaseUser) -> dict[str, float]:
    tdee = tdee_for_user(user, float(goal.start_weight_kg or 75))
    deficit = 500.0
    if goal.goal_type == "lose" and goal.target_rate_kg_per_week:
        deficit = min(900.0, max(300.0, float(goal.target_rate_kg_per_week) * 7700.0 / 7.0))
    elif goal.goal_type == "gain":
        deficit = -300.0
    daily_kcal = max(1200, int(round(tdee - deficit)))

    # macros
    start_w = float(goal.start_weight_kg or 75)
    protein_g = max(80.0, start_w * 1.8)
    fat_kcal = daily_kcal * 0.25
    fat_g = fat_kcal / 9.0
    protein_kcal = protein_g * 4.0
    carb_kcal = max(0.0, daily_kcal - fat_kcal - protein_kcal)
    carb_g = carb_kcal / 4.0
    return {
        "daily_kcal": daily_kcal,
        "protein_target_g": round(protein_g, 2),
        "fat_target_g": round(fat_g, 2),
        "carb_target_g": round(carb_g, 2),
    }

def filter_recipe_qs(user: AbstractBaseUser):
    prefs = getattr(user, "preferences", None)
    qs = Recipe.objects.all().prefetch_related("tags", "ingredients")
    if prefs:
        if prefs.diet_type == "vegan":
            qs = qs.filter(is_vegan=True)
        elif prefs.diet_type == "vegetarian":
            qs = qs.filter(is_vegetarian=True)
        elif prefs.diet_type == "halal":
            qs = qs.filter(is_halal=True)
        excl = set([*(prefs.allergens or []), *(prefs.disliked_ingredients or [])])
        if excl:
            qs = qs.exclude(ingredients__name__in=[s for s in excl])
    return qs.distinct()

def pick_meals(qs):
    b = qs.filter(tags__name__iexact="breakfast").first() or qs.order_by("per_serving_kcal").first()
    l = qs.exclude(id=getattr(b, "id", None)).order_by("per_serving_kcal").last()
    d = qs.exclude(id__in=[getattr(b, "id", None), getattr(l, "id", None)]).order_by("-protein_g").first()
    return b, l, d

@transaction.atomic
def generate_plan(user: AbstractBaseUser, start_date: date, days: int = 7) -> MealPlan:
    goal = user.goals.filter(is_active=True).first()
    if not goal:
        raise ValueError("No active goal found for user.")
    targets = daily_targets(goal, user)
    qs = filter_recipe_qs(user)

    plan = MealPlan.objects.create(
        user=user,
        start_date=start_date,
        end_date=start_date + timedelta(days=days - 1),
        created_from_goal_id=goal.id,
        **targets
    )
    for i in range(days):
        d = start_date + timedelta(days=i)
        day = PlanDay.objects.create(
            meal_plan=plan,
            date=d,
            kcal_target=targets["daily_kcal"],
            protein_target_g=targets["protein_target_g"],
            fat_target_g=targets["fat_target_g"],
            carb_target_g=targets["carb_target_g"],
        )
        b, l, dnr = pick_meals(qs)
        if b:   PlanItem.objects.create(plan_day=day, meal_type="breakfast", recipe=b, servings=1)
        if l:   PlanItem.objects.create(plan_day=day, meal_type="lunch",     recipe=l, servings=1)
        if dnr: PlanItem.objects.create(plan_day=day, meal_type="dinner",    recipe=dnr, servings=1)
    return plan