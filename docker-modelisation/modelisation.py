import os
import requests
from time import sleep

sleep(5)
api_address='my_api_container'
# port de l'API
api_port = 8000
# test API

def StatusCode(status_code,status_attendu):
    if status_code == status_attendu:
        return 'SUCCESS'
    else:
        return 'FAILURE'


headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

identification ={'username': 'alice',
            'password': 'wonderland'}


r = requests.post(
        url='http://{address}:{port}/token'.format(address=api_address, port=api_port),
        headers=headers,data= identification
    )
bear = r.json()['access_token']

headers2 = {
    'accept': 'application/json',
    'Authorization': f"Bearer {bear}",
}


output = '''
    ============================
        modelisation test
    ============================
        request done at "/modelisation"

    parameters tested : {params}
    parameters changed : {param}
    expected result = {status_code_attendu}
    actual restult = {status_code}

    ==>  {test_status}

    '''
params = {
    'Model': 'Randomforest',
    'SeniorCitizen': 0,
    'Partner': 'yes',
    'Dependents': 'yes',
    'tenure': 50,
    'PhoneService': 'yes',
    'OnlineSecurity': 'yes',
    'OnlineBackup': 'yes',
    'DeviceProtection': 'yes',
    'TechSupport': 'yes',
    'PaperlessBilling': 'yes',
    'MonthlyCharges': 50,
    'PaymentMethod': 'bank transfer (automatic)',
    'Contract': 'month-to-month',
    'InternetService': 'dsl',
    'MultipleLines': 'yes',
    }

test_true = {
    'Model': ['Randomforest','DecisionTreeClassifier'],
    'SeniorCitizen': [1],
    'Partner': ['no'],
    'Dependents': ['no'],
    'tenure': [],
    'PhoneService': ['no'],
    'OnlineSecurity': ['no'],
    'OnlineBackup': ['no'],
    'DeviceProtection': ['no'],
    'TechSupport': ['no'],
    'PaperlessBilling': ['no'],
    'MonthlyCharges': [],
    'PaymentMethod': ["credit card (automatic)","electronic check","mailed check"],
    'Contract': ["one year","two year"],
    'InternetService': ["fiber optic","no"],
    'MultipleLines': ['no',"no phone service"],
    }

for param in params:
    liste_test= test_true[param]
    if len(liste_test)>0:
        for test in liste_test:
            param_test=params.copy()
            param_test[param]=test
            resp = requests.post('http://{address}:{port}/modelisation'.format(address=api_address, port=api_port), 
                        headers=headers2,params=param_test)
            status_code=resp.status_code
            test_status = StatusCode(status_code,200)
            with open('work/log.txt', 'a') as file: 
                file.write(output.format(status_code=status_code, test_status=test_status,
                                status_code_attendu=200,
                              params=param_test,param=param))
    param_test=params.copy()
    param_test[param]="test"
    resp = requests.post('http://{address}:{port}/modelisation'.format(address=api_address, port=api_port), 
                headers=headers2,params=param_test)
    status_code=resp.status_code
    test_status = StatusCode(status_code,422)
    with open('work/log.txt', 'a') as file: 
        file.write(output.format(status_code=status_code, test_status=test_status,
                            status_code_attendu=422,
                            params=param_test,param=param))

param_test=params.copy()
param_test["SeniorCitizen"]=2
resp = requests.post('http://{address}:{port}/modelisation'.format(address=api_address, port=api_port), 
                headers=headers2,params=param_test)
status_code=resp.status_code
test_status = StatusCode(status_code,422)
with open('work/log.txt', 'a') as file: 
    file.write(output.format(status_code=status_code, test_status=test_status,
                        status_code_attendu=422,
                        params=param_test,param="SeniorCitizen"))

##false token
headers3 = {
    'accept': 'application/json',
    'Authorization': "Bearer false",
}
resp = requests.post('http://{address}:{port}/modelisation'.format(address=api_address, port=api_port), 
                headers=headers3,params=params)
status_code=resp.status_code
test_status = StatusCode(status_code,401)
with open('work/log.txt', 'a') as file: 
    file.write(output.format(status_code=status_code, test_status=test_status,
                        status_code_attendu=401,
                        params=params,param="token"))