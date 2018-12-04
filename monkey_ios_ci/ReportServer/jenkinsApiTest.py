# -*- coding:UTF-8 -*-
import jenkins
from MonkeyParamters import *
class jenkinsApi():

    def getlastSuccessfulBuildNum(self):

        user_id='xxxx'
        api_token='xxxx'
        server=jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)
        #print server.get_job_info(self.job_name)
        lastSuccessfulBuildNum = server.get_job_info(job_name)['lastSuccessfulBuild']['number']
        #print lastSuccessfulBuildNum
        return lastSuccessfulBuildNum


if __name__ == '__main__':
    ja =jenkinsApi()
    lastSuccessfulBuildNum = ja.getlastSuccessfulBuildNum()
    apk_href = jenkins_server_url + "/job/" + job_name + "/" + str(lastSuccessfulBuildNum)
    print apk_href