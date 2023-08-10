#!/usr/bin/python3
from models.base_model import BaseModel
import json
import os


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        self.__objects[obj.__class__.__name__ + '.' + str(obj)] = obj

    def save(self):
        print("=====================")
        print(self.__file_path)
        with open(self.__file_path, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        from ..base_model import BaseModel
        file_path = self.__file_path
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                objdict = json.load(f)
                for k, v in objdict.values():
                    c_name = k.split('.')[1]
                    if c_name == 'BaseModel':
                        inst = BaseModel(**v)
                        self.__objects[k] = inst
