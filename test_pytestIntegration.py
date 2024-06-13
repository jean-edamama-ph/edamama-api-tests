import requests
import pytest
import json
import urllib.parse
from datetime import datetime

def pytestIntegration(strSuite):
    strUrl = 'https://api.zephyrscale.smartbear.com/v2/automations/executions/junit?projectKey=AUTO&autoCreateTestCases=true'

    #strToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb250ZXh0Ijp7ImJhc2VVcmwiOiJodHRwczovL2VkYW1hbWEuYXRsYXNzaWFuLm5ldCIsInVzZXIiOnsiYWNjb3VudElkIjoiNjMyZDJmYjdmNTY4NjE1YmRjN2M5NDU2In19LCJpc3MiOiJjb20ua2Fub2FoLnRlc3QtbWFuYWdlciIsInN1YiI6ImZjZDgzNjk0LTllMzAtM2NiNy05MGRjLTQ5ZmFiNTRjN2M3MyIsImV4cCI6MTc0OTc4NTgxMCwiaWF0IjoxNzE4MjQ5ODEwfQ.SYe9jByPTCb-N5kKXd-PqKueNljaKjsFfeeCBBSBULg'
    strToken = 'Input your Zephyr Token'
    dictHeaders = {'Authorization': f'Bearer {strToken}'}

    strFilePath = 'reports/output/junitxml_report.xml'
    # file_path = 'reports/backup/output/junitxml_report.xml'
    dictFiles = {'file': open(strFilePath, 'rb')}
    
    strDate = datetime.today().strftime("%m-%d-%Y")
    strTitle = f'{strDate} {strSuite} Test Execution'
    dictValue = {"name": f"{strTitle}"}
    dictFormData = {'testCycle': dictValue}
    
    response = requests.post(strUrl, json=json.dumps(dictFormData), files = dictFiles, headers = dictHeaders)

    print(response.json())
    print(strTitle)
    assert response.status_code == 200


@pytest.mark.api_test()
def test_API_Test_Suite():    
    pytestIntegration('API SUITE')


