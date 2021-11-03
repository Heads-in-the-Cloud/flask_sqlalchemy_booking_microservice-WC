from flask import Flask, json, request, make_response
from utopia import app
from utopia.booking_service import BookingService
import logging
from utopia.models.users import find_user, refresh_token
from flask_jwt_extended import get_current_user, JWTManager, jwt_required

BOOKING_SERVICE = BookingService()
jwt = JWTManager(app)
TRAVELER = 3

##################### GET #####################



@app.route('/booking/admin/read/bookings', methods=['GET'])
@jwt_required()
def readBookings():
    current_user = get_current_user()
    if current_user['role_id'] == TRAVELER:
        return make_response('need at least agent privileges to access this resource', 403)

    return BOOKING_SERVICE.read_bookings()


@app.route('/booking/public/find/booking/id=<id>', methods=['GET'])
def findBooking(id):

    return BOOKING_SERVICE.find_booking(id)


@app.route('/booking/admin/read/passengers', methods=['GET'])
def readPassengers():

    return BOOKING_SERVICE.read_passengers()

@app.route('/booking/public/find/passenger/id=<id>', methods=['GET'])
def findPassenger(id):

    return BOOKING_SERVICE.find_passenger(id)



##################### POST #####################



@app.route('/booking/public/add/booking', methods=['POST'])
def addBookingEmpty():

    return BOOKING_SERVICE.add_booking_empty()   

@app.route('/booking/public/add/booking/flight=<flight_id>/user=<user_id>', methods=['POST'])
def addBooking(flight_id, user_id):

    return BOOKING_SERVICE.add_booking(request.json, flight_id, user_id)

@app.route('/booking/public/add/passenger', methods=['POST'])
def addPassenger():

    return BOOKING_SERVICE.add_passenger(request.json)  


@app.route('/booking/public/add/passengers', methods=['POST'])
def addPassengers():

    return BOOKING_SERVICE.add_passengers(request.json)   



##################### PUT #####################

@app.route('/booking/public/update/passenger', methods=['PUT'])
def updatePassenger():

    return BOOKING_SERVICE.update_passenger(request.json)  


@app.route('/booking/public/update/passengers', methods=['PUT'])
def updateBookingPassengers():

    return BOOKING_SERVICE.update_booking_passengers(request.json)  

@app.route('/booking/public/update/booking', methods=['PUT'])
@jwt_required()
def updateBookingMethod():

    return BOOKING_SERVICE.update_booking_method(request.json)  


@app.route('/booking/public/update/is_active', methods=['PUT'])
def updateIsActive():

    return BOOKING_SERVICE.set_is_active(request.json)


@app.route('/booking/public/update/booking_payment', methods=['PUT'])
def updateBookingPayment():

    return BOOKING_SERVICE.update_booking_payment(request.json)

@app.route('/booking/public/update/flight_bookings', methods=['PUT'])
def updateFlightBookings():

    return BOOKING_SERVICE.update_flight_bookings(request.json)
  


##################### DELETE #####################

@app.route('/booking/public/delete/booking/id=<id>', methods=['DELETE'])
def deleteBooking(id):

    return BOOKING_SERVICE.delete_booking(id)   

@app.route('/booking/public/delete/passenger/id=<id>', methods=['DELETE'])
def deletePassenger(id):

    return BOOKING_SERVICE.delete_passenger(id)  

@app.route('/booking/public/delete/booking_agent/id=<id>', methods=['DELETE'])
def deleteBookingAgent(id):

    return BOOKING_SERVICE.delete_booking_agent(id)  

@app.route('/booking/public/delete/booking_user/id=<id>', methods=['DELETE'])
def deleteBookingUser(id):

    return BOOKING_SERVICE.delete_booking_user(id)  

@app.route('/booking/public/delete/booking_guest/id=<id>', methods=['DELETE'])
def deleteBookingGuest(id):

    return BOOKING_SERVICE.delete_booking_guest(id) 


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return find_user(identity)

@app.after_request
def refresh_expiring_jwts(response):
    return refresh_token(response)