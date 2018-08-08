import requests
import time
import os, sys
from dotenv import load_dotenv
from datetime import datetime, timedelta

session_keys = ['area', 'deny', 'dwell_time', 'local', 'revisit_count', 'revisit_period', 'row_key',
                'ts', 'wifi_id']

def csv_dump_sessions(email, token, shop_id, target_date):
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'x-user-email': email,
    'x-user-token': token
  }

  input_datetime = datetime.fromisoformat(target_date)
  start_datetime = f'{target_date} 23:59:59'
  end_timestamp = datetime(input_datetime.year, input_datetime.month, input_datetime.day).timestamp() * 1000

  start_rts = requests.get(f'https://api.walkinsights.com/api/v1/shops/{shop_id}/rts/{start_datetime}',
                          headers=headers, params={ 'user_email': email, 'user_token': token }) \
                      .json()['rts']

  since = f'{start_rts}:out'

  spent_time = 0
  total_spent_time = 0
  finished = False
  number_of_requests = 0

  with open(f"{shop_id}_{input_datetime.strftime('%Y%m%d')}.csv", 'w') as f:
    f.write(','.join(session_keys) + '\n')
    while not finished:
      start_time = time.time()
      response_json = requests.get(f'https://dropwizard.walkinsights.com/api/v1/shops/{shop_id}/wifi_sessions',
                                  headers=headers,
                                  params={
                                    'user_email': email,
                                    'user_token': token,
                                    'since': since,
                                    'limit': 200
                                  }) \
                              .json()

      spent_time += time.time() - start_time
      total_spent_time += spent_time
      number_of_requests += 1
      print(f'--- {spent_time}\tseconds spent for {number_of_requests}th api call ---')
      print(f'--- {total_spent_time}\tseconds spent for requests sent so far ---')
      spent_time = 0

      if not response_json['sessions']:
        break

      csv_lines = []
      for session in response_json['sessions']:
        csv_lines.append(','.join([str(x[1]) for x in sorted(list(session.items()))]))

      f.write('\n'.join(csv_lines) + '\n')
      if int(response_json['sessions'][-1]['ts']) < end_timestamp:
        break
      since = response_json['since']


  print(f'--- {total_spent_time} seconds in total {number_of_requests} api calls ---')
  print(f'average response time: {total_spent_time / number_of_requests}')

if __name__ == "__main__":
  load_dotenv()
  csv_dump_sessions(os.getenv('X_USER_EMAIL'), os.getenv('X_USER_TOKEN'), sys.argv[1], sys.argv[2])
