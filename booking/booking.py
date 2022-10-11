from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
import grpc
import showtime_pb2
import showtime_pb2_grpc
from werkzeug.exceptions import NotFound
from operator import itemgetter

app = Flask(__name__)

#Init Config
PORT = 3003
HOST = '0.0.0.0'

#Load database
with open('{}/data/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

#Index route
@app.route("/", methods=['GET'])
def home():
   print("coucou" + request.host)
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

#Get all bookings
@app.route("/booking", methods=['GET'])
def get_json():
   res = make_response(jsonify(bookings), 200)
   return res

#Get bookings of a user specifying an id in the  path
@app.route("/booking/<userid>", methods=['GET'])
def get_booking_for_user(userid):
   for b in bookings:
      if b["userid"] == userid:
          return make_response(jsonify(b), 200)
   return make_response(jsonify({"error":"bad input parameter"}), 400)

#Add a booking for a user specifying its id in the path
@app.route("/booking/<userid>", methods=['POST'])
def add_booking_by_user(userid):
   #Get movie to be added
   req = request.get_json()
   #### Verify that the movie is scheduled
   # GRPC Request to the showtime API 
   schedules = []
   with grpc.insecure_channel('dns:///showtime:3002') as channel:
      stub = showtime_pb2_grpc.ShowtimeStub(channel)
      allSchedule = stub.GetSchedule(showtime_pb2.Empty())
      for schedule in allSchedule:
         schedules.append({"date": schedule.date, "movies":schedule.movies})
      channel.close()
   
   sch_dates = [sch["date"] for sch in schedules]
   if req["date"] not in sch_dates:
      return make_response(jsonify({"error":"wrong date"}))
   sch_idx = sch_dates.index(req["date"])
   if req["movieid"] not in schedules[sch_idx]["movies"]:
      return make_response(jsonify({"error": "movie not scheduled at this date"}))
   
   ### Verify that the booking doesn't exist and create it if so
   for b in bookings:
      if b["userid"] == userid:
         dates = [b_["date"] for b_ in b["dates"]]
         if req["date"] in dates:
            idx = dates.index(req["date"])
            if req["movieid"] in b["dates"][idx]["movies"]:
               return make_response(jsonify({"error":"an existing item already exists"}), 409)
            b["dates"][idx]["movies"].append(req["movieid"])
            return make_response(jsonify(b), 200)
         to_push = {"date" : req["date"], "movies" : [req["movieid"]]}
         b["dates"].append(to_push)
         return make_response(jsonify(b),200)
            
 
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
