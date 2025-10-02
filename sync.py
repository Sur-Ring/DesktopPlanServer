import datetime

from data import *

def update_sync_time(meta_data:Server_Meta_Data=None):
    if meta_data is None:
        meta_data = load_meta_data("data/meta.json")
    meta_data.sync_time = datetime.datetime.now()
    return meta_data.sync_time.strftime("%Y-%m-%d %H:%M:%S")

def sync_data(data):
    # 尝试更新服务器数据
    # 如果客户端是最新数据, 那么通知客户端
    # 如果客户端是旧数据, 返回服务器数据
    # 如果两侧失去同步, 那么返回客户端数据
    sync_stat = -1  # 负数. 为错误保留; 0. 无需同步; 1. 更新到服务器; 2. 拉取服务器数据; 3. 失去同步
    if type(data) is not dict:
        return {"sync_stat": -1, "error_msg": "错误的数据格式"}

    if "sync_time" not in data:
        return {"sync_stat": -1, "error_msg": "错误的数据格式"}

    if "edit_time" not in data:
        return {"sync_stat": -1, "error_msg": "错误的数据格式"}

    try:
        client_sync_time = datetime.datetime.strptime(data["sync_time"], "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        print(f"同步时间解析错误: {e}")
        return {"sync_stat": -1, "error_msg": "同步时间解析错误"}

    try:
        client_edit_time = datetime.datetime.strptime(data["edit_time"], "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        print(f"编辑时间解析错误: {e}")
        return {"sync_stat": -1, "error_msg": "编辑时间解析错误"}

    meta_data = load_meta_data("data/meta.json")
    if meta_data.sync_time == client_sync_time: # 如果同步时间一致，那么说明没有被其他客户端修改过
        if client_edit_time >= client_sync_time: # 如果修改时间在其后，说明在本机修改过，需要更新服务器
            # 更新服务器数据
            client_todo_data = Server_Todo_Data.from_dict(data["todo_data"])
            save_todo_data("data/data.json", client_todo_data)
            new_sync_time = update_sync_time(meta_data)
            return {"sync_stat": 1, "sync_time":new_sync_time}
        else: # 如果修改时间一致，说明本机没修改过，无需同步
            return {"sync_stat": 0}
    elif meta_data.sync_time >= client_sync_time: # 如果服务端的同步时间更靠后，说明被其他客户端修改过
        if client_edit_time == client_sync_time: # 如果本机的修改时间和同步时间一致，说明本机没有修改过，因此拉取服务端的修改
            # 拉取服务器数据
            server_todo_data = load_todo_data("data/data.json")
            return {"sync_stat": 2, "sync_time":meta_data.sync_time.strftime("%Y-%m-%d %H:%M:%S"), "server_data": server_todo_data.to_dict()}
        elif client_edit_time >= client_sync_time: # 如果本机的修改时间在同步时间之后，说明本机也修改过，需要处理冲突
            # 处理冲突
            server_todo_data = load_todo_data("data/data.json")
            return {"sync_stat": 3, "server_data": server_todo_data.to_dict()}
        else: # 如果本机的修改时间在同步时间之前，这没有意义，我计划在同步时更新修改时间，如果仍然出现该情况，那么是UB
            return {"sync_stat": 0}
    else: # 如果服务端的同步时间更靠前，那么本机可能与其他服务器同步过，这是UB
        return {"sync_stat": 0}

def set_data(data):
    client_todo_data = Server_Todo_Data.from_dict(data["todo_data"])
    save_todo_data("data/data.json", client_todo_data)
    new_sync_time = update_sync_time()
    return {"sync_time":new_sync_time}