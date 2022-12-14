# LOGIN-GRAPHQL-API
Repository for practical work on GRAPHQL

### Installation

First clone the repo: `git clone https://github.com/Mashbrow/LOGIN-GRAPHQL-API` 
To launch with docker-compose, get to the LOGIN-GRAPHQL-API folder and type `docker-compose up` in your terminal.

### What was done so far

 - Green Practical Work completely done
   - File `movie` contains the green version for the GRAPHQL API. The other folders contains services based on GRPC and REST.


In this project, only movie is using graphql, so type 'localhost:3001/graphql' in your terminal to start using the graphql requests.  

Here are the queries, mutations and types you can use with the movie service:  

```
type Query {  
    movie_with_id(_id: String!): Movie  
    movies: [Movie]  
}  

type Mutation {  
    update_movie_rate(_id: String!, _rate: Float!): Movie  
}  

type Movie {  
    id: String!  
    title: String!  
    director: String!  
    rating: Float!  
    actors: [Actor]  
}  
type Actor {  
    id: String!  
    firstname: String!  
    lastname: String!  
    birthyear: Int!  
    films: [String!]  
}
```
