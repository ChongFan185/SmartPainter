#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import sys

#from src.main.python.programmingtheiot.common import ConfigConst

sys.path.insert(0, '../../../')
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask
import programmingtheiot.common.ConfigConst as ConfigConst


class SensorAdapterManager(object):
    """
    Shell representation of class for student implementation.
    
    """

    def __init__(self, useEmulator: bool = False, pollRate: int = 5, allowConfigOverride: bool = True):
        self.useEmulator = useEmulator
        self.pollRate = pollRate
        self.allowConfigOverride = allowConfigOverride
        self.dataMsgListener = IDataMessageListener()
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate)
        # whether use Emulator
        if self.useEmulator is True:
            logging.info("Use Emulator")
            # load the Humidity emulator
            humidityModule = __import__('programmingtheiot.cda.emulated.HumiditySensorEmulatorTask',
                                        fromlist=['HumiditySensorEmulatorTask'])
            heClazz = getattr(humidityModule, 'HumiditySensorEmulatorTask')
            self.humidityEmulator = heClazz()
            # load the Pressure emulator
            pressureModule = __import__('programmingtheiot.cda.emulated.PressureSensorEmulatorTask',
                                        fromlist=['PressureSensorEmulatorTask'])
            heClazz = getattr(pressureModule, 'PressureSensorEmulatorTask')
            self.pressureEmulator = heClazz()
            # load the Temp emulator
            tempModule = __import__('programmingtheiot.cda.emulated.TemperatureSensorEmulatorTask',
                                        fromlist=['TemperatureSensorEmulatorTask'])
            heClazz = getattr(tempModule, 'TemperatureSensorEmulatorTask')
            self.tempEmulator = heClazz()
        else:
            logging.info("Use Simulator")
            self.dataGenerator = SensorDataGenerator()
            configUtil = ConfigUtil()
            #define data range
            humidityFloor = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HUMIDITY_SIM_FLOOR_KEY,
                                                SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY)
            humidityCeiling = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HUMIDITY_SIM_CEILING_KEY,
                                                  SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
            pressureFloor = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.PRESSURE_SIM_FLOOR_KEY,
                                                SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
            pressureCeiling = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.PRESSURE_SIM_CEILING_KEY,
                                                  SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)
            tempFloor = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEMP_SIM_FLOOR_KEY,
                                            SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
            tempCeiling = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEMP_SIM_CEILING_KEY,
                                              SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
            #generate dataset
            self.humidityData = self.dataGenerator.generateDailyEnvironmentHumidityDataSet(minValue=humidityFloor,
                                                                                           maxValue=humidityCeiling,
                                                                                           useSeconds=False)
            self.pressureData = self.dataGenerator.generateDailyEnvironmentPressureDataSet(minValue=pressureFloor,
                                                                                           maxValue=pressureCeiling,
                                                                                           useSeconds=False)
            self.tempData = self.dataGenerator.generateDailyIndoorTemperatureDataSet(minValue=tempFloor,
                                                                                     maxValue=tempCeiling,
                                                                                     useSeconds=False)
            #create task with data
            self.htask = HumiditySensorSimTask(dataSet=self.humidityData)
            self.ptask = PressureSensorSimTask(dataSet=self.pressureData)
            self.ttask = TemperatureSensorSimTask(dataSet=self.tempData)

    def handleTelemetry(self):
        if self.useEmulator is False:
            #use simulator
            self.dataMsgListener.handleSensorMessage(self.htask.generateTelemetry())
            logging.info("Simulated humidity data: name=%s, timeStamp=%s, curValue=%f", self.htask.sensorData.getName(),
                         self.htask.sensorData.getTimeStamp(),self.htask.sensorData.getValue())
            self.dataMsgListener.handleSensorMessage(self.ptask.generateTelemetry())
            logging.info("Simulated pressure data: name=%s, timeStamp=%s, curValue=%f", self.ptask.sensorData.getName(),
                         self.ptask.sensorData.getTimeStamp(), self.ptask.sensorData.getValue())
            self.dataMsgListener.handleSensorMessage(self.ttask.generateTelemetry())
            logging.info("Simulated temp data: name=%s, timeStamp=%s, curValue=%f", self.ttask.sensorData.getName(),
                         self.ttask.sensorData.getTimeStamp(), self.ttask.sensorData.getValue())
        else:
            #use emulator
            data = self.humidityEmulator.generateTelemetry()
            self.dataMsgListener.handleSensorMessage(data)
            logging.info("Emulator humidity data: name=%s, timeStamp=%s, curValue=%f", data.getName(),
                         data.getTimeStamp(), data.getValue())
            data = self.pressureEmulator.generateTelemetry()
            self.dataMsgListener.handleSensorMessage(data)
            logging.info("Emulator pressure data: name=%s, timeStamp=%s, curValue=%f", data.getName(),
                         data.getTimeStamp(), data.getValue())
            data = self.tempEmulator.generateTelemetry()
            self.dataMsgListener.handleSensorMessage(data)
            logging.info("Emulator temp data: name=%s, timeStamp=%s, curValue=%f", data.getName(),
                         data.getTimeStamp(), data.getValue())

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener is not None:
            self.dataMsgListener = listener

    def startManager(self):
        self.scheduler.start()

    def stopManager(self):
        self.scheduler.shutdown()
