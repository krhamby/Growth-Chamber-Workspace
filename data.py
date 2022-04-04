# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TSL2561
# This code is designed to work with the TSL2561_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Light?sku=TSL2561_I2CS#tabs-0-product_tabset-2

# import smbus
import json

from app import db, Data
from datetime import datetime
import random

# imports for VEML7700
import time
import board
import adafruit_veml7700

def lux():
	while True:
	# 	# Get I2C bus
	# 	bus = smbus.SMBus(1)

	# 	# TSL2561 address, 0x39(57)
	# 	# Select control register, 0x00(00) with command register, 0x80(128)
	# 	#		0x03(03)	Power ON mode
	# 	bus.write_byte_data(0x49, 0x00 | 0x80, 0x03)
	# 	# TSL2561 address, 0x39(57)
	# 	# Select timing register, 0x01(01) with command register, 0x80(128)
	# 	#		0x02(02)	Nominal integration time = 402ms
	# 	bus.write_byte_data(0x49, 0x01 | 0x80, 0x02)

	# 	time.sleep(0.5)

	# 	# Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
	# 	# ch0 LSB, ch0 MSB
	# 	data = bus.read_i2c_block_data(0x49, 0x0C | 0x80, 2)

	# 	# Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
	# 	# ch1 LSB, ch1 MSB
	# 	data1 = bus.read_i2c_block_data(0x49, 0x0E | 0x80, 2)

	# 	# Convert the data
	# 	ch0 = data[1] * 256 + data[0]
	# 	ch1 = data1[1] * 256 + data1[0]

	# 	# Data to be written
	# 	dict = {
	# 		"FullSpectrum": ch0,
	# 		"IR": ch1,
	# 		"Visible": ch0-ch1
	# 	}

	# 	json_data = json.dumps(dict, indent=4)

	# 	with open("test.json", "w") as outfile:

	# 		outfile.write(json_data)

	# 	# Output data to screen
	# 	print("-------------------")
	# 	print("Full Spectrum(IR + Visible) in lux: ")
	# 	print(ch0)
	# 	print("Infrared Value in lux: ")
	# 	print(ch1)
	# 	print("Visible Value in lux:")
	# 	print(ch0 - ch1)

		i2c = board.I2C()
		veml7700 = adafruit_veml7700.VEML7700(i2c)

		#configuration for high-light environments
		veml7700.light_integration_time = veml7700.ALS_25MS
		veml7700.light_gain = veml7700.ALS_GAIN_1_8

		while True:
			print("Lux:", veml7700.lux)
			time.sleep(3)



		# generate random data and store it in the database
		# ch0 = random.randint(80000, 85000)

		# newData = Data(timestamp=datetime.now().isoformat(), lux=ch0, temperature=random.randint(
		# 	65, 75), humidity=random.randint(80, 85))
		# db.session.add(newData)
		# db.session.commit()

		# time.sleep(5)
