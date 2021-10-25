from flask import Flask, app, jsonify
from flask_sqlalchemy import SQLAlchemy

from utopia.models.flights import FLIGHT_SCHEMA, Flight, Route, Airport, FlightSchema, FLIGHT_SCHEMA_MANY, ROUTE_SCHEMA, ROUTE_SCHEMA_MANY, AIRPORT_SCHEMA, AIRPORT_SCHEMA_MANY,FlightBookings

from utopia.models.booking import BOOKING_SCHEMA_FULL, BOOKING_SCHEMA_FULL_MANY,  Booking, BookingPayment, BookingSchemaFull, Passenger, BOOKING_SCHEMA, BOOKING_SCHEMA_MANY, PASSENGER_SCHEMA, PASSENGER_SCHEMA_MANY, FLIGHT_BOOKINGS_SCHEMA, FLIGHT_BOOKINGS_SCHEMA_MANY, BOOKING_PAYMENT_SCHEMA

from utopia.models.users import BookingUser, BookingAgent, BookingGuest, BOOKING_GUEST_SCHEMA, USER_SCHEMA, BOOKING_AGENT_SCHEMA, User, BOOKING_USER_SCHEMA, BOOKING_AGENT_SCHEMA,BOOKING_USER_SCHEMA

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

        return jsonify({'bookings': BOOKING_SCHEMA_FULL_MANY.dump(bookings)})
    
    def find_booking(self, id):
        logging.info('finding booking with id %s ' %id)
        session = Session()

        booking = session.query(Booking).filter_by(id=id).first()
        
        return BOOKING_SCHEMA_FULL.dump(booking)

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
        booking_schema = BookingSchemaFull
        if user_id == 'guest':
            logging.info('creating a guest booking')
            
            booking_to_add.booking_guest = BookingGuest(booking_id= booking_to_add.id, contact_email = 
            booking['booking_guest']['contact_email'], contact_phone = booking['booking_guest']['contact_phone'])
            booking_schema = BookingSchemaFull(exclude=['booking_agent', 'booking_user'])
        else:
            user = session.query(User).get(user_id)
            if user.user_role.id == TRAVELER:
                logging.info('creating a user booking')
                booking_to_add.booking_user = BookingUser(booking_id = booking_to_add.id, user_id = user.id)
                booking_schema = BookingSchemaFull(exclude=['booking_guest', 'booking_agent'])
            else:
                logging.info('creating an agent booking')
                booking_to_add.booking_agent = BookingAgent(booking_id=booking_to_add.id, agent_id = user.id)
                booking_schema = BookingSchemaFull(exclude=['booking_guest', 'booking_user'])

        
        
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
        booking =  booking_schema.dump(booking_to_add)

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