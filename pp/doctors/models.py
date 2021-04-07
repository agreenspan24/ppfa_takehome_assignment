from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Doctor(models.Model):
  name = models.CharField(max_length= 50, null= False)

  NEUROSURGEON = 'NS'
  CARDIOLOGIST = 'CD'
  EAR_NOSE_AND_THROAT = 'EN'
  PODIATRIST = 'PD'
  DENTIST = 'DT'
  SPECIALTIES = [
      (NEUROSURGEON, 'Neurosurgeon'),
      (CARDIOLOGIST, 'Cardiologist'),
      (EAR_NOSE_AND_THROAT, 'Ear, Nose, & Throat'),
      (PODIATRIST, 'Podiatrist'),
      (DENTIST, 'Dentist')
  ]

  specialty = models.CharField(
    max_length= 2,
    choices= SPECIALTIES,
    default= DENTIST,
    null= False
  )

  rating = models.PositiveIntegerField(
    validators= [MinValueValidator(1), MaxValueValidator(5)]
  )
