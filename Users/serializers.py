from Users.models import Profile
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class ProfilesListSerializer(serializers.ModelSerializer):
    """
    Сериализатор спискового представления юзера
    """
    profile_pic_link = serializers.URLField(required=False, allow_null=True)
    user_id = serializers.IntegerField(min_value=1, validators=[UniqueValidator(queryset=Profile.objects.all())])

    class Meta:
        model = Profile
        fields = [
            'id',
            'user_id',
            'profile_pic_link',
        ]

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
    profile_pic_link = serializers.URLField(required=False)
    user_id = serializers.IntegerField(min_value=1, validators=[UniqueValidator(queryset=Profile.objects.all())],
                                       required=False)

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
            'profile_pic_link',
            'created_dt',
        ]

    def get_unlocked_pins(self, instance: Profile):
        return [int(x) for x in instance.unlocked_pins.split(',')]

    def get_unlocked_geopins(self, instance: Profile):
        return [int(x) for x in instance.unlocked_geopins.split(',')]

    def get_achievements(self, instance: Profile):
        return [int(x) for x in instance.achievements.split(',')]

    def update(self, instance: Profile, validated_data):
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance
