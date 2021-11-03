from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy.sql.sqltypes import Boolean, Date
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import backref, relation, relationship
from utopia import app
from utopia.models.base import Base


from utopia.models.users import BookingAgentSchema, BookingGuestSchema, BookingUserSchema
from utopia.models.flights import FlightSchema, FlightBookingsSchema


ma = Marshmallow(app)





class BookingPayment(Base):
    __tablename__ = 'booking_payment'

    booking_id = Column(Integer, ForeignKey('booking.id'), primary_key=True)
    stripe_id = Column(String(255))
    refunded = Column(Boolean, default=False)


class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    is_active =  Column(Boolean, default=True)
    confirmation_code = Column(String(255))
    passengers = relationship('Passenger', backref='booking', lazy='subquery', cascade='save-update, merge, all, delete, delete-orphan')
    flight_bookings = relationship('FlightBookings', backref='booking', lazy='subquery', cascade='all, delete', uselist=False)
    booking_payment = relationship('BookingPayment', backref='booking', lazy='subquery', cascade='all, delete', uselist=False)
    booking_agent = relationship('BookingAgent', backref='booking', lazy='subquery', cascade='save-update, merge, delete, delete-orphan', uselist=False)
    booking_user = relationship('BookingUser', backref='booking', lazy='subquery', cascade='save-update, merge, delete, delete-orphan', uselist=False)
    booking_guest = relationship('BookingGuest', backref='booking', lazy='subquery', cascade='save-update, merge, delete, delete-orphan', uselist=False)




class Passenger(Base):
    __tablename__= 'passenger'

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('booking.id'))
    given_name = Column(String(255))
    family_name = Column(String(255))
    dob = Column(Date)
    gender = Column(String(45))
    address = Column(String(45))





######################################## SCHEMAS ########################################





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





class BookingPaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookingPayment
    booking_id = auto_field()
    stripe_id = auto_field()
    refunded = auto_field()



class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        ordered = True
    id = auto_field()
    is_active = auto_field()
    confirmation_code = auto_field()



class BookingSchemaFull(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        ordered = True
    id = auto_field()
    is_active = auto_field()
    confirmation_code = auto_field()
    flight_bookings = fields.Nested(FlightBookingsSchema, only=['flight_id', 'flight'])
    booking_agent = fields.Nested(BookingAgentSchema, only=['agent_id', 'user'])
    booking_user = fields.Nested(BookingUserSchema, only = ['user_id', 'user'])
    booking_guest = fields.Nested(BookingGuestSchema, only = ['contact_email', 'contact_phone'])
    passengers = fields.List(fields.Nested(PassengerSchema))   


BOOKING_SCHEMA = BookingSchema()
PASSENGER_SCHEMA = PassengerSchema()
FLIGHT_BOOKINGS_SCHEMA = FlightBookingsSchema()
BOOKING_PAYMENT_SCHEMA = BookingPaymentSchema()
BOOKING_SCHEMA_FULL = BookingSchemaFull()

BOOKING_SCHEMA_MANY = BookingSchema(many=True)
PASSENGER_SCHEMA_MANY = PassengerSchema(many=True)
FLIGHT_BOOKINGS_SCHEMA_MANY = FlightBookingsSchema(many=True)
BOOKING_PAYMENT_SCHEMA_MANY = BookingPaymentSchema(many=True)
BOOKING_SCHEMA_FULL_MANY = BookingSchemaFull(many=True)
