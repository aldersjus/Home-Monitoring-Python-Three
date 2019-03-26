#Created by Justin Alderson
#Connects to Firebase and diplays relevant data that was previously uploaded from Raspberry Pi

from flask import *
import datetime
from motion import Movement
from firebase import firebase
import json
from datetime import datetime

app = Flask(__name__)

#firebase connect to real time database
firebase = firebase.FirebaseApplication('https://your_database_name.firebaseio.com', None)

@app.route("/")
def index():
    #get time
    oclock = datetime.now()
    #get previous hour
    motion = 'Motion Hour: %d' % (oclock.hour - 1)
    print(motion)
    #get movements from firebase
    movements = []
    result = firebase.get('Motion',motion)
    #turn the data into objects
    for r in result:
        j = json.loads(r)
        print(j)
        #pass in as a map, recreated objects
        objectA = Movement(**j)
        print(objectA.getCount())
        print(objectA.getDateTime())
        movements.append(objectA)

    #find the latest movement in the previous hour, turn into json to be passed in
    object = movements[-1]
    templateData = {
      'last' : object.getDateTime(),
      'total': len(movements)
    }

    #create a list of strings from movements to be passed in later
    displayAll = []
    for o in movements:
        s = 'Count: %s Date: %s'%(o.getCount(),o.getDateTime())
        displayAll.append(s)

    #render and pass in the data
    return render_template('index.html', **templateData, movements=displayAll)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
