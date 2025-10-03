from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, MeView, UserPreferenceViewSet, GoalViewSet, WeightLogViewSet

router = DefaultRouter()
router.register(r"preferences", UserPreferenceViewSet, basename="preferences")
router.register(r"goals", GoalViewSet, basename="goals")
router.register(r"weights", WeightLogViewSet, basename="weights")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]
