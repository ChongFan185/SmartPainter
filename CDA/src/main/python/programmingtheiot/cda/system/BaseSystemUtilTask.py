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
from programmingtheiot.data.SensorData import SensorData
import programmingtheiot.common.ConfigConst as ConfigConst

class BaseSystemUtilTask():
	"""
    Shell representation of class for student implementation.

    """

	def __init__(self,sensorName = ConfigConst.NOT_SET):
		###
		# TODO: fill in the details here
		self.latestSensorData = None
		self.sensorName = sensorName

	def generateTelemetry(self) -> SensorData:
		###
		# TODO: fill in the details here
		#
		# NOTE: Use self._getSystemUtil() to retrieve the value from the sub-class
		# create sensor data
		self.latestSensorData = SensorData()
		# set sensor data
		self.latestSensorData.setValue(self._getSystemUtil())
		return self.latestSensorData

	def getTelemetryValue(self) -> float:
		logging.info(self.__class__.__name__)
		# create latestSensorData if none
		if self.latestSensorData == None:
			self.generateTelemetry()
		return self.latestSensorData.getValue()

	def _getSystemUtil(self) -> float:
		"""
            Template method implemented by sub-class.

            Retrieve the system utilization value as a float.

            @return float
        """
		pass
