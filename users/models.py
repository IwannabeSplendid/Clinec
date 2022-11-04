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
    date_of_birth = models.DateField(blank=True)
    IIN = models.CharField(max_length=12, blank=True)
    gov_id = models.CharField(max_length=12,blank=True)
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=11,blank=True)
    department_ID = models.CharField(max_length=6, blank=True)
    spec_ID = models.CharField(max_length=6, blank=True)
    experience = models.CharField(max_length=2, blank=True)
    photo = models.ImageField(upload_to='images', blank=True)
    category=models.CharField(max_length=10, blank=True)
    appointment_price = models.CharField(max_length = 7, blank=True)
    working_schedule = models.CharField(max_length = 50, blank=True)
    education = models.CharField(max_length=30, blank=True)
    rating = models.CharField(max_length = 2, blank=True)
    address = models.CharField(max_length = 30, blank=True)
    homepage = models.URLField(blank=True)

    def __str__(self):
        return f"Doctor {str(self.user)}"


#patient
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, primary_key=True)
    date_of_birth = models.DateField(blank=True)
    IIN = models.CharField(max_length=12, blank=True)
    gov_id = models.CharField(max_length=12,blank=True)
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    blood_group = models.CharField(max_length=2, blank=True)
    contact_close = models.CharField(max_length=11,blank=True)
    phone_number = models.CharField(max_length=11,blank=True)
    address = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(max_length=10, blank=True)
    registration_date = models.DateField()
    email = models.EmailField(blank=True)

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