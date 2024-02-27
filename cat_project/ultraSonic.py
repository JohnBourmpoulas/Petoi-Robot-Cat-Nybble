import RPi.GPIO as GPIO
import time

class UltraSonic:
    def __init__(self, trigger_pin, echo_pin, stop_event):
        # Check if the mode is already set
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BOARD)

        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.stop_event = stop_event

        # Set up GPIO pins
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        # Send a pulse to trigger the ultrasonic sensor
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        # Measure the time taken for the echo to return
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        while GPIO.input(self.echo_pin) == 0:
            pulse_start_time = time.time()

        while GPIO.input(self.echo_pin) == 1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time

        # Calculate distance based on the time taken
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        
        return distance

    def continuous_distance_check(self):
        # Continuously check distance until stop event is set
        while not self.stop_event.is_set():
            distance = self.get_distance()
            print(f"Distance: {distance} cm")
            time.sleep(1)
