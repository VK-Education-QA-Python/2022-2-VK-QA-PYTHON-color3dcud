from utils.logs_analyze import LogAnalyzer


class MysqlBuilder:
    log_file_name = 'access.log'

    def __init__(self, client, files_path):
        self.client = client
        self.file_name = files_path + self.log_file_name
        self.log_analyzer = LogAnalyzer(logs_file=self.file_name)

    def create_total_req(self):
        file_name = self.log_file_name
        total_req = self.log_analyzer.get_total_requests()
        self.client.execute_query(f'insert into `total_req` (`file_name`, `total_req`) values ("{file_name}", {total_req})')

    def create_req_by_method(self):
        req_by_method = self.log_analyzer.get_total_requests_by_method()

        for i in range(len(req_by_method)):
            method = req_by_method[i][0]
            count = req_by_method[i][1]
            self.client.execute_query(f'insert into `req_by_method` (`request_method`, `total_req`) values ("{method}", {count})')

    def create_top_ten_requests(self):
        top_requests = self.log_analyzer.get_top_requests()

        for i in range(len(top_requests)):
            req_url = top_requests[i][1]
            count = top_requests[i][0]
            self.client.execute_query(
                f'insert into `top_ten_requests` (`request_url`, `total_req`) values ("{req_url}", {count})')

    def create_biggest_req(self):
        biggest_req = self.log_analyzer.get_biggest_req_by_size()

        for i in range(len(biggest_req)):
            req_url = biggest_req[i][2]
            req_size = biggest_req[i][5]
            req_code = biggest_req[i][4]
            ip = biggest_req[i][0]
            self.client.execute_query(
                f'insert into `biggest_req` (`req_url`, `req_size`, `req_code`, `ip`) values ("{req_url}", {req_size}, {req_code}, "{ip}")')

    def create_top_ips_500(self):
        top_ips = self.log_analyzer.get_most_often_ip_500()

        for i in range(len(top_ips)):
            ip = top_ips[i][1]
            count = top_ips[i][0]
            self.client.execute_query(
                f'insert into `top_ips_500` (`ip`, `total_req`) values ("{ip}", {count})')
