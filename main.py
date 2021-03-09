import RPi.GPIO as GPIO
from flask import Flask, render_template,redirect, url_for, request, redirect
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:

room1 = {
   26 : {'name' : 'LED Bulb1', 'state' : GPIO.LOW},
   19 : {'name' : 'LED Bulb2', 'state' : GPIO.LOW},
   }
room2 = {
   13 : {'name' : 'LED Bulb3', 'state' : GPIO.LOW},
   6 : {'name' : 'LED Bulb4', 'state' : GPIO.LOW}
   }

# Set each pin as an output and make it low:
for n in room1:
   GPIO.setup(n, GPIO.OUT)
   GPIO.output(n, GPIO.LOW)
for n in room2:
   GPIO.setup(n, GPIO.OUT)
   GPIO.output(n, GPIO.LOW)

@app.route("/")
def main():

   return render_template('index.html')

@app.route("/room1")
def rooom1():
   # For each pin, read the pin state and store it in the pins dictionary:
   for n in room1:
     room1[n]['state'] = GPIO.input(n)
   # Put the pin dictionary into the template data dictionary:
     templateData = {
      	'room1' : room1
     	 }
   # Pass the template data into the template main.html and return it to the user
   return render_template('room1.html', **templateData)

@app.route("/room2")
def rooom2():
   # For each pin, read the pin state and store it in the pins dictionary:
   for n in room2:
      room2[n]['state'] = GPIO.input(n)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'room2' : room2
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('room2.html', **templateData)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   if changePin==26 or changePin==19:
       deviceName = room1[changePin]['name']
   else:
       deviceName = room2[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " OFF."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " ON."
   if action == "toggle":
      # Read the pin and set it to whatever it isn't (that is, toggle it):
      GPIO.output(changePin, not GPIO.input(changePin))
      message = "Toggled " + deviceName + "."

   # For each pin, read the pin state and store it in the pins dictionary:
   for n in room1:
      room1[n]['state'] = GPIO.input(n)
   for n in room2:
      room2[n]['state'] = GPIO.input(n)


   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData={
      'message' : message,
      'room1' : room1,
      'room2' : room2
 }
   if changePin==26 or changePin==19:
      return redirect("/room1")
   else:
      return redirect("/room2")
   #return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='192.168.1.171', port=8082, debug=True)

