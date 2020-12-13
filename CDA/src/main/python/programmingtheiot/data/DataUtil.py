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
import json

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData


class DataUtil():
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, encodeToUtf8=False):
		pass

	def actuatorDataToJson(self, actuatorData):
		# convert data to json
		return json.dumps(actuatorData, indent=4, cls=JsonDataEncoder, ensure_ascii=True)

	def sensorDataToJson(self, sensorData):
		# convert data to json
		return json.dumps(sensorData, indent=4, cls=JsonDataEncoder, ensure_ascii=True)

	def systemPerformanceDataToJson(self, sysPerfData):
		# convert data to json
		return json.dumps(sysPerfData, indent=4, cls=JsonDataEncoder, ensure_ascii=True)

	def jsonToActuatorData(self, jsonData):
		# process data
		print(str(jsonData))
		jsonData = str(jsonData).replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		# load json data
		adDict = json.loads(jsonData)
		# create object and put json data in it
		ad = ActuatorData()
		# vars() get the properties dict of the object
		mvDict = vars(ad)
		# iter properties and fill it
		for key in adDict:
			if key in mvDict:
				setattr(ad, key, adDict[key])
		return ad

	def jsonToSensorData(self, jsonData):
		# process data
		print(str(jsonData))
		jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		# load json data
		adDict = json.loads(jsonData)
		# create object and put json data in it
		ad = SensorData()
		# vars() get the properties dict of the object
		mvDict = vars(ad)
		# iter properties and fill it
		for key in adDict:
			if key in mvDict:
				setattr(ad, key, adDict[key])
		return ad

	def jsonToSystemPerformanceData(self, jsonData):
		# process data
		jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		# load json data
		adDict = json.loads(jsonData)
		# create object and put json data in it
		ad = SystemPerformanceData()
		# vars() get the properties dict of the object
		mvDict = vars(ad)
		# iter properties and fill it
		for key in adDict:
			if key in mvDict:
				setattr(ad, key, adDict[key])
		return ad


class JsonDataEncoder(json.JSONEncoder):
	"""
	Convenience class to facilitate JSON encoding of an object that
	can be converted to a dict.
	
	"""

	def default(self, o):
		return o.__dict__
