# from configparser import ConfigParser
import configparser
import os
from threading import local
from pypylon import pylon
import pypylon
import datetime
import sys



day_config = "camera_config_day.ini"
night_config = "camera_config_night.ini"





#get current day/night
def get_time_period():
    config = configparser.ConfigParser()
    curr_time = datetime.datetime.now().time()
    if curr_time >= datetime.time(19, 0) or curr_time < datetime.time(7, 0):    #start night-1700, end night 0700
        daily_status = "night"
        if os.path.isfile(day_config):
            try:
                config.read(day_config)
                print(f"Setting is {daily_status}")
            except Exception as e:
                print(e)
                sys.exit()
    else:
        daily_status = "day"
        if os.path.isfile(night_config):
            try:
                config.read(night_config)
                print(f"Setting is {daily_status}")
            # except configparser.Error as e:
            except Exception as e:
                print(e)
                sys.exit()
    return daily_status, config




#get value
def get_config_value():

    daily_status, config = get_time_period()

    #-------------------------------------------------
    #ImageFormatControl
    Width                   = config.get("ImageFormatControl", "Width")
    Height                  = config.get("ImageFormatControl", "Height")
    OffsetX                 = config.get("ImageFormatControl", "OffsetX")
    OffsetY                 = config.get("ImageFormatControl", "OffsetY")
    CenterX                 = config.get("ImageFormatControl", "CenterX")
    CenterY                 = config.get("ImageFormatControl", "CenterY")
    BinningHorizontalMode   = config.get("ImageFormatControl", "BinningHorizontalMode")
    BinningHorizontal       = config.get("ImageFormatControl", "BinningHorizontal")
    BinningVerticalMode     = config.get("ImageFormatControl", "BinningHorizontalMode")
    BinningVertical         = config.get("ImageFormatControl", "BinningHorizontal")
    PixelFormat             = config.get("ImageFormatControl", "PixelFormat")
    ReverseX                = config.get("ImageFormatControl", "ReverseX")
    ReverseY                = config.get("ImageFormatControl", "ReverseY")
    TestImageSelector       = config.get("ImageFormatControl", "TestImageSelector")

    #-------------------------------------------------
    #AnalogControl
    GainAuto                = config.get("AnalogControl", "GainAuto")
    GainSelector            = config.get("AnalogControl", "GainSelector")
    Gain                    = config.get("AnalogControl", "Gain")
    BlackLevel              = config.get("AnalogControl", "BlackLevel")
    BlackLevelSelector      = config.get("AnalogControl", "BlackLevelSelector")
    Gamma                   = config.get("AnalogControl", "Gamma")
    DigitalShift            = config.get("AnalogControl", "DigitalShift")

    #-------------------------------------------------
    #ImageQualityControl
    PgiMode                 = config.get("ImageQualityControl", "PgiMode")

    #-------------------------------------------------
    #AcquisitionControl
    ShutterMode             = config.get("AcquisitionControl", "ShutterMode")
    ExposureAuto            = config.get("AcquisitionControl", "ExposureAuto")
    ExposureTimeMode        = config.get("AcquisitionControl", "ExposureTimeMode")
    ExposureMode            = config.get("AcquisitionControl", "ExposureMode")
    ExposureTime            = config.get("AcquisitionControl", "ExposureTime")
    AcquisitionBurstFrameCount=config.get("AcquisitionControl", "AcquisitionBurstFrameCount")
    TriggerSelector         = config.get("AcquisitionControl", "TriggerSelector")
    TriggerMode             = config.get("AcquisitionControl", "TriggerMode")
    TriggerSource           = config.get("AcquisitionControl", "TriggerSource")
    TriggerActivation       = config.get("AcquisitionControl", "TriggerActivation")
    TriggerDelay            = config.get("AcquisitionControl", "TriggerDelay")
    AcquisitionFrameRateEnable=config.get("AcquisitionControl", "AcquisitionFrameRateEnable")
    AcquisitionFrameRate    = config.get("AcquisitionControl", "AcquisitionFrameRate")
    AcquisitionStatusSelector=config.get("AcquisitionControl", "AcquisitionStatusSelector")

    #-------------------------------------------------
    #AutoFunctionControl
    AutoTargetBrightness    = config.get("AutoFunctionControl", "AutoTargetBrightness")
    AutoFunctionProfile     = config.get("AutoFunctionControl", "AutoFunctionProfile")
    AutoGainLowerLimit      = config.get("AutoFunctionControl", "AutoGainLowerLimit")
    AutoGainUpperLimit      = config.get("AutoFunctionControl", "AutoGainUpperLimit")
    AutoExposureTimeLowerLimit=config.get("AutoFunctionControl", "AutoExposureTimeLowerLimit")
    AutoExposureTimeUpperLimit=config.get("AutoFunctionControl", "AutoExposureTimeUpperLimit")
    AutoFunctionROISelector = config.get("AutoFunctionControl", "AutoFunctionROISelector")
    AutoFunctionROIWidth    = config.get("AutoFunctionControl", "AutoFunctionROIWidth")
    AutoFunctionROIHeight   = config.get("AutoFunctionControl", "AutoFunctionROIHeight")
    AutoFunctionROIOffsetX  = config.get("AutoFunctionControl", "AutoFunctionROIOffsetX")
    AutoFunctionROIOffsetY  = config.get("AutoFunctionControl", "AutoFunctionROIOffsetY")
    AutoFunctionROIUseBrightness=config.get("AutoFunctionControl", "AutoFunctionROIUseBrightness")
    AutoFunctionROIUseWhiteBalance=config.get("AutoFunctionControl", "AutoFunctionROIUseWhiteBalance")

    #-------------------------------------------------
    #LUTControl
    LUTSelector             = config.get("LUTControl", "LUTSelector")
    LUTEnable               = config.get("LUTControl", "LUTEnable")

    #-------------------------------------------------
    #DigitalIOControl
    LineSelector            = config.get("DigitalIOControl", "LineSelector")
    LineMode                = config.get("DigitalIOControl", "LineMode")
    LineInverter            = config.get("DigitalIOControl", "LineInverter")
    LineDebouncerTime       = config.get("DigitalIOControl", "LineDebouncerTime")
    UserOutputValueAll      = config.get("DigitalIOControl", "UserOutputValueAll")

    #-------------------------------------------------
    #CounterAndTimerControl
    TimerSelector           = config.get("CounterAndTimerControl", "TimerSelector")
    TimerDuration           = config.get("CounterAndTimerControl", "TimerDuration")
    TimerDelay              = config.get("CounterAndTimerControl", "TimerDelay")
    TimerTriggerSource      = config.get("CounterAndTimerControl", "TimerTriggerSource")
    CounterSelector         = config.get("CounterAndTimerControl", "CounterSelector")
    CounterEventSource      = config.get("CounterAndTimerControl", "CounterEventSource")
    CounterResetSource      = config.get("CounterAndTimerControl", "CounterResetSource")

    #-------------------------------------------------
    #ChunkDataControl
    ChunkSelector           = config.get("ChunkDataControl", "ChunkSelector")
    ChunkEnable             = config.get("ChunkDataControl", "ChunkEnable")

    #-------------------------------------------------
    #EventControl
    EventSelector           = config.get("EventControl", "EventSelector")
    EventNotification       = config.get("EventControl", "EventNotification")

    #-------------------------------------------------
    #LensControl
    LensConnection          = config.get("LensControl", "LensConnection")
    MotorCompensateMode     = config.get("LensControl", "MotorCompensateMode")
    FocusAuto               = config.get("LensControl", "FocusAuto")
    FocusAutoReset          = config.get("LensControl", "FocusAutoReset")
    FocusStepper            = config.get("LensControl", "FocusStepper")
    FocusStepperLowerLimit  = config.get("LensControl", "FocusStepperLowerLimit")
    FocusStepperLowerLimit  = config.get("LensControl", "FocusStepperLowerLimit")
    FocusPosition           = config.get("LensControl", "FocusPosition")
    FocusPosition           = config.get("LensControl", "FocusPosition")
    ZoomPosition            = config.get("LensControl", "ZoomPosition")
    BslFocusXOffset         = config.get("LensControl", "BslFocusXOffset")
    BslFocusYOffset         = config.get("LensControl", "BslFocusYOffset")

    
    

    return locals()


