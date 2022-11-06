# API_with_DRF
## How to run this project locally
### 1. Clone the project
 ```
 git clone https://github.com/salamkayodeji/API_with_DRF
 
 cd API_with_DRF
 ```
### 2. To build project
#The docker install all files in requirements.txt and run all the test also.
```
docker build -t web:latest .

```
### 3. Running the project
```
docker run -d --name API_with_DRF -e "PORT=8765" -e "DEBUG=1" -p 8007:8765 web:latest
```
### 4. Open the project

http://127.0.0.1:8007/

username = admin
password = rootaccess1234

## How to access this project online

### 1. Visit https://pacific-stream-12949.herokuapp.com/

### The project has two seperate API documentation visit anyone:

    ## Option 1: https://pacific-stream-12949.herokuapp.com/docs/  

    ## Option 2: https://pacific-stream-12949.herokuapp.com/api/docs/

## Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE. Endpoints should be logically organized around _collections_ and _elements_, both of which are resources.

ENDPOINT 1:, `todo`, so we will use the following URLS - `/todo/` and `/todo/<id>` for collections and elements, respectively:

## Use
We can test the API by visiting the api documentation :
[API_DOCUMENTATION]{https://pacific-stream-12949.herokuapp.com/docs/}, 
[API_DOCUMENTATION]{https://pacific-stream-12949.herokuapp.com/api/docs/}, 


or we can use [Postman](https://www.postman.com/)

Postman is an API platform for building and using APIs. Postman simplifies each step of the API lifecycle and streamlines collaboration so you can create better APIs—faster.

First, we make run our docker is running or we https://pacific-stream-12949.herokuapp.com.

Then we paste the any of the links in our postman app

http://127.0.0.1:8007/todo/ or https://pacific-stream-12949.herokuapp.com/todo/

we get:
```
{
    "detail": "Authentication credentials were not provided."
}
```

To get a token you need to paste the link

```
http://127.0.0.1:8007/token/ username="admin" password="rootaccess1234"

```
after that, we get the token
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNjI5MjMyMSwianRpIjoiNGNkODA3YTlkMmMxNDA2NWFhMzNhYzMxOTgyMzhkZTgiLCJ1c2VyX2lkIjozfQ.hP1wPOPvaPo2DYTC9M1AuOSogdRL_mGP30CHsbpf4zA",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA2MjIxLCJqdGkiOiJjNTNlNThmYjE4N2Q0YWY2YTE5MGNiMzhlNjU5ZmI0NSIsInVzZXJfaWQiOjN9.Csz-SgXoItUbT3RgB3zXhjA2DAv77hpYjqlgEMNAHps"
}
```
We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token will expire after a hour.
We can use the refresh token to request a need access token.

so you can run 
### TODO

http://127.0.0.1:8000/todo/ or https://pacific-stream-12949.herokuapp.com/todo/

with the following endpoints

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`todo` | GET | READ | Get all movies
`todo/:id` | GET | READ | Get a single movie
`todo`| POST | CREATE | Create a new movie
`todo/:id` | PUT | UPDATE | Update a movie
`todo/:id` | DELETE | DELETE | Delete a movie

### EVENTS

http://127.0.0.1:8000/event/ or https://pacific-stream-12949.herokuapp.com/event/

with the following endpoints

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`event` | GET | READ | Get all Events
`event/:id` | GET | READ | Edit a Events
`event`| POST | CREATE | Create a new Events
`event/:id` | PUT | UPDATE | Update a Events
`event/:id` | DELETE | DELETE | Delete a Events

### DUPLICATE TODO AND ALL EVENTS RELATED TO IT

http://127.0.0.1:8000/duplicate_todo/<int:pk> or https://pacific-stream-12949.herokuapp.com/duplicate_todo/<int:pk>

with the following endpoints

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`duplicate_todo/:id` | GET | READ | Get a list of all Todo and Items related to it


### DUPLICATE AN EVENTS

http://127.0.0.1:8000/duplicate_event/<int:pk> or https://pacific-stream-12949.herokuapp.com/duplicate_event/<int:pk>

with the following endpoints

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`duplicate_event/:id` | GET | READ | Get a list of EVENTS

### GET ALL EVENTS AND TODOS

http://127.0.0.1:8000/get_all or https://pacific-stream-12949.herokuapp.com/get_all

with the following endpoints

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`get_all/` | GET | READ | Get a dictionary with all TODOS and EVENTS

### GET A TODO AND ALL EVENTS RELATED TO IT

http://127.0.0.1:8000/get_event_todo/<int:pk> or https://pacific-stream-12949.herokuapp.com/get_event_todo/<int:pk>

with the following endpoints

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`get_event_todo/:id` | GET | READ | Returns a list of Todo and Events related to it

### GET A TODO AND ALL EVENTS RELATED TO IT

http://127.0.0.1:8000/get_event/<int:pk> or https://pacific-stream-12949.herokuapp.com/get_event/<int:pk>

with the following endpoints

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`get_event/:id` | GET | READ | Returns a list of all events with the same id
