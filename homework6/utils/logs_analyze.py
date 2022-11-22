import collections


class LogAnalyzer:
    HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

    def __init__(self, logs_file):
        self.logs_file = logs_file
        self.logs_list = self.get_logs_list(logs_file=logs_file)
        self.first_read = 1

    def get_logs_list(self, logs_file=None):
        logs_list = []
        with open(logs_file, 'r') as logs:
            for log in logs:
                logs_list.append(log.split())

        return logs_list

    def get_total_requests(self):
        return len(self.logs_list)

    def get_total_requests_by_method(self):
        log_requests = []
        for i in range(len(self.logs_list)):
            log_requests.append(self.logs_list[i][5])
        total_requests_by_method = dict(collections.Counter(log_requests))
        clear_list = []

        for request in total_requests_by_method:
            if request[1:] in self.HTTP_METHODS:
                clear_list.append((request[1:], total_requests_by_method[request]))

        return clear_list

    def get_top_requests(self, quantity=None):
        if quantity is None:
            quantity = 10

        full_req = []
        for i in range(len(self.logs_list)):
            if self.logs_list[i][10] == '"-"':
                full_req.append(self.logs_list[i][5][1:] + ' ' + self.logs_list[i][6])
            else:
                full_req.append(self.logs_list[i][5][1:] + ' ' + self.logs_list[i][10].replace('"', '')[:-1] +
                                self.logs_list[i][6])
        req_cnt = dict(collections.Counter(full_req))
        req_cnt_tuple = sorted([(v, k) for k, v in req_cnt.items()])[-quantity:]
        req_revers = req_cnt_tuple[::-1]

        return req_revers

    def get_biggest_req_by_size(self, quantity=None):
        if quantity is None:
            quantity = 5

        error_400 = []
        for i in range(len(self.logs_list)):
            if int(self.logs_list[i][8]) in range(400, 500):
                error_400.append(self.logs_list[i])

        error_400_reduced = []
        for i in range(len(error_400)):
            error_400_reduced.append((error_400[i][0], error_400[i][5], error_400[i][6].replace('%', ''),
                                      error_400[i][10], error_400[i][8], int(error_400[i][9])))

        sorted_400 = sorted(error_400_reduced, key=lambda error_400_reduced: error_400_reduced[-1])[-quantity:]
        reverse_400 = sorted_400[::-1]

        return reverse_400

    def get_most_often_ip_500(self, quantity=None):
        if quantity is None:
            quantity = 5

        error_500_ips = []
        for i in range(len(self.logs_list)):
            if int(self.logs_list[i][8]) in range(500, 600):
                error_500_ips.append(self.logs_list[i][0])

        count_ips = dict(collections.Counter(error_500_ips))
        count_ips_tuple = sorted([(v, k) for k, v in count_ips.items()])[-quantity:]
        count_ips_reverse = count_ips_tuple[::-1]

        return count_ips_reverse
