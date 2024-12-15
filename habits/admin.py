from django.contrib import admin
from .models import UsefulHabit, PleasantHabit, Reward


class UsefulHabitAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'action', 'time', 'place', 'reward', 'related_habit',
        'periodicity', 'duration', 'is_public'
    ]
    list_filter = ['is_public', 'periodicity']
    search_fields = ['action', 'reward__description', 'related_habit__action']
    ordering = ['user', 'action']
    autocomplete_fields = ['reward', 'related_habit']


class PleasantHabitAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'is_reward', 'related_useful_habit']
    list_filter = ['is_reward']
    search_fields = ['action', 'related_useful_habit__action']
    ordering = ['user', 'action']
    autocomplete_fields = ['related_useful_habit']


class RewardAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'cost']
    list_filter = ['user']
    search_fields = ['description']
    ordering = ['user', 'description']


# Регистрация моделей в админке
admin.site.register(UsefulHabit, UsefulHabitAdmin)
admin.site.register(PleasantHabit, PleasantHabitAdmin)
admin.site.register(Reward, RewardAdmin)
