from rest_framework import serializers
from apps.docbook.models import Appointment
from apps.docbook.models import Availability
from django.db import transaction
from apps.accounts.services.patient_services import get_patient


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

        doctor = availability.doctor
        patient = get_patient(request.user.id)

        attrs['doctor'] = doctor
        attrs['patient'] = patient

        # ✅ FIX: set base_fee from doctor profile
        attrs['base_fee'] = doctor.consultation_fee

        # Optional defaults
        attrs.setdefault('discount_amount', 0)
        attrs.setdefault('tax_amount', 0)

        return attrs

    def create(self, validated_data):
        availability = validated_data['availability']

        with transaction.atomic():
            availability = Availability.objects.select_for_update().get(
                id=availability.id
            )
            
            if not availability.is_available:
                raise serializers.ValidationError(
                    {"availability": "This slot is not available."}
                )

            if hasattr(availability, 'appointment'):
                raise serializers.ValidationError(
                    {"availability": "This slot is already booked."}
                )

            appointment = Appointment.objects.create(**validated_data)
            availability.is_available = False
            availability.save(update_fields=["is_available", "updated_at"])

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
