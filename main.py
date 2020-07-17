from flask import Flask, request,  render_template, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import requests
import datetime
import json
import os



app = Flask(__name__)

load_dotenv('twilio.env')
app.config.from_pyfile('settings.py')

apiKey = os.getenv('NASA_API_KEY')


#will be the homepage of our website
@app.route("/")
def home():
    return render_template("template.html")


@app.route("/date",methods = ['GET', 'POST'])
def incoming():
    #following tutorial from twilio website
    body = request.values.get('Body', None)
    #body will store the user's response to our phone number
    
    resp = MessagingResponse()
    
    #call the api request, using the date provided in the url
    if body == 'today' or body == 'Today':
        #api defaults to 'today's so will just return this
        r = requests.get('https://api.nasa.gov/planetary/apod?hd=true&api_key=' + apiKey )
        data = r.json()
        photo = data.get('url')
        Message = 'Hey there! The NASA APOD can be accessed at: ' + str(photo)
    
        #respond with the message
        resp.message(Message)
        
       #check to see if the date is in the proper format
    else:
        try:
            #split the input based on the format, then check using the datetime library if its valid
            temp = body
            #this temp variable gets rid of any confusion
            datetime.datetime.strptime(temp, '%Y-%m-%d')
            #modified API call to fill in the blanks
            r = requests.get('https://api.nasa.gov/planetary/apod?hd=true&date=' + body + '&api_key='+ apiKey )
            data = r.json()
            photo = data.get('url')
            Message = 'Hey there! The NASA APOD can be accessed at: ' + str(photo)
            resp.message(Message)
        except ValueError: #this runs when the input is random
            isValidDate= False
            Message= "Hey there! It looks like your input was incorrect or not recognized! Please try again!"
            resp.message(Message) 
    
    
            
    return str(resp)
 


#this will run in debug mode, aka when the name of the file switches to __main__
if __name__ == "__main__":
    #enforced debugging thing for ngrok
    #app.run(host="localhost", port= 80)
    app.run(debug=True)