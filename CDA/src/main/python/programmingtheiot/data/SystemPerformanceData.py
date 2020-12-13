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
from programmingtheiot.data.BaseIotData import BaseIotData
import programmingtheiot.common.ConfigConst as ConfigConst

class SystemPerformanceData(BaseIotData):
    """
	Shell representation of class for student implementation.
	
	"""
    DEFAULT_VAL = 0.0

    def __init__(self, d=None):
        super(SystemPerformanceData, self).__init__(name = ConfigConst.SYS_PERF_DATA, d=d)
        if d:
            self.cpu = d['cpuUtil']
            self.disk = d['diskUtil']
            self.memory = d['memUtil']
        else:
            self.cpu = self.DEFAULT_VAL
            self.disk = self.DEFAULT_VAL
            self.memory = self.DEFAULT_VAL

    def getCpuUtilization(self):
        # cpu getter
        return self.cpu

    def getDiskUtilization(self):
        # disk getter
        return self.disk

    def getMemoryUtilization(self):
        # memory getter
        return self.memory

    def setCpuUtilization(self, cpuUtil):
        # cpu setter
        self.cpu = cpuUtil

    def setDiskUtilization(self, diskUtil):
        # disk setter
        self.disk = diskUtil

    def setMemoryUtilization(self, memUtil):
        # memory setter
        self.memory = memUtil

    def _handleUpdateData(self, data):
        # updata data to this
        self.cpu = data.cpu
        self.disk = data.disk
        self.memory = data.memory
