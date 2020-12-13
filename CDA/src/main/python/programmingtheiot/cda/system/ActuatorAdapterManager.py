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

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask

class ActuatorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self, useEmulator: bool = False):
		self.useEmulator = useEmulator
		self.dataMsgListener = IDataMessageListener()
		if self.useEmulator is True:
			logging.info("Use Emulator")
			# load the Humidifier actuation emulator
			humidifierModule = __import__('programmingtheiot.cda.emulated.HumidifierEmulatorTask',
										  fromlist=['HumidifierEmulatorTask'])
			hueClazz = getattr(humidifierModule, 'HumidifierEmulatorTask')
			self.humidifierEmulator = hueClazz()
			# load the Hvac actuation emulator
			hvacModule = __import__('programmingtheiot.cda.emulated.HvacEmulatorTask',
										  fromlist=['HvacEmulatorTask'])
			hueClazz = getattr(hvacModule, 'HvacEmulatorTask')
			self.hvacEmulator = hueClazz()
			# load the LED actuation emulator
			ledModule = __import__('programmingtheiot.cda.emulated.LedDisplayEmulatorTask',
									fromlist=['LedDisplayEmulatorTask'])
			hueClazz = getattr(ledModule, 'LedDisplayEmulatorTask')
			self.ledEmulator = hueClazz()
		else:
			logging.info("Use Simulator")
			# create the humidifier actuator
			self.humidifierActuator = HumidifierActuatorSimTask()
			# create the HVAC actuator
			self.hvacActuator = HvacActuatorSimTask()


	def sendActuatorCommand(self, data: ActuatorData) -> bool:
		logging.info("Actuator command received.Processing...")
		if self.useEmulator is True:
			if data.actuatorType == ActuatorData.HVAC_ACTUATOR_TYPE:
				# set hvac data (command, value ...)
				self.hvacEmulator.handleActuation(data.getCommand(), data.getValue(), data.getStateData())
			elif data.actuatorType == ActuatorData.HUMIDIFIER_ACTUATOR_TYPE:
				# set humidifier data (command, value ...)
				self.humidifierEmulator.handleActuation(data.getCommand(), data.getValue(), data.getStateData())
			elif data.actuatorType == ActuatorData.LED_DISPLAY_ACTUATOR_TYPE:
				# set led
				self.ledEmulator.handleActuation(data.getCommand(), data.getValue(), data.getStateData())
			else:
				logging.info("Cant Find Actuator Type")
				pass
			self.humidifierEmulator
			self.hvacEmulator
		else:
			if data.actuatorType == ActuatorData.HVAC_ACTUATOR_TYPE:
				# set hvac data (command, value ...)
				self.hvacActuator.updateActuator(data)
			elif data.actuatorType == ActuatorData.HUMIDIFIER_ACTUATOR_TYPE:
				# set humidifier data (command, value ...)
				self.humidifierActuator.updateActuator(data)
			elif data.actuatorType == ActuatorData.LED_DISPLAY_ACTUATOR_TYPE:
				logging.info("No LED device")
			else:
				logging.info("Cant Find Actuator Type")
				pass
		# pass data to listener
		self.dataMsgListener.handleActuatorCommandResponse(data)
	
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if listener is not None:
			self.dataMsgListener = listener
