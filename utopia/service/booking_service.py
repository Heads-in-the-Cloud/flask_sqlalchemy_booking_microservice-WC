from flask import Flask, app, jsonify
from flask_sqlalchemy import SQLAlchemy
from utopia.models.models import Booking, Passenger, FlightBookings, BOOKING_SCHEMA, BOOKING_SCHEMA_MANY, PASSENGER_SCHEMA, PASSENGER_SCHEMA_MANY, FLIGHT_BOOKINGS_SCHEMA, FLIGHT_BOOKINGS_SCHEMA_MANY
from utopia.models.flight_models import Flight, Route, Airport, FlightSchema, FLIGHT_SCHEMA_MANY, ROUTE_SCHEMA, ROUTE_SCHEMA_MANY, AIRPORT_SCHEMA, AIRPORT_SCHEMA_MANY

from utopia.models.base import Session

from rstr import Rstr

import logging
logging.basicConfig(level=logging.INFO)


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
        flight = session.query(Flight).filter_by(id=1).first()
        
        print('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf')
        print('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf')
        print('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf')
        print('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf')
        print(FlightSchema().dump(flight))
        print(FLIGHT_BOOKINGS_SCHEMA.dump(flight.flight_bookings))
        # print(FLIGHT_BOOKINGS_SCHEMA.dump(booking.flight_bookings))
        print(flight.flight_bookings.booking)
        # flight_bookings = session.query(FlightBookings).filter_by(flight_id=booking.flight_bookings.flight_id).first()
        # print(FlightSchema().dump(flight_bookings.flight))
        # print(BOOKING_SCHEMA.dump(flight_bookings.booking))
        print(FlightSchema().dump(booking.flight_bookings.flight))
        print(FlightSchema().dump(booking.flight_bookings.flight))
        print(ROUTE_SCHEMA.dump(booking.flight_bookings.flight.route))
        return BOOKING_SCHEMA.dump(booking)

    def read_passengers(self):
        logging.info('reading all passengers')
        session = Session()

        passengers = session.query(Passenger).all()

        return jsonify({'passengers' : PASSENGER_SCHEMA_MANY.dump(passengers)})

    def find_passenger(self, id):
        logging.info('finding passenger with id %s' %id)
        session = Session()

        passenger = Passenger.query.get_or_404(id)

        return PASSENGER_SCHEMA.dump(passenger)



  ##################### POST #####################
  
    def add_booking_empty(self):
        logging.info('add an empty booking')
        session = Session()

        booking = Booking(confirmation_code=generate_random_chars(CONFIRMATION_CODE_LENGTH))

        session.add(booking)
        session.commit()
        return BOOKING_SCHEMA.dump(booking)

    def add_passenger(self, passenger):
        logging.info('add passenger')
        session = Session()

        passenger = Passenger(booking_id = passenger['booking_id'],
                    given_name = passenger['given_name'],
                    family_name=passenger['family_name'],
                    dob=passenger['dob'],
                    gender=passenger['gender'],
                    address=passenger['address']
        )
        session.add(passenger)
        session.commit()

        return PASSENGER_SCHEMA.dump(passenger)

    def add_passengers(self, passengers):
        logging.info('add passengers')
        session = Session()

        passenger_list = []

        for passenger in passengers:
            passenger_to_add = Passenger(booking_id = passenger['booking_id'],
                        given_name = passenger['given_name'],
                        family_name=passenger['family_name'],
                        dob=passenger['dob'],
                        gender=passenger['gender'],
                        address=passenger['address']
            )
            passenger_list.append(passenger_to_add)

        session.bulk_save_objects(passenger_list, return_defaults=True)  
        session.commit()

        return jsonify({'passengers' : PASSENGER_SCHEMA_MANY.dump(passenger_list)})



##################### DELETE #####################


    def delete_booking(self, id):
        logging.info('delete booking with id %s' %id)
        session = Session()

        booking = session.query(Booking).filter_by(id=id)
        session.delete(booking)
        session.commit()

        return ''

    def delete_passenger(self, id):
        logging.info('delete passenger with id %s ' %id)
        session = Session()

        passenger = Passenger.query.get_or_404(id)

        if len(passenger.booking.passengers) == 1:
            session.delete(passenger.booking)
        else:
            session.delete(passenger)
        session.commit()

        return ''