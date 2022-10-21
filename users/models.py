from ast import Param
from posixpath import supports_unicode_filenames
from random import choices
from sqlite3 import IntegrityError
from unicodedata import name
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

#USER
class User(AbstractUser):

    #model fields to change (need? or make via ordinary models of patients and doctors?)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

    #permissions


#extended models of users

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=11,blank=True)

    def __str__(self):
        return f"Doctor {str(self.user)}"


#patient
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, primary_key=True)
    gov_id = models.CharField(max_length=12,blank=True)
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=11,blank=True)
    email = models.EmailField(blank=True)
    contact_close = models.CharField(max_length=11,blank=True)

    assigned_doctor = models.ForeignKey(Doctor, related_name='assigned_patients', on_delete=models.PROTECT, default = Doctor.objects.get(surname="House").pk) #why added pk?

    def __str__(self):
        return f"{self.name} {self.surname}"

#appointments
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    medical_service = models.CharField(max_length = 50)
    date = models.DateField()

    def __str__(self):
        return f"Patient: {self.patient.name}; Doctor: {self.doctor.surname}; date: {self.date}"


#treatments
class Treatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='treatments')
    description = models.CharField(max_length=200, default='Description empty')
    medicaments = models.CharField(max_length=50, default='Mediacements empty')
    date = models.DateField()

    def __str__(self):
        return f"Patient: {self.patient.name}; Doctor: {self.doctor.surname}; date: {self.date}"