from rest_framework import serializers
from goals.models import GoalCategory, BoardParticipant, Board
from core.serializers import UserProfileSerializer


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объектов модели GoalCategory.
    Проверяет, является ли пользователь владельцем или редактором доски, связанной с категорией цели.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_board(self, value: Board) -> Board:
        """
        Проверяет, что доска, связанная с категорией, не удалена и пользователь является владельцем или редактором.
        """
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
    """
    Сериализатор для вывода списка объектов модели GoalCategory.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")

class GoalCategoryDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода объектов модели GoalCategory.
    """
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
