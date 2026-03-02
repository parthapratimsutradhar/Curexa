from rest_framework import serializers
from apps.docbook.models import Appointment
from apps.docbook.models import Availability
from django.db import transaction


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            'appointment_type',
            'availability',
            'notes',
        )

    def validate(self, attrs):
        availability: Availability = attrs['availability']
        request = self.context['request']

        if availability.is_leave:
            raise serializers.ValidationError(
                {"availability": "Doctor is on leave on this day."}
            )

        if hasattr(availability, 'appointment'):
            raise serializers.ValidationError(
                {"availability": "This slot is already booked."}
            )

        attrs['doctor'] = availability.doctor
        attrs['patient'] = request.user.patientprofile

        return attrs

    def create(self, validated_data):
        availability = validated_data['availability']

        with transaction.atomic():
            availability = Availability.objects.select_for_update().get(
                id=availability.id
            )

            if hasattr(availability, 'appointment'):
                raise serializers.ValidationError(
                    {"availability": "This slot is already booked."}
                )

            appointment = Appointment.objects.create(**validated_data)

        return appointment


class AppointmentReadSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='availability.date', read_only=True)
    start_time = serializers.TimeField(source='availability.start_time', read_only=True)
    end_time = serializers.TimeField(source='availability.end_time', read_only=True)

    class Meta:
        model = Appointment
        fields = (
            'id',
            'appointment_type',
            'appointment_status',
            'doctor',
            'patient',
            'date',
            'start_time',
            'end_time',
            'notes',
            'created_at',
        )