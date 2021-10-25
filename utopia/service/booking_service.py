from flask import Flask, app, jsonify
from flask_sqlalchemy import SQLAlchemy
from utopia.models.models import BOOKING_AGENT_SCHEMA, BOOKING_GUEST_SCHEMA, BOOKING_USER_SCHEMA, USER_SCHEMA, Booking, BookingAgent, BookingGuest, BookingPayment, BookingUser, Passenger, FlightBookings, BOOKING_SCHEMA, BOOKING_SCHEMA_MANY, PASSENGER_SCHEMA, PASSENGER_SCHEMA_MANY, FLIGHT_BOOKINGS_SCHEMA, FLIGHT_BOOKINGS_SCHEMA_MANY, BOOKING_PAYMENT_SCHEMA, User
BOOKING_AGENT_SCHEMA, BOOKING_USER_SCHEMA, BookingPayment, BookingUser, BookingAgent, BookingGuest
from utopia.models.flight_models import FLIGHT_SCHEMA, Flight, Route, Airport, FlightSchema, FLIGHT_SCHEMA_MANY, ROUTE_SCHEMA, ROUTE_SCHEMA_MANY, AIRPORT_SCHEMA, AIRPORT_SCHEMA_MANY

from utopia.models.base import Session

from rstr import Rstr

import logging
logging.basicConfig(level=logging.INFO)

TRAVELER = 3

CONFIRMATION_CODE_LENGTH = 50

def generate_random_chars(length):
    rstr = Rstr()
    return rstr.xeger(r'[a-zA-Z0-9_.-]{'+str(length)+'}')


class BookingService:

##################### GET #####################



    def read_bookings(self):
        logging.info('reading all bookings')

        session = Session()
        bookings = session.query(Booking).all()

        return jsonify({'bookings': BOOKING_SCHEMA_MANY.dump(bookings)})
    
    def find_booking(self, id):
        logging.info('finding booking with id %s ' %id)
        session = Session()

        booking = session.query(Booking).filter_by(id=id).first()
        bp = booking.booking_payment
        fb = booking.flight_bookings
        f = fb.flight
        r = f.route
        ba = booking.booking_agent
        bu = booking.booking_user
        bg = booking.booking_guest
        user = ba.user
        print(BOOKING_PAYMENT_SCHEMA.dump(bp))
        print(FLIGHT_BOOKINGS_SCHEMA.dump(fb))
        print(FLIGHT_SCHEMA.dump(f))
        print(ROUTE_SCHEMA.dump(r))
        print(BOOKING_AGENT_SCHEMA.dump(ba))
        print(BOOKING_USER_SCHEMA.dump(bu))
        print(BOOKING_GUEST_SCHEMA.dump(bg))
        print(USER_SCHEMA.dump(user))
        return BOOKING_SCHEMA.dump(booking)

    def read_passengers(self):
        logging.info('reading all passengers')
        session = Session()

        passengers = session.query(Passenger).all()

        return jsonify({'passengers' : PASSENGER_SCHEMA_MANY.dump(passengers)})

    def find_passenger(self, id):
        logging.info('finding passenger with id %s' %id)
        session = Session()

        passenger = session.query(Passenger).get(id)

        return PASSENGER_SCHEMA.dump(passenger)



  ##################### POST #####################
  
    def add_booking_empty(self):
        logging.info('add an empty booking')
        session = Session()

        booking = Booking(confirmation_code=generate_random_chars(CONFIRMATION_CODE_LENGTH))

        session.add(booking)
        session.commit()
        return BOOKING_SCHEMA.dump(booking)


    def add_booking(self, booking, flight_id, user_id):
        logging.info('add booking to flight %s with user %s' %(flight_id, user_id))
        session = Session()

        booking_to_add = Booking(confirmation_code=generate_random_chars(CONFIRMATION_CODE_LENGTH))

        session.add(booking_to_add)
        session.flush()

        logging.info('flush booking, booking id is now %d' %booking_to_add.id)

        if user_id == 'guest':
            logging.info('creating a guest booking')
            booking_to_add.booking_guest = BookingGuest(booking_id= booking_to_add.id, contact_email = 
            booking['contact_email'], contact_phone = booking['contact_phone'])
        else:
            user = session.query(User).get(user_id)
            if user.user_role.id == TRAVELER:
                logging.info('creating a user booking')
                booking_to_add.booking_user = BookingUser(booking_id = booking_to_add.id, user_id = user.id)
            else:
                logging.info('creating an agent booking')
                booking_to_add.booking_agent = BookingAgent(booking_id=booking_to_add.id, agent_id = user.id)
        
        
        
        logging.info('finding flight %s' %flight_id)
        flight = session.query(Flight).get(flight_id)
        booking_to_add.flight_bookings = FlightBookings(booking_id=booking_to_add.id, flight_id=flight.id)
        
        booking_to_add.booking_payment = BookingPayment(booking_id=booking_to_add.id, stripe_id=generate_random_chars(25))

        logging.info('adding passengers')
        if 'passengers' in booking:
            for passenger in booking['passengers']:
                passenger['booking_id'] = booking_to_add.id
                booking_to_add.passengers.append(Passenger(**passenger))
        
        session.commit()
        booking =  BOOKING_SCHEMA.dump(booking_to_add)
        session.close()

        return booking

        
    def add_passenger(self, passenger):
        logging.info('add passenger')
        session = Session()

        passenger = Passenger(**passenger)

        session.add(passenger)
        session.commit()

        return PASSENGER_SCHEMA.dump(passenger)

    def add_passengers(self, passengers):
        logging.info('add passengers')
        session = Session()

        passenger_list = []

        for passenger in passengers:
            passenger_to_add = Passenger(**passenger)
            passenger_list.append(passenger_to_add)

        session.bulk_save_objects(passenger_list, return_defaults=True)  
        session.commit()

        return jsonify({'passengers' : PASSENGER_SCHEMA_MANY.dump(passenger_list)})



##################### DELETE #####################


    def delete_booking(self, id):
        logging.info('delete booking with id %s' %id)
        session = Session()

        booking = session.query(Booking).get(id)
        session.delete(booking)
        session.commit()

        return ''

    def delete_passenger(self, id):
        logging.info('delete passenger with id %s ' %id)
        session = Session()

        passenger = session.query(Passenger).get(id)

        if len(passenger.booking.passengers) == 1:
            session.delete(passenger.booking)
        else:
            session.delete(passenger)
        session.commit()

        return ''