import datetime
from enum import Enum

from data import *

class SYNC_RESULT(int, Enum):
    FAIL = -1
    SUCCESS = 0
    SYNC = 1

def pack_result(result: SYNC_RESULT, sync_time:str, tab_list:list) -> dict:
    return {"result":result,"sync_time":sync_time,"tab_list":tab_list}

def get_data() -> dict:
    server_data = get_todo_data()
    return pack_result(SYNC_RESULT.SUCCESS, server_data.get_sync_time(), server_data.get_tab_list())

def put_data(client_data) -> dict:
    server_data = get_todo_data()
    # 更新到客户端的数据, 同时更新时间点
    new_sync_time = server_data.update_tab_list(client_data["tab_list"])
    return pack_result(SYNC_RESULT.SUCCESS, server_data.get_sync_time(), [])