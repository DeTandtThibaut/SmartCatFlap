
#pylint: skip-file
from RPi import GPIO
import time


# a) Stop alle 8 de databits in de correcte volgorde in een list.
#databits = [16, 12, 25, 24, 23, 26, 19, 13]
databits = [13, 19, 26, 23, 24, 25, 12, 16]

class LCD:
    def __init__(self, rs, e, databits):
        self.rs = rs
        self.e = e
        self.databits = databits
        # Initialiseer alle GPIO pinnen.
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.e, GPIO.OUT)
        for bit in databits:
            GPIO.setup(bit, GPIO.OUT)

        time.sleep(0.1)
        self.init_LCD()
    
        



    # stuur instructie
    def send_instruction(self, value):
        # rs laag: voor instruction
        GPIO.output(self.rs, GPIO.LOW)
        # enable hoog
        GPIO.output(self.e, GPIO.HIGH)
        self.set_data_bits(value)
        # enable terug laag
        GPIO.output(self.e, GPIO.LOW)
        time.sleep(0.1)
        


    # stuur 1 character
    def send_character(self, character):
        # rs hoog: voor data
        GPIO.output(self.rs, GPIO.HIGH)
        # enable hoog
        GPIO.output(self.e, GPIO.HIGH)
        # data klaarzetten
        self.set_data_bits(character)
        # enable laag
        GPIO.output(self.e, GPIO.LOW)
        # wait
        time.sleep(0.1)



    # set_data_bits(value)
    def set_data_bits(self, byte):
        mask = 0x80
        for i in range(8):
            GPIO.output(self.databits[i], byte & (mask >> i))


    def clear_display(self):
        self.send_instruction(0b00000001)

    # write_message(message).
    def write_message(self, message):
        for char in message[0:16]:
            self.send_character(ord(char))
        for char in message[16:]:
            self.move_screen()
            self.send_character(ord(char))




    # init_LCD()
    def init_LCD(self):
        # set datalengte op 8 bit (= DB4 hoog), 2 lijnen (=DB3), 5x7 display (=DB2).
        self.send_instruction(0b00111000)
        # display on (=DB2), cursor on (=DB1), blinking on (=DB0)
        self.send_instruction(0b00001111)
        # clear display en cursor home (DB0 hoog)
        self.send_instruction(0b00000001)



    # set cursor
    def set_cursor(self, row, col):
        # byte maken: row (0 of 1) = 0x0* voor rij 0 of 0x4* voor rij 1. col = 0x*0 - 0x*F
        byte = row << 6 | col
        # byte | 128 want DB7 moet 1 zijn
        self.send_instruction(byte | 128)



    # move screen: verplaatst het scherm
    def move_screen(self):
        self.send_instruction(0b00011000)



#if __name__ == "__main__":
#    try:
#        setup()
#        #write_message("Hello World!")
#        #send_instruction(0b11000000)
#        #write_message("Hello World!Hello World2")
#        
#        #write_message("test")
#        message = input("Choose a string to display: ")
#        write_message(message)
#
#        set_cursor(0, 40)
#        
#        # j) Vraag een input van de gebruiker.
#        message = input("Choose a string to display: ")
#        write_message(message)
#            
#    except KeyboardInterrupt as e:
#        print("quitting...")