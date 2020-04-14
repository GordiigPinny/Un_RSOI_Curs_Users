from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list


class Profile(models.Model):
    """
    Профиль пользователя
    """
    user_id = models.PositiveIntegerField(null=False, blank=False, unique=True)
    rating = models.PositiveIntegerField(null=False, default=0)
    money = models.PositiveIntegerField(null=False, default=0)
    created_dt = models.DateTimeField(auto_now_add=True)
    pin_sprite = models.PositiveIntegerField(default=1, null=False)
    geopin_sprite = models.PositiveIntegerField(default=2, null=False)
    unlocked_pins = models.TextField(blank=True, null=False, default='1',
                                     validators=[validate_comma_separated_integer_list])
    achievements = models.TextField(blank=True, null=False, default='1',
                                    validators=[validate_comma_separated_integer_list])
    pic_id = models.PositiveIntegerField(null=True)

    def get_unlocked_pins(self):
        return [int(x) for x in self.unlocked_pins.split(',')]

    def add_pin(self, pin_id: int, price: int, save: bool = True):
        self.unlocked_pins += f',{pin_id}'
        self.money -= price
        if save:
            self.save()

    def get_achievements(self):
        return [int(x) for x in self.achievements.split(',')]

    def add_achievement(self, achievement_id: int, save: bool = True):
        self.achievements += f',{achievement_id}'
        if save:
            self.save()

    def update_rating(self, d_rating: int, save: bool = True):
        self.rating = max(self.rating + d_rating, 0)
        if save:
            self.save()

    def __str__(self):
        return f'Profile({self.id}) for user {self.user_id}'
