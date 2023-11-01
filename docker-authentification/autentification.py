import os
import requests
from time import sleep

sleep(5)
api_address='my_api_container'
# port de l'API
api_port = 8000
# test API

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

test={
    1 : {"status_code_attendu":200,
         "params": {
        'username': 'alice',
        'password': 'wonderland'}
        },
    2 :{"status_code_attendu":200,
         "params": {
        'username': 'bob',
        'password': 'builder'}
       },
    3:{"status_code_attendu":200,
         "params": {
        'username': 'clementine',
        'password': 'mandarine'}              
        },
    4 :{"status_code_attendu":401,
         "params": {
        'username': 'clementine',
        'password': 'manda'}              
        }, 
    5:{"status_code_attendu":401,
         "params": {
        'username': 'pierre',
        'password': 'granite'}              
        }   
    }

output = '''
    ============================
        Authentication test
    ============================

    request done at "/permissions"
    | username="{username}"
    | password="{password}"

    expected result = {status_code_attendu}
    actual restult = {status_code}

    ==>  {test_status}

    '''

for i in test:



    r = requests.post(
        url='http://{address}:{port}/token'.format(address=api_address, port=api_port),
        headers=headers,data= test[i]["params"]
    )
    


    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code == test[i]["status_code_attendu"]:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    with open('work/log.txt', 'a') as file: 
        file.write(output.format(status_code=status_code, test_status=test_status,
                            status_code_attendu=test[i]["status_code_attendu"],
                            username=test[i]["params"]["username"],password=test[i]["params"]["password"]))