from models.biggest_requests_by_size import BiggestReqBase
from models.req_by_method import ReqByMethodBase
from models.top_ips_500 import TopIpsBase
from models.top_ten_requests import TopTenReqBase
from models.total_req import TotalReqBase

TABLES_BASE = {
    'total_req': TotalReqBase,
    'req_by_method': ReqByMethodBase,
    'top_ten_requests': TopTenReqBase,
    'biggest_req': BiggestReqBase,
    'top_ips_500': TopIpsBase
}
