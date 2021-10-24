from flask import Flask
from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import backref, relation, relationship
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields
# from utopia.models.flight_models import Flight
from utopia import app
from utopia.models.base import Base


ma = Marshmallow(app)


class FlightBookings(Base):
    __tablename__ = 'flight_bookings'

    booking_id = Column(Integer, ForeignKey('booking.id'), primary_key=True)
    flight_id = Column(Integer, ForeignKey('flight.id'), primary_key=True)


class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    is_active =  Column(Boolean, default=True)
    confirmation_code = Column(String(255))
    passengers = relationship('Passenger', backref='booking', lazy='subquery', cascade='all, delete')
    flight_bookings = relationship('FlightBookings', backref='booking', lazy='subquery', cascade='all, delete', uselist=False)

class Passenger(Base):
    __tablename__= 'passenger'

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('booking.id'))
    given_name = Column(String(255))
    family_name = Column(String(255))
    dob = Column(String(10))
    gender = Column(String(45))
    address = Column(String(45))



class FlightBookingsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FlightBookings
    booking_id = auto_field()
    flight_id = auto_field()

class PassengerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Passenger
        ordered = True
    id = auto_field()
    booking_id = auto_field()
    given_name = auto_field()
    family_name = auto_field()
    dob = auto_field()
    gender = auto_field()
    address = auto_field()

class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        ordered = True
    id = auto_field()
    is_active = auto_field()
    confirmation_code = auto_field()

BOOKING_SCHEMA = BookingSchema()
PASSENGER_SCHEMA = PassengerSchema()
FLIGHT_BOOKINGS_SCHEMA = FlightBookingsSchema()

BOOKING_SCHEMA_MANY = BookingSchema(many=True)
PASSENGER_SCHEMA_MANY = PassengerSchema(many=True)
FLIGHT_BOOKINGS_SCHEMA_MANY = FlightBookingsSchema(many=True)