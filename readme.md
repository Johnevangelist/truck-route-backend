## About

This is a Danjo backend project basically build to demonstrate a map of the route along with optimal location to fuel up along the route
Assuming the vehicle has a maximum range of 500 miles and achieves 10 miles per gallon
the response contains the input locations, distance between the two locations, nearest affordable fuel-station along the route 

## setup 

you need to insert the csv file of fuel stations with in your region 
get an api from 'open route source (free)' or you can use any desired api 
create a .env file and insert the api key into 'ORS_API_KEY='
after inserting the key install all the required dependecies 
run `python manage.py runserver` on the terminal the django server starts up 
you need to go to postman or any other desired api calling tool then you need to post 'http://127.0.0.1:8000/api/fuel-plan/'
before post insert the start and end in the body 
example : {
  "start": "Los Angeles, CA",
  "end": "New York, NY"
}
then send it you will get the response in json 

## production 

if you are willing to use it for production then go to the backend/settings.py change the django secret key currently it has been set to use the local environment 
if you want to generate the django keys then use this cmd in the terminal `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
before using this cmd make sure you change 'SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")' in the backend/settings.py
make sure you install `pip install python-dotenv`
then insert the django generated key in the .env file 

## credits 

This project is made by @JohnEvangelist
