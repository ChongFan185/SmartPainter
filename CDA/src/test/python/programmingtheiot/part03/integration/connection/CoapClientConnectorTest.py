#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 
import sys
sys.path.insert(0, '../../../../../../main/python')
import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector

class CoapClientConnectorTest(unittest.TestCase):
	"""
	This test case class contains very basic integration tests for
	CoapClientConnector. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing CoapClientConnector class...")
		
		self.cfg = ConfigUtil()
		self.mcc = CoapClientConnector()
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	#@unittest.skip("Ignore for now.")
	def testConnectAndDiscover(self):
		#start server by "D:\360Downloads\jdk_8\bin\java.exe -jar cf-server-2.5.0-SNAPSHOT.jar"
		self.mcc.sendDiscoveryRequest(timeout=10)

	#@unittest.skip("Ignore for now.")
	def testConnectAndGetCon(self):
		self.mcc.sendGetRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, enableCON=True, timeout=5)

	#@unittest.skip("Ignore for now.")
	def testConnectAndGetNon(self):
		self.mcc.sendGetRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, enableCON=False, timeout=5)

	# @unittest.skip("Ignore for now.")
	def testConnectAndPutCon(self):
		msg = "This is a test."
		self.mcc.sendPutRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, payload=msg,
		                               enableCON=True, timeout=5)

	# @unittest.skip("Ignore for now.")
	def testConnectAndPutNon(self):
		msg = "This is a test."
		self.mcc.sendPutRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, payload=msg,
		                               enableCON=False, timeout=5)

	# @unittest.skip("Ignore for now.")
	def testConnectAndPostCon(self):
		msg = "This is a test."
		self.mcc.sendPostRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, payload=msg,
		                                enableCON=True, timeout=5)

	# @unittest.skip("Ignore for now.")
	def testConnectAndPostNon(self):
		msg = "This is a test."
		self.mcc.sendPostRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, payload=msg,
		                                enableCON=False, timeout=5)

	# @unittest.skip("Ignore for now.")
	def testConnectAndDeleteCon(self):
		self.mcc.sendDeleteRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, enableCON=True,
		                                  timeout=5)

	# @unittest.skip("Ignore for now.")
	def testConnectAndDeleteNon(self):
		self.mcc.sendDeleteRequest(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, enableCON=False,
		                                  timeout=5)

	#@unittest.skip("Ignore for now.")
	def testConnectAndGet(self):
		# TODO: implement this
		pass

	#@unittest.skip("Ignore for now.")
	def testConnectAndDelete(self):
		# TODO: implement this
		pass

	#@unittest.skip("Ignore for now.")
	def testConnectAndPost(self):
		# TODO: implement this
		pass

	#@unittest.skip("Ignore for now.")
	def testConnectAndPut(self):
		# TODO: implement this
		pass

	#@unittest.skip("Ignore for now.")
	def testIntegrateWithGdaGetCdaCmdTopic(self):
		# TODO: implement this
		pass

	#@unittest.skip("Ignore for now.")
	def testIntegrateWithGdaPostCdaMgmtTopic(self):
		# TODO: implement this
		pass

if __name__ == "__main__":
	unittest.main()
	