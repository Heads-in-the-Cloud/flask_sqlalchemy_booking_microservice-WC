import unittest

from flask.json import jsonify
from utopia.models.users import User
from utopia.models.flights import Airplane, Route, FLIGHT_SCHEMA, Flight
from tests.test_booking import setup_booking, setup_passenger, teardown_booking, teardown_passenger, get_user, get_flight
from utopia.models.base import db_session
from utopia.booking_service import BookingService
from utopia import app
from flask import Flask


DEPARTURE_TIME = '2050-09-20 12:00:00'

AGENT=1
TRAVELER = 3
GUEST = 'guest'

BOOKING_SERVICE = BookingService()



def find_flight(id):

    flight = db_session.query(Flight).get(id)
    flight = FLIGHT_SCHEMA.dump(flight)
    db_session.close()

    return flight

def setup_flight():

    flight = {'route_id': get_route(), 'airplane_id' : get_airplane(), 'departure_time': DEPARTURE_TIME, 'reserved_seats': 0, 'seat_price': 100}

    flight = Flight(**flight)
    db_session.add(flight)

    db_session.commit()
    flight_id = flight.id

    # db_session.close()


    return flight_id

def teardown_flight(id):

    flight = db_session.query(Flight).get(id)
    db_session.delete(flight)
    db_session.commit()
    db_session.close()

def get_route():

    route = db_session.query(Route).first()

    route_id = route.id
    return route_id

def get_airplane():

    airplane = db_session.query(Airplane).first()

    airplane_id = airplane.id
    return airplane_id

def setup_wrapper():

    flight_id = setup_flight()
    booking = {}
    booking['passengers'] = [setup_passenger(None) for x in range(3)]
    booking = setup_booking(booking, flight_id, get_user(AGENT))
    return jsonify({'flight_id':flight_id, 'booking': booking})



class TestBooking(unittest.TestCase):

    def test_add_seats(self):
        with app.app_context():

            test_data = setup_wrapper().json

            flight_id = test_data['flight_id']
            booking = test_data['booking']

            flight = find_flight(flight_id)
            self.assertEqual(flight['reserved_seats'], len(booking['passengers']))

            teardown_booking(booking['id'])
            teardown_flight(flight_id)
                
    def test_remove_seats_by_booking(self):
        with app.app_context():
            test_data = setup_wrapper().json
            flight_id = test_data['flight_id']
            booking = test_data['booking']

            teardown_booking(booking['id'])

            flight = find_flight(flight_id)
            self.assertEqual(flight['reserved_seats'], 0)
            teardown_flight(flight_id) 


    def test_remove_seats_by_passenger(self):
        with app.app_context():
            test_data = setup_wrapper().json
            flight_id = test_data['flight_id']
            booking = test_data['booking']


            reserved_seats = len(booking['passengers'])
            for passenger in booking['passengers']:
                flight = find_flight(flight_id)
                self.assertEqual(flight['reserved_seats'], reserved_seats)
                reserved_seats-=1

                teardown_passenger(passenger['id'])

            flight = find_flight(flight_id)
            self.assertEqual(flight['reserved_seats'], 0)

            teardown_flight(flight_id) 

    def test_seats_deactivate_booking(self):
        with app.app_context():
            test_data = setup_wrapper().json
            flight_id = test_data['flight_id']
            booking = test_data['booking']

            booking['is_active'] = False
            BOOKING_SERVICE.set_is_active(booking)

            flight = find_flight(flight_id)
            self.assertEqual(flight['reserved_seats'], 0)

            teardown_booking(booking['id'])
            teardown_flight(flight_id)

    def test_seats_activate_booking(self):
        with app.app_context():
            test_data = setup_wrapper().json
            flight_id = test_data['flight_id']
            booking = test_data['booking']

            booking['is_active'] = False
            BOOKING_SERVICE.set_is_active(booking)
            booking['is_active'] = True
            BOOKING_SERVICE.set_is_active(booking)

            flight = find_flight(flight_id)
            self.assertEqual(flight['reserved_seats'], len(booking['passengers']))

            teardown_booking(booking['id'])
            teardown_flight(flight_id)


    def test_seats_change_flight(self):
        with app.app_context():
            test_data = setup_wrapper().json
            flight_id_1 = test_data['flight_id']
            booking = test_data['booking']

            flight_id_2 = setup_flight()

            flight_bookings = {'booking_id': booking['id'], 'flight_id': flight_id_2}

            BOOKING_SERVICE.update_flight_bookings(flight_bookings)

            self.assertEqual(find_flight(flight_id_1)['reserved_seats'], 0)
            self.assertEqual(find_flight(flight_id_2)['reserved_seats'], len(booking['passengers']))

            teardown_booking(booking['id'])
            teardown_flight(flight_id_1)
            teardown_flight(flight_id_2)

    def test_seats_deleted_flight(self):
        with app.app_context():
            test_data = setup_wrapper().json
            flight_id = test_data['flight_id']
            booking = test_data['booking']

            teardown_flight(flight_id)

            booking['is_active'] = False
            BOOKING_SERVICE.set_is_active(booking)
            
            passenger = setup_passenger(None)
            passenger['booking_id'] = booking['id']
            BOOKING_SERVICE.add_passenger(passenger)

            teardown_booking(booking['id'])

    def test_seats_add_passenger(self):
        with app.app_context():
            test_data = setup_wrapper().json
            flight_id = test_data['flight_id']
            booking = test_data['booking']

            
            passenger = setup_passenger(None)
            passenger['booking_id'] = booking['id']
            BOOKING_SERVICE.add_passenger(passenger)

            flight = find_flight(flight_id)
            self.assertEqual(flight['reserved_seats'], len(booking['passengers'])+1)

            teardown_flight(flight_id)
            teardown_booking(booking['id'])

    
    def test_seats_add_passenger(self):
        with app.app_context():
            test_data = setup_wrapper().json
            flight_id = test_data['flight_id']
            booking = test_data['booking']

            
            passenger = setup_passenger(None)
            passenger['booking_id'] = booking['id']
            booking['passengers'] = [passenger]

            BOOKING_SERVICE.update_booking_passengers(booking)

            flight = find_flight(flight_id)
            self.assertEqual(flight['reserved_seats'], 1)

            teardown_flight(flight_id)
            teardown_booking(booking['id'])

    def test_seats_add_passenger_bulk(self):
        with app.app_context():
            test_data = setup_wrapper().json
            flight_id = test_data['flight_id']
            booking = test_data['booking']

            
            passengers = [setup_passenger(booking['id']) for x in range(10)]
            
            BOOKING_SERVICE.add_passengers(passengers)

            flight = find_flight(flight_id)
            self.assertEqual(flight['reserved_seats'], len(passengers) + len(booking['passengers']))

            teardown_flight(flight_id)
            teardown_booking(booking['id'])



    


                     
