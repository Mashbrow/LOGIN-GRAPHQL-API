from flask import Flask, render_template, request, jsonify, make_response
from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from ariadne.constants import PLAYGROUND_HTML
import requests
import json
from werkzeug.exceptions import NotFound


app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

#type_defs = load_schema_from_path('..\movie\movie.graphql')
#query = QueryType()

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/user", methods=['GET'])
def get_json():
   return make_response(jsonify(users), 200)

@app.route("/user/<userid>", methods=['GET'])
def get_average_user_rating(userid):
   r_sum = 0
   cond = False
   for element in users:
      if userid == element["id"]:
         cond = True
   if not cond:
      return make_response(jsonify({"error":"no user found"}), 400)
      
   host_ = 'http://' + request.host.split(':')[0]
   request_booking = requests.get(host_ + ':' + '3201'+'/booking/'+str(userid))
   if request_booking.ok : 
      bookings = request_booking.json()
   else:
      return make_response({"error":"no movies booked for that user"}, 409)
      
   movies_list = []
   #with grpc.insecure_channel('localhost:3001') as channel:
      #stub = movie_pb2_grpc.MovieStub(channel)
      #allMovies = stub.GetListMovies(movie_pb2.Empty())
      #for movie in allMovies:
         #movies_list.append({"id": movie.id, "rating":movie.rating})
      #channel.close()
   query = """query{
  movies {
    id
    rating
  }
}"""
   request_movie = requests.post('http://localhost:3001/graphql', json ={"query": query})
   if request_movie.ok:
      movies_list = request_movie.json()['data']['movies']
   
   booked_movies = []
   for date in bookings["dates"]:
      booked_movies += date["movies"]

   for b_movie in booked_movies:
      for m in movies_list:
         if b_movie == m["id"]:
            r_sum += m["rating"]

   average = r_sum/len(booked_movies)      
   return make_response(jsonify({"average_rating":average}), 200)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
