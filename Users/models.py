from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list


class Profile(models.Model):
    """
    Профиль пользователя
    """
    user_id = models.PositiveIntegerField(null=False, blank=False, unique=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    pin_sprite = models.PositiveIntegerField(default=1, null=False)
    geopin_sprite = models.PositiveIntegerField(default=1, null=False)
    unlocked_pins = models.TextField(blank=True, null=False, default='1',
                                     validators=[validate_comma_separated_integer_list])
    unlocked_geopins = models.TextField(blank=True, null=False, default='1',
                                        validators=[validate_comma_separated_integer_list])
    achievements = models.TextField(blank=True, null=False, default='1',
                                    validators=[validate_comma_separated_integer_list])
    profile_pic_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'Profile({self.id}) for user {self.user_id}'
