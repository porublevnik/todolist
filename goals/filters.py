import django_filters
from django.db import models
from django_filters import rest_framework

from goals.models import Goal


class GoalDateFilter(rest_framework.FilterSet):
    """
    Фильтр для целей на основе даты.
    Позволяет фильтровать цели по полю `deadline`.
    """

    class Meta:
        model = Goal
        fields = {
            "deadline": ("lte", "gte"),  # Фильтрация по полю `deadline`. Доступные операторы: lte (меньше или равно), gte (больше или равно).
            "category": ("exact", "in"),  # Фильтрация по полю `category`. Доступные операторы: exact (равно), in (в списке значений).
            "status": ("exact", "in"),  # Фильтрация по полю `status`. Доступные операторы: exact (равно), in (в списке значений).
            "priority": ("exact", "in"),  # Фильтрация по полю `priority`. Доступные операторы: exact (равно), in (в списке значений).
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},  # Использование `IsoDateTimeFilter` для поля `deadline` типа DateTimeField.
    }