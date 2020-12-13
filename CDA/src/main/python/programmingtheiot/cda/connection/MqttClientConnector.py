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
import paho.mqtt.client as mqttClient

from programmingtheiot.common import ConfigUtil
from programmingtheiot.common import ConfigConst

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.DataUtil import DataUtil

from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient

DEFAULT_QOS = 1

class MqttClientConnector(IPubSubClient):
    """
    Shell representation of class for student implementation.
    
    """

    def __init__(self, clientID: str = None):
        """
        Default constructor. This will set remote broker information and client connection
        information based on the default configuration file contents.
        
        @param clientID Defaults to None. Can be set by caller. If this is used, it's
        critically important that a unique, non-conflicting name be used so to avoid
        causing the MQTT broker to disconnect any client using the same name. With
        auto-reconnect enabled, this can cause a race condition where each client with
        the same clientID continuously attempts to re-connect, causing the broker to
        disconnect the previous instance.
        """
        self.config = ConfigUtil.ConfigUtil()
        # read host from config
        self.host = self.config.getProperty(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY,
                                            ConfigConst.DEFAULT_HOST)
        # read port from config. default 1883
        self.port = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY,
                                           ConfigConst.DEFAULT_MQTT_PORT)
        # read keepalive time from config
        self.keepAlive = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY,
                                                ConfigConst.DEFAULT_KEEP_ALIVE)
        # print config
        logging.info('\tMQTT Broker Host: ' + self.host)
        logging.info('\tMQTT Broker Port: ' + str(self.port))
        logging.info('\tMQTT Keep Alive:  ' + str(self.keepAlive))
        # declear variables
        self.mc = None
        self.clientID = clientID
        self.dataMsgListener = None
        self.connectClient()
        self.callback = None

    def connect(self)->bool:
        self.connectClient()

    def disconnect(self)->bool:
        self.disconnectClient()

    def connectClient(self) -> bool:
        # create a mqtt client if not created
        if not self.mc:
            self.mc = mqttClient.Client(client_id=self.clientID, clean_session=True)
            self.mc.on_connect = self.onConnect
            self.mc.on_disconnect = self.onDisconnect
            self.mc.on_message = self.onMessage
            self.mc.on_publish = self.onPublish
            self.mc.on_subscribe = self.onSubscribe
        # connect to broker if not connected
        if not self.mc.is_connected():
            self.mc.connect(self.host, self.port, self.keepAlive)
            self.mc.loop_start()
            return True
        else:
            logging.error('MQTT client is already connected. Ignoring connect request.')
            return False
        
    def disconnectClient(self) -> bool:
        # disconnect to broker
        if self.mc.is_connected():
            self.mc.disconnect()
            self.mc.loop_stop()
        return True

    def onConnect(self, client, userdata, flags, rc):
        logging.info("onConnect:%s,%s,%s,%s" % (client,userdata,flags,rc))
        logging.info('[Callback] Connected to MQTT broker. Result code: ' + str(rc))
        # NOTE: Use the QoS of your choice - '1' is only an example
        # subscribe and set callback
        #self.mc.subscribe(topic=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value, qos=1)
        #self.mc.message_callback_add(sub=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value,
        #                                     callback=self.onActuatorCommandMessage)

    def onDisconnect(self, client, userdata, rc):
        logging.info("onDisconnect:%s,%s,%s" % (client,userdata,rc))
        
    def onMessage(self, client, userdata, msg):
        logging.info("onMessage:%s,%s,%s,%s" % (client, userdata,msg.topic,msg.payload))
            
    def onPublish(self, client, userdata, mid):
        logging.info("onPublish:%s,%s,%s" % (client,userdata,mid))
    
    def onSubscribe(self, client, userdata, mid, granted_qos):
        logging.info("onSubscribe: %s,%s,%s,%s" % (client,userdata,mid,granted_qos))
    
    def publishMessage(self, resource:ResourceNameEnum, msg, qos: int = IPubSubClient.DEFAULT_QOS):
        logging.info("publishMesage is called,topic:"+str(resource)+",msg:"+str(msg))
        # check qos
        if qos<0 or qos>2:
            qos=IPubSubClient.DEFAULT_QOS
        # client publish
        msgInfo = self.mc.publish(str(resource), msg, qos)
        msgInfo.wait_for_publish()
    
    def subscribeToTopic(self, resource:ResourceNameEnum, qos: int = IPubSubClient.DEFAULT_QOS):
        logging.info("subscribeToTopic is called")
        # check qos
        if qos<0 or qos>2:
            qos=IPubSubClient.DEFAULT_QOS
        # client subscribe
        self.mc.subscribe(str(resource), qos)
        
    def subscribeToTopic(self, resource:str, qos: int = IPubSubClient.DEFAULT_QOS):
        logging.info("subscribeToTopic is called:"+resource)
        # check qos
        if qos<0 or qos>2:
            qos=IPubSubClient.DEFAULT_QOS
        # client subscribe
        self.mc.subscribe(resource, qos)

    def unsubscribeFromTopic(self, resource:ResourceNameEnum):
        logging.info("unsubscribeToTopic is called")
        # client unsubscribe
        self.mc.unsubscribe(str(resource))

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        logging.info("setDataMessageListener is called")
        if listener:
            self.dataMsgListener = listener
            return True
        return False

    def onActuatorCommandMessage(self, client, userdata, msg):
        logging.info('[Callback] Actuator command message received. Topic: %s.', msg.topic)
        logging.info(msg.payload)
        if self.dataMsgListener:
            try:
                actuatorData = DataUtil().jsonToActuatorData(msg.payload)
                self.dataMsgListener.handleActuatorCommandMessage(actuatorData)
            except:
                logging.exception("Failed to convert incoming actuation command payload to ActuatorData: ")