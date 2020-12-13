#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import random

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask
import programmingtheiot.common.ConfigConst as ConfigConst

class HvacActuatorSimTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super(HvacActuatorSimTask, self).__init__(actuatorType=ActuatorData.HVAC_ACTUATOR_TYPE, simpleName=ConfigConst.HVAC_ACTUATOR_NAME)

	def activateActuator(self, val: float) -> bool:
		return super(HvacActuatorSimTask, self).activateActuator(val)

	def deactivateActuator(self) -> bool:
		return super(HvacActuatorSimTask, self).deactivateActuator()

	def updateActuator(self, data: ActuatorData) -> ActuatorData:
		return super(HvacActuatorSimTask, self).updateActuator(data)
