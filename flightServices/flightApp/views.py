from django.shortcuts import render
from .models import Reservation, Passenger, Flight
from .serializers import PassengerSerializer, ReservationSerializer, FlightSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

@api_view(['POST'])
def find_flights(request):
    flights = Flight.objects.filter(departureCity=request.data['departureCity'], arrivalCity=request.data['arrivalCity'],
                                    dateOfDeparture=request.data['dateOfDeparture'])
    serializer=FlightSerializer(flights, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def save_reservations(request):
    flight = Flight.objects.get(id=request.data['flightId'])
    passenger = Passenger(firstName=request.data['firstName'], lastName=request.data['lastName'],
                          email=request.data['email'], phoneNumber=request.data['phone'])
    Passenger.save(passenger)
    reservation = Reservation(flight = flight, passenger=passenger)
    Reservation.save(reservation)
    return Response(status=status.HTTP_201_CREATED)