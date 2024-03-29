from rest_framework import serializers
from goals.models import Goal, GoalCategory, BoardParticipant
from core.serializers import UserProfileSerializer


class GoalCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объектов модели Goal.
    Проверяет, что пользователь является владельцем категории, связанной с целью.
    """
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.all()
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        """
        Проверяет, что категория, связанная с целью, не удалена и пользователь является владельцем категории.
        """
        if value.is_deleted:
            raise serializers.ValidationError("категория удалена")


        if not BoardParticipant.objects.filter(
                board_id=value.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user=self.context["request"].user,
        ).exists():
            raise serializers.ValidationError("Вы не создавали эту категорию")

        return value


class GoalSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода списка объектов модели Goal.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "category")

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        """
        Проверяет, что категория, связанная с целью, не удалена и пользователь является владельцем категории.
        """
        if value.is_deleted:
            raise serializers.ValidationError("категория удалена")

        if self.instance.category.board_id != value.board_id:
            raise serializers.ValidationError("Вы не создавали эту категорию")
        return value


class GoalDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода объектов модели Goal.
    """
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "category")

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        """
        Проверяет, что категория, связанная с целью, не удалена и пользователь является владельцем категории.
        """
        if value.is_deleted:
            raise serializers.ValidationError("категория удалена")


        if self.instance.category.board_id != value.board_id:
            raise serializers.ValidationError("Вы не создавали эту категорию")
        return value
