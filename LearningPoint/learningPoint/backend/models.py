from django.db import models

from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from datetime import *
import datetime as dt
import json


class Unit(models.Model):
    unit_id = models.CharField(primary_key=True, max_length=10)
    description = models.CharField(max_length=10000)
    coordinator = models.CharField(max_length=100)

    def __str__(self):
        return str(self.unit_id)


class Room(models.Model):
    room_number = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    building_name = models.CharField(max_length=100)

    def __str__(self):
        return self.room_number


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True)
    faculty = models.CharField(max_length=100, null=True)
    units = models.ManyToManyField(Unit, blank=True)

    def __str__(self):
        return self.user.username

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Tutor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True)
    units = models.ManyToManyField(Unit)

    def __str__(self):
        return self.user.username

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Appointment(models.Model):
    id = models.CharField(primary_key=True, max_length=1000)
    students = models.ManyToManyField(Student, blank=True)
    tutor = models.ForeignKey(
        Tutor, on_delete=models.CASCADE)
    time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, validators=[
        MinValueValidator(10),
        MaxValueValidator(120)
    ])
    capacity = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])
    vacancy = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(0)
    ])
    location = models.CharField(max_length=1000, null=True)
    topics = models.CharField(max_length=10000, null=True)
    creator = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def save(self, *args, **kwargs):
        if self.vacancy > self.capacity:
            raise ValidationError(
                "Vacancy must be less than or equal to the capacity")

        return super(Appointment, self).save(*args, **kwargs)