def setConfig(camera):

    config_value = get_config_value()

    try:
        #-------------------------------------------------
        #ImageFormatControl
        # print(type(int(config_value["OffsetX"])), int(config_value["OffsetX"]))
        camera.Height.SetValue(int(config_value["Height"]))
        camera.Width.SetValue(int(config_value["Width"]))
        if int(config_value["CenterX"]) == 0:
            camera.OffsetX.SetValue(int(config_value["OffsetX"]))
        if int(config_value["CenterY"]) == 0:
            camera.OffsetY.SetValue(int(config_value["OffsetY"]))
        camera.BinningHorizontalMode.SetValue(str(config_value["BinningHorizontalMode"]))
        camera.BinningHorizontal.SetValue(int(config_value["BinningHorizontal"]))
        camera.BinningVerticalMode.SetValue(str(config_value["BinningVerticalMode"]))
        camera.BinningVertical.SetValue(int(config_value["BinningVertical"]))
        camera.ReverseX.SetValue(bool(config_value["ReverseX"]))
        camera.ReverseY.SetValue(bool(config_value["ReverseY"]))
        if str(config_value["PixelFormat"])=="Mono8":
            camera.PixelFormat.SetValue(str("Mono8"))
        #-------------------------------------------------
        #AutoFunctionControl
        # camera.AutoTargetBrightness.SetValue(float(config_value["AutoTargetBrightness"]))
        # # camera.AutoFunctionProfile.SetValue(config_value["AutoFunctionProfile"])
        # camera.AutoGainLowerLimit.SetValue(float(config_value["AutoGainLowerLimit"]))
        # camera.AutoGainUpperLimit.SetValue(float(config_value["AutoGainUpperLimit"]))
        # camera.AutoExposureTimeLowerLimit.SetValue(float(config_value["AutoExposureTimeLowerLimit"]))
        # camera.AutoExposureTimeUpperLimit.SetValue(float(config_value["AutoExposureTimeUpperLimit"]))
        # # camera.AutoFunctionROISelector.SetValue(config_value["AutoFunctionROISelector"])
        # camera.AutoFunctionROIWidth.SetValue(int(config_value["AutoFunctionROIWidth"]))
        # camera.AutoFunctionROIHeight.SetValue(int(config_value["AutoFunctionROIHeight"]))
        # camera.AutoFunctionROIOffsetX.SetValue(int(config_value["AutoFunctionROIOffsetX"]))
        # camera.AutoFunctionROIOffsetY.SetValue(int(config_value["AutoFunctionROIOffsetY"]))
        # camera.AutoFunctionROIUseBrightness.SetValue(config_value["AutoFunctionROIUseBrightness"])
        # camera.AutoFunctionROIUseWhiteBalance.SetValue(config_value["AutoFunctionROIUseWhiteBalance"])
    

        # #-------------------------------------------------
        # #AnalogControl
        camera.GainAuto.SetValue(str(config_value["GainAuto"]))
        camera.GainSelector.SetValue(str(config_value["GainSelector"]))
        # camera.Gain.SetValue(float(config_value["Gain"]))
        camera.BlackLevelSelector.SetValue(str(config_value["BlackLevelSelector"]))
        camera.BlackLevel.SetValue(float(config_value["BlackLevel"]))
        camera.Gamma.SetValue(float(config_value["Gamma"]))
        camera.DigitalShift.SetValue(int(config_value["DigitalShift"]))

        #-------------------------------------------------
        #ImageQualityControl
        camera.PgiMode.SetValue(str(config_value["PgiMode"]))
        
        # #-------------------------------------------------
        # #AcquisitionControl
        camera.ShutterMode.SetValue(str(config_value["ShutterMode"]))
        camera.ExposureAuto.SetValue(str(config_value["ExposureAuto"]))
        camera.ExposureTimeMode.SetValue(str(config_value["ExposureTimeMode"]))
        camera.ExposureMode.SetValue(str(config_value["ExposureMode"]))
        camera.ExposureTime.SetValue(float(config_value["ExposureTime"]))
        camera.AcquisitionBurstFrameCount.SetValue(int(config_value["AcquisitionBurstFrameCount"]))
        camera.TriggerSelector.SetValue(str(config_value["TriggerSelector"]))
        camera.TriggerMode.SetValue(str(config_value["TriggerMode"]))
        camera.TriggerSource.SetValue(str(config_value["TriggerSource"]))
        camera.TriggerActivation.SetValue(str(config_value["TriggerActivation"]))
        camera.TriggerDelay.SetValue(float(config_value["TriggerDelay"]))
        camera.AcquisitionFrameRateEnable.SetValue(bool(config_value["AcquisitionFrameRateEnable"]))
        camera.AcquisitionFrameRate.SetValue(float(config_value["AcquisitionFrameRate"]))
        camera.AcquisitionStatusSelector.SetValue(str(config_value["AcquisitionStatusSelector"]))

        # #LUTControl
        # camera.LUTSelector.SetValue(config_value["LUTSelector"])
        # camera.LUTEnable.SetValue(config_value["LUTEnable"])

        # #DigitalIOControl
        # camera.LineSelector.SetValue(config_value["LineSelector"])
        # camera.LineMode.SetValue(config_value["LineMode"])
        # camera.LineInverter.SetValue(config_value["LineInverter"])
        # camera.LineDebouncerTime.SetValue(float(config_value["LineDebouncerTime"]))
        # camera.UserOutputValueAll.SetValue(config_value["UserOutputValueAll"])

        # #-------------------------------------------------
        # #CounterAndTimerControl
        # camera.TimerSelector.SetValue(config_value["TimerSelector"])
        # camera.TimerDuration.SetValue(float(config_value["TimerDuration"]))
        # camera.TimerDelay.SetValue(float(config_value["TimerDelay"]))
        # camera.TimerTriggerSource.SetValue(config_value["TimerTriggerSource"])
        # camera.CounterSelector.SetValue(config_value["CounterSelector"])
        # camera.CounterEventSource.SetValue(config_value["CounterEventSource"])
        # camera.CounterResetSource.SetValue(config_value["CounterResetSource"])

        # #-------------------------------------------------
        # #ChunkDataControl
        # camera.ChunkSelector.SetValue(config_value["ChunkSelector"])
        # camera.ChunkEnable.SetValue(config_value["ChunkEnable"])

        # #-------------------------------------------------
        # #EventControl
        # camera.EventSelector.SetValue(config_value["EventSelector"])
        # camera.EventNotification.SetValue(config_value["EventNotification"])

        # #-------------------------------------------------
        # #LensControl
        if str(camera.LensConnection.GetValue()).lower == "connect" :
                camera.MotorCompensateMode.SetValue(str(config_value["MotorCompensateMode"]))
                camera.FocusAuto.SetValue(str(config_value["FocusAuto"]))
                # camera.FocusAutoReset.SetValue(config_value["FocusAutoReset"])
                camera.FocusStepper.SetValue(str(config_value["FocusStepper"]))                         #AutoFocusSearchPoint
                camera.FocusStepperLowerLimit.SetValue(int(config_value["FocusStepperLowerLimit"]))   #AutoFocusSearchPointLowerLimit
                camera.FocusStepperUpperLimit.SetValue(int(config_value["FocusStepperLowerLimit"]))   #AutoFocusSearchPointUpperLimit
                camera.FocusPosition.SetValue(int(config_value["FocusPosition"]))
                camera.ZoomPosition.SetValue(int(config_value["ZoomPosition"]))
                camera.BslFocusXOffset.SetValue(int(config_value["BslFocusXOffset"]))       #FocusXPosition
                camera.BslFocusYOffset.SetValue(int(config_value["BslFocusYOffset"]))     #FocusYPosition
    
    except Exception as e:
        print("error", e)

    return camera