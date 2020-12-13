#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import sys

sys.path.insert(0, '../../../')
import logging
import random

from programmingtheiot.data.SensorData import SensorData


class BaseSensorSimTask():
	"""
	Shell representation of class for student implementation.
	
	"""

	DEFAULT_MIN_VAL = 0.0
	DEFAULT_MAX_VAL = 1000.0

	def __init__(self, sensorType: int = SensorData.DEFAULT_SENSOR_TYPE, dataSet=None, minVal: float = DEFAULT_MIN_VAL,
	             maxVal: float = DEFAULT_MAX_VAL):
		# init class
		self.sensorType = sensorType
		self.dataSet = dataSet
		self.sensorData = None
		self.minVal = minVal
		self.maxVal = maxVal
		self.currentIndex = 0
		if self.dataSet is None:
			self.useRandom = True
		else:
			self.useRandom = False

	def generateTelemetry(self) -> SensorData:
		# create SensorData instance
		sd = SensorData(self.sensorType)
		if self.useRandom is True:
			# generate data
			sd.setValue(random.uniform(self.minVal, self.maxVal))
		else:
			# use origin data set
			if self.dataSet.getDataEntryCount() >= self.currentIndex + 1:
				sd.setValue(self.dataSet.getDataEntry(self.currentIndex))
			# set and check index
			self.currentIndex += 1
			if self.currentIndex >= self.dataSet.getDataEntryCount() - 1:
				self.currentIndex = 0
		self.sensorData = sd
		return sd

	def getTelemetryValue(self) -> float:
		if self.sensorData is None:
			# generate data
			return self.generateTelemetry().value
		else:
			# use current data
			return self.sensorData.value
