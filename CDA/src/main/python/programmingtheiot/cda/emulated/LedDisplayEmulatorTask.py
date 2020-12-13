#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from pisense import SenseHAT

class LedDisplayEmulatorTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super(LedDisplayEmulatorTask, self).__init__(actuatorType = ActuatorData.LED_DISPLAY_ACTUATOR_TYPE, simpleName = "LED_Display")
		# Create an instance of SenseHAT and set the emulate flag to True if running the emulator, or False if using real hardware
		# This can be read from ConfigUtil using the ConfigConst.CONSTRAINED_DEVICE section and the ConfigConst.ENABLE_SENSE_HAT_KEY
		# If the ConfigConst.ENABLE_SENSE_HAT_KEY is False, set the emulate flag to True, otherwise set to False
		configUtil = ConfigUtil()
		#get ENABLE_SENSE_HAT_KEY value (bool)
		enableSenseHAT = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_SENSE_HAT_KEY)
		if enableSenseHAT is False:
			enableEmulation = True
		else:
			enableEmulation = False
		# create senseHAT instance
		self.sh = SenseHAT(emulate=enableEmulation)

	def handleActuation(self, cmd: int, val: float = 0.0, stateData: str = None) -> int:
		# NOTE: use the API instructions for pisense for help
		if cmd == ActuatorData.COMMAND_ON:
			if self.sh.screen:
			# scroll the state data across the screen
				self.sh.screen.scroll_text("ON,"+stateData)
			else:
				logging.warning("No SenseHAT LED screen instance to update.")
				return -1
		else:
			if self.sh.screen:
			# clear the screen
				self.sh.screen.clear()
			else:
				logging.warning("No SenseHAT LED screen instance to clear / close.")
				return -1
	