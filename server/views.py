from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BookingSerializer
from django.conf import settings
# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core import serializers
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from .serializers import BookingSerializer, MenuSerializer
from .models import Booking, Menu
@api_view(['GET', 'POST'])
def BookTime(request):
    if request.method=='GET':
        return Response({"message": "Success!"})
    if request.method=='POST':
        booking = BookingSerializer(data = request.data)
        booking.is_valid(raise_exception=True)
        booking.save()

        subject = 'Little Lemon Reservation'
        message = """Hi {},

        Do your reservation for Little Lemon.

        Your reservation information is as follows:
        Name: {} {}
        Phone number: {}
        Number of People: {}
        Date: {}
        Time: {}
        Additional Comments: {}

        """.format(booking.data['first_name'],
                booking.data['first_name'],
                booking.data['last_name'],
                booking.data['phone_number'],
                booking.data['people'],
                booking.data['date'],
                booking.data['time'],
                booking.data['additional_comments'],
        )
        return Response({"message": 'Email: {}'.format(booking.data['email'])})
class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = Booking.objects.all()
#
# Page views
#
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html')

def reservations(request:HttpRequest) -> HttpResponse:
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'reservations.html',{"bookings":booking_json})