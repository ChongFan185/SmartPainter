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
import programmingtheiot.common.ConfigConst as ConfigConst
from apscheduler.schedulers.background import BackgroundScheduler

from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask


class SystemPerformanceManager(object):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self, pollRate: int = 30):
        ## create instance of SystemCpuUtilTask,SystemMemUtilTask,BackgroundScheduler and set the pollRate
        self.cpuUtilTask = SystemCpuUtilTask()
        self.memUtilTask = SystemMemUtilTask()
        self.scheduler = BackgroundScheduler()
        self.pollRate = pollRate

    def handleTelemetry(self):
        ## get system utilization
        self.cpuUtilPct = self.cpuUtilTask.getTelemetryValue()
        self.memUtilPct = self.memUtilTask.getTelemetryValue()
        logging.info('CPU utilization is %s percent, and memory utilization is %s percent.', str(self.cpuUtilPct),
                     str(self.memUtilPct))

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        pass

    def startManager(self):
        logging.info("Started SystemPerformanceManager.")
        ##start scheduler
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate)
        self.scheduler.start()
        pass

    def stopManager(self):
        logging.info("Stopped SystemPerformanceManager.")
        self.scheduler.shutdown()
        pass