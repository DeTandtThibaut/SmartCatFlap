from RPi import GPIO
import time

# a) Stop alle 8 de databits in de correcte volgorde in een list.
bits = [13, 19, 26, 23, 24, 25, 12, 16]

RS = 21 
E = 20 #data doorsturen

def setup():
    # for (i = 0; i < 8; i+=1):
    #     bit[i] = pinnen[i]

    # b) Initialiseer alle GPIO pinnen.
    GPIO.setmode(GPIO.BCM)
    for bit in bits:
        GPIO.setup(bit, GPIO.OUT,initial=GPIO.LOW)
    
    GPIO.setup(RS, GPIO.OUT,  initial=GPIO.LOW)
    GPIO.setup(E,  GPIO.OUT, initial=GPIO.HIGH)
    

# c) Schrijf de set_data_bits(value) functie. De parameter van de deze functie is een byte. Deze functie
# moet de value waarde parallel op de 8 databus lijnen plaatsen. Schrijf hiervoor een for loop die de
# parameter value bit per bit overloopt. Je checkt telkens de waarde van die bit om de overeenkomstige
# databus bitlijn hoog of laag te plaatsen. In deze functie gaan we de RS lijn NIET aanpassen.
def set_data_bits(byte):
    mask = 0x01
    print("byte: " + bin(byte))
    for i in range(len(bits)):
        print(((mask << i) & byte))
        GPIO.output(bits[i], ((mask << i) & byte) > 0)

# d) Schrijf de send_instruction(value). Deze methode zet de RS lijn op het correcte niveau en maakt een
# klokpuls met de E lijn. (van hoog naar laag = inlezen). Deze methode roept ook de methode
# set_data_bits(value) aan.
def send_instruction(value):
    #RS moet laag staan voor instruction
    GPIO.output(RS, GPIO.LOW)
    GPIO.output(E, GPIO.HIGH)
    set_data_bits(value)
    GPIO.output(E, GPIO.LOW)
    time.sleep(0.01)

# e) Schrijf de send_character(value). Idem als daarnet maar met de RS lijn op data input.
def send_character(character):
    #RS moet hoog staan voor character
    GPIO.output(RS, GPIO.HIGH)
    GPIO.output(E, GPIO.HIGH)
    set_data_bits(character)
    GPIO.output(E, GPIO.LOW)
    time.sleep(0.01)

# i) Schrijf een def write_message(message). Deze methode overloopt het bericht en schrijft karakter per
# karakter naar het LCD display.
def write_message(message):
    for char in message[0:16]:
        send_character(ord(char))   
    
    send_instruction((0x80 | 0x40))

    for char in message[16:]:
        send_character(ord(char))

# f) Schrijf een init_LCD(). In deze definition roep je de instructie function set, display on en clear display &
# cursor home aan. Dus 3 instructies na elkaar doorsturen (in de juiste volgorde)
def init_LCD():
    # funtion set: set datalengte op 8 bit (= DB4 hoog), 2 lijnen (=DB3), 5x7 display (=DB2).
    send_instruction(0b00111000)

    # display on (=DB2), cursor on (=DB1), blinking on (=DB0)
    send_instruction(0b00001111)
    #clear display
    # clear display en cursor home (DB0 hoog)
    send_instruction(0b00000001)
    # #cursor home
    #send_instruction(0x40)

try:
    setup()
    init_LCD()

    # h) Test de methode send_character(value) uit. Geef b.v. de ascii code 65 mee en de letter ‘A’ zou op het
    # display moeten verschijnen.
    #send_character(ord("A"))
    # text = "HALLO Laura"
    # for char in text:
    #     send_character(ord(char))
    #send_character(65)#letter A schrijven
    write_message('Hello')


    # j) Vraag een input van de gebruiker. De ingegeven tekst druk je af op het display. Zorg er ook voor dat de tekst
    # correct wordt weergeven als de tekst meer dan 16 karakters bedraagt. Los dit op door gebruik te maken van een
    # instructie.
    # message = input("What do you want to display? > ")
    # write_message(message)
    
except KeyboardInterrupt as e:
    print(e)
finally:
    GPIO.cleanup()