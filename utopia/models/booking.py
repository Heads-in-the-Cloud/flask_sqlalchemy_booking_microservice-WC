from enum import auto
from flask import Flask
from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import backref, relation, relationship
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields
# from utopia.models.flight_models import Flight
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

# class BookingAgent(Base):
#     __tablename__ = 'booking_agent'

#     booking_id = Column(Integer, ForeignKey('booking.id'), primary_key=True)
#     agent_id = Column(Integer, ForeignKey('user.id'))

# class BookingUser(Base):
#     __tablename__ = 'booking_user'

#     booking_id = Column(Integer, ForeignKey('booking.id'), primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.id'))

# class BookingGuest(Base):
#     __tablename__ = 'booking_guest'

#     booking_id = Column(Integer, ForeignKey('booking.id'), primary_key=True)
#     contact_email = Column(String(255))
#     contact_phone = Column(String(45))

# class User(Base):
#     __tablename__ = 'user'

#     id = Column(Integer, primary_key=True)
#     role_id = Column(Integer, ForeignKey('user_role.id'))
#     given_name = Column(String(255))
#     family_name = Column(String(255))
#     username = Column(String(45))
#     email = Column(String(255))
#     password = Column(String(255))
#     phone = Column(String(45))
#     booking_agent = relationship('BookingAgent', backref='user', lazy='subquery', cascade='all, delete', uselist=False)
#     booking_user = relationship('BookingUser', backref='user', lazy='subquery', cascade='all, delete', uselist=False)

# class UserRole(Base):
#     __tablename__ = 'user_role'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(45))
#     users = relationship('User', backref='user_role', lazy='subquery', cascade='all, delete')

class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    is_active =  Column(Boolean, default=True)
    confirmation_code = Column(String(255))
    passengers = relationship('Passenger', backref='booking', lazy='subquery', cascade='all, delete')
    flight_bookings = relationship('FlightBookings', backref='booking', lazy='subquery', cascade='all, delete', uselist=False)
    booking_payment = relationship('BookingPayment', backref='booking', lazy='subquery', cascade='all, delete', uselist=False)
    booking_agent = relationship('BookingAgent', backref='booking', lazy='subquery', cascade='all, delete', uselist=False)
    booking_user = relationship('BookingUser', backref='booking', lazy='subquery', cascade='all, delete', uselist=False)
    booking_guest = relationship('BookingGuest', backref='booking', lazy='subquery', cascade='all, delete', uselist=False)




class Passenger(Base):
    __tablename__= 'passenger'

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('booking.id'))
    given_name = Column(String(255))
    family_name = Column(String(255))
    dob = Column(String(10))
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


# class UserRoleSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = UserRole
#         ordered = True
#     id = auto_field()
#     name = auto_field()


# class UserSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = User
#         ordered = True
#         fields = ('id', 'given_name', 'family_name', 'username', 'email', 'password', 'phone', 'user_role')
#     user_role = fields.Nested(UserRoleSchema)




class BookingPaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookingPayment
    booking_id = auto_field()
    stripe_id = auto_field()
    refunded = auto_field()

# class BookingAgentSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = BookingAgent
#     booking_id = auto_field()
#     agent_id = auto_field()
#     user = fields.Nested(UserSchema, only = ['username'])

# class BookingGuestSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = BookingGuest
#     booking_id = auto_field()
#     contact_email = auto_field()
#     contact_phone = auto_field()


# class BookingUserSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = BookingUser
#     booking_id = auto_field()
#     user_id = auto_field()
#     user = fields.Nested(UserSchema, only = ['username'])



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
# BOOKING_AGENT_SCHEMA = BookingAgentSchema()
# BOOKING_USER_SCHEMA = BookingUserSchema()
# BOOKING_GUEST_SCHEMA = BookingGuestSchema()
# USER_SCHEMA = UserSchema()
# USER_ROLE_SCHEMA = UserRoleSchema()
BOOKING_SCHEMA_FULL = BookingSchemaFull()

BOOKING_SCHEMA_MANY = BookingSchema(many=True)
PASSENGER_SCHEMA_MANY = PassengerSchema(many=True)
FLIGHT_BOOKINGS_SCHEMA_MANY = FlightBookingsSchema(many=True)
BOOKING_PAYMENT_SCHEMA_MANY = BookingPaymentSchema(many=True)
# BOOKING_AGENT_SCHEMA_MANY = BookingAgentSchema(many=True)
# BOOKING_USER_SCHEMA_MANY = BookingUserSchema(many=True)
# USER_SCHEMA_MANY = UserSchema(many=True)
# USER_ROLE_SCHEMA_MANY = UserRoleSchema(many=True)
BOOKING_SCHEMA_FULL_MANY = BookingSchemaFull(many=True)

