import collections

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

logs_list = []
with open('access.log', 'r') as logs:
    for log in logs:
        logs_list.append(log.split())

print('Общее кол-во запрсоов - ', len(logs_list))

log_requests = []
for i in range(len(logs_list)):
    log_requests.append(logs_list[i][5])
cnt = dict(collections.Counter(log_requests))
print('\n Общее кол-во запросов по типу:')
for req in cnt:
    if req[1:] in HTTP_METHODS:
        print(req[1:], cnt[req])

full_req = []
for i in range(len(logs_list)):
    if logs_list[i][10] == '"-"':
        full_req.append(logs_list[i][5][1:]+' '+logs_list[i][6])
    else:
        full_req.append(logs_list[i][5][1:]+' '+logs_list[i][10].replace('"', '')[:-1]+logs_list[i][6])
req_cnt = dict(collections.Counter(full_req))
req_cnt_tuple = sorted([(v, k) for k, v in req_cnt.items()])[-10:]
req_revers = req_cnt_tuple[::-1]
print('\n Топ 10 запросов:')
for i in range(len(req_revers)):
    re = req_revers[i][1].split()[1]
    print(f'{re} - {req_revers[i][0]} запросов')

error_400 = []
for i in range(len(logs_list)):
    if int(logs_list[i][8]) in range(400, 500):
        error_400.append(logs_list[i])
error_400_reduced = []
for i in range(len(error_400)):
    error_400_reduced.append((error_400[i][0], error_400[i][5], error_400[i][6],
                             error_400[i][10], error_400[i][8], int(error_400[i][9])))
sorted_400 = sorted(error_400_reduced, key=lambda error_400_reduced: error_400_reduced[-1])[-5:]
reverse_400 = sorted_400[::-1]
print('\n Топ-5 самых больших по размеру запросов с клиентской ошибкой:')
for i in range(len(sorted_400)):
    print(f'Запрос {reverse_400[i][2]}, size= {reverse_400[i][5]}, code= {reverse_400[i][4]}, ip= {reverse_400[i][0]}')
