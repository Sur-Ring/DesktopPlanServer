import json
import datetime

class Server_Meta_Data:
    pwd: str
    http_port: int
    hello_port: int
    def __init__(self, pwd:str="默认密码", http_port:int=5000, hello_port:int=5001):
        self.pwd = pwd
        self.http_port = http_port
        self.hello_port = hello_port

    @classmethod
    def from_dict(cls, data:dict):
        """从字典创建实例"""
        return cls(
            pwd=data.get("pwd", "默认密码"),
            http_port=data.get("http_port", 5000),
            hello_port=data.get("hello_port", 5001),
        )

    def to_dict(self):
        """转换为字典"""
        return {
            "pwd": self.pwd,
            "http_port": self.http_port,
            "hello_port": self.hello_port,
        }

class Server_Todo_Entry_Data:
    name: str
    ddl: str
    def __init__(self, name:str="新条目", ddl:str=""):
        self.name = name
        self.ddl = ddl

    @classmethod
    def from_dict(cls, data:dict):
        """从字典创建实例"""
        return cls(
            name=data.get("name", "新条目"),
            ddl=data.get("ddl", "")
        )

    def to_dict(self):
        """转换为字典"""
        return {
            "name": self.name,
            "ddl": self.ddl
        }

class Server_Todo_Tab_Data:
    name: str
    todo_entry_list: list[Server_Todo_Entry_Data]
    def __init__(self, name:str="新条目", todo_entry_list:list[Server_Todo_Entry_Data]=None):
        self.name = name
        if todo_entry_list is not None:
            self.todo_entry_list = todo_entry_list
        else:
            self.todo_entry_list = []

    @classmethod
    def from_dict(cls, data:dict):
        """从字典创建实例"""
        entry_list = [Server_Todo_Entry_Data.from_dict(entry_data)
                      for entry_data in data.get("todo_entry_list", [])]
        return cls(
            name=data.get("name", "新条目"),
            todo_entry_list=entry_list
        )

    def to_dict(self):
        """转换为字典"""
        return {
            "name": self.name,
            "todo_entry_list": [entry.to_dict() for entry in self.todo_entry_list]
        }

class Server_Todo_Data:
    sync_time: datetime.datetime
    todo_tab_list: list[Server_Todo_Tab_Data]
    def __init__(self, sync_time:str="无时间", todo_tab_list:list[Server_Todo_Tab_Data]=None):
        try:
            self.sync_time = datetime.datetime.strptime(sync_time, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            print(f"时间解析失败: {e}")
            self.sync_time = datetime.datetime.now()

        if todo_tab_list is not None:
            self.todo_tab_list = todo_tab_list
        else:
            self.todo_tab_list = []

    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建实例"""
        tab_list = [Server_Todo_Tab_Data.from_dict(tab_data)
                    for tab_data in data.get("tab_list", [])]
        return cls(
            sync_time=data.get("sync_time", "无时间"),
            todo_tab_list=tab_list
        )

    def get_sync_time(self):
        return self.sync_time.strftime("%Y-%m-%d %H:%M:%S")
    def update_sync_time(self):
        print("更新时间")
        self.sync_time = datetime.datetime.now()
        self.save("./data/data.json")
        return self.get_sync_time()

    def get_tab_list(self):
        return [tab.to_dict() for tab in self.todo_tab_list]
    def update_tab_list(self, new_tab_list:list[dict]):
        print("更新列表")
        self.todo_tab_list = [Server_Todo_Tab_Data.from_dict(tab_data) for tab_data in new_tab_list]
        self.update_sync_time()

    def to_dict(self):
        """转换为字典"""
        return {
            "sync_time": self.sync_time.strftime("%Y-%m-%d %H:%M:%S"),
            "todo_tab_list": [tab.to_dict() for tab in self.todo_tab_list]
        }

    def save(self, file_path:str):
        print("保存数据")
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.to_dict(), file, ensure_ascii=False, indent=2)
            print(f"数据已保存到 {file_path}")
        except Exception as e:
            print(f"保存文件时出错: {e}")

def load_todo_data(file_path:str) -> Server_Todo_Data:
    print("加载数据")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        print("读取成功:", json_data)
        return Server_Todo_Data.from_dict(json_data)
    except FileNotFoundError:
        print("文件不存在")
    except json.JSONDecodeError:
        print("JSON格式错误")
    except Exception as e:
        print(f"读取文件时出错: {e}")
    return Server_Todo_Data()

def load_meta_data(file_path:str) -> Server_Meta_Data:
    print("加载元数据")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        print("读取成功:", json_data)
        return Server_Meta_Data.from_dict(json_data)
    except FileNotFoundError:
        print("文件不存在")
    except json.JSONDecodeError:
        print("JSON格式错误")
    except Exception as e:
        print(f"读取文件时出错: {e}")
    return Server_Meta_Data()

_meta_data = load_meta_data("data/meta.json")
_todo_data = load_todo_data("data/data.json")

def get_hello_port():
    return _meta_data.hello_port
def get_http_port():
    return _meta_data.http_port

def get_todo_data() -> Server_Todo_Data:
    return _todo_data
