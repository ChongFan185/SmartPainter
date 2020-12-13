import sys
sys.path.insert(0, '../../../../../../main/python')
import logging
import unittest
from programmingtheiot.cda.embedded.HumidityI2cSensorAdapterTask import HumidityI2cSensorAdapterTask
from programmingtheiot.cda.embedded.PressureI2cSensorAdapterTask import PressureI2cSensorAdapterTask
from programmingtheiot.cda.embedded.TemperatureI2cSensorAdapterTask import TemperatureI2cSensorAdapterTask

class EmbeddedSensorAdapterTest(unittest.TestCase):
    def test_i2c_sensor(self):
        humiI2c = HumidityI2cSensorAdapterTask()
        presI2c = PressureI2cSensorAdapterTask()
        tempI2c = TemperatureI2cSensorAdapterTask()
        logging.info("hum: %d", humiI2c.generateTelemetry().getValue())
        logging.info("hum: %d", presI2c.generateTelemetry().getValue())
        logging.info("hum: %d", tempI2c.generateTelemetry().getValue())

if __name__ == '__main__':
    unittest.main()
