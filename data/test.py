from pprint import pprint

import requests

# # Расписание всех аудиторий
# g = requests.get('http://localhost:8080/api/audiences_week',
#                  json={'date': '2023-04-23'}).json()
# pprint(g)

# # Расписание конкретной аудитории
g = requests.get('http://localhost:8080/api/audiences_week/1',
                 json={'date': '2023-04-23'}).json()
pprint(g)