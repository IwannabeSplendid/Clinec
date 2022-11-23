from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Patient, Doctor, Appointment, Treatment, Chatrooms, Messages

# Register your models here.
#to manipulate models using admin

#register user, and userAdmin (so Admin is not overwritten our custom user)
admin.site.register(User, UserAdmin)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Treatment)
admin.site.register(Chatrooms)
admin.site.register(Messages)