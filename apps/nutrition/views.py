from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Q
from .models import Tag, Ingredient, Recipe
from .serializers import (
    TagSerializer, IngredientSerializer,
    RecipeListSerializer, RecipeDetailSerializer
)

class IsAuthenticatedReadOnly(permissions.IsAuthenticated):
    """
    Auth required; everything read-only for now.
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedReadOnly]

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all().order_by("name")
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get("query")
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.prefetch_related("tags").all()
    permission_classes = [IsAuthenticatedReadOnly]

    def get_serializer_class(self):
        return RecipeDetailSerializer if self.action == "retrieve" else RecipeListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        p = self.request.query_params

        # search by title/description
        q = p.get("query")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

        # diet filters
        diet = p.get("diet")  # vegan|vegetarian|halal
        if diet == "vegan":
            qs = qs.filter(is_vegan=True)
        elif diet == "vegetarian":
            qs = qs.filter(is_vegetarian=True)
        elif diet == "halal":
            qs = qs.filter(is_halal=True)

        # include/exclude tags
        tags_csv = p.get("tags")  # comma-separated
        if tags_csv:
            tag_list = [t.strip() for t in tags_csv.split(",") if t.strip()]
            qs = qs.filter(tags__name__in=tag_list).distinct()

        # exclude ingredients by name
        exclude_csv = p.get("exclude_ingredients")
        if exclude_csv:
            excl = [x.strip().lower() for x in exclude_csv.split(",") if x.strip()]
            qs = qs.exclude(ingredients__name__in=excl)

        # ordering (default by title)
        order = p.get("order_by")
        if order in {"-per_serving_kcal","per_serving_kcal","-protein_g","protein_g"}:
            qs = qs.order_by(order, "title")

        return qs
