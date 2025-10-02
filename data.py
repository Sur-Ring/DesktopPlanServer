import json
import datetime

class Server_Meta_Data:
    pwd: str
    sync_time: datetime.datetime
    def __init__(self, pwd:str="默认密码", sync_time:str="无时间"):
        self.pwd = pwd
        try:
            self.sync_time = datetime.datetime.strptime(sync_time, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            print(f"时间解析失败: {e}")
            self.sync_time = datetime.datetime.now()

    @classmethod
    def from_dict(cls, data:dict):
        """从字典创建实例"""
        return cls(
            pwd=data.get("pwd", "默认密码"),
            sync_time=data.get("sync_time", "无时间")
        )

    def to_dict(self):
        """转换为字典"""
        return {
            "pwd": self.pwd,
            "sync_time": self.sync_time.strftime("%Y-%m-%d %H:%M:%S")
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
    todo_tab_list: list[Server_Todo_Tab_Data]
    def __init__(self, todo_tab_list:list[Server_Todo_Tab_Data]=None):
        if todo_tab_list is not None:
            self.todo_tab_list = todo_tab_list
        else:
            self.todo_tab_list = []

    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建实例"""
        tab_list = [Server_Todo_Tab_Data.from_dict(tab_data)
                    for tab_data in data.get("todo_tab_list", [])]
        return cls(todo_tab_list=tab_list)

    def to_dict(self):
        """转换为字典"""
        return {
            "todo_tab_list": [tab.to_dict() for tab in self.todo_tab_list]
        }

def save_todo_data(file_path:str, data:Server_Todo_Data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data.to_dict(), file, ensure_ascii=False, indent=2)
        print(f"数据已保存到 {file_path}")
    except Exception as e:
        print(f"保存文件时出错: {e}")

def load_todo_data(file_path:str) -> Server_Todo_Data:
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

def save_meta_data(file_path:str, data:Server_Meta_Data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data.to_dict(), file, ensure_ascii=False, indent=2)
        print(f"数据已保存到 {file_path}")
    except Exception as e:
        print(f"保存文件时出错: {e}")

def load_meta_data(file_path:str) -> Server_Meta_Data:
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