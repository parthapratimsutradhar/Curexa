from rest_framework.views import APIView
from django.views import View
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.docbook.serializers.appointment_serializer import AppointmentCreateSerializer, AppointmentReadSerializer
from apps.docbook.services import appointment_services


class AppointmentBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AppointmentCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        appointment = serializer.save()
        payment_payload = appointment_services.appointment_checkout(appointment)

        return Response(
            {
                "appointment_id": appointment.id,
                "payment": payment_payload,
                "message": "Appointment booked successfully"
            },
            status=status.HTTP_201_CREATED
        )

class AppointmentsByDoctorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        result = appointment_services.get_doctor_grouped_appointments(
            date=data.get("date"),
            start_date=data.get("date_from"),
            end_date=data.get("date_to"),
            doctor_id=data.get("doctor_id"),
            status=data.get("status"),
            sort_by=data.get("sort_by", "start_time"),
            order=data.get("order", "asc"),
        )

        return Response(result, status=status.HTTP_200_OK)


class AppointmentsListView(View):
    def get(swlf, request):
        return render(request, "enduser/docbook/my_appointments.html")
    

class AppointmentBookView(View):
    def get(swlf, request):
        return render(request, "enduser/docbook/book_appointment.html")
