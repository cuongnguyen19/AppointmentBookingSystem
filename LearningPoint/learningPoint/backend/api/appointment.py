from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views import View
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import status, filters
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import *

from backend.serializers import *
from backend.settings import backend_settings
from backend.utils.common import import_string, import_string_list

import json


class AppointmentCreateView(APIView):

    def post(self, request):
        user = self.request.user
        # Check to see if is tutor to perform action on this api
        if user.is_staff:
            tutor = Tutor.objects.get(user_id=user.id)
            students = []
            if request.data.get('student_ids'):
                for student_id in request.data.get('student_ids'):
                    student = Student.objects.get(id=student_id)
                    if student:
                        students.append(student.id)
            tutor_id = tutor.id

            data = request.data
            data['tutor'] = tutor_id
            data['students'] = students

            appointment = Appointment()

            serializer = AppointmentSerializer(instance=appointment, data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Reject if is not tutor
        return Response({"message": "You are not allowed to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)


class AppointmentListView(APIView):

    def get(self, request):
        user = self.request.user
        # Check if is tutor to get the appropriate list of appointments
        if user.is_staff:
            tutor = Tutor.objects.get(user_id=user.id)
            appointment_list = Appointment.objects.all().filter(
                tutor=tutor)

            o = request.GET.get("o")
            if o:
                appointment_list = appointment_list.order_by(o)
            else:
                appointment_list = appointment_list

            q = request.GET.get("q")  # search start
            if q:
                qs = Q(id__icontains=q) | Q(
                    description__icontains=q) | Q(
                    location__icontains=q) | Q(
                    topic__icontains=q) | Q(
                    meeting_type__icontains=q) | Q(
                    status__icontains=q) | Q(
                    notes__icontains=q)
                appointment_list = appointment_list.filter(qs)
            else:
                appointment_list = appointment_list  # search end
        # else get list of appointments from student account
        else:
            student = Student.objects.get(user_id=user.id)
            appointment_list = Appointment.objects.all()
            o = request.GET.get("o")
            if o:
                appointment_list = appointment_list.order_by(o)
            else:
                appointment_list = appointment_list

            q = request.GET.get("q")  # search start
            if q:
                qs = Q(id__icontains=q) | Q(
                    description__icontains=q) | Q(
                    location__icontains=q) | Q(
                    topic__icontains=q) | Q(
                    meeting_type__icontains=q) | Q(
                    status__icontains=q) | Q(
                    notes__icontains=q)
                appointment_list = appointment_list.filter(qs)
            else:
                appointment_list = appointment_list  # search end

        appointments = []
        for appointment in appointment_list.values():
            tutor_id = appointment["tutor_id"]
            tutor = Tutor.objects.get(id=tutor_id)
            tutor_name = tutor.first_name + " " + tutor.last_name
            appointment["tutor_name"] = tutor_name
            appointments.append(appointment)

        return Response(appointments, status=status.HTTP_200_OK)


class AppointmentBookedListView(APIView):

    def get(self, request):
        user = self.request.user
        user_name = user.username
        # only show this view to student
        if not user.is_staff:
            student = Student.objects.get(user_id=user.id)
            appointment_list = Appointment.objects.all().filter(
                students__in=[student])

            o = request.GET.get("o")
            if o:
                appointment_list = appointment_list.order_by(o)
            else:
                appointment_list = appointment_list

            q = request.GET.get("q")  # search start
            if q:
                qs = Q(id__icontains=q) | Q(
                    description__icontains=q) | Q(
                    location__icontains=q) | Q(
                    topic__icontains=q) | Q(
                    meeting_type__icontains=q) | Q(
                    status__icontains=q) | Q(
                    notes__icontains=q)
                appointment_list = appointment_list.filter(qs)
            else:
                appointment_list = appointment_list  # search end

            return Response(appointment_list.values(), status=status.HTTP_200_OK)
        # reject if is not student
        return Response({"message": "You are not allowed to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)


class AppointmentUpdateView(UpdateAPIView):
    permission_classes = import_string_list(
        backend_settings.UPDATE_APPOINTMENT_PERMISSION_CLASSES)
    serializer_class = import_string(
        backend_settings.UPDATE_APPOINTMENT_SERIALIZER)

    def update(self, request, id):
        """
        `Update Appointment`
        """
        user = self.request.user
        # only allow tutor to update appointment
        if user.is_staff:
            appointment = Appointment.objects.get(
                id=id)
            data = request.data
            serializer = self.serializer_class(
                instance=appointment, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "You are not allowed to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)


class AppointmentDeleteView(APIView):
    def delete(self, request, id):
        """
        `Delete Appointment`
        """

        # appointment_ids = request.data.get('appointment_ids')
        # appointment = Appointment.objects.all().filter(
        #     id__in=appointment_ids)
        user = self.request.user
        # only allow tutor to delete appointment
        if user.is_staff:
            appointment = Appointment.objects.get(
                id=id)
            return Response(appointment.delete(), status=status.HTTP_200_OK)
        return Response({"message": "You are not allowed to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)


class AppointmentBookView(UpdateAPIView):
    permission_classes = import_string_list(
        backend_settings.APPOINTMENT_PERMISSION_CLASSES)
    serializer_class = import_string(
        backend_settings.APPOINTMENT_SERIALIZER)

    def update(self, request, id):
        user = self.request.user
        # only student can book appointments
        if not user.is_staff:
            print(user.id)
            student = Student.objects.get(user_id=user.id)

            appointment = Appointment.objects.get(
                id=id)

            if (student in list(appointment.students.all())):
                return Response({"message": "You have already booked this appointment"},
                                status=status.HTTP_400_BAD_REQUEST)

            students = []
            for s in appointment.students.all():
                students.append(s.id)

            students.append(student.id)

            data = {}

            data['students'] = students
            data['vacancy'] = appointment.vacancy-1

            if data['vacancy'] < 0:
                return Response({"message": "There is no vacancy left for this appointment"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(
                instance=appointment, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "You are not allowed to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)


class AppointmentUnbookView(UpdateAPIView):

    def update(self, request, id):
        user = self.request.user
        # only students can  unbook appointment
        if not user.is_staff:
            student = Student.objects.get(user_id=user.id)

            appointment = Appointment.objects.get(id=id)

            students = []
            for s in appointment.students.all():
                students.append(s.id)

            students.remove(student.id)

            data = {}

            data['students'] = students
            data['vacancy'] = appointment.vacancy+1

            serializer = AppointmentSerializer(
                instance=appointment, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "You are not allowed to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
