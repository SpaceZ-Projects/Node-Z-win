
from subprocess import Popen, PIPE
from shutil import which
import os
import math
import random
import time
import sys

__version__ = '1.4.1'

class GPU:
    def __init__(self, ID, uuid, load, memoryTotal, memoryUsed, memoryFree, driver, gpu_name, serial, display_mode, display_active, temp_gpu, fan_speed):
        self.id = ID
        self.uuid = uuid
        self.load = load
        self.memoryUtil = float(memoryUsed)/float(memoryTotal)
        self.memoryTotal = memoryTotal
        self.memoryUsed = memoryUsed
        self.memoryFree = memoryFree
        self.driver = driver
        self.name = gpu_name
        self.serial = serial
        self.display_mode = display_mode
        self.display_active = display_active
        self.temperature = temp_gpu
        self.fan_speed = fan_speed

def safeFloatCast(strNumber):
    try:
        number = float(strNumber)
    except ValueError:
        number = float('nan')
    return number

def getGPUs():
    nvidia_smi = which('nvidia-smi')
    if nvidia_smi is None:
        nvidia_smi = "%s\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe" % os.environ['systemdrive']
    try:
        p = Popen([nvidia_smi,"--query-gpu=index,uuid,utilization.gpu,memory.total,memory.used,memory.free,driver_version,name,gpu_serial,display_active,display_mode,temperature.gpu,fan.speed", "--format=csv,noheader,nounits"], stdout=PIPE)
        stdout, stderror = p.communicate()
    except:
        return []
    output = stdout.decode('UTF-8')
    lines = output.split(os.linesep)
    numDevices = len(lines)-1
    GPUs = []
    for g in range(numDevices):
        line = lines[g]
        vals = line.split(', ')
        for i in range(13):
            if i == 0:
                deviceIds = int(vals[i])
            elif i == 1:
                uuid = vals[i]
            elif i == 2:
                gpuUtil = safeFloatCast(vals[i]) / 100
            elif i == 3:
                memTotal = safeFloatCast(vals[i])
            elif i == 4:
                memUsed = safeFloatCast(vals[i])
            elif i == 5:
                memFree = safeFloatCast(vals[i])
            elif i == 6:
                driver = vals[i]
            elif i == 7:
                gpu_name = vals[i]
            elif i == 8:
                serial = vals[i]
            elif i == 9:
                display_active = vals[i]
            elif i == 10:
                display_mode = vals[i]
            elif i == 11:
                temp_gpu = safeFloatCast(vals[i])
            elif i == 12:
                fan_speed = safeFloatCast(vals[i])
        GPUs.append(GPU(deviceIds, uuid, gpuUtil, memTotal, memUsed, memFree, driver, gpu_name, serial, display_mode, display_active, temp_gpu, fan_speed))
    return GPUs


def getAvailable(order = 'first', limit=1, maxLoad=0.5, maxMemory=0.5, memoryFree=0, includeNan=False, excludeID=[], excludeUUID=[]):
    GPUs = getGPUs()
    GPUavailability = getAvailability(GPUs, maxLoad=maxLoad, maxMemory=maxMemory, memoryFree=memoryFree, includeNan=includeNan, excludeID=excludeID, excludeUUID=excludeUUID)
    availAbleGPUindex = [idx for idx in range(0,len(GPUavailability)) if (GPUavailability[idx] == 1)]
    GPUs = [GPUs[g] for g in availAbleGPUindex]

    if (order == 'first'):
        GPUs.sort(key=lambda x: float('inf') if math.isnan(x.id) else x.id, reverse=False)
    elif (order == 'last'):
        GPUs.sort(key=lambda x: float('-inf') if math.isnan(x.id) else x.id, reverse=True)
    elif (order == 'random'):
        GPUs = [GPUs[g] for g in random.sample(range(0,len(GPUs)),len(GPUs))]
    elif (order == 'load'):
        GPUs.sort(key=lambda x: float('inf') if math.isnan(x.load) else x.load, reverse=False)
    elif (order == 'memory'):
        GPUs.sort(key=lambda x: float('inf') if math.isnan(x.memoryUtil) else x.memoryUtil, reverse=False)

    GPUs = GPUs[0:min(limit, len(GPUs))]
    deviceIds = [gpu.id for gpu in GPUs]

    return deviceIds

