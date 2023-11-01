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

identification ={'username': 'alice',
            'password': 'wonderland'}

output = '''
    ============================
        Get test
    ============================

    request done at "/"

    expected result = {status_code_attendu}
    actual restult = {status_code}

    ==>  {test_status}

    '''


r = requests.post(
        url='http://{address}:{port}/token'.format(address=api_address, port=api_port),
        headers=headers,data= identification
    )
bear = r.json()['access_token']

headers2 = {
    'accept': 'application/json',
    'Authorization': f"Bearer {bear}",
}

response = requests.get('http://{address}:{port}/'.format(address=api_address, port=api_port), 
                        headers=headers2)

# statut de la requête
status_code = response.status_code

# affichage des résultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'

with open('work/log.txt', 'a') as file: 
    file.write(output.format(status_code=status_code, test_status=test_status,
                        status_code_attendu=200))

##false token
headers3 = {
    'accept': 'application/json',
    'Authorization': "Bearer false",
}

response = requests.get('http://{address}:{port}/'.format(address=api_address, port=api_port), 
                        headers=headers3)

# statut de la requête
status_code = response.status_code

# affichage des résultats
if status_code == 401:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'

with open('work/log.txt', 'a') as file: 
    file.write(output.format(status_code=status_code, test_status=test_status,
                        status_code_attendu=401))