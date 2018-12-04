# coding=utf-8


'''
配置config.yaml执行
'''

import re,os,time,shutil
import logger
import MonkeyParamters
from report import *
from jenkinsApiTest import jenkinsApi

CRASH = 'CRASH'
crash = 'crash'
IOSMonkeyLog = 'IOSMonkeyLog'
CrashLog = 'CrashLog'
crashLogPath='Retired'
base_dir = os.path.dirname(__file__)
ipadir = os.path.join(base_dir)+'/TestIPA'
def file_name(file_dir):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.ipa':
                L.append(os.path.join(root, file))
    return L


def parseLog(monkeydir,files):
    '''
    根据log文件地址,写入到error文件中
    :param logcatpath: log文件地址
    :param wirteerrorpath: 写入error的文件地址
    :return:0表示有错误日志,1表示没有错误日志
    '''
    crashnum = 0
    emCrash = ErrorMsg(CRASH, crashnum, '')
    curtime = time.strftime("%Y-%m-%d", time.localtime())
    crashloglist = os.listdir(base_dir + '/' + CrashLog)
    if 'Retired' in files:
        crashfiles = os.listdir(base_dir+'/'+IOSMonkeyLog+'/'+crashLogPath)
        for crfile in crashfiles:
            if(re.findall('TruckManager-%s' % curtime, crfile)):
                crashnum += 1
                emCrash.error_count = crashnum
                emCrash.error_desc = emCrash.error_desc + "发现CRASH,请参考日志" + '<br>'
                logger.log_info("发现CRASH日志,CRASH错误数:%s" % crashnum)
                shutil.copyfile(base_dir+'/'+IOSMonkeyLog+'/'+crashLogPath+'/'+crfile,base_dir+'/'+CrashLog+'/'+crfile)
                crashloglist.append(base_dir+'/'+CrashLog+'/'+crfile)
        return 0, emCrash,crashloglist
    else:
        emCrash.error_count = crashnum
        emCrash.error_desc = emCrash.error_desc + "未发现CRASH" + '<br>'
        logger.log_info("没有发现CRASH日志")
        return 1,emCrash,crashloglist

def send_report(monkeydir):
    files = os.listdir(monkeydir)
    ja = jenkinsApi()
    lastSuccessfulBuildNum = ja.getlastSuccessfulBuildNum()
    apk_href = MonkeyParamters.jenkins_server_url + "/job/" + MonkeyParamters.job_name + "/" + str(lastSuccessfulBuildNum)
    ipaname = ''.join(file_name(ipadir)).split('/')[-1]
    result = parseLog(monkeydir,files)
    if result[0] == 0:
        emCrash = result[1]
        crashloglist = result[2]
        model = MonkeyParamters.devicename
        system_version = MonkeyParamters.system_version
        error_list = [emCrash]
        log_list = crashloglist
        runtime = '02:00:00'
        monkeycmd="xcodebuild -project XCTestWD.xcodeproj -scheme XCTestWDUITests -destination 'platform=iOS,name=iPhone6 Plus' XCTESTWD_PORT=8001 clean test"
        # 获取monkeylog所有日志send_mail(devices,monkeylog, writeerror,str(difftime),monkeycmd)
        code, msg = send_monkey_report(ipaname, apk_href,runtime, model, system_version, error_list, monkeycmd, log_list)
        if code == 0:
            logger.log_info(msg)

    else:
        emCrash = result[1]
        crashloglist = result[2]
        model = MonkeyParamters.devicename
        system_version = MonkeyParamters.system_version
        error_list = [emCrash]
        log_list = crashloglist
        runtime='02:00:00'
        monkeycmd = "xcodebuild -project XCTestWD.xcodeproj -scheme XCTestWDUITests -destination 'platform=iOS,name=iPhone6 Plus' XCTESTWD_PORT=8001 clean test"
        # 获取monkeylog所有日志send_mail(devices,monkeylog, writeerror,str(difftime),monkeycmd)
        code, msg = send_monkey_report(ipaname, apk_href, runtime,model, system_version, error_list, monkeycmd, log_list)
        if code == -1:
            logger.log_error(msg)



if __name__ == '__main__':

    monkeydir = '/Users/truckmanager_test/Documents/Monkey_IOS_CI/ReportServer/IOSMonkeyLog'
    files = os.listdir(monkeydir)
    result = parseLog(monkeydir,files)
    print result[0],result[2]
    #writeerror='/Users/lifucai/TruckManager 2017-7-18 下午5-58.error'
    #result = parseLog(monkeydir,files)
    #print result[0],result[2]
    #send_report(monkeydir)






