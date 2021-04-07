from django.db import models
from django.core.validators import RegexValidator

class Appointment(models.Model):
    ANNUAL_CHECKUP = 'CH'
    GENERAL_CONSULTATION = 'GC'
    GENERAL_FOLLOW_UP = 'GF'
    NEW_PATIENT_VISIT = 'NP'
    SCREENING_FOR_DISEASE = 'SD'
    VACCINATION = 'VC'
    APPOINTMENT_REASONS = [
        (ANNUAL_CHECKUP, 'Annual Checkup'),
        (GENERAL_CONSULTATION, 'General Consultation'),
        (GENERAL_FOLLOW_UP, 'General Follow Up'),
        (NEW_PATIENT_VISIT, 'New Patient Visit'),
        (SCREENING_FOR_DISEASE, 'Screening for Disease'),
        (VACCINATION, 'Vaccination'),
    ]

    phone_number_regex = RegexValidator(regex=r'\([1-9][\d]{2}\)[1-9][\d]{2}-[1-9][\d]{3}', message='Phone numbers must be in the format (xxx)xxx-xxxx')

    datetime = models.DateTimeField(null=False)
    reason = models.CharField(
        max_length=2,
        choices=APPOINTMENT_REASONS,
        default='GC',
        null=False
    )
    new_patient = models.BooleanField(null=False)
    contact_phone_number = models.CharField(validators=[phone_number_regex], max_length=13)

    doctors = models.ManyToManyField("doctors.Doctor", related_name= "doctors")