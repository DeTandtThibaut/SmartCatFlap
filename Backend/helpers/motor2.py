import RPi.GPIO as GPIO
import time

class motor:

    # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
    global step_sleep
    step_sleep = 0.002

    
    #step_count = 1024 # 5.625*(1/64) per step, 4096 steps is 360°

    #direction = False # True for clockwise, False for counter-clockwise

    # defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
    global step_sequence
    step_sequence = [[1,0,0,1],
                     [1,0,0,0],
                     [1,1,0,0],
                     [0,1,0,0],
                     [0,1,1,0],
                     [0,0,1,0],
                     [0,0,1,1],
                     [0,0,0,1]]


    def __init__(self,direction = False,multiplier = 0,in1 = 17,in2 = 27,in3 = 22,in4 = 6):
        self.direction = direction
        self.motor_step_counter = multiplier;
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        self.motor_pins = [self.in1,self.in2,self.in3,self.in4]

        # setting up
        GPIO.setmode( GPIO.BCM )
        GPIO.setup( self.in1, GPIO.OUT )
        GPIO.setup( self.in2, GPIO.OUT )
        GPIO.setup( self.in3, GPIO.OUT )
        GPIO.setup( self.in4, GPIO.OUT )

        # initializing
        GPIO.output( self.in1, GPIO.LOW )
        GPIO.output( self.in2, GPIO.LOW )
        GPIO.output( self.in3, GPIO.LOW )
        GPIO.output( self.in4, GPIO.LOW )

    def cleanup(self):
        GPIO.output( self.in1, GPIO.LOW )
        GPIO.output( self.in2, GPIO.LOW )
        GPIO.output( self.in3, GPIO.LOW )
        GPIO.output( self.in4, GPIO.LOW )
        #GPIO.cleanup()


    def turn_motor(self,direction,multiplier):
        self.direction = direction
        step_count = 1024 * multiplier
        try:
            i = 0
            for i in range(step_count):
                for pin in range(0, len(self.motor_pins)):
                    GPIO.output( self.motor_pins[pin], step_sequence[self.motor_step_counter][pin] )
                if self.direction==True:
                    self.motor_step_counter = (self.motor_step_counter - 1) % 8
                elif self.direction==False:
                    self.motor_step_counter = (self.motor_step_counter + 1) % 8
                else: 
                    print( "direction should always be either True or False" )
                    GPIO.output( self.in1, GPIO.LOW )
                    GPIO.output( self.in2, GPIO.LOW )
                    GPIO.output( self.in3, GPIO.LOW )
                    GPIO.output( self.in4, GPIO.LOW )
                    
                    exit( 1 )
                time.sleep(step_sleep)

        except KeyboardInterrupt:
            GPIO.output( self.in1, GPIO.LOW )
            GPIO.output( self.in2, GPIO.LOW )
            GPIO.output( self.in3, GPIO.LOW )
            GPIO.output( self.in4, GPIO.LOW )
            
            exit( 1 )

    def end(self):
        GPIO.output( self.in1, GPIO.LOW )
        GPIO.output( self.in2, GPIO.LOW )
        GPIO.output( self.in3, GPIO.LOW )
        GPIO.output( self.in4, GPIO.LOW )
        
        exit( 0 )
