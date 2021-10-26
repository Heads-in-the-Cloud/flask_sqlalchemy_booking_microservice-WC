from enum import auto
from flask import Flask
from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import backref, relation, relationship
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields
from utopia import app
from utopia.models.base import Base



ma = Marshmallow(app)



class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('user_role.id'))
    given_name = Column(String(255))
    family_name = Column(String(255))
    username = Column(String(45))
    email = Column(String(255))
    password = Column(String(255))
    phone = Column(String(45))
    booking_agent = relationship('BookingAgent', backref='user', lazy='subquery', cascade='all, delete', uselist=False)
    booking_user = relationship('BookingUser', backref='user', lazy='subquery', cascade='all, delete', uselist=False)

class UserRole(Base):
    __tablename__ = 'user_role'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    users = relationship('User', backref='user_role', lazy='subquery', cascade='all, delete')


class BookingAgent(Base):
    __tablename__ = 'booking_agent'

    booking_id = Column(Integer, ForeignKey('booking.id'), primary_key=True)
    agent_id = Column(Integer, ForeignKey('user.id'))

class BookingUser(Base):
    __tablename__ = 'booking_user'

    booking_id = Column(Integer, ForeignKey('booking.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))

class BookingGuest(Base):
    __tablename__ = 'booking_guest'

    booking_id = Column(Integer, ForeignKey('booking.id'), primary_key=True)
    contact_email = Column(String(255))
    contact_phone = Column(String(45))




class UserRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserRole
        ordered = True
    id = auto_field()
    name = auto_field()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        ordered = True
        fields = ('id', 'given_name', 'family_name', 'username', 'email', 'password', 'phone', 'user_role')
    user_role = fields.Nested(UserRoleSchema)

class BookingAgentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookingAgent
    booking_id = auto_field()
    agent_id = auto_field()
    user = fields.Nested(UserSchema, only = ['username'])

class BookingGuestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookingGuest
    booking_id = auto_field()
    contact_email = auto_field()
    contact_phone = auto_field()


class BookingUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookingUser
    booking_id = auto_field()
    user_id = auto_field()
    user = fields.Nested(UserSchema, only = ['username'])


USER_SCHEMA = UserSchema()
USER_ROLE_SCHEMA = UserRoleSchema()

BOOKING_AGENT_SCHEMA = BookingAgentSchema()
BOOKING_USER_SCHEMA = BookingUserSchema()
BOOKING_GUEST_SCHEMA = BookingGuestSchema()

USER_SCHEMA_MANY = UserSchema(many=True)
USER_ROLE_SCHEMA_MANY = UserRoleSchema(many=True)

BOOKING_AGENT_SCHEMA_MANY = BookingAgentSchema(many=True)
BOOKING_USER_SCHEMA_MANY = BookingUserSchema(many=True)
BOOKING_GUEST_SCHEMA = BookingGuestSchema(many=True)
