import math
import threading
import time
from adafruit_servokit import ServoKit
from camera import Camera
from ultraSonic import UltraSonic
import RPi.GPIO as GPIO

TRIGGER_PIN = 11  # Replace with real PIN
ECHO_PIN = 12  # Replace with real PIN

# The RobotCat class represents a robotic cat that combines functionalities of Camera and UltraSonic classes.
class RobotCat(Camera, UltraSonic):
    def __init__(self):
        Camera.__init__(self)  # Initializing Camera class for face recognition functionality
        # Creating an event for stopping threads
        self.stop_event = threading.Event()
        # Initializing UltraSonic class with trigger_pin, echo_pin, and stop_event parameters for obstacle detection
        UltraSonic.__init__(self, trigger_pin=11, echo_pin=18, stop_event=self.stop_event)
        
        # Creating another event for stopping threads
        self.stop_event = threading.Event()

        # Creating thread for the camera to perform face recognition
        self.camera_thread = threading.Thread(target=self.start_camera)
        self.camera_thread.start()

        # Creating thread for obstacle detection using UltraSonic sensors
        self.obstacle_detection_thread = threading.Thread(target=self.continuous_distance_check)
        self.obstacle_detection_thread.start()
        
        # Initializing ServoKit object for controlling servos
        self.kit = ServoKit(channels=16)

        # Pins configuration for each motor
        self.front_left_motor_pins = [3, 4]
        self.front_right_motor_pins = [1,2]
        self.back_left_motor_pins = [7, 8]  # Same as front_left
        self.back_right_motor_pins = [5, 6]  # Same as front_right
        self.tail_motor_pin = 0
        
        # Making the robot cat stand up initially
        self.stand_up()
        
    # Method to create a stop event
    def create_stop_event(self):
        return threading.Event()
  
    # Method to move the robot cat forward
    def move_forward(self):
        for _ in range(3):
            for angle in range(140,30, 10):
                # Setting angles for various servos to create forward motion
                self.kit.servo[6].angle = angle  
                self.kit.servo[5].angle = angle
                self.kit.servo[8].angle = angle  
                self.kit.servo[7].angle = angle 
                self.kit.servo[2].angle = angle  
                self.kit.servo[1].angle = angle
                self.kit.servo[4].angle = angle  
                self.kit.servo[3].angle = angle 
                time.sleep(0.05)
                
            for angle in range(30,140, 10):
                # Setting angles for various servos to create forward motion
                self.kit.servo[6].angle = angle  
                self.kit.servo[5].angle = angle
                self.kit.servo[8].angle = angle  
                self.kit.servo[7].angle = angle 
                
                self.kit.servo[2].angle = angle  
                self.kit.servo[1].angle = angle
                self.kit.servo[4].angle = angle  
                self.kit.servo[3].angle = angle 
                time.sleep(0.05)
         
    # Method to move the tail of the robot cat
    def move_tail(self):
        tail_motor_pin = 0
        for angle in range(0, 90, 5):
            # Setting angle for the tail servo to move the tail
            self.kit.servo[tail_motor_pin].angle = angle
            time.sleep(0.05)

    # Method to make the robot cat stand up
    def stand_up(self):
        # Angles for front legs to stand up
        self.kit.servo[5].angle = 90
        self.kit.servo[6].angle = 90
        self.kit.servo[7].angle = 90
        self.kit.servo[8].angle = 90       
        time.sleep(1)  
        self.kit.servo[1].angle = 90
        self.kit.servo[2].angle = 90
        self.kit.servo[3].angle = 90
        self.kit.servo[4].angle = 90
        time.sleep(1)
        
    # Method to make the robot cat sit down
    def sit_down(self):        
        # Set angles for front legs to sit down
        self.kit.servo[5].angle = 180
        self.kit.servo[6].angle = 90
        self.kit.servo[7].angle = 0
        self.kit.servo[8].angle = 90
        time.sleep(1)
        self.kit.servo[1].angle = 0
        self.kit.servo[2].angle = 90
        self.kit.servo[3].angle = 180
        self.kit.servo[4].angle = 90

    # Method to check if servo angles have exceeded limits
    def check_limits(self):
        all_pins = (
            self.front_left_motor_pins
            + self.front_right_motor_pins
            + self.back_left_motor_pins
            + self.back_right_motor_pins
        )

        for pin in all_pins:
            servo_angle = self.kit.servo[pin].angle
            if servo_angle is not None and servo_angle > 90:
                self.kit.servo[pin].angle = 90
            elif servo_angle is not None and servo_angle < 0:
                self.kit.servo[pin].angle = 0

# Main block to create an instance of the RobotCat class and handle KeyboardInterrupt
if __name__ == "__main__":
    my_cat = RobotCat()
    
    try:    
        while True:
            # The code executing the robot...
            pass
            
            #time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
