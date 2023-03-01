from django.contrib.auth import password_validation
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views import View
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Student, Tutor
from backend.settings import backend_settings
from backend.tokens import activation_token
from backend.utils.common import import_string, import_string_list
from backend.utils.domain import get_current_domain
from backend.utils.email import send_verify_email, send_email_welcome
from backend.utils.users import (
    get_user_profile_data,
    get_user_serializer,
    has_user_activate_token,
    has_user_verify_code,
    set_user_verified,
    get_user_from_uid,
)


class RegisterSerializer(get_user_serializer()):
    """
    User register serializer
    """

    def validate_password(self, value):
        """
        Validate user password
        """

        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        """
        Override create method to create user password
        """

        user = super().create(validated_data)
        user.set_password(validated_data['password'])

        # Disable verified if enable verify user, else set it enabled
        user_verified = not (has_user_activate_token()
                             or has_user_verify_code())
        set_user_verified(user, user_verified)
        user.save()
        return user


class RegisterView(CreateAPIView):
    """
    Register a new user to the system
    """

    permission_classes = import_string_list(
        backend_settings.REGISTER_PERMISSION_CLASSES)
    serializer_class = import_string(backend_settings.REGISTER_SERIALIZER)

    def create(self, request, *args, **kwargs):
        is_staff = request.data.get('is_staff')
        if (is_staff):
            try:
                tutor_id = Tutor.objects.get(
                    id=request.data.get('id'))
                return Response({"message": "Tutor ID already exits and in use"}, status.HTTP_400_BAD_REQUEST)
            except:
                pass

        else:
            try:
                student_id = Student.objects.get(
                    id=request.data.get('id'))
                return Response({"message": "Student ID already exits and in use"}, status.HTTP_400_BAD_REQUEST)
            except:
                pass

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = get_user_profile_data(user, request)

        domain = get_current_domain(request)

        # Send email activation link
        if has_user_activate_token() or has_user_verify_code():
            send_verify_email(user, domain, request.data.get('id'))
        else:
            send_email_welcome(user)

        return Response(data, status=status.HTTP_201_CREATED)


class ActivateView(View):
    """
    Activate account by use token sent to email
    """

    def get(self, request, id, uidb64, token):
        """
        Override to get the activation uid and token

        Args:
            request (object): Request object
            uidb64 (string): The uid
            token (string): The user token
            id(int): Student or Tutor ID

        """

        user = get_user_from_uid(uidb64)

        if user and activation_token.check_token(user, token):
            set_user_verified(user)

            send_email_welcome(user)

            if backend_settings.USER_ACTIVATE_SUCCESS_TEMPLATE:
                return render(request, backend_settings.USER_ACTIVATE_SUCCESS_TEMPLATE)

            if (user.is_staff):
                tutor = Tutor.objects.create(
                    user=user, id=id, first_name=user.first_name, last_name=user.last_name, email=user.email)

            else:
                student = Student.objects.create(
                    user=user, id=id, first_name=user.first_name, last_name=user.last_name, email=user.email)

            return HttpResponse(_('Your account has been activated successfully.'))

        if backend_settings.USER_ACTIVATE_FAILED_TEMPLATE:
            return render(request, backend_settings.USER_ACTIVATE_FAILED_TEMPLATE)
        return HttpResponse(
            _('Either the provided activation token is invalid or this account has already been activated.')
        )
