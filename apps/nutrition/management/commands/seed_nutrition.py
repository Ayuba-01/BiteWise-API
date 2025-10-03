import random
from django.core.management.base import BaseCommand
from apps.nutrition.models import Tag, Ingredient, Recipe, RecipeIngredient

TAGS = ["breakfast","high-protein","low-carb","quick","budget","vegan","vegetarian","halal"]
INGREDIENTS = [
    ("Eggs","Dairy"), ("Chicken Breast","Meat"), ("Oats","Pantry"), ("Greek Yogurt","Dairy"),
    ("Banana","Produce"), ("Spinach","Produce"), ("Olive Oil","Pantry"), ("Rice","Pantry"),
    ("Salmon","Meat"), ("Broccoli","Produce"), ("Chickpeas","Pantry"), ("Tomatoes","Produce")
]

RECIPES = [
    # title, kcal, P, C, F, tags, items=[(ingredient, qty, unit)]
    ("Veggie Omelette", 350, 25, 5, 22, ["breakfast","quick","halal"],
     [("Eggs",3,"pcs"),("Spinach",50,"g"),("Olive Oil",1,"tbsp"),("Tomatoes",60,"g")]),
    ("Chicken & Rice", 520, 45, 55, 12, ["high-protein","budget","halal"],
     [("Chicken Breast",150,"g"),("Rice",120,"g"),("Broccoli",80,"g"),("Olive Oil",1,"tbsp")]),
    ("Overnight Oats", 420, 22, 60, 12, ["breakfast","vegetarian","budget"],
     [("Oats",60,"g"),("Greek Yogurt",120,"g"),("Banana",100,"g")]),
    ("Salmon & Greens", 480, 35, 10, 30, ["low-carb","high-protein","halal"],
     [("Salmon",150,"g"),("Spinach",80,"g"),("Olive Oil",1,"tbsp")]),
    ("Chickpea Salad", 380, 18, 40, 14, ["vegan","budget","quick"],
     [("Chickpeas",120,"g"),("Tomatoes",80,"g"),("Olive Oil",1,"tbsp"),("Spinach",60,"g")]),
]

class Command(BaseCommand):
    help = "Seed basic tags, ingredients, and recipes for demo"

    def handle(self, *args, **options):
        # tags
        tag_objs = {}
        for t in TAGS:
            tag_objs[t], _ = Tag.objects.get_or_create(name=t)

        # ingredients
        ing_objs = {}
        for name, cat in INGREDIENTS:
            ing_objs[name], _ = Ingredient.objects.get_or_create(name=name, defaults={"category": cat})

        # recipes
        created = 0
        for title, kcal, p, c, f, tags, items in RECIPES:
            r, made = Recipe.objects.get_or_create(
                title=title,
                defaults=dict(
                    per_serving_kcal=kcal, protein_g=p, carbs_g=c, fat_g=f,
                    is_vegan="vegan" in tags, is_vegetarian="vegetarian" in tags, is_halal="halal" in tags,
                    description="", instructions=""
                )
            )
            if made:
                created += 1
                # attach tags
                r.tags.add(*[tag_objs[t] for t in tags])
                # attach ingredients
                for ing_name, qty, unit in items:
                    RecipeIngredient.objects.create(recipe=r, ingredient=ing_objs[ing_name], quantity=qty, unit=unit)

        self.stdout.write(self.style.SUCCESS(f"Seed complete. New recipes: {created}"))
