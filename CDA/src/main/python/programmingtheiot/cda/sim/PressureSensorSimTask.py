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

from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.SensorData import SensorData


class PressureSensorSimTask(BaseSensorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, dataSet = None):
		super(PressureSensorSimTask, self).__init__(SensorData.PRESSURE_SENSOR_TYPE, dataSet=dataSet,
		                                            minVal=SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE,
		                                            maxVal=SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)

	def generateTelemetry(self) -> SensorData:
		# call super class method
		sd = super(PressureSensorSimTask, self).generateTelemetry()
		sd.setName(ConfigConst.PRESSURE_SENSOR_NAME)
		return sd

	def getTelemetryValue(self) -> float:
		# call super class method
		return super(PressureSensorSimTask, self).getTelemetryValue()
