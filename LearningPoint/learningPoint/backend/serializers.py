from rest_framework import serializers
from .models import Appointment, Student, Tutor


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("first_name",
                  "last_name",
                  "email",
                  "faculty",
                  "units")


class UpdateTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ("first_name",
                  "last_name",
                  "email",
                  "units")


class UpdateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ("time",
                  "capacity",
                  "vacancy",
                  "duration",
                  "location",
                  "topics",
                  "creator")
