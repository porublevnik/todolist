from rest_framework import serializers
from goals.models import Goal, GoalCategory, BoardParticipant
from core.serializers import UserProfileSerializer


class GoalCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.all()
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("категория удалена")

        # if value.user != self.context["request"].user:
        #     raise serializers.ValidationError("not owner of category")

        if not BoardParticipant.objects.filter(
                board_id=value.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer].exists(),
                user=self.context["request"].user,
        ).exists():
            raise serializers.ValidationError("Вы не создавали эту категорию")

        return value


class GoalSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "category")

    # def validate_category(self, value):
    #     if value.is_deleted:
    #         raise serializers.ValidationError("категория удалена")
    #
    #     # if value.user != self.context["request"].user:
    #     #     raise serializers.ValidationError("not owner of category")
    #
    #     if self.instance.category.board_id != value.board_id:
    #         raise serializers.ValidationError("Вы не создавали эту категорию")
    #     return value


class GoalDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "category")

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("категория удалена")

        # if value.user != self.context["request"].user:
        #     raise serializers.ValidationError("not owner of category")

        if self.instance.category.board_id != value.board_id:
            raise serializers.ValidationError("Вы не создавали эту категорию")
        return value
