#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector

from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

from programmingtheiot.cda.embedded.StepMotorAdapterTask import StepMotorAdapterTask

class DeviceDataManager(IDataMessageListener):
    """
    Shell representation of class for student implementation.
    
    """

    def __init__(self, enableMqtt: bool = True, enableCoap: bool = False):
        # set enable connection
        self.enableMqtt = enableMqtt
        self.enableCoap = enableCoap
        # load config
        self.configUtil = ConfigUtil()
        self.enableEmulator = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE,
                                                         ConfigConst.ENABLE_EMULATOR_KEY)
        self.stepmotor = StepMotorAdapterTask()
        # create system Perf manager
        self.sysPerfManager = SystemPerformanceManager()
        # set sensor config
        self.sam = SensorAdapterManager(useEmulator=self.enableEmulator)
        #set actuator config
        self.aam = ActuatorAdapterManager(useEmulator=self.enableEmulator)
        #set data generation config
        self.enableHandleTempChangeOnDevice = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE,
                                                                         ConfigConst.ENABLE_HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)

        self.triggerHvacTempFloor = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE,
                                                             ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY);

        self.triggerHvacTempCeiling = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE,
                                                               ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY);
        #self.stepmotor.moveTo(-40,-40,True)
        # set Mqtt client
        if enableMqtt is True:
            self.mqttClient = MqttClientConnector()
            #self.mqttClient.subscribeToTopic(ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE.value)
            #self.mqttClient.subscribeToTopic(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value)
            self.mqttClient.subscribeToTopic("ProgrammingIoT/StepMotor/Instruction")
            #self.mqttClient.mc.message_callback_add(callback=self.actuatorCallBack, sub=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value)
            self.mqttClient.mc.message_callback_add(callback=self.stepMotorCallBack, sub="ProgrammingIoT/StepMotor/Instruction")

    def actuatorCallBack(self,client, userdata, message):
        logging.info("MQTT CallBack:%s,%s" % (message.topic, message.payload))
        self._handleIncomingDataAnalysis(message)
    
    def stepMotorCallBack(self,client, userdata, message):
        logging.info("MQTT CallBack:%s,%s" % (message.topic, message.payload))
        point = str(message.payload.decode()).split(",")
        if len(point) == 2:
            self.stepmotor.moveTo(int(point[0]),int(point[1]),True)

    def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
        logging.info("handleActuatorCommandResponse called")
        #pass data to handler
        super().handleActuatorCommandResponse(data)
        #translate data to json and set updstream
        du = DataUtil()
        self._handleUpstreamTransmission(ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE.value, du.actuatorDataToJson(data))

    def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
        logging.info("handleIncommingMessage called")
        #translate json to object and pass it to analysis
        du = DataUtil()
        du.jsonToActuatorData(msg)
        self._handleIncomingDataAnalysis(msg)

    def handleSensorMessage(self, data: SensorData) -> bool:
        logging.info("handleSensorMessage called")
        super().handleSensorMessage(data)
        # translate sensor data to json and handle it
        du = DataUtil()
        self._handleUpstreamTransmission(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE.value, du.sensorDataToJson(data))
        self._handleSensorDataAnalysis(data)

    def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
        logging.info("handleSystemPerformanceMessage called")
        #translate sys perf data to json and set upstream
        du = DataUtil()
        self._handleUpstreamTransmission(ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURC.value, du.systemPerformanceDataToJson(data))

    def startManager(self):
        #start manager
        self.sysPerfManager.startManager()
        self.sam.startManager()
        self.sam.setDataMessageListener(self)
        self.mqttClient.connectClient()

    def stopManager(self):
        #stop manager
        self.sysPerfManager.stopManager()
        self.sam.stopManager()
        self.mqttClient.disconnectClient()

    def _handleIncomingDataAnalysis(self, msg: str):
        """
        Call this from handleIncomeMessage() to determine if there's
        any action to take on the message. Steps to take:
        1) Validate msg: Most will be ActuatorData, but you may pass other info as well.
        2) Convert msg: Use DataUtil to convert if appropriate.
        3) Act on msg: Determine what - if any - action is required, and execute.
        """
        logging.info("_handleIncomingDataAnalysis called，msg:"+str(msg))
        #du = DataUtil()
        #self.aam.sendActuatorCommand(du.jsonToActuatorData(msg))

    def _handleSensorDataAnalysis(self, data: SensorData):
        """
        Call this from handleSensorMessage() to determine if there's
        any action to take on the message. Steps to take:
        1) Check config: Is there a rule or flag that requires immediate processing of data?
        2) Act on data: If # 1 is true, determine what - if any - action is required, and execute.
        """
        logging.info("_handleSensorDataAnalysis called，msg:"+str(data))
        if self.enableHandleTempChangeOnDevice is True:
            hvac = ActuatorData(ActuatorData.HVAC_ACTUATOR_TYPE)
            if data.getValue() < self.triggerHvacTempCeiling and data.getValue() > self.triggerHvacTempFloor:
                # start hvac when in trigger range
                hvac.setCommand(ActuatorData.COMMAND_ON)
            else:
                # stop hvac when not in range
                hvac.setCommand(ActuatorData.COMMAND_OFF)
            # send command
            self.aam.sendActuatorCommand(hvac)

    def handleActuatorCommandMessage(self, data: ActuatorData) -> bool:
        if data:
            logging.info("Processing actuator command message.")

            # TODO: add further validation before sending the command
            self.aam.sendActuatorCommand(data)
            return True
        else:
            logging.warning("Received invalid ActuatorData command message. Ignoring.")
            return False

    def _handleUpstreamTransmission(self, resourceName: ResourceNameEnum, msg: str):
        """
        Call this from handleActuatorCommandResponse(), handlesensorMessage(), and handleSystemPerformanceMessage()
        to determine if the message should be sent upstream. Steps to take:
        1) Check connection: Is there a client connection configured (and valid) to a remote MQTT or CoAP server?
        2) Act on msg: If # 1 is true, send message upstream using one (or both) client connections.
        """
        logging.info("_handleUpstreamTransmission called")
        # send message to mqtt broker
        if self.enableMqtt is True:
            self.mqttClient.publishMessage(resourceName, msg)