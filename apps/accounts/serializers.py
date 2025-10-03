from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .models import UserPreference, Goal, WeightLog
from django.db import IntegrityError, transaction


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ("email", "password", "full_name", "sex", "dob", "height_cm", "activity_level", "timezone")
    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "full_name", "sex", "dob", "height_cm", "activity_level", "timezone", "date_joined")
        read_only_fields = ("id", "email", "date_joined")


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ("diet_type","allergens","disliked_ingredients","created_at","updated_at")
        read_only_fields = ("created_at","updated_at")

    def create(self, validated_data):
        # ensure one-to-one created or updated
        user = self.context["request"].user
        pref, _ = UserPreference.objects.update_or_create(user=user, defaults=validated_data)
        return pref

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = (
            "id","goal_type","target_rate_kg_per_week","start_weight_kg",
            "target_weight_kg","start_date","is_active","created_at","updated_at"
        )
        read_only_fields = ("id","created_at","updated_at")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        try:
            with transaction.atomic():
                # if creating another active goal, deactivate existing
                if validated_data.get("is_active", True):
                    Goal.objects.filter(user=validated_data["user"], is_active=True).update(is_active=False)
                return Goal.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"is_active": "Only one active goal is allowed per user."})

    def update(self, instance, validated_data):
        # if setting active=True, deactivate others
        make_active = validated_data.get("is_active", instance.is_active)
        if make_active and not instance.is_active:
            Goal.objects.filter(user=instance.user, is_active=True).exclude(pk=instance.pk).update(is_active=False)
        return super().update(instance, validated_data)

class WeightLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightLog
        fields = ("id","date","weight_kg","note","created_at")
        read_only_fields = ("id","created_at")

    def validate(self, attrs):
        # optional: basic sanity checks
        w = attrs.get("weight_kg")
        if w is not None and (w <= 0 or w > 500):
            raise serializers.ValidationError({"weight_kg": "Weight must be between 0 and 500kg."})
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        try:
            return WeightLog.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"date": "You already have a weight log for this date."})
