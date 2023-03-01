from django.utils.translation import gettext as _

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from backend.settings import backend_settings
from backend.utils.users import get_user_model, get_all_users


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """

    if 'email' in backend_settings.USER_FIELDS:
        email = serializers.EmailField(validators=[UniqueValidator(
            queryset=get_all_users(),
            message=_('User with this email already exists.')
        )])

    if 'username' in backend_settings.USER_FIELDS:
        username = serializers.CharField(validators=[UniqueValidator(
            queryset=get_all_users(),
            message=_('User with this username already exists.')
        )])

    class Meta:
        model = get_user_model()

        fields = backend_settings.USER_FIELDS
        read_only_fields = backend_settings.USER_READ_ONLY_FIELDS
        extra_kwargs = {'password': {'write_only': True}}

    def get_has_password(self, user):
        """
        Custom response field to check user has password or not
        """

        return bool(user.password)
