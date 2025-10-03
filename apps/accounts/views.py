from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, MeSerializer
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializers import (
    RegisterSerializer, MeSerializer,
    UserPreferenceSerializer, GoalSerializer, WeightLogSerializer
)
from .models import UserPreference, Goal, WeightLog

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class MeView(APIView):
    def get(self, request):
        return Response(MeSerializer(request.user).data)
    def patch(self, request):
        ser = MeSerializer(request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


class UserPreferenceViewSet(viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin):
    """
    /preferences (GET->retrieve current, POST->create/update, PATCH->update)
    Treats it as a singleton per user.
    """
    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # return existing or 404
        return get_object_or_404(UserPreference, user=self.request.user)

    # convenience route: /preferences/me
    @action(detail=False, methods=["get"])
    def me(self, request):
        obj, _ = UserPreference.objects.get_or_create(user=request.user)
        return Response(self.get_serializer(obj).data)

class GoalViewSet(viewsets.ModelViewSet):
    """
    /goals (list/create)
    /goals/{id} (retrieve/update/partial_update/destroy)
    """
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).order_by("-is_active","-updated_at")

class WeightLogViewSet(viewsets.ModelViewSet):
    """
    /weights (list/create)
    /weights/{id} (retrieve/update/delete)
    """
    serializer_class = WeightLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = WeightLog.objects.filter(user=self.request.user)
        # filter by ?from=YYYY-MM-DD&to=YYYY-MM-DD
        f = self.request.query_params.get("from")
        t = self.request.query_params.get("to")
        if f:
            qs = qs.filter(date__gte=f)
        if t:
            qs = qs.filter(date__lte=t)
        return qs.order_by("-date","-created_at")