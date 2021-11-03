import unittest
from flask import Flask, json, jsonify
from utopia.models.flights import Flight
from utopia.models.users import User


from utopia import app
from utopia.booking_service import BookingService
import random
from sqlalchemy.exc import IntegrityError, OperationalError
from utopia.models.base import db_session
BOOKING_SERVICE = BookingService()


ADMIN = 1
AGENT=2
TRAVELER = 3
GUEST = 'guest'

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

def get_user(role_id):
    user = db_session.query(User).filter_by(role_id=role_id).first()
    id = user.id
    db_session.close()
    return id

def get_flight():
    flight = db_session.query(Flight).first()
    flight_id = flight.id
    db_session.close()
    return flight_id

class TestBooking(unittest.TestCase):

    def test_add_booking(self):
        with app.app_context():

            booking_count = len(BOOKING_SERVICE.read_bookings().json['bookings'])

            booking = setup_booking({}, get_flight(), get_user(AGENT) )
            self.assertEqual(booking_count+1, len(BOOKING_SERVICE.read_bookings().json['bookings']))

            teardown_booking(booking['id'])
    
    def test_add_passenger(self):
        with app.app_context():

            booking_count = len(BOOKING_SERVICE.read_bookings().json['bookings'])

            booking = setup_booking({}, get_flight(), get_user(AGENT))
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

    def test_booking_agent(self):
        with app.app_context():

            passengers = [ setup_passenger(None) for x in range(10)]
            booking = {'passengers' : passengers}

            flight_id = get_flight()
            user_id = get_user(AGENT)

            booking = setup_booking(booking, flight_id, user_id)
            
            self.assertEqual(booking['flight_bookings']['flight_id'], flight_id)
            self.assertEqual(booking['booking_agent']['agent_id'], user_id)
            
            for p_original, p_added in zip(passengers, booking['passengers']):
                self.assertEqual(p_original['given_name'], p_added['given_name'])
                self.assertEqual(p_original['family_name'], p_added['family_name'])
                self.assertEqual(p_original['address'], p_added['address'])
                self.assertEqual(p_original['dob'].strftime("%Y-%m-%d"), p_added['dob'])
                self.assertEqual(p_original['gender'], p_added['gender'])
        
            teardown_booking(booking['id'])

    def test_booking_user(self):
        with app.app_context():

            passengers = [ setup_passenger(None) for x in range(10)]
            booking = {'passengers' : passengers}
            flight_id = get_flight()
            user_id = get_user(TRAVELER)


            booking = setup_booking(booking, flight_id, user_id)
            
            self.assertEqual(booking['flight_bookings']['flight_id'], flight_id)
            self.assertEqual(booking['booking_user']['user_id'], user_id)
            
            for p_original, p_added in zip(passengers, booking['passengers']):
                self.assertEqual(p_original['given_name'], p_added['given_name'])
                self.assertEqual(p_original['family_name'], p_added['family_name'])
                self.assertEqual(p_original['address'], p_added['address'])
                self.assertEqual(p_original['dob'].strftime("%Y-%m-%d"), p_added['dob'])
                self.assertEqual(p_original['gender'], p_added['gender'])
        
            teardown_booking(booking['id'])


    def test_booking_guest(self):
        with app.app_context():

            passengers = [ setup_passenger(None) for x in range(10)]
            booking = {'passengers' : passengers}
            booking_guest = {'contact_email' : 'jdoe@gmail.com', 'contact_phone' : '555 555 5555'}
            booking['booking_guest'] = booking_guest

            flight_id = get_flight()

            booking = setup_booking(booking, flight_id, GUEST)
            
            self.assertEqual(booking['flight_bookings']['flight_id'], flight_id)
            self.assertEqual(booking['booking_guest']['contact_email'], booking_guest['contact_email'])
            self.assertEqual(booking['booking_guest']['contact_phone'], booking_guest['contact_phone'])
         
            for p_original, p_added in zip(passengers, booking['passengers']):
                self.assertEqual(p_original['given_name'], p_added['given_name'])
                self.assertEqual(p_original['family_name'], p_added['family_name'])
                self.assertEqual(p_original['address'], p_added['address'])
                self.assertEqual(p_original['dob'].strftime("%Y-%m-%d"), p_added['dob'])
                self.assertEqual(p_original['gender'], p_added['gender'])
        
            teardown_booking(booking['id'])

    
    def test_booking_no_passengers(self):
        with app.app_context():

            booking = {}
            booking_guest = {'contact_email' : 'jdoe@gmail.com', 'contact_phone' : '555 555 5555'}
            booking['booking_guest'] = booking_guest

            flight_id = get_flight()

            booking = setup_booking(booking, flight_id, GUEST)
            
            self.assertEqual(booking['flight_bookings']['flight_id'], flight_id)
            self.assertEqual(booking['booking_guest']['contact_email'], booking_guest['contact_email'])
            self.assertEqual(booking['booking_guest']['contact_phone'], booking_guest['contact_phone'])
            self.assertEqual(booking['passengers'], [])

        
            teardown_booking(booking['id'])
    
    def test_booking_wrong_flight(self):
          with app.app_context():
            passengers = [ setup_passenger(None) for x in range(10)]
            booking = {'passengers' : passengers}

            self.assertRaises(AttributeError, setup_booking, booking, 0, get_user(AGENT))
            self.assertRaises(AttributeError, setup_booking, booking, None, get_user(AGENT))

    def test_booking_wrong_user(self):
            with app.app_context():
                passengers = [ setup_passenger(None) for x in range(10)]
                booking = {'passengers' : passengers}

                self.assertRaises(AttributeError, setup_booking, booking, get_flight(), 0)
                self.assertRaises(AttributeError, setup_booking, booking, get_flight(), None)

    def test_booking_wrong_guest(self):
            with app.app_context():
                passengers = [ setup_passenger(None) for x in range(10)]
                booking = {'passengers' : passengers}

                self.assertRaises(KeyError, setup_booking, booking, get_flight(), GUEST)

                booking['booking_guest'] = {'not_contact_email':'jdoe@gmail.com', 'contact_phone' : '555 555 5555'}

                self.assertRaises(KeyError, setup_booking, booking, get_flight(), GUEST)

    # def test_booking_bad_passengers(self):
    #         with app.app_context():
    #             passengers = [ setup_passenger(None) for x in range(10)]
    #             for passenger in passengers:
    #                 passenger['given_name'] = None
    #             booking = {'passengers' : passengers}

    #             self.assertRaises(OperationalError, setup_booking, booking, get_flight(), get_user(AGENT))

    def test_booking_passengers_with_id(self):
                with app.app_context():
                    passengers = [ setup_passenger(-1) for x in range(10)]
                    booking = {'passengers' : passengers}

                    booking = setup_booking(booking, get_flight(), get_user(AGENT))
                    teardown_booking(booking['id'])

    def test_booking_passengers_missing_field(self):
            with app.app_context():
                    passengers = [ setup_passenger(-1) for x in range(10)]
                    passengers.append({'booking_id': -1, 'family_name' : 'Doe', 'dob':'1997-12-31',
    'gender' : 'male', 'address' : '123 Glendora avenue, Plymouth PA'})
                    booking = {'passengers' : passengers}

                    self.assertRaises(KeyError, setup_booking, booking, get_flight(), get_user(AGENT))

    def test_update_booking_passengers(self):
                with app.app_context():
                        passengers = [ setup_passenger(None) for x in range(10)]
                        booking = {'passengers' : passengers}

                        flight_id = get_flight()
                        user_id = get_user(AGENT)

                        booking = setup_booking(booking, flight_id, user_id)

                        passengers = [{'booking_id': -1, 'given_name':'Jane', 'family_name' : 'Austen', 'dob':'1998-12-31',
                                        'gender' : 'female', 'address' : '123 Glendora avenue, Chino Hills'}]
                        booking['passengers'] = passengers
                        updated_booking = BOOKING_SERVICE.update_booking_passengers(booking)
                        self.assertEqual(len(updated_booking['passengers']), len(passengers))
                        p_added = updated_booking['passengers'][0]
                        p_original = passengers[0]
                        self.assertEqual(p_original['given_name'], p_added['given_name'])
                        self.assertEqual(p_original['family_name'], p_added['family_name'])
                        self.assertEqual(p_original['address'], p_added['address'])
                        self.assertEqual(p_original['dob'].strftime("%Y-%m-%d"), p_added['dob'])
                        self.assertEqual(p_original['gender'], p_added['gender'])
                        teardown_booking(updated_booking['id'])
        
    def test_update_passenger(self):
            with app.app_context():
                
                passenger = {'booking_id': -1, 'given_name':'Jane', 'family_name' : 'Austen', 'dob':'1998-12-31',
                                        'gender' : 'female', 'address' : '123 Glendora avenue, Chino Hills'}
                booking = {'passengers' : [passenger]}

                
                passenger = setup_booking(booking, get_flight(), get_user(3))['passengers'][0]
                update_passenger = {'id': passenger['id'], 'given_name':'Jane', 'family_name' : 'Austen',
                                        'address' : '123 Glendora avenue, Chino Hills'}
                BOOKING_SERVICE.update_passenger(update_passenger)

                passenger_from_db = BOOKING_SERVICE.find_passenger(passenger['id'])

                self.assertEqual(passenger_from_db['given_name'], update_passenger['given_name'])
                self.assertEqual(passenger_from_db['family_name'], update_passenger['family_name'])
                self.assertEqual(passenger_from_db['address'], update_passenger['address'])
                self.assertEqual(passenger_from_db['dob'], passenger['dob'])
                self.assertEqual(passenger_from_db['gender'], passenger['gender'])

                teardown_passenger(passenger_from_db['id'])


    def test_change_booking_type(self):
        with app.app_context():

            booking = {}

            admin = get_user(ADMIN)
            agent = get_user(AGENT)
            traveler = get_user(TRAVELER)
            booking = setup_booking(booking,get_flight(), agent)

            booking['booking_user']  = {'user_id' : traveler}  
            booking['booking_agent'] = None      
            booking = BOOKING_SERVICE.update_booking_method(booking)
            self.assertEqual(booking['booking_agent'], None)
            self.assertEqual(booking['booking_user']['user_id'], traveler)

            booking_guest = {'contact_email': 'jdoe@gmail.com', 'contact_phone':'555 555 5555'}
            booking['booking_guest'] = booking_guest      
            booking['booking_user'] = None      

            booking = BOOKING_SERVICE.update_booking_method(booking)
            self.assertEqual(booking['booking_guest']['contact_email'], booking_guest['contact_email'])
            self.assertEqual(booking['booking_guest']['contact_phone'], booking_guest['contact_phone'])
           
           
      
            booking['booking_guest'] = None
            booking['booking_agent'] = {'agent_id' : agent}
            booking = BOOKING_SERVICE.update_booking_method(booking)
            self.assertEqual(booking['booking_user'], None)
            self.assertEqual(booking['booking_guest'], None)
            self.assertEqual(booking['booking_agent']['agent_id'], agent)

            teardown_booking(booking['id'])

   
    def test_booking_type_wrong_id(self):
            with app.app_context():
                booking = {'id':0}
                
                self.assertRaises( AttributeError, BOOKING_SERVICE.update_booking_method, booking)

    



    def test_booking_type_wrong_fk(self):
            with app.app_context():
                
                agent_id = get_user(AGENT)
                traveler_id = get_user(TRAVELER)
                booking = setup_booking({}, get_flight(), agent_id)
                booking['booking_agent'] = {'agent_id' : traveler_id}
                self.assertRaises(IntegrityError, BOOKING_SERVICE.update_booking_method, booking)
                teardown_booking(booking['id'])

        









