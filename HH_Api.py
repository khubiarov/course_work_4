import requests
import json

sj_token = 'v3.r.137530181.b1f12ca1e0c7b4943c11c72d08c500e0e4864152.e3587859ac72dd5bf6e192e4b5cb9199ce2292bf'
auth_data = {'X-Api-App-Id': sj_token}

req = requests.get('https://api.superjob.ru/2.20/vacancies/?keyword="программист"/', headers=auth_data)

req = req.json()
req = json.dumps(req, ensure_ascii=False)
req = json.loads(req)
for item in req['objects']:
    print(item['profession'])



#with open("sj_log.txt",'wt',encoding='utf-8')as file:
 #   file.write(req)