from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from datetime import datetime
from pytz import timezone

from .serializers import AppointmentSerializer
from .models import Appointment

class GetDeleteUpdateAppointments(RetrieveUpdateAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self, pk):
        return Appointment.objects.get(pk= pk)

    def get(self, request, pk):
        appointment = None

        try:
            appointment = self.get_queryset(pk)

        except:
            return Response("Appointment does not exist", status= status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(appointment)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        appointment = None

        try:
            appointment = self.get_queryset(pk)

        except:
            return Response("Appointment does not exist.", status= status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            appointment,
            data= request.data,
            partial= True
        )

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except ValidationError as e:
            return Response(e.detail, status= status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        appointment = None

        try:
            appointment = self.get_queryset(pk)

        except:
            return Response("Appointment does not exist.", status= status.HTTP_404_NOT_FOUND)

        appointment.delete()

        return Response(status= status.HTTP_204_NO_CONTENT)


class GetPostAppointments(ListCreateAPIView):
    serializer_class = AppointmentSerializer

    def parse_date_from_query_params(self, param_name):
        raw_date = self.request.query_params.get(param_name, None)

        if not raw_date:
            return None

        try:
            return timezone("UTC").localize(datetime.strptime(raw_date, "%m-%d-%Y"))

        except:
            return None

    def get_queryset(self):
        appointments = Appointment.objects.all()

        start_date = self.parse_date_from_query_params("start_date")
        end_date = self.parse_date_from_query_params("end_date",)

        if start_date:
            appointments = appointments.filter(datetime__gte= start_date)

        if end_date:
            appointments = appointments.filter(datetime__lte= end_date)

        return appointments

    def get(self, request):
        appointments = self.get_queryset()

        serializer = self.serializer_class(appointments, many= True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)

        try:
            serializer.is_valid(raise_exception= True)
            serializer.save()

        except ValidationError as e:
            return Response(e.detail, status= status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status= status.HTTP_201_CREATED)

    