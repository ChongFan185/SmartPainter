#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import sys

import smbus

sys.path.insert(0, '../../../')
import logging

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask

class TemperatureI2cSensorAdapterTask(BaseSensorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super(TemperatureI2cSensorAdapterTask, self).__init__(SensorData.TEMP_SENSOR_TYPE, minVal = SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP, maxVal = SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
		# Example only: Read the spec for the SenseHAT temp sensor to obtain the appropriate starting address, and use i2c-tools to verify.
		self.tempAddr = 0x5C
		# init the I2C bus at the temp address
		# WARNING: only use I2C bus 1 when working with the SenseHAT on the Raspberry Pi!!
		self.i2cBus = smbus.SMBus(1)
		self.i2cBus.write_byte_data(self.tempAddr, 0, 0)

	def generateTelemetry(self) -> SensorData:
		# get a value from senseHAT
		sensorData = SensorData(sensorType=self.sensorType)
		# set this value to sensorData
		val = self.i2cBus.read_byte()
		print(val)
		sensorData.setValue(val)
		# save last sensorData
		self.latestSensorData = sensorData

		return sensorData
	
	def getTelemetryValue(self) -> float:
		return self.latestSensorData.getValue()
	