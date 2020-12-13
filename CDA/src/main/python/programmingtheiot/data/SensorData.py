#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import sys

sys.path.insert(0, '../../')
from programmingtheiot.data.BaseIotData import BaseIotData
import programmingtheiot.common.ConfigConst as ConfigConst

class SensorData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
	DEFAULT_VAL = 0.0
	DEFAULT_SENSOR_TYPE = 0

	# These are just sensor type samples - these can be changed however
	# you'd like; you can also create an enum representing the values
	HUMIDITY_SENSOR_TYPE = 1
	PRESSURE_SENSOR_TYPE = 2
	TEMP_SENSOR_TYPE = 3

	def __init__(self, name = ConfigConst.SENSOR_MSG, sensorType=DEFAULT_SENSOR_TYPE, d=None):
		super(SensorData, self).__init__(name=name, d=d)
		self.sensorType = sensorType
		self.value = 0
		if d:
			super(d)

	def getSensorType(self) -> int:
		"""
		Returns the sensor type to the caller.
		
		@return int
		"""
		return self.sensorType

	def getValue(self) -> float:
		# value getter
		return self.value

	def setValue(self, newVal: float):
		# value setter
		self.value = newVal

	def _handleUpdateData(self, data):
		# update data to this
		self.value = data.value
