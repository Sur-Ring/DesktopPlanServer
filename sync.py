import datetime
from enum import Enum

from data import *

class SYNC_RESULT(Enum):
    FAIL = -1
    SUCCESS = 0

def pack_result(result: SYNC_RESULT, sync_time:str, tab_list:list) -> dict:
    return {"result":result,"sync_time":sync_time,"tab_list":tab_list}

def pull_data() -> dict:
    server_data = get_todo_data()
    return pack_result(SYNC_RESULT.SUCCESS, server_data.get_sync_time(), server_data.get_tab_list())

def push_data(client_data) -> dict:
    server_data = get_todo_data()

    # 如果客户端不一致, 则返回新数据, 要求客户端保持同步, 其实也可以要求客户端自行pull
    if client_data["sync_time"] != server_data.get_sync_time():
        return pack_result(SYNC_RESULT.FAIL, server_data.get_sync_time(), server_data.get_tab_list())

    # 更新到客户端的数据, 同时更新时间点
    new_sync_time = server_data.update_tab_list(client_data["tab_list"])
    # 返回最近更新的时间点 由于使用客户端的数据, 因此无需返回
    return pack_result(SYNC_RESULT.SUCCESS, server_data.get_sync_time(), [])