def getAvailability(GPUs, maxLoad=0.5, maxMemory=0.5, memoryFree=0, includeNan=False, excludeID=[], excludeUUID=[]):
    GPUavailability = [1 if (gpu.memoryFree>=memoryFree) and (gpu.load < maxLoad or (includeNan and math.isnan(gpu.load))) and (gpu.memoryUtil < maxMemory  or (includeNan and math.isnan(gpu.memoryUtil))) and ((gpu.id not in excludeID) and (gpu.uuid not in excludeUUID)) else 0 for gpu in GPUs]
    return GPUavailability

def getFirstAvailable(order = 'first', maxLoad=0.5, maxMemory=0.5, attempts=1, interval=900, verbose=False, includeNan=False, excludeID=[], excludeUUID=[]):
    
    for i in range(attempts):
        if (verbose):
            print('Attempting (' + str(i+1) + '/' + str(attempts) + ') to locate available GPU.')
        available = getAvailable(order=order, limit=1, maxLoad=maxLoad, maxMemory=maxMemory, includeNan=includeNan, excludeID=excludeID, excludeUUID=excludeUUID)
        if (available):
            if (verbose):
                print('GPU ' + str(available) + ' located!')
            break
        if (i != attempts-1):
            time.sleep(interval)
    if (not(available)):
        raise RuntimeError('Could not find an available GPU after ' + str(attempts) + ' attempts with ' + str(interval) + ' seconds interval.')

    return available


