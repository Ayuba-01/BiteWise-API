from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..planning.models import MealPlan
from .models import GroceryList
from .serializers import GroceryListSerializer
from .services import build_grocery_list

class GroceryListViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        # GET /grocery-lists/{meal_plan_id}
        plan = get_object_or_404(MealPlan, id=pk, user=request.user)
        gl = getattr(plan, "grocery_list", None)
        if not gl:
            return Response({"error": {"code": "NOT_FOUND", "message": "No grocery list generated for this plan."}}, status=404)
        return Response(GroceryListSerializer(gl).data)

    @action(detail=True, methods=["post"])
    def generate(self, request, pk=None):
        # POST /grocery-lists/{meal_plan_id}/generate
        plan = get_object_or_404(MealPlan, id=pk, user=request.user)
        gl = build_grocery_list(plan)
        return Response(GroceryListSerializer(gl).data, status=status.HTTP_201_CREATED)
