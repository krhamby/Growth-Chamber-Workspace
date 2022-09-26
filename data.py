import json

# imports for database
from app import db, Data, Schedule
from datetime import datetime

# imports for VEML7700
import time
import board
import adafruit_veml7700

# VEML7700 initialization
i2c = board.I2C()
veml7700 = adafruit_veml7700.VEML7700(i2c)

# VEML7700 configuration for high-light environments
veml7700.light_integration_time = veml7700.ALS_25MS
veml7700.light_gain = veml7700.ALS_GAIN_1_8

# imports for DHT22
import adafruit_dht

# DHT22 initialization
dhtDevice = adafruit_dht.DHT22(board.D17)

from app import light

def lightControl():
	schedule = Schedule.query.filter_by(id = "lux").first()
	if schedule:
		startTime = schedule.startTime
		endTime = schedule.endTime
		if startTime <= datetime.now().strftime("%H:%M") <= endTime:
			light.on()
			print("light on")
		else:
			light.off()
			print("light off")


def lux():
	print("ALS: " + str(veml7700.light))
	lux = veml7700.lux
	adjusted_lux = (6.0135*10**-13)*(lux**4) - (9.3924*10**-9)*(lux**3) + (8.1488*10**-5)*(lux**2) + (1.0023)*(lux)
	print("Lux: " + str(lux))
	print("Adjusted Lux: " + str(adjusted_lux))
	return veml7700.lux

def temp():
	while True:
		try:
			temperature_c = dhtDevice.temperature
			if temperature_c is None:
				continue
			temperature_f = temperature_c * (9 / 5) + 32
			return temperature_f
			
		except RuntimeError as error:
			# Errors happen fairly often, DHT's are hard to read, just keep going
			print(error.args[0])
			time.sleep(1)
			continue
		except Exception as error:
			dhtDevice.exit()
			raise error

def humidity():
	while True:
		try:
			sum = 0
			for i in range(0, 5):
				humidity = dhtDevice.humidity
				sum += humidity
				time.sleep(1)

			return sum / 5
			
		except RuntimeError as error:
			# Errors happen fairly often, DHT's are hard to read, just keep going
			print(error.args[0])
			time.sleep(1)
			continue
		except Exception as error:
			dhtDevice.exit()
			raise error
	

def main():
	while True:
		db.session.add(Data(timestamp = datetime.now().isoformat(), lux = lux(), temperature = temp(), humidity = humidity()))
		db.session.commit()

		lightControl()

		time.sleep(5)
		
