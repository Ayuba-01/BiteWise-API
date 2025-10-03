from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    category = models.CharField(max_length=64, blank=True)  # e.g., Produce, Dairy
    is_halal = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    serving_size = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    per_serving_kcal = models.PositiveIntegerField()
    protein_g = models.DecimalField(max_digits=6, decimal_places=2)
    carbs_g = models.DecimalField(max_digits=6, decimal_places=2)
    fat_g = models.DecimalField(max_digits=6, decimal_places=2)
    is_halal = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField(Tag, blank=True, related_name="recipes")
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient", related_name="recipes")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=24)

    class Meta:
        unique_together = (("recipe", "ingredient"),)

    def __str__(self):
        return f"{self.ingredient.name} x {self.quantity}{self.unit} for {self.recipe.title}"

