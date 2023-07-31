from plistlib import Dict

from django.db import transaction
from rest_framework import serializers

from core.models import User
from goals.models import Board, BoardParticipant


class BoardCreateSerializer(serializers.ModelSerializer):
    user: serializers.HiddenField = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model: Board = Board
        read_only_fields: tuple = ("id", "created", "updated")
        fields: str = "__all__"

    def create(self, validated_data: Dict) -> Board:
        """
        Создает новую доску и добавляет пользователя в качестве владельца.
        """
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role.choices
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields: str = "__all__"
        read_only_fields: tuple = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields: str = "__all__"
        read_only_fields: tuple = ("id", "created", "updated")

    def update(self, instance: Board, validated_data: Dict) -> Board:
        owner = validated_data.pop("user")
        old_participants = instance.participants.exclude(user=owner)
        new_participants = validated_data.pop("participants")
        new_part_with_id = {}
        for participant in new_participants:
            new_part_with_id[participant["user"].id] = participant

        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_part_with_id:
                    old_participant.delete()
                else:
                    if old_participant.role != new_part_with_id[old_participant.user_id]["role"]:
                        old_participant.role = new_part_with_id[old_participant.user_id]["role"]
                    old_participant.save()
                new_part_with_id.pop(old_participant.user_id)

            for new_participant in new_part_with_id.values():
                BoardParticipant.objects.create(
                    user=new_participant['user'],
                    board=instance, role=new_participant['role'])

        instance.title = validated_data["title"]
        instance.save()

        return instance

class BoardListSerializer(serializers.ModelSerializer):

    class Meta:
        model: Board = Board
        fields: str = "__all__"