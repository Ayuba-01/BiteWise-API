from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone as tz
from django.db.models import Q, UniqueConstraint

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    # core login
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    sex = models.CharField(max_length=10, blank=True)          # later: choices
    dob = models.DateField(null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    activity_level = models.CharField(max_length=20, blank=True)
    timezone = models.CharField(max_length=64, default="Europe/London")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=tz.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # email + password only required for creates

    objects = UserManager()

    def __str__(self):
        return self.email


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    diet_type = models.CharField(max_length=32, blank=True)  # none|vegetarian|vegan|halal|kosher|pescatarian
    allergens = models.JSONField(default=list, blank=True)   # e.g., ["nuts","dairy"]
    disliked_ingredients = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences<{self.user_id}>"

class Goal(models.Model):
    GOAL_TYPES = (("lose","lose"),("maintain","maintain"),("gain","gain"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    goal_type = models.CharField(max_length=16, choices=GOAL_TYPES)
    target_rate_kg_per_week = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    start_weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    target_weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # at most ONE active goal per user
            UniqueConstraint(
                fields=["user"],
                condition=Q(is_active=True),
                name="unique_active_goal_per_user",
            )
        ]

    def __str__(self):
        return f"Goal<{self.user_id}:{self.goal_type}, active={self.is_active}>"

class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weight_logs")
    date = models.DateField()
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user","date"], name="unique_weightlog_per_user_per_date")
        ]
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"WeightLog<{self.user_id} {self.date} {self.weight_kg}kg>"