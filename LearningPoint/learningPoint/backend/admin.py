from django.contrib import admin
from .models import Unit, Room, Student, Appointment, Tutor
# Register your models here.

admin.site.register(Unit)
admin.site.register(Room)
admin.site.register(Student)
admin.site.register(Appointment)
admin.site.register(Tutor)