def showUtilization(all=True, attrList=None, useOldCode=False):
    GPUs = getGPUs()
    if all:
        if useOldCode:
            print(' ID | Name | Serial | UUID || GPU util. | Memory util. | Fan speed || Memory total | Memory used | Memory free || Display mode | Display active |')
            print('------------------------------------------------------------------------------------------------------------------------------')
            for gpu in GPUs:
                print(' {0:2d} | {1:s}  | {2:s} | {3:s} || {4:3.0f}% | {5:3.0f}% | {6:3.0f}% || {7:.0f}MB | {8:.0f}MB | {9:.0f}MB || {10:s} | {11:s}'.format(gpu.id, gpu.name, gpu.serial, gpu.uuid, gpu.load * 100, gpu.memoryUtil * 100, gpu.fan_speed, gpu.memoryTotal, gpu.memoryUsed, gpu.memoryFree, gpu.display_mode, gpu.display_active))
        else:
            attrList = [
                [{'attr': 'id', 'name': 'ID'},
                 {'attr': 'name', 'name': 'Name'},
                 {'attr': 'serial', 'name': 'Serial'},
                 {'attr': 'uuid', 'name': 'UUID'}],
                [{'attr': 'temperature', 'name': 'GPU temp.', 'suffix': 'C', 'transform': lambda x: x, 'precision': 0},
                 {'attr': 'load', 'name': 'GPU util.', 'suffix': '%', 'transform': lambda x: x * 100, 'precision': 0},
                 {'attr': 'fan_speed', 'name': 'Fan speed', 'suffix': '%', 'transform': lambda x: x, 'precision': 0},
                 {'attr': 'memoryUtil', 'name': 'Memory util.', 'suffix': '%', 'transform': lambda x: x * 100, 'precision': 0}],
                [{'attr': 'memoryTotal', 'name': 'Memory total', 'suffix': 'MB', 'precision': 0},
                 {'attr': 'memoryUsed', 'name': 'Memory used', 'suffix': 'MB', 'precision': 0},
                 {'attr': 'memoryFree', 'name': 'Memory free', 'suffix': 'MB', 'precision': 0}],
                [{'attr': 'display_mode', 'name': 'Display mode'},
                 {'attr': 'display_active', 'name': 'Display active'}]
            ]

    else:
        if useOldCode:
            print(' ID  GPU  MEM  FAN')
            print('-------------------')
            for gpu in GPUs:
                print(' {0:2d} {1:3.0f}% {2:3.0f}% {3:3.0f}%'.format(gpu.id, gpu.load * 100, gpu.memoryUtil * 100, gpu.fan_speed))
        else:
            attrList = [
                [{'attr': 'id', 'name': 'ID'},
                 {'attr': 'load', 'name': 'GPU', 'suffix': '%', 'transform': lambda x: x * 100, 'precision': 0},
                 {'attr': 'fan_speed', 'name': 'FAN', 'suffix': '%', 'transform': lambda x: x, 'precision': 0},
                 {'attr': 'memoryUtil', 'name': 'MEM', 'suffix': '%', 'transform': lambda x: x * 100, 'precision': 0}],
            ]

    if not useOldCode:
        if attrList is not None:
            headerString = ''
            GPUstrings = [''] * len(GPUs)
            for attrGroup in attrList:
                for attrDict in attrGroup:
                    headerString = headerString + '| ' + attrDict['name'] + ' '
                    headerWidth = len(attrDict['name'])
                    minWidth = len(attrDict['name'])

                    attrPrecision = '.' + str(attrDict['precision']) if 'precision' in attrDict.keys() else ''
                    attrSuffix = str(attrDict['suffix']) if 'suffix' in attrDict.keys() else ''
                    attrTransform = attrDict['transform'] if 'transform' in attrDict.keys() else lambda x: x
                    for gpu in GPUs:
                        attr = getattr(gpu, attrDict['attr'])

                        attr = attrTransform(attr)

                        if isinstance(attr, float):
                            attrStr = ('{0:' + attrPrecision + 'f}').format(attr)
                        elif isinstance(attr, int):
                            attrStr = ('{0:d}').format(attr)
                        elif isinstance(attr, str):
                            attrStr = attr
                        elif sys.version_info[0] == 2:
                            if isinstance(attr, unicode):
                                attrStr = attr.encode('ascii', 'ignore')
                        else:
                            raise TypeError(
                                'Unhandled object type (' + str(type(attr)) + ') for attribute \'' + attrDict[
                                    'name'] + '\'')

                        attrStr += attrSuffix

                        minWidth = max(minWidth, len(attrStr))

                    headerString += ' ' * max(0, minWidth - headerWidth)

                    minWidthStr = str(minWidth - len(attrSuffix))

                    for gpuIdx, gpu in enumerate(GPUs):
                        attr = getattr(gpu, attrDict['attr'])

                        attr = attrTransform(attr)

                        if isinstance(attr, float):
                            attrStr = ('{0:' + minWidthStr + attrPrecision + 'f}').format(attr)
                        elif isinstance(attr, int):
                            attrStr = ('{0:' + minWidthStr + 'd}').format(attr)
                        elif isinstance(attr, str):
                            attrStr = ('{0:' + minWidthStr + 's}').format(attr)
                        elif sys.version_info[0] == 2:
                            if isinstance(attr, unicode):
                                attrStr = ('{0:' + minWidthStr + 's}').format(attr.encode('ascii', 'ignore'))
                        else:
                            raise TypeError(
                                'Unhandled object type (' + str(type(attr)) + ') for attribute \'' + attrDict[
                                    'name'] + '\'')

                        attrStr += attrSuffix

                        GPUstrings[gpuIdx] += '| ' + attrStr + ' '

                headerString = headerString + '|'
                for gpuIdx, gpu in enumerate(GPUs):
                    GPUstrings[gpuIdx] += '|'

            headerSpacingString = '-' * len(headerString)
            print(headerString)
            print(headerSpacingString)
            for GPUstring in GPUstrings:
                print(GPUstring)