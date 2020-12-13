#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 by Andrew D. King
#
import sys
import time

sys.path.insert(0, '../../../../../../main/python')
import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector


class CoapClientPerformanceTest(unittest.TestCase):
	"""
	This test case class contains very basic integration tests for
	CoapClient performance.
	"""
	NS_IN_MILLIS = 1000000

	# NOTE: We'll use only 10,000 requests for CoAP
	MAX_TEST_RUNS = 50

	@classmethod
	def setUpClass(self):
		logging.disable(level=logging.WARNING)

	def setUp(self):
		self.coapClient = CoapClientConnector()

	def tearDown(self):
		self.coapClient.disconnectClient()

	# @unittest.skip("Ignore for now.")
	def testPostRequestCon(self):
		print("Testing POST - CON")

		self._execTestPost(self.MAX_TEST_RUNS, True)

	# @unittest.skip("Ignore for now.")
	def testPostRequestNon(self):
		print("Testing POST - NON")

		self._execTestPost(self.MAX_TEST_RUNS, False)

	def _execTestPost(self, maxTestRuns: int, useCon: bool):
		sensorData = SensorData()
		payload = DataUtil().sensorDataToJson(sensorData)

		startTime = time.time_ns()

		for seqNo in range(0, maxTestRuns):
			self.coapClient.sendPostRequest(resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, enableCON=useCon,
			                                payload=payload)

		endTime = time.time_ns()
		elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS

		print("POST message - useCON = " + str(useCon) + " [" + str(maxTestRuns) + "]: " + str(elapsedMillis) + " ms")

if __name__ == "__main__":
	unittest.main()
