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

class ActuatorData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
	DEFAULT_COMMAND = 0
	COMMAND_OFF = DEFAULT_COMMAND
	COMMAND_ON = 1

	# for now, actuators will be 1..99
	# and displays will be 100..1999
	DEFAULT_ACTUATOR_TYPE = 0
	
	HVAC_ACTUATOR_TYPE = 1
	HUMIDIFIER_ACTUATOR_TYPE = 2
	LED_DISPLAY_ACTUATOR_TYPE = 100

	def __init__(self, name = ConfigConst.ACTUATOR_CMD, actuatorType = DEFAULT_ACTUATOR_TYPE, d = None):
		super(ActuatorData, self).__init__(name=name, d=d)
		#init variables
		self.actuatorType = actuatorType
		self.value = 0
		self.command = self.DEFAULT_COMMAND
		self.stateData = ""
		pass
	
	def getCommand(self) -> int:
		#command getter
		return self.command
	
	def getStateData(self) -> str:
		#stateData getter
		return self.stateData
	
	def getValue(self) -> float:
		#value getter
		return self.value
	
	def isResponseFlagEnabled(self) -> bool:
		return False
	
	def setCommand(self, command: int):
		#command setter
		self.command = command
	
	def setAsResponse(self):
		pass
		
	def setStateData(self, stateData: str):
		#stateData setter
		self.stateData = stateData
	
	def setValue(self, val: float):
		#value setter
		self.value = val
		
	def _handleUpdateData(self, data):
		#Update Actuator value, command and stateData
		self.value = data.value
		self.command = data.command
		self.stateData = data.stateData
