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
from programmingtheiot.data.SensorData import SensorData

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

from pisense import SenseHAT

class TemperatureSensorEmulatorTask(BaseSensorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, dataSet = None):
		super(TemperatureSensorEmulatorTask, self).__init__(SensorData.TEMP_SENSOR_TYPE, minVal = SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP, maxVal = SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
		configUtil = ConfigUtil()
		#get ENABLE_SENSE_HAT_KEY value (bool)
		enableSenseHAT = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_SENSE_HAT_KEY)
		if enableSenseHAT is False:
			enableEmulation = True
		else:
			enableEmulation = False
		# create senseHAT instance
		self.sh = SenseHAT(emulate=enableEmulation)

	def generateTelemetry(self) -> SensorData:
		#get a value from emulator
		sensorData = SensorData(name = ConfigConst.TEMP_SENSOR_NAME, sensorType = self.sensorType)
		sensorVal = self.sh.environ.temperature
		#set this value to sensorData
		sensorData.setValue(sensorVal)
		#save last sensorData
		self.latestSensorData = sensorData

		return sensorData
