from rest_framework import serializers
from goals.models import GoalCategory, BoardParticipant
from core.serializers import UserProfileSerializer


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_board(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Доска удалена")
        allow = BoardParticipant.objects.filter(
            board=value,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context["request"].user,
        ).exists()
        if not allow:
            raise serializers.ValidationError("Вы должны быть владельцем или редактором")
        return value

class GoalCategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")

class GoalCategoryDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


    def validate_board(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Доска удалена")
        allow = BoardParticipant.objects.filter(
            board=value,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context["request"].user,
        ).exists()
        if not allow:
            raise serializers.ValidationError("Вы должны быть владельцем или редактором")
        return value
