import json
import time
import RPi.GPIO as GPIO

# GPIO pin definitions for stepper motors
STEP_PIN1 = 18  # Stepper motor cleaning and peeling
DIR_PIN1 = 23  # Stepper motor cleaning and peeling
STEP_PIN2 = 19  # Stepper motor 2 cutting
DIR_PIN2 = 24  # Stepper motor 2 cutting
STEP_PIN3 = 20  # Stepper motor 3 pouring and adding
DIR_PIN3 = 25  # Stepper motor 3 pouring and adding
STEP_PIN4 = 21  # Stepper motor 4 cooking
DIR_PIN4 = 26  # Stepper motor 4 cooking

# Setup for GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP_PIN1, GPIO.OUT)
GPIO.setup(DIR_PIN1, GPIO.OUT)
GPIO.setup(STEP_PIN2, GPIO.OUT)
GPIO.setup(DIR_PIN2, GPIO.OUT)
GPIO.setup(STEP_PIN3, GPIO.OUT)
GPIO.setup(DIR_PIN3, GPIO.OUT)
GPIO.setup(STEP_PIN4, GPIO.OUT)
GPIO.setup(DIR_PIN4, GPIO.OUT)


def to_perform_stepper_action(step_pin, dir_pin, steps, direction_length):
    GPIO.output(dir_pin, direction_length)
    for _ in range(steps):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(0.01)  # to adjust the delay
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(0.01)


def cleaning_and_peeling():
    to_perform_stepper_action(STEP_PIN1, DIR_PIN1, 200, GPIO.HIGH)


def cutting():
    to_perform_stepper_action(STEP_PIN2, DIR_PIN2, 200, GPIO.HIGH)


def pouring_and_adding():
    to_perform_stepper_action(STEP_PIN3, DIR_PIN3, 200, GPIO.HIGH)


def cooking():
    to_perform_stepper_action(STEP_PIN4, DIR_PIN4, 200, GPIO.HIGH)


def further_execute_step(step):
    action = step['action'].lower()
    parameters = step['parameters'].lower()
    time_required = step['time']

    if action == "cleaning and peeling":
        cleaning_and_peeling()
    elif action == "add":
        to_perform_stepper_action(STEP_PIN4, DIR_PIN4, 100, GPIO.LOW)

    elif action == "cutting":
        cutting()
    elif action == "pouring and adding":
        pouring_and_adding()
    elif action == "cooking":
        cooking()
    elif action == "cook":
        print(f"Cooking for {time_required} minutes, {parameters}")

    if time_required > 0:
        time.sleep(time_required * 60)


def main():
    with open('actions.json', 'r') as file:
        data = json.load(file)

    for step in data['steps']:
        further_execute_step(step)

    GPIO.cleanup()


if __name__ == '__main__':
    main()