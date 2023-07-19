from .models import Booking
from rest_framework import serializers

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
                    'id',
                    'first_name',
                    'last_name',
                    'email',
                    'phone_number',
                    'people',
                    'date',
                    'time',
                    'additional_comments'
                ]