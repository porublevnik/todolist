from rest_framework import serializers
from goals.models import GoalComment, BoardParticipant, Goal
from core.serializers import UserProfileSerializer


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объектов модели GoalComment.
    Проверяет, является ли пользователь автором комментария.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_goal(self, value: Goal) -> Goal:
        """
        Проверяет, что пользователь является автором комментария.
        """
        if value.status == Goal.Status.archived:
            raise serializers.ValidationError("Нельзя писать комментарии к удаленным целям")

        validated_users = BoardParticipant.objects.filter(
            user=self.context["request"].user,
            board=value.category.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]).exists()

        if not validated_users:
            raise serializers.ValidationError("Можно писать комментарии только имея роль 'Владелец' или 'Редактор'")

        return value


class GoalCommentSerializer(GoalCommentCreateSerializer):
    """
    Сериализатор для вывода объектов модели GoalComment.
    """
    user = UserProfileSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)
