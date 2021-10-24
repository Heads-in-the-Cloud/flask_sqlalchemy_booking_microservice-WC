import unittest
from flask import Flask, json, jsonify

from utopia import app
from utopia.service.booking_service import BookingService
import random

BOOKING_SERVICE = BookingService()


def setup_booking_empty():

    return BOOKING_SERVICE.add_booking_empty()

def setup_passenger(id):
    passenger = {'booking_id': id, 'given_name' : 'John', 'family_name' : 'Doe', 'dob':'1997-12-31',
    'gender' : 'male', 'address' : '123 Glendora avenue, Plymouth PA'}
    return BOOKING_SERVICE.add_passenger(passenger)

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
            
            added_passenger = BOOKING_SERVICE.find_passenger(passenger['id'])
            self.assertEqual(passenger['booking_id'], added_passenger['booking_id'])
            self.assertEqual(passenger['family_name'], added_passenger['family_name'])
            self.assertEqual(passenger['address'], added_passenger['address'])

            teardown_passenger(added_passenger['id'])
            self.assertEqual(booking_count, len(BOOKING_SERVICE.read_bookings().json['bookings']))


