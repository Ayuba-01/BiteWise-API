from django.contrib import admin
from .models import User, UserPreference, Goal, WeightLog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "is_staff", "date_joined")

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "diet_type", "updated_at")

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("user", "goal_type", "is_active", "start_date", "updated_at")
    list_filter = ("goal_type","is_active")

@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "weight_kg", "created_at")
    list_filter = ("date",)
