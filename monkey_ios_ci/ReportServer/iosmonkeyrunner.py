# -*- coding: UTF8 -*-

import os,logger
import time
import MonkeyParamters
import subprocess
from parseLogAndReport import *

base_dir = os.path.dirname(__file__)
ipadir = os.path.join(base_dir)+'/TestIPA'
descpath = os.path.join(base_dir)+'/IOSMonkeyLog'
def file_name(file_dir):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.ipa':
                L.append(os.path.join(root, file))
    return L
ipa_path = ''.join(file_name(ipadir))


def install(path,udid):
    cmd = 'ios-deploy –r -b ' + '"' + ipa_path + '"' + ' -i ' + udid
    logger.log_info("安装ipa命令：%s" % cmd)
    try:
        os.system(cmd)
    except Exception as msg:
        logger.log_error(msg)
        raise

def monkey(devicename):
    cmd_monkey = "xcodebuild -project /Users/truckmanager_test/Documents/iosMonkey/Fastmonkey-xcode9.2/XCTestWD-master/XCTestWD/XCTestWD.xcodeproj " \
                 "-scheme XCTestWDUITests " \
                 "-destination 'platform=iOS,name=" + devicename + "' " + \
                 "XCTESTWD_PORT=8001 " + \
                 "clean test"

    logger.log_info("monkey命令：%s" % cmd_monkey)
    try:
        os.system(cmd_monkey)
    except Exception as msg:
        logger.log_error(msg)
        raise

def get_log(descpath,udid):
    cmd_log = "idevicecrashreport -e -u %s %s" % (udid, descpath)
    logger.log_info("拷贝log命令：%s" % cmd_log)
    try:
        os.system(cmd_log)
    except Exception as msg:
        logger.log_error(msg)
        raise

if __name__ == '__main__':
    logger.log_info("install ipa....")
    install(ipa_path, MonkeyParamters.udid)
    logger.log_info("开始Monkey测试....")
    monkey(MonkeyParamters.devicename)
    logger.log_info("获取log文件...")
    get_log(descpath,MonkeyParamters.udid)
    logger.log_info("统计和发送测试报告...")
    send_report(descpath)
