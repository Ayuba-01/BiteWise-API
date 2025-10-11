from rest_framework.routers import DefaultRouter
from .views import MealPlanViewSet

router = DefaultRouter()
router.register(r"meal-plans", MealPlanViewSet, basename="meal-plans")
urlpatterns = router.urls
