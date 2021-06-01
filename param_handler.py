from abc import ABCMeta, abstractmethod
import os.path
import pickle
import json


class ParamHandler(metaclass=ABCMeta):
    def __init__(self, source): # принимает адрес конфиг-файла
        self.source = source 
        self.params = {} # словарь ключей и значений для конфига

    def add_param(self, key, value):  #добавляет новую опцию, или затирает существующую, указанным значением
        self.params[key] = value
    
    def get_param(self, key):  #возвращает значение опции с указанным именем
        return self.params.get(key)
    
    def get_all_params(self):  #возвращает значения всех опций
        return self.params

    def remove_param(self, key):  #удаляет значение опции с указанным именем
        self.params.pop(key)

    def remove_all_params(self):  #удаляет значения всех опций (очистка)
        self.params.clear()
    
    @abstractmethod
    def read(self):  #абстрактный метод, выполняет чтение данных из файла в конкретном формате.
        pass
    
    @abstractmethod
    def write(self):  #абстрактный метод, выполняет запись данных в файл в конкретном формате.
        pass


class ParamHandlerException(Exception):
    pass

class ParamHandlerFactory(object):
    # types = {'json': JsonParamHandler, 'pickle': 'PickleParamHandler'} #cловаврь куда будет класться {typeconfig: NameParamhandler}
    types = {}


    @classmethod
    def add_type(cls, name, klass):
        if not name:
            raise ParamHandlerException('Type must have a name.')
 
        if not issubclass(klass, ParamHandler):
            raise ParamHandlerException(f'Class "{klass}" is not ParamHandler.')
        cls.types[name] = klass

    @classmethod
    def create(cls, source):
        # Шаблон "Simple Factory"
        _, ext = os.path.splitext(str(source).lower())
        ext = ext.lstrip('.')
        klass = cls.types.get(ext)
        if klass is None:
            raise ParamHandlerException(f'Type "{ext}" not found.')
        return klass(source)



class JsonParamHandler(ParamHandler): 
    def __init__(self, source):
        self.source = source
        self.params = {}

    def read(self):
        """Чтение из json-файла и присвоение значений в self.params"""
        with open(self.source) as f:
            self.params = json.load(f)


 
    def write(self):
        """Запись в json-файл параметров self.params"""
        with open(self.source, 'w') as f:
            json.dump(self.params, f, indent=4)


class PickleParamHandler(ParamHandler):
    def __init__(self, source):
        self.source = source
        self.params = {}

    def read(self):
        """Чтение из pikle-файла и присвоение значений в self.params"""
        with open(self.source, 'rb') as f:
            self.params = pickle.load(f)
            
    def write(self):
        """Запись в pikle-файл параметров self.params""" 
        with open(self.source, 'wb') as f:
            pickle.dump(self.params, f)        



ParamHandlerFactory.add_type('json', JsonParamHandler)
ParamHandlerFactory.add_type('pickle', PickleParamHandler)
# config = ParamHandlerFactory.create('data_file.pickle')
# config.add_param('key1', 'val1')
# config.add_param('key2', 'val2')
# config.add_param('key4', 'val3')
# config.write() 
# print(config.read())
