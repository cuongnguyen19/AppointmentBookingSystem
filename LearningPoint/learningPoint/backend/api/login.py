from django.contrib.auth.models import update_last_login, User, Group
from django.contrib.auth import authenticate

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from backend.settings import backend_settings
from backend.utils.common import import_string, import_string_list
from backend.utils.users import (
    get_user_model,
    get_user_profile_data,
    has_user_verified,
    set_user_verified,
)
from backend.exceptions import (
    NotActivated,
    LoginFailed,
    MissingEmail,
    InvalidAccessToken,
)


class LoginSerializer(serializers.ModelSerializer):
    """
    User login serializer
    """

    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    def validate(self, data):
        user = authenticate(**data)
        if user:

            # Check user is activated or not
            if has_user_verified(user):

                # added user model to OrderedDict that serializer is validating
                data['user'] = user

                return data
            raise NotActivated()
        raise LoginFailed()


class LoginView(CreateAPIView):
    """
    This is used to Login into system.
    """

    permission_classes = import_string_list(
        backend_settings.LOGIN_PERMISSION_CLASSES)
    serializer_class = import_string(backend_settings.LOGIN_SERIALIZER)

    def post(self, request, *args, **kwargs):
        """
        Override to check user login

        Args:
            request (object): The request object

        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Update last logged in
        update_last_login(None, user)
        data = get_user_profile_data(user, request)

        return Response(data, status=status.HTTP_200_OK)
