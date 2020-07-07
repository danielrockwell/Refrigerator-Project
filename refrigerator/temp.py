import csv
from datetime import datetime
import time

CURRENT_DAY = datetime.now().strftime("%d_%m_%Y")

# TEMPERATURE_PROBE_PATH instructions at http://raspberrypi.tomasgreno.cz/thermal-sensor-1wire.html
TEMPERATURE_PROBE_PATH = '/sys/bus/w1/devices/28-01144a221baa/w1_slave'
CSV_FIELD_NAMES = ['date','temperature_celsius']

'''The getTemperature function parses the temperature data from the TEMPERATURE_PROBE_PATH
    and returns the current temperature in °C'''
def getTemperature():
    with open(TEMPERATURE_PROBE_PATH, 'r') as sensor_file:
        second_line_of_file = sensor_file.readlines()[1].strip()
        temperature = second_line_of_file.split("=")[1]
        temperatureInCelsius = int(temperature) / 1000
    return temperatureInCelsius

# The getDateAndTime function returns the current datetime and current temperature
def getDateAndTime(current_day):
    currentTemperature = getTemperature()
    currentTime = current_day.isoformat(sep=' ', timespec='milliseconds')
    return currentTemperature, currentTime

# The writeToCSV function writes the data to a temp_log CSV file
def writeToCSV():
    current_day = datetime.now()
    date_format = str(current_day.date()).replace("-","_")
    with open(f"/home/pi/4740_project1/logs/temp_logs/{date_format}_temp_log.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames = CSV_FIELD_NAMES)

        # Create header for file if new day (new file is created each day)
        if file.tell() < 1:
            writer.writeheader()
        curr_temp,curr_time = getDateAndTime(current_day)
        writer.writerow({'date': curr_time, 'temperature_celsius': curr_temp})
        time.sleep(0.1)
        # TESTING
        # print(f'Current Datetime: {curr_time} | Current Temp: {curr_temp}')

# Check the sensor's temeprature approx. every second and write to CSV
def log_temp():
    while True:
        writeToCSV()

def main():
    log_temp()

if __name__ == '__main__':
    main()

