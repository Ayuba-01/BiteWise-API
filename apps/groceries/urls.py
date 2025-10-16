from django.urls import path
from .views import GroceryListViewSet

grocery_list = GroceryListViewSet.as_view
urlpatterns = [
    path("grocery-lists/<int:pk>/", grocery_list({"get": "retrieve"}), name="grocery-list-get"),
    path("grocery-lists/<int:pk>/generate/", grocery_list({"post": "generate"}), name="grocery-list-generate"),
]
