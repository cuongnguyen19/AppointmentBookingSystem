from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

from backend.settings import backend_settings
from backend.utils.common import import_string, import_string_list
from backend.utils.users import get_all_users, get_user_serializer
from backend.models import Student, Tutor

from backend.serializers import UpdateStudentSerializer, UpdateTutorSerializer

import json


class ProfileSerializer(get_user_serializer()):
    """
    Profile serializer
    """

    def __init__(self, *args, **kwargs):
        """
        Custom to add partial=True to PUT method request to skip blank
        validations
        """

        if kwargs.get('context'):
            request = kwargs['context'].get('request', None)

            if request and getattr(request, 'method', None) == 'PUT':
                kwargs['partial'] = True

        super().__init__(*args, **kwargs)


class ProfileView(APIView):
    """
    Get user profile information
    """

    def get(self, request):
        user = self.request.user
        if not user.is_staff:
            student = Student.objects.get(user_id=user.id)
            dict_obj = model_to_dict(student)
            return Response(dict_obj, status=status.HTTP_200_OK)
        else:
            tutor = Tutor.objects.get(user_id=user.id)
            dict_obj = model_to_dict(tutor)
            return Response(dict_obj, status=status.HTTP_200_OK)


class ProfileUpdateView(RetrieveUpdateAPIView):
    """
    Get update user profile information
    """

    serializer_class = import_string(
        backend_settings.UPDATE_STUDENT_SERIALIZER)
    serializer_class_tutor = import_string(
        backend_settings.UPDATE_TUTOR_SERIALIZER)

    def get_object(self):
        return self.request.user

    def update(self, request, id, *args, **kwargs):
        """
        Custom update user profile
        """
        user = User.objects.get(id=id)
        if not user.is_staff:
            student = Student.objects.get(user_id=id)
            serializer_student = self.serializer_class(
                instance=student, data=request.data, partial=True)
            if serializer_student.is_valid():
                serializer_student.save()
                super().update(request, *args, **kwargs)
                return Response(serializer_student.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer_student.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            tutor = Tutor.objects.get(user_id=user.id)
            serializer_tutor = self.serializer_class_tutor(
                instance=tutor, data=request.data, partial=True)
            if serializer_tutor.is_valid():
                serializer_tutor.save()
                super().update(request, *args, **kwargs)
                return Response(serializer_tutor.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer_tutor.errors, status=status.HTTP_400_BAD_REQUEST)
