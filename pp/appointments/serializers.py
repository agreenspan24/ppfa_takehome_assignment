from rest_framework import serializers

from datetime import timedelta

from .models import Appointment
from ..doctors.models import Doctor
from ..doctors.serializers import DoctorSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    doctors = DoctorSerializer(many= True, default= [])

    class Meta:
        model = Appointment
        fields = ("id", "datetime", "reason", "new_patient", "contact_phone_number", "doctors")

    def find_or_create_doctor(self, doctor):
        existing_doctor = Doctor.objects.filter(name= doctor["name"]).first()

        if not existing_doctor:
            existing_doctor = Doctor.objects.create(**doctor)

        return existing_doctor

    def doctor_has_conflicting_appointments(self, doctor_id, datetime):
        return Appointment.objects.filter(
            doctors__id= doctor_id
        ).filter(
            datetime__gt= datetime - timedelta(hours= 1),
            datetime__lt= datetime + timedelta(hours= 1)
        ).exists()

    def create(self, validated_data):
        doctors = validated_data.pop("doctors", [])

        appointment = Appointment.objects.create(**validated_data)

        for doctor in doctors:
            doc = self.find_or_create_doctor(doctor)

            if not self.doctor_has_conflicting_appointments(doc.id, appointment.datetime):
                appointment.doctors.add(doc)

        return appointment

    def update(self, appointment, new_appointment):
        new_doctors = new_appointment.pop("doctors", [])
        new_appt_doctors = list(map(lambda d: d["name"], new_doctors))

        for (key, value) in new_appointment.items():
            setattr(appointment, key, value)

        appointment.save()

        existing_doctors = appointment.doctors.all()
        existing_appt_doctors = list(map(lambda d: d.id, existing_doctors))

        for new_doctor in new_doctors:
            doc = self.find_or_create_doctor(new_doctor)

            if not doc.id in existing_appt_doctors and \
                not self.doctor_has_conflicting_appointments(doc.id, appointment.datetime):
                appointment.doctors.add(doc)

        for old_doctor in existing_doctors:
            if not old_doctor.name in new_appt_doctors:
                appointment.doctors.remove(old_doctor)

        return appointment