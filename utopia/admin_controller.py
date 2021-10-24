from flask import Flask, json, request
from utopia import app
from utopia.service.booking_service import BookingService
import logging

BOOKING_SERVICE = BookingService()


##################### GET #####################



@app.route('/booking/admin/read/bookings', methods=['GET'])
def readBookings():

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



@app.route('/booking/public/add/booking', methods=['GET'])
def addBookingEmpty():

    return BOOKING_SERVICE.add_booking_empty()   

@app.route('/booking/public/add/passenger', methods=['POST'])
def addPassenger():

    return BOOKING_SERVICE.add_passenger(request.json)  


@app.route('/booking/public/add/passengers', methods=['POST'])
def addPassengers():

    return BOOKING_SERVICE.add_passengers(request.json)   



##################### DELETE #####################

@app.route('/booking/public/delete/booking/id=<id>', methods=['DELETE'])
def deleteBooking(id):

    return BOOKING_SERVICE.delete_booking(id)   

@app.route('/booking/public/delete/passenger/id=<id>', methods=['DELETE'])
def deletePassenger(id):

    return BOOKING_SERVICE.delete_passenger(id)  