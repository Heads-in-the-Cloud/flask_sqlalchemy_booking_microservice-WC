from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from sqlalchemy.sql.sqltypes import Boolean, Date
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import backref, relation, relationship
from utopia import app
from utopia.models.base import Base, db_session
from flask_jwt_extended import get_jwt, create_access_token, set_access_cookies, get_jwt_identity
from datetime import datetime, timedelta, timezone


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


def find_user(username):
    user = db_session.query(User).filter_by(username=username).first()

    user = UserSchema().dump(user)
    return user

def refresh_token(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):

        # Case where there is not a valid JWT. Just return the original respone
        return response

############################# SCHEMAS #############################


class UserRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserRole
        ordered = True
        fields = ('id', 'name')



class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        ordered = True
        fields = ('id', 'username', 'role_id', 'user_role', 'given_name', 'family_name',  'email', 'password', 'phone')
    user_role = fields.Nested(UserRoleSchema, only=['name'])


class BookingAgentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookingAgent
        fields = ('booking_id', 'agent_id', 'user')
    user = fields.Nested(UserSchema, only = ['username'])

class BookingGuestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookingGuest
        fields = ('booking_id', 'contact_email', 'contact_phone')



class BookingUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookingUser
        fields = ('booking_id', 'user_id', 'user')
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
