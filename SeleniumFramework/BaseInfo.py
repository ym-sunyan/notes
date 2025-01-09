# -*- encoding: utf-8 -*-
#python:3.6
'''
@File    :   BaseInfo.py
@Time    :   2021/04/06 15:36:41
@Author  :   sunyan
@Version :   1.0
@email   :   c_yansun
@Desc    :   配置文件类
'''
# here put the import lib
import os
import sys
import configparser

class BaseInfo(object):
    '''基础配置文件'''
    def __init__(self):
        self.base_info_dict = {}
        self.ini_dict = {}
        self.Set()
        self.ReadBaseInfoIni()
        self.ChangeBaseInfo()

    def ReadBaseInfoIni(self):
        ini_path = "{}\\BaseInfo.ini".format(self.base_info_dict['base_path'])
        if not os.path.isfile(ini_path):
            return
        self.config = configparser.ConfigParser()
        self.config.read(ini_path, encoding="utf-8")
        if self.config.sections() == []:
            return
        for node in self.config.sections():
            ini_node_dict = {}
            if self.config.items(node) == []:
                continue
            for item in self.config.items(node):
                ini_node_dict["{}".format(item[0])] = item[1]
            self.ini_dict[node] = ini_node_dict
        print(self.ini_dict)
        
    def ChangeBaseInfo(self):
        if self.ini_dict == {}:
            return
        if "base_info_dict" not in self.ini_dict.keys():
            return
        for key, value in self.ini_dict["base_info_dict"].items():
            if value == "None":
                continue
            self.base_info_dict[key] = value
        pass

    def Set(self):
        # self.base_info_dict["base_path"] = os.path.dirname(sys.argv[0])
        self.base_info_dict["base_path"] = os.getcwd()
        if self.base_info_dict["base_path"] == "":
            self.base_info_dict["base_path"] = os.path.dirname(os.path.realpath(__file__))
        self.base_info_dict['base_url'] = 'https://copilot.microsoft.com/'
        self.base_info_dict['google_data_path'] = rf"{self.base_info_dict['base_path']}/user_data"
        self.base_info_dict["chromedriver_path"] = r'C:\tools\chromedriver\chromedriver.exe'
        self.base_info_dict['download_path'] = rf'{self.base_info_dict["base_path"]}\xlsx'

        self.base_info_dict["from_"] = f'{os.environ.get("USERNAME")}@qti.qualcomm.com'
        self.base_info_dict["to_"] = [f'{os.environ.get("USERNAME")}@qti.qualcomm.com']
        self.base_info_dict["cc_"]= [f'{os.environ.get("USERNAME")}@qti.qualcomm.com']
        
    