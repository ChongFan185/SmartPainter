#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 
import sys

sys.path.insert(0, '../../../')
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask
import programmingtheiot.common.ConfigConst as ConfigConst

class HumidifierActuatorSimTask(BaseActuatorSimTask):
	"""
	This is a simple wrapper for an Actuator abstraction - it provides
	a container for the actuator's state, value, name, and status. A
	command variable is also provided to instruct the actuator to
	perform a specific function (in addition to setting a new value
	via the 'val' parameter.
	
	"""

	def __init__(self):
		super(HumidifierActuatorSimTask, self).__init__(actuatorType=ActuatorData.HUMIDIFIER_ACTUATOR_TYPE,
		                                                simpleName=ConfigConst.HUMIDIFIER_ACTUATOR_NAME)

	def activateActuator(self, val: float) -> bool:
		return super(HumidifierActuatorSimTask, self).activateActuator(val)

	def deactivateActuator(self) -> bool:
		return super(HumidifierActuatorSimTask, self).deactivateActuator()

	def updateActuator(self, data: ActuatorData) -> ActuatorData:
		return super(HumidifierActuatorSimTask, self).updateActuator(data)