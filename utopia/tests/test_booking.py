import unittest
from flask import Flask, json, jsonify

from utopia import app
from utopia.service.booking_service import BookingService
import random

BOOKING_SERVICE = BookingService()


FLIGHT_ID = 1
AGENT_ID=1
USER_ID = 31

def setup_booking_empty():

    return BOOKING_SERVICE.add_booking_empty()

def setup_passenger(id):
    passenger = {'booking_id': id, 'given_name' : 'John', 'family_name' : 'Doe', 'dob':'1997-12-31',
    'gender' : 'male', 'address' : '123 Glendora avenue, Plymouth PA'}
    return passenger

def setup_booking(booking, flight_id, user_id):

    return BOOKING_SERVICE.add_booking(booking, flight_id, user_id)


def teardown_booking(id):

    BOOKING_SERVICE.delete_booking(id)

def teardown_passenger(id):

    BOOKING_SERVICE.delete_passenger(id)

class TestAirline(unittest.TestCase):

    def test_add_booking(self):
        with app.app_context():

            booking_count = len(BOOKING_SERVICE.read_bookings().json['bookings'])

            booking = setup_booking_empty()
            self.assertEqual(booking_count+1, len(BOOKING_SERVICE.read_bookings().json['bookings']))

            teardown_booking(booking['id'])
    
    def test_add_passenger(self):
        with app.app_context():

            booking_count = len(BOOKING_SERVICE.read_bookings().json['bookings'])

            booking = setup_booking_empty()
            passenger = setup_passenger(booking['id'])
            passenger = BOOKING_SERVICE.add_passenger(passenger) 

            added_passenger = BOOKING_SERVICE.find_passenger(passenger['id'])
            self.assertEqual(passenger['booking_id'], added_passenger['booking_id'])
            self.assertEqual(passenger['family_name'], added_passenger['family_name'])
            self.assertEqual(passenger['address'], added_passenger['address'])
            self.assertEqual(passenger['dob'], added_passenger['dob'])
            self.assertEqual(passenger['gender'], added_passenger['gender'])
            self.assertEqual(passenger['given_name'], added_passenger['given_name'])


            teardown_passenger(added_passenger['id'])
            self.assertEqual(booking_count, len(BOOKING_SERVICE.read_bookings().json['bookings']))

    def test_find_flight_bookings(self):
        with app.app_context():

            passengers = [ setup_passenger(None) for x in range(10)]
            booking = {'passengers' : passengers}
            booking = setup_booking(booking, FLIGHT_ID, AGENT_ID)
            
            self.assertEqual(booking['flight_bookings']['flight_id'], FLIGHT_ID)
            self.assertEqual(booking['booking_agent']['agent_id'], AGENT_ID)
            
            for p_original, p_added in zip(passengers, booking['passengers']):
                self.assertEqual(p_original['given_name'], p_added['given_name'])
                self.assertEqual(p_original['family_name'], p_added['family_name'])
                self.assertEqual(p_original['address'], p_added['address'])
                self.assertEqual(p_original['dob'], p_added['dob'])
                self.assertEqual(p_original['gender'], p_added['gender'])
        
            teardown_booking(booking['id'])




