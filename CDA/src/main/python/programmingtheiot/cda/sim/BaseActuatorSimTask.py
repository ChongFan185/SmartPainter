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

from programmingtheiot.data.ActuatorData import ActuatorData


class BaseActuatorSimTask():
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, actuatorType: int = ActuatorData.DEFAULT_ACTUATOR_TYPE, simpleName: str = "Actuator"):
		self.actuatorType = actuatorType
		self.simpleName = simpleName
		self.actuatorData = ActuatorData(name = simpleName)

	def activateActuator(self, val: float) -> bool:
		logging.info("""\n*******\n* ON *\n*******\n%s Value: %f\n""",self.simpleName, val)
		self.actuatorData.setCommand(ActuatorData.COMMAND_ON)
		return True

	def deactivateActuator(self) -> bool:
		logging.info("""\n*******\n* OFF *\n*******\n""")
		self.actuatorData.setCommand(ActuatorData.COMMAND_OFF)
		return True

	def getLatestActuatorResponse(self) -> ActuatorData:
		return self.actuatorData

	def getSimpleName(self) -> str:
		return self.simpleName

	def updateActuator(self, data: ActuatorData) -> bool:
		if data is not None:
			if data.getCommand() == ActuatorData.COMMAND_ON:
				self.activateActuator(data.value)
			else:
				self.deactivateActuator()
		self.actuatorData._handleUpdateData(data)
		self.actuatorData.setAsResponse()
		logging.info("Emulating %s actuator %s:", self.simpleName,
		             "ON" if self.actuatorData.getCommand() == ActuatorData.COMMAND_ON else "OFF")
		return True
