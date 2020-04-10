from Users.models import Profile
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ApiRequesters.Media.MediaRequester import MediaRequester
from ApiRequesters.utils import get_token_from_request
from ApiRequesters.exceptions import BaseApiRequestError


class ProfilesListSerializer(serializers.ModelSerializer):
    """
    Сериализатор спискового представления юзера
    """
    pic_id = serializers.IntegerField(min_value=1, required=False, allow_null=True, default=None)
    user_id = serializers.IntegerField(min_value=1, validators=[UniqueValidator(queryset=Profile.objects.all())])

    class Meta:
        model = Profile
        fields = [
            'id',
            'user_id',
            'pic_id',
        ]

    def validate_pic_id(self, value: int):
        if value is None:
            return value
        r = MediaRequester()
        token = get_token_from_request(self.context['request'])
        try:
            _ = r.get_image_info(value, token)
            return value
        except BaseApiRequestError:
            return None

    def create(self, validated_data):
        new = Profile.objects.create(**validated_data)
        return new


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор юзера
    """
    pin_sprite = serializers.IntegerField(required=False)
    created_dt = serializers.DateTimeField(read_only=True)
    geopin_sprite = serializers.IntegerField(required=False)
    unlocked_pins = serializers.SerializerMethodField()
    unlocked_geopins = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()
    pic_id = serializers.IntegerField(min_value=1, required=False, allow_null=True, default=None)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'user_id',
            'pin_sprite',
            'geopin_sprite',
            'unlocked_pins',
            'unlocked_geopins',
            'achievements',
            'pic_id',
            'created_dt',
        ]

    def get_unlocked_pins(self, instance: Profile):
        return [int(x) for x in instance.unlocked_pins.split(',')]

    def get_unlocked_geopins(self, instance: Profile):
        return [int(x) for x in instance.unlocked_geopins.split(',')]

    def get_achievements(self, instance: Profile):
        return [int(x) for x in instance.achievements.split(',')]

    def validate_pic_id(self, value: int):
        if value is None:
            return value
        r = MediaRequester()
        token = get_token_from_request(self.context['request'])
        try:
            _ = r.get_image_info(value, token)
            return value
        except BaseApiRequestError:
            return None

    def update(self, instance: Profile, validated_data):
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance
