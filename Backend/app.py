import time
from RPi import GPIO
from helpers.klasseknop import Button
from helpers.DHT11 import sensor_dht11
from helpers.ldr import ldr
from helpers.motor2 import motor
from helpers.lcd import LCD
import threading
import datetime
import serial
from subprocess import check_output

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from repositories.DataRepository import DataRepository


# Code voor Hardware
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dht11 = sensor_dht11(5)
ldr = ldr()
motor = motor()
status = 0;
rs = 21
e = 20
lcd = LCD(rs, e, [13, 19, 26, 23, 24, 25, 12, 16])

#led3 = 21
#knop1 = Button(20)

#GPIO.setup(led3, GPIO.OUT)
#GPIO.output(led3, GPIO.LOW)


def change_toestand_luik(vorige_toestand,nieuwe_toestand):
    print("luik toestand veranderd")
    stappen = vorige_toestand - nieuwe_toestand
    if(stappen>0):
        direction = True
        cycles = abs(stappen)
        motor.turn_motor(direction,cycles)
        motor.end()
    elif(stappen<0):
        direction = False
        cycles = abs(stappen)
        motor.turn_motor(direction,cycles)
        motor.end()
    elif(stappen == 0):
        direction = False
        cycles = 0
        motor.turn_motor(direction,cycles)
        motor.end()
    else:
        print("De opgegeven stappen zijn niet geldig")




def show_data():
      result = dht11.read_data()
      print("Dht11 sensor data succesvol ingelezen")
      if result.is_valid():
          DataRepository.insert_sensorData("C",result.temperature)
          print("Temperatuur inserted")

          DataRepository.insert_sensorData("% luchtvochtig",result.humidity)
          print("Luchtvochtigheid inserted")

          print("Temperature: %-3.1f C" % result.temperature)
          print("Humidity: %-3.1f %%" % result.humidity)
      else:
          print("Error: %d" % result.error_code)
        
def insert_ldr(Meting):
   
    DataRepository.insert_sensorData("% licht",Meting)
    print("LDR inserted")

def insert_serial(Message):

    Message = Message.replace("\r\n", "")
    if(Message == "UID tag : 7A 6D 06 70"):
        TagUID = "7A 6D 06 70"
        PoesNaam = "Luna"
        DataRepository.insert_rfid(TagUID,PoesNaam)
        print("Luna inserted")
    elif(Message == "UID tag : 17 7F 18 AF"):
        TagUID = "17 7F 18 AF"
        PoesNaam = "Mona"
        DataRepository.insert_rfid(TagUID,PoesNaam)
        print("Mona inserted")
    elif(Message == "knop1 is ingedrukt"):
        knop = "Binnen"
        DataRepository.update_rfid(knop)
        print("Knop binnen inserted")
    elif(Message == "knop2 is ingedrukt"):
        knop = "Buiten"
        DataRepository.update_rfid(knop)
        print("Knop buiten inserted")
    else:
        print("No data to insert")



def read_serialport():
    ser = serial.Serial('/dev/serial0')
    string_ascii = ser.readline()
    print(f"received: {string_ascii}")
    string_utf = string_ascii.decode(encoding='utf-8')
    print(f"decoded: {string_utf}")
    insert_serial(string_utf)
    ser.close()
    


#def lees_knop(pin):
#    if knop1.pressed:
#        print("**** button pressed ****")
#        if GPIO.input(led3) == 1:
#            switch_light({'lamp_id': '3', 'new_status': 0})
#        else:
#            switch_light({'lamp_id': '3', 'new_status': 1})


#knop1.on_press(lees_knop)


# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)


# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.

def data_input():
    while True:
        #print('*** We zetten alles uit **')
        #DataRepository.update_status_alle_lampen(0)
        #GPIO.output(led3, 0)
        #status = DataRepository.read_status_lampen()
        #socketio.emit('B2F_status_lampen', {'lampen': status})
        
        show_data()
        time.sleep(60)


thread1 = threading.Timer(1, data_input)
thread1.start()

def serial_communication():
    while True:
        read_serialport()
        time.sleep(0.1)


thread2 = threading.Timer(0.1, serial_communication)
thread2.start()

def loopLDR():
    print("ldr functie geopend")
    while True:
        ldr_value = ldr.readldr(0)
        print("LDR Value: = {} %".format((ldr_value/1023)*100))
        insert_ldr(((ldr_value/1023)*100))
        time.sleep(60)
        #ldr.spi.close()

thread3 = threading.Timer(1, loopLDR)
thread3.start()

def show_status():
        
        lcd.clear_display()
        if status == 0:  
            print("IP weergeven op lcd")
            ips = check_output(['hostname', '--all-ip-addresses']).split()
            print(ips)
            lcd.write_message(ips[0].decode())
            if len(ips) > 1:
                lcd.set_cursor(1, 0)
                lcd.write_message(ips[1].decode())
        else:
            if status == 1:  
                message = ""
            else:  
                message = ""
            
            print("message sent")
            lcd.set_cursor(1, 0)
            lcd.write_message(message)

#thread4 = threading.Timer(1,show_status)
#thread4.start()


print("**** Program started ****")
show_status()

# API ENDPOINTS
endpoint = '/api/v1'


@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route(endpoint + '/dht11', methods=['GET'])
def get_dht11():
    if request.method == 'GET':
        return jsonify(types=DataRepository.read_dht11()), 200

@app.route(endpoint + '/temperatuur', methods=['GET'])
def get_temperatuur():
    if request.method == 'GET':
        return jsonify(types=DataRepository.read_SensorData("C")), 200

@app.route(endpoint + '/licht', methods=['GET'])
def get_licht():
    if request.method == 'GET':
        return jsonify(types=DataRepository.read_SensorData("% licht")), 200

@app.route(endpoint + '/luchtvochtigheid', methods=['GET'])
def get_luchtvochtigheid():
    if request.method == 'GET':
        return jsonify(types=DataRepository.read_SensorData("% luchtvochtig")), 200

@app.route(endpoint + '/toestand', methods=['GET'])
def get_toestand():
    if request.method == 'GET':
        return jsonify(types=DataRepository.read_toestand_motor("motor")), 200

@app.route(endpoint + '/recent/temperatuur', methods=['GET'])
def get_latest_temperatuur():
    if request.method == 'GET':
        return jsonify(types=DataRepository.get_latest_SensorData("C")), 200

@app.route(endpoint + '/recent/licht', methods=['GET'])
def get_latest_licht():
    if request.method == 'GET':
        return jsonify(types=DataRepository.get_latest_SensorData("% licht")), 200

@app.route(endpoint + '/recent/luchtvochtigheid', methods=['GET'])
def get_latest_luchtvochtigheid():
    if request.method == 'GET':
        return jsonify(types=DataRepository.get_latest_SensorData("% luchtvochtig")), 200

@app.route(endpoint + '/luna', methods=['GET'])
def get_luna():
    if request.method == 'GET':
        return jsonify(types=DataRepository.read_luna()), 200

@app.route(endpoint + '/mona', methods=['GET'])
def get_mona():
    if request.method == 'GET':
        return jsonify(types=DataRepository.read_mona()), 200  

@app.route(endpoint + '/luna/toestand', methods=['GET'])
def get_recent_luna():
    if request.method == 'GET':
        return jsonify(types=DataRepository.read_recent_luna()), 200

@app.route(endpoint + '/mona/toestand', methods=['GET'])
def get_recent_mona():
    if request.method == 'GET':
        return jsonify(types=DataRepository.read_recent_mona()), 200

@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # Send to the client!
    # vraag de status op van de motor uit de DB
    status_motor = DataRepository.read_toestand_motor("motor")
    emit('B2F_toestand_motor', {'motor': status_motor}, broadcast=True)

@socketio.on('F2B_switch_motor')
def switch_Motor(data):
    print('F2B_switch_motor opgeroepen')
    # Ophalen van de data
    Naam = data['Naam']
    nieuwe_toestand = int(data['nieuwe_toestand'])
    jsonObject = DataRepository.read_toestand_motor("motor")
    oude_toestand = int(jsonObject['Toestand'])

    print(f"{Naam} wordt geswitcht van {oude_toestand} naar {nieuwe_toestand}")
    
    # Stel de status in op de DB
    nieuwe_toestand_string = data['nieuwe_toestand']
    res = isinstance(nieuwe_toestand_string, str)
    print(res)
    DataRepository.update_toestand_motor(nieuwe_toestand_string,Naam)
    socketio.emit('B2F_updated_motor', broadcast=True)
    print("updated motor")

    

    if(nieuwe_toestand != oude_toestand):
        change_toestand_luik(oude_toestand,nieuwe_toestand)
    




#@socketio.on('F2B_switch_light')
#def switch_light(data):
#    # Ophalen van de data
#    lamp_id = data['lamp_id']
#    new_status = data['new_status']
#    print(f"Lamp {lamp_id} wordt geswitcht naar {new_status}")
#
#    # Stel de status in op de DB
#    res = DataRepository.update_status_lamp(lamp_id, new_status)
#
#    # Vraag de (nieuwe) status op van de lamp en stuur deze naar de frontend.
#    data = DataRepository.read_status_lamp_by_id(lamp_id)
#    socketio.emit('B2F_verandering_lamp', {'lamp': data}, broadcast=True)
#
#    # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
#    if lamp_id == '3':
#        print(f"TV kamer moet switchen naar {new_status} !")
#        GPIO.output(led3, new_status)

# ANDERE FUNCTIES


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
