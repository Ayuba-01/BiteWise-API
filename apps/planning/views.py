from datetime import date, datetime
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import MealPlan, PlanItem
from .serializers import MealPlanSerializer
from .services import generate_plan
from nutrition.models import Recipe

class MealPlanViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MealPlanSerializer

    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user).prefetch_related("days__items__recipe")

    def create(self, request, *args, **kwargs):
        # POST /api/v1/meal-plans {start_date?, days?}
        start_str = request.data.get("start_date")
        days = int(request.data.get("days", 7))
        try:
            start = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else date.today()
            plan = generate_plan(request.user, start, days=days)
        except ValueError as e:
            return Response({"error": {"code": "BAD_REQUEST", "message": str(e)}}, status=400)
        return Response(self.get_serializer(plan).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def substitute(self, request, pk=None):
        """
        POST /api/v1/meal-plans/{id}/substitute
        body: { plan_item_id, new_recipe_id, new_servings? }
        """
        plan = self.get_object()
        item_id = request.data.get("plan_item_id")
        new_recipe_id = request.data.get("new_recipe_id")
        new_servings = request.data.get("new_servings", 1)

        item = get_object_or_404(PlanItem, id=item_id, plan_day__meal_plan=plan)
        recipe = get_object_or_404(Recipe, id=new_recipe_id)
        item.recipe = recipe
        item.servings = new_servings
        item.save()
        return Response({"message": "Substituted successfully."})
