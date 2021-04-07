from django.test import TestCase
import requests
from .models import Appointment
from datetime import datetime, timedelta

class AppointmentTest(TestCase):
    def create_appointment(self, data= {}):
        base_data = {
            "datetime": datetime.now(),
            "reason": "GC",
            "new_patient": True,
            "contact_phone_number": "(214)543-2542"
        }

        merged_data = {**base_data, **data}

        response = requests.post("http://localhost:8000/api/v1/appointments/", data= merged_data)

        if response.status_code != 201:
            return None

        return response.json()


    def delete_appointment(self, id):
        response = requests.delete(f"http://localhost:8000/api/v1/appointments/{id}")

        if response.status_code != 200:
            return None


    def get_appointment(self, id):
        response = requests.get(f"http://localhost:8000/api/v1/appointments/{id}")

        if response.status_code != 200:
            return None

        return response.json()


    def get_appointments(self, start_date= None, end_date= None):
        response = requests.get("http://localhost:8000/api/v1/appointments", params= {
            "start_date": start_date,
            "end_date": end_date
        })

        if response.status_code != 200:
            return None

        return response.json()


    def update_appointment(self, id, data):
        response = requests.post(f"http://localhost:8000/api/v1/appointments/{id}", data= data)

        if response.status_code != 200:
            return None

        return response.json()


    def delete_all_appointments(self):
        appointments = self.get_appointments()

        for appt in appointments:
            self.delete_appointment(appt["id"])


    def setUp(self):
        pass


    def tearDown(self):
        self.delete_all_appointments()


    def test_get_appointments(self):
        appt_one = self.create_appointment()
        appt_two = self.create_appointment()

        server_appointments = self.get_appointments()

        self.assertIsNotNone(appt_one)
        self.assertIsNotNone(appt_two)
        self.assertIsNotNone(server_appointments)

        server_appt_ids = list(map(lambda a: a["id"], server_appointments))

        self.assertEqual(len(server_appt_ids), 2, "More appointments exist on server than created")
        self.assertIn(appt_one["id"], server_appt_ids, "Appointment one not in list from server")
        self.assertIn(appt_two["id"], server_appt_ids, "Appointment two not in list from server")


    def test_create_appointment(self):
        appt = self.create_appointment()

        self.assertIsNotNone(appt, "Appointment was not created")


    def test_delete_appointment(self):
        appt = self.create_appointment()
        self.assertIsNotNone(appt)

        self.delete_appointment(appt["id"])

        all_appointments = self.get_appointments()

        self.assertIsNotNone(all_appointments)
        self.assertNotIn(appt["id"], map(lambda a: a["id"], all_appointments), "Appointment was not deleted")


    def test_get_appointment_by_pk(self):
        appt = self.create_appointment()
        self.assertIsNotNone(appt)

        fetched_appt = self.get_appointment(appt["id"])

        self.assertIsNotNone(fetched_appt)
        self.assertEqual(appt["id"], fetched_appt["id"])
        self.assertEqual(appt["datetime"], fetched_appt["datetime"])
        self.assertEqual(appt["reason"], fetched_appt["reason"])
        self.assertEqual(appt["new_patient"], fetched_appt["new_patient"])
        self.assertEqual(appt["contact_phone_number"], fetched_appt["contact_phone_number"])


    def test_update_appointment(self):
        appt = self.create_appointment()
        self.assertIsNotNone(appt)

        appt_updates = {
            "datetime": datetime.now() + timedelta(hours= 2),
            "reason": "CH",
            "new_patient": False
        }

        updated_appt = self.update_appointment(appt["id"], appt_updates)
        self.assertIsNotNone(updated_appt)

        fetched_appt = self.get_appointment(appt["id"])
        self.assertIsNotNone(fetched_appt)

        self.assertEqual(fetched_appt["id"], appt["id"])
        self.assertEqual(fetched_appt["datetime"], updated_appt["datetime"])
        self.assertEqual(fetched_appt["reason"], updated_appt["reason"])
        self.assertEqual(fetched_appt["new_patient"], updated_appt["new_patient"])
        self.assertEqual(fetched_appt["contact_phone_number"], appt["contact_phone_number"])


    def test_get_appointments_filtered(self):
        appt_today = self.create_appointment()
        appt_next_week = self.create_appointment({
            "datetime": datetime.now() + timedelta(days= 7)
        })

        self.assertIsNotNone(appt_today)
        self.assertIsNotNone(appt_next_week)

        fetched_appts = self.get_appointments(
            start_date= datetime.now().strftime("%m-%d-%Y"),
            end_date= (datetime.now() + timedelta(days= 2)).strftime("%m-%d-%Y")
        )

        self.assertIsNotNone(fetched_appts)
        self.assertIn(appt_today["id"], map(lambda a: a["id"], fetched_appts))
        self.assertNotIn(appt_next_week["id"], map(lambda a: a["id"], fetched_appts))

