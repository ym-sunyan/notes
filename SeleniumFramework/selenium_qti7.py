'''
Author: c_yansun c_yansun@qti.qualcomm.com
Date: 2023-12-12 10:20:01
LastEditors: c_yansun c_yansun@qti.qualcomm.com
LastEditTime: 2024-08-05 09:27:39
FilePath: \SNPEV5\selenium_qti7.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# -*- encoding: utf-8 -*-
#python>=3.6
from csv import excel
import os
import re
import sys
import wget
import zipfile
import time
import codecs
import shutil
import getpass
import operator
import traceback
from time import sleep
try:
    from CopyChromeUserData import CopyUserData
except:
    print("CopyChromeUserData导入失败，无法copy新的userdata")
    exit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait       #WebDriverWait注意大小写
from selenium.webdriver.support import expected_conditions as EC

def current_stack(print_sign:bool=True):
    '''
    @Time    :   2024/07/10 16:38:59
    @功能    :   获取堆栈调用情况
    print_sign=True 输出error信息
    '''
    import inspect
    stack = inspect.stack()
    def FormatStackInformation(stack):
        '''
        @Time    :   2024/07/10 15:47:08
        @功能    :   格式化堆栈中每一个函数调用的信息
        # 将每一行的字段信息进行拆解，生成字典
        '''
        keys = ['frame','file', 'line', 'function_name', 'code_context', 'index']
        stack_list = []
        for obj in stack:
            frame_info_list = list(obj)
            frame_info_list[4] = frame_info_list[4][0]
            frame_dict = dict(zip(keys,frame_info_list))
            frame_dict['完整堆栈信息'] = str(obj)
            stack_list.append(frame_dict)

        stack_func_list = [] #堆栈调用函数顺序
        for obj in stack_list:
            if obj['function_name'] == '<module>':
                break
            stack_func_list.append(obj['function_name'])
        return stack_list, stack_func_list
    
    def Print():
        '''
        @Time    :   2024/07/10 17:12:33
        @功能    :   格式化输出
        '''
        error_info = '堆栈调用顺序:\n'
        for data_obj in stack_call_list[0]['current_stack']:
            if data_obj['function_name'] == '<module>': break
            func_name = f'''函数名称 : {data_obj['function_name']}'''.ljust(50)
            line = f'''调用函数所在行 : {data_obj['line']}'''.ljust(20)
            error_info += f"{line}{func_name} 函数所在文件 : {data_obj['file']}\n"
        if print_sign:
            print(error_info)
        return  error_info
        
    
    stack_call_list = [] #堆栈调用流程
    stack_func_list = [] #堆栈函数调用顺序
    stack_call_info = []
    for index, frame_info in enumerate(stack):
        frame = frame_info.frame
        args, _, _, value_list = inspect.getargvalues(frame)
        if frame_info.function == 'current_stack':
            stack_list, stack_func_list = FormatStackInformation(value_list['stack'])
            stack_call_list.append({frame_info.function:stack_list})
            stack_call_info.append(Print())
        else:
            stack_call_list.append({frame_info.function:str(value_list)})
    return stack_call_list, stack_func_list, '\n'.join(stack_call_info)

def DownloadFile(chrome_dirver_version,path_list):
    '''
    @Time    :   2023/02/22 10:14:08
    @功能    :   None
    '''
    url = f"https://registry.npmmirror.com/-/binary/chromedriver/{chrome_dirver_version}/chromedriver_win32.zip"
    path = "\\".join(path_list[:-2])
    try:
        wget.download(url, path)
        file = rf"{path}\chromedriver_win32.zip"
        f = zipfile.ZipFile(file,'r') # 压缩文件位置
        for f_handle in f.namelist():
            f.extract(f_handle,"\\".join(path_list[:-1]))               # 解压位置
        f.close()
        try:
            os.remove(file)
            print(f"del {file} finish....")
            return True
        except:
            print(f"del {file} failed...")
            return False
    except:
        print(url)
        return False

def AutoDownloadChromeDriver(chrome_dirver_version="100.0.4896.20",chrome_driver_path=None):
    '''
    @Time    :   2023/02/21 18:37:44
    @功能    :   None
    '''
    path_list = chrome_driver_path.split(os.path.sep)
    for i in range(500):
        chrome_dirver_version = ".".join(chrome_dirver_version.split(".")[:-1])+"."+str(i)
        url = f"https://registry.npmmirror.com/-/binary/chromedriver/{chrome_dirver_version}/chromedriver_win32.zip"
        path = "\\".join(path_list[:-2])
        try:
            wget.download(url, path)
            file = rf"{path}\chromedriver_win32.zip"
            f = zipfile.ZipFile(file,'r') # 压缩文件位置
            for f_handle in f.namelist():
                f.extract(f_handle,"\\".join(path_list[:-1]))               # 解压位置
            f.close()
            try:
                os.remove(file)
                print(f"del {file} finish....")
                return True
            except:
                print(f"del {file} failed...")
                return False
        except:
            print(url)
    return None        

def GetChromeVersion(error_info, base_version):
    '''
    @Time    :   2023/02/22 10:02:48
    @功能    :   None
    '''
    print(error_info)
    version_error_sign = "Current browser version is "
    if "selenium.common.exceptions.WebDriverException: Message: 'chromedriver.exe' executable needs" in error_info:
        # 没有chromedriver.exe 的情况
        # selenium.common.exceptions.WebDriverException: Message: 'chromedriver.exe' executable needs to be in PATH. Please see https://chromedriver.chromium.org/home
        # return "100.0.4896.20"
        return base_version
    elif version_error_sign in error_info:
        # # chromedriver.exe版本不对的情况
        # selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 103
        # Current browser version is 110.0.5481.104 with binary path C:\Program Files\Google\Chrome\Application\chrome.exe
        error_info_list = error_info.split("\n")
        for info in error_info_list:
            if info.strip().startswith(version_error_sign):
                print(info)
                return info.strip().replace(version_error_sign,"").split(" ")[0]
    else: 
        return None
    return None

class Chrome_cls(object):
    '''关闭所有浏览器（真实浏览器和虚拟浏览器）'''
    def __init__(self, find_list=None):
        self.kill_cmd = "taskkill /pid {} -t -f"
        self.find_list = find_list
        self.program_list = self.get_tasklist()

    def AddFindPro(self, find_list):
        '''增加需要查找的启动程序'''
        self.find_list += find_list
        print(self.find_list)

    def GetTaskList(self):
        tasklist_v_fo_csv = os.popen("tasklist /v /fo csv").read()
        tasklist_v_fo_csv_list = tasklist_v_fo_csv.split("\n")
        temp_list = []
        for tasklist_str in tasklist_v_fo_csv_list:
            tasklist = re.sub("\[|\]|\"", "", tasklist_str).split(",")
            if tasklist == []:
                continue
            temp_list.append(tasklist)
        return temp_list
    
    def get_tasklist(self):
        if self.find_list == None:
            self.find_list = ["chrome.exe"]
        if self.find_list == []:
            return []
        temp_list = []
        for task_info in self.GetTaskList():
            if task_info != "" and task_info[0] in self.find_list:
                temp_list.append(task_info)
        return temp_list

    def KillChrome(self):
        for temp in self.program_list:
            if "Google Chrome" in temp[-1]:
                cmd = self.kill_cmd.format(int(temp[1]))
                print('kill Google Chrome:[{}]'.format(cmd))
                os.system(cmd)

    def StartChrome(self):
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application"
        os.chdir(chrome_path)
        chrome_start = "start chrome chrome.exe --remote-debugging-port=9222"
        # chrome_start = "chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\\SUNYAN_NEW_PY3\\selenium+\\chrome_Default"
        os.system(chrome_start)

def WaitXpath(driver, url, xpath):
    '''
    @Time    :   2022/01/11 08:57:16
    @功能    :   None
    '''
    # capa = DesiredCapabilities.CHROME
    # capa["pageLoadStrategy"] = "none"
    # driver=webdriver.Chrome(desired_capabilities=capa)  # 关键!记得添加
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(url)
    except:
        return None
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))  # 这里可选择多个selector
    return True

class SeleniumBaseClass(object):
    '''selenium_base类中操作是不基于任何一个web页面和框架'''
    def __init__(self, 
            browser=None,
            url=None, 
            download_path=None,
            chromedriver_path=None,
            ):
        self.browser = browser
        self.url=url
        self.download_path = download_path
        self.chromedriver_path=chromedriver_path  # chromedriver路径 **必须提供
        self.js = None
        self.handles_dict = {}
        self.Check()
        
    def Check(self):
        '''登录浏览器之前的操作，不登录则不需要'''
        if self.chromedriver_path == None:
            print("chromedriver_path={} ,path error".format(self.chromedriver_path))
            exit()
        if not os.path.isfile(self.chromedriver_path):
            print("chromedriver_path={} ,path error".format(self.chromedriver_path))
            if not os.path.isdir(os.path.dirname(self.chromedriver_path)):
                os.makedirs(os.path.dirname(self.chromedriver_path))

        if self.download_path ==None or not os.path.isdir(self.download_path):
            for i in range(10):
                print("download_path={}, 未提供下载路径。程序的下载位置，跟随浏览器的最后一次下载位置".format(self.download_path))

    
    def OpenBaseChrome(self, virtual_browser=False):
        '''
        @Time    :   2020/05/27 07:52:50
        @功能 :   selenium根据virtual_browser参数来启动打开真实浏览器还是虚拟浏览器
        virtual_browser=False #是否启动虚拟浏览器，不使用真实的userdata；默认值false 不启动虚拟浏览器;tue启动虚拟浏览器
        '''
        '''selenium打开真实chrome浏览器'''
        os.environ['webdriver.chrome.driver'] = self.chromedriver_path
        options = webdriver.ChromeOptions()
        if self.download_path != None and os.path.isdir(self.download_path):
            # 指定文件下载路径下载路径
            prefs = {"download.default_directory": self.download_path}
            options.add_experimental_option("prefs", prefs)
        if virtual_browser == False:
            options.add_argument(
                "--user-data-dir=" + r"C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(getpass.getuser()))
        self.browser = webdriver.Chrome(self.chromedriver_path, chrome_options=options)
        self.browser.get(self.url)

    def OpenChrome(self, headless=False):
        # '''selenium打开真实chrome浏览器'''
        # os.environ['webdriver.chrome.driver'] = self.chromedriver_path
        # options = webdriver.ChromeOptions()
        # if headless:
        #     options.add_argument('headless') # 设置option
        # if self.download_path != None and os.path.isdir(self.download_path):
        #     # 指定文件下载路径下载路径
        #     prefs = {"download.default_directory": self.download_path}
        #     options.add_experimental_option("prefs", prefs)
        # if self.google_data_path is not None and os.path.isdir(self.google_data_path):
        #     options.add_argument("--user-data-dir=" + self.google_data_path)
        # else:
        #     options.add_argument("--user-data-dir=" + self.chrome_path)

        # # options.add_argument('--incognito') # 隐身模式（无痕模式）
        # # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--disable-javascript') 
        # while 1:
        #     try:
        #         self.browser = webdriver.Chrome(self.chromedriver_path, chrome_options=options)
        #         break
        #     except:
        #         base_version = "100.0.4896.20" 
        #         # base_version = "110.0.5481.104"
        #         chrome_version = GetChromeVersion(traceback.format_exc(), base_version)
        #         sign = AutoDownloadChromeDriver(chrome_dirver_version=chrome_version, chrome_driver_path=self.chromedriver_path)
        #         if sign is None:
        #             for i in range(10):
        #                 print(f"auto update chromedriver {chrome_version} error. Manual version update required\n url: https://registry.npmmirror.com/binary.html?path=chromedriver/")
        #             break

        # self.browser.get(self.url)
        # try_times = 10
        # if self.IsXpathExist('//*[@id="root"]/div/div/div[5]/div/div/form/h2'):
        #     while try_times>0:
        #         try:
        #             # 点击登录按钮
        #             click_sign = self.Click('//*[@id="root"]/div/div/div[5]/div/div/form/button')
        #             if click_sign:
        #                 try_times = 0
        #         except:
        #             try_times -= 1
        #             sleep(2)
        # self.browser.implicitly_wait(5)
        pass
    
    def OpenChromeNotLog(self, headless=False):
        # '''selenium打开真实chrome,无需登录'''
        # os.environ['webdriver.chrome.driver'] = self.chromedriver_path
        # options = webdriver.ChromeOptions()
        # if headless:
        #     options.add_argument('headless') # 设置option
        # if self.download_path != None and os.path.isdir(self.download_path):
        #     # 指定文件下载路径下载路径
        #     prefs = {"download.default_directory": self.download_path}
        #     options.add_experimental_option("prefs", prefs)
        # if self.google_data_path is not None and os.path.isdir(self.google_data_path):
        #     options.add_argument("--user-data-dir=" + self.google_data_path)
        # else:
        #     options.add_argument("--user-data-dir=" + self.chrome_path)

        # # options.add_argument('--incognito') # 隐身模式（无痕模式）
        # # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--disable-javascript') 
        # self.browser = webdriver.Chrome(self.chromedriver_path, chrome_options=options)
        # self.browser.get(self.url)
        # self.browser.implicitly_wait(5)
        pass
    
    def GetHandle(self, xpath, attribute_name=By.XPATH, handle=None):
        '''
        @Time    :   2023/02/20 10:45:34
        @功能    :   获得元素句柄
        handle!=None，表示写入基于该handle的下层输入框,否则是基于顶层的句柄
        '''
        try:
            if handle is None:
                return self.browser.find_element(attribute_name, xpath)
            return handle.find_element(attribute_name, xpath)
        except Exception as e:
            traceback.print_exc()
            _,_,info = current_stack()
            return None
    
    def GetHandles(self, xpath, attribute_name=By.XPATH, handle=None):
        '''
        @Time    :   2023/02/20 10:48:15
        @功能    :   获取某一类句柄,复数
        handle!=None，表示写入基于该handle的下层输入框,否则是基于顶层的句柄
        '''
        try:
            if handle is None:
                return self.browser.find_elements(attribute_name, xpath)
            return handle.find_elements(attribute_name, xpath)
        except:
            return None

    def ScrollBar_Mid(self):
        scroll_position = 500
        self.browser.execute_script(f"window.scrollTo(0, {scroll_position});")

    def WaitLoadingInfo(self, xpath, attribute_name=By.XPATH, handle=None, waiting_time=30):
        '''
        @Time    :   2022/08/10 14:39:26
        @功能    :   等待页面加载完成
        handle!=None，表示写入基于该handle的下层输入框,否则是基于顶层的句柄
        '''
        while waiting_time > 0:
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print(time_str)
            try:
                new_handle = self.GetHandle(attribute_name=attribute_name, xpath=xpath, handle=handle)
                if new_handle != None: return True
            except: 
                waiting_time -= 1
                time.sleep(1)
        return False

    def GetAllHandles(self):
        self.handles = self.browser.window_handles

    def Send(self, xpath, attribute_name=By.XPATH, handle=None, waiting_time=10, send_info=""):
        '''
        @Time    :   2020/12/09 15:16:44
        @功能    :   编辑框写入内容
        handle!=None，表示写入基于该handle的下层输入框,否则是基于顶层的句柄
        '''
        while waiting_time > 0:
            try:
                new_handle = self.GetHandle(attribute_name=attribute_name, xpath=xpath, handle=handle)
                new_handle.send_keys(send_info)
                return True
            except:
                waiting_time -= 1
                if waiting_time == 0:
                    traceback.print_exc()
                    _,_,info = current_stack()
                sleep(1)
        return False

    def RunJs(self):
        '''执行js脚本'''
        # self.js = 'window.open("http://www.youdao.com/");'
        if self.js:
            self.browser.execute_script(self.js)
        else:
            print("error: js=[{}]".format(self.js))

    def OpenNewPage(self, js, handel_name):
        '''打开新的标签页, 返回当前标签页句柄'''
        self.js = js
        self.RunJs()
        self.handles_dict[handel_name] = self.browser.current_window_handles
    
    def GetText(self, xpath, attribute_name=By.XPATH, handle=None, waiting_time=10, text=""):
        '''
        @Time    :   2023/12/12 10:43:46
        @功能    :   获得xpath地址对应的文本
        如果handle!=None，表示基于该handle获得下层xpath地址的内容,否则是基于顶层的句柄
        '''
        while waiting_time>0:
            try:
                new_handle = self.GetHandle(attribute_name=attribute_name, xpath=xpath, handle=handle)
                return new_handle.text
            except:
                waiting_time -= 1
                if waiting_time == 0:
                    _,_,info = current_stack()
                    traceback.print_exc()
                sleep(1)
        return text

    def Click(self, xpath, attribute_name=By.XPATH, handle=None, waiting_time=10):
        '''
        @Time    :   2023/12/12 11:02:33
        @功能    :   None
        点击xpath地址对应的按钮 复选框等可点击的操作
        如果handle!=None，表示基于该handle获得下层操作,否则是基于顶层的句柄
        '''

        while waiting_time>0:
            try:
                new_handle = self.GetHandle(attribute_name=attribute_name, xpath=xpath, handle=handle)
                new_handle.click()
                return True
            except:
                waiting_time -= 1
                if waiting_time == 0:
                    _,_,info = current_stack()
                    traceback.print_exc()
                sleep(1)
        return False


    def ClearInputText(self, xpath, attribute_name=By.XPATH, handle=None, waiting_time=10):
        '''
        @Time    :   2023/12/12 11:04:47
        @功能    :   None
        清空可编辑状态下的编辑框等的文本
        如果handle!=None，表示基于该handle获得下层操作,否则是基于顶层的句柄
        '''
        while waiting_time>0:
            try:
                new_handle = self.GetHandle(attribute_name=attribute_name, xpath=xpath, handle=handle)
                new_handle.clear()
                return True
            except:
                waiting_time -= 1
                if waiting_time == 0:
                    _,_,info = current_stack()
                    traceback.print_exc()
                sleep(1)
        return False

    def GetTableRowsAndCols_xpath(self, table_xpath, row_label, col_label, attribute_name=By.XPATH, waiting_time=10):
        '''
        @Time    :   2023/12/12 11:05:41
        @功能    :   获得表的行列数
        '''
        table_rows, table_cols = [], []
        while waiting_time > 0:
            try:
                table = self.GetHandle(attribute_name=attribute_name, xpath=table_xpath)
                table_rows = self.GetHandle(attribute_name=By.TAG_NAME, xpath=row_label, handle=table)
                # 用1的原因：可能第一行是标题行数据会有不同
                table_cols = self.GetHandle(attribute_name=By.TAG_NAME, xpath=col_label, handle=table_rows[0])
                return len(table_rows), len(table_cols)
            except:
                waiting_time -= 1
                if waiting_time == 0:
                    _,_,info = current_stack()
                    traceback.print_exc()
                sleep(1)
        return None, None
        
    def GetUrl_Xpath(self, xpath, attribute_name=By.XPATH, handle=None, waiting_time=10):
        """_summary_
        获得url地址
        如果handle!=None，表示基于该handle获得下层操作,否则是基于顶层的句柄
        """        
        while waiting_time>0:
            try:
                new_handle = self.GetHandle(attribute_name=attribute_name, xpath=xpath, handle=handle)
                return new_handle.get_attribute('href')
            except:
                waiting_time -= 1
                if waiting_time == 0:
                    _,_,info = current_stack()
                    traceback.print_exc()
                sleep(1)
        return None

    def IsXpathExist(self, xpath, attribute_name=By.XPATH, handle=None):
        '''判断元素是否存在'''
        try:
            new_handle = self.GetHandle(attribute_name=attribute_name, xpath=xpath, handle=handle)
            if new_handle != None:
                return True
        except:
            return False

    def Refresh(self, xpath_):
        '''当页面刷新不完全的时候进行刷新动作，最多3次'''
        counts = 3
        while (counts):
            if self.IsXpathExist(xpath_):
                break
            self.browser.refresh()
            sleep(10)
            counts -= 1

    def Selected(self, xpath, val, attribute_name=By.XPATH, handle=None, waiting_time=10):
        '''下拉列表框值的选择'''
        while waiting_time > 0:
            try:
                new_handle = self.GetHandle(attribute_name=attribute_name, xpath=xpath, handle=handle)
                Select(new_handle).select_by_value(val)
                return True
            except:
                waiting_time -= 1
                if waiting_time == 0:
                    _,_,info = current_stack()
                    traceback.print_exc()
                sleep(1)
        return False

    def ScrollBar_TOP(self):
        '''滚动条，滚动到顶端'''
        # js = "var q=document.body.scrollTop=0"
        js = "var q=document.documentElement.scrollTop=0"
        # self.browser.execute_script(js)
        self.js = js
        self.RunJs()

    def ScrollBar_Bottom(self):
        '''滚动条，滚动到底端 '''
        js = "var q=document.documentElement.scrollTop=100000"
        # self.browser.execute_script(js)
        self.js = js
        self.RunJs()

    def Back(self):
        '''浏览器返回操作'''
        self.browser.back()

    def ClosePage(self):
        '''关闭浏览器当前页'''
        self.browser.close()

    def Close(self):
        '''关闭selenum句柄'''
        self.browser.close()
        self.browser.quit()

    def BackAndRefresh(self):
        '''
        @Time    :   2023/12/12 11:58:01
        @功能    :   回退并刷新
        '''
        self.browser.back()
        self.browser.refresh()
        pass

    def Refresh(self):
        '''
        @Time    :   2023/12/12 11:58:01
        @功能    :   刷新
        '''
        self.browser.refresh()
    
class selenium_qti(SeleniumBaseClass):
    '''
    @Time    :   2021/10/28 09:35:22
    @Author  :   sunyan
    @Desc    :   selenium_qti针对高通case页面处理进行封装
    参数说明：
    browser selenium句柄为空则表示需要重新创建
    url 网页地址
    download_path 如果需要下载log到指定的位置可以设置此参数
    chromedriver_path 必须参数chromedriver.exe的位置
    debug 在需要对网页内容进行修改的时候需要关注此参数，默认为非调试模式。
    修改内容会被更新到网页上， ture表示调试模式不将修改内容保存到网页
    '''
    def __init__(self,
                 browser=None,
                 url="",
                 download_path=None,
                 chromedriver_path=None,
                 google_data_path=None,
                 del_userdata=False,
                 debug=False):

        SeleniumBaseClass.__init__(self, browser, url, download_path, chromedriver_path)
        self.url = url
        self.debug = debug #是否启动调试模式，默认值false，不启动调试模式；true 启动调试模式
        self.browser = browser
        self.del_userdata = del_userdata
        self.download_path = download_path  #下载excel表格则必须提供该参数
        self.chromedriver_path = chromedriver_path
        self.google_data_path = google_data_path
        self.CheckQti()
        self.ReadMe()
        self.DelOldUserData()
        self.chrome_path = rf"C:\Users\{getpass.getuser()}\AppData\Local\Google\Chrome\User Data"
        cud = CopyUserData(from_path=self.chrome_path, to_path=self.google_data_path, del_userdata=self.del_userdata)
        cud.CopyChrome()
    
    def ReadMe(self):
        '''
        @Time    :   2021/10/29 10:29:28
        @功能    :   None
        '''
        print("""
        selenium_qti 类参数说明：
        url： 需要打开的url地址
        debug： #是否启动调试模式，默认值false，不启动调试模式；true 启动调试模式
        del_userdata： 是否每次都删除本地的userdata文件夹
        download_path： #设置下载路径的
        chromedriver_path： chromedriver.exe 全路径
        google_data_path： user_data路径
        """)
        pass
    
    def GetTaskList(self):
        tasklist_v_fo_csv = os.popen("tasklist /v /fo csv").read()
        tasklist_v_fo_csv_list = tasklist_v_fo_csv.split("\n")
        temp_list = []
        for tasklist_str in tasklist_v_fo_csv_list:
            tasklist = re.sub("\[|\]|\"", "", tasklist_str).split(",")
            if tasklist == []:
                continue
            temp_list.append(tasklist)
        return temp_list

    def CheckQti(self):
        '''登录浏览器之前的操作，不登录则不需要'''
        if self.chromedriver_path == None:
            print("chromedriver_path={} ,path error".format(self.chromedriver_path))
            exit()
        if not os.path.isfile(self.chromedriver_path):
            print("chromedriver_path={} ,path error".format(self.chromedriver_path))
            if not os.path.isdir(os.path.dirname(self.chromedriver_path)):
                os.makedirs(os.path.dirname(self.chromedriver_path))
        if self.download_path ==None or not os.path.isdir(self.download_path):
            for i in range(10):
                print("download_path={}, 未提供下载路径。程序的下载位置，跟随浏览器的最后一次下载位置".format(self.download_path))

    def AcceptAllCookies(self):
        '''
        @Time    :   2024/04/01 17:26:25
        @功能    :   处理高通cookies提示
        '''
        time.sleep(10)
        handle = self.GetHandle('/html/body/div[2]/div[2]/div/div/div[2]/div/div/button')
        if handle is None:
            return handle
        handle.click()
        return True
    
    def SignIn(self):
        '''
        @Time    :   2024/04/01 17:38:27
        @功能    :   None
        '''
        try_times = 10
        if self.IsXpathExist('//*[@id="root"]/div/div/div[5]/div/div/form/h2'):
            while try_times>0:
                try:
                    # 点击登录按钮
                    click_sign = self.Click('//*[@id="root"]/div/div/div[5]/div/div/form/button')
                    if click_sign: return True
                except:
                    try_times -= 1
                    sleep(2)
        return False
    
    def DelOldUserData(self):
        '''
        @Time    :   2024/07/29 09:26:07
        @功能    :   删除本地的google_data_path
        '''
        try:
            shutil.rmtree(self.google_data_path)
            return True
        except:return False
    
    def OpenChrome(self, headless=False):
        '''selenium打开真实chrome浏览器'''
        # self.DelOldUserData()
        os.environ['webdriver.chrome.driver'] = self.chromedriver_path
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless') # 设置option
        if self.download_path != None and os.path.isdir(self.download_path):
            # 指定文件下载路径下载路径
            prefs = {"download.default_directory": self.download_path}
            options.add_experimental_option("prefs", prefs)
        if self.google_data_path is not None and os.path.isdir(self.google_data_path):
            options.add_argument("--user-data-dir=" + self.google_data_path)
        else:
            options.add_argument("--user-data-dir=" + self.chrome_path)

        # options.add_argument('--incognito') # 隐身模式（无痕模式）
        # options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-javascript') 
        while 1:
            try:
                self.browser = webdriver.Chrome(self.chromedriver_path, chrome_options=options)
                break
            except:
                base_version = "100.0.4896.20" 
                _,_,info = current_stack()
                traceback.print_exc()
                # base_version = "110.0.5481.104"
                chrome_version = GetChromeVersion(traceback.format_exc(), base_version)
                sign = AutoDownloadChromeDriver(chrome_dirver_version=chrome_version, chrome_driver_path=self.chromedriver_path)
                if sign is None:
                    for i in range(10):
                        print(f"auto update chromedriver {chrome_version} error. Manual version update required\n url: https://registry.npmmirror.com/binary.html?path=chromedriver/")
                    break

        self.browser.get(self.url)
        self.AcceptAllCookies()
        if not self.SignIn():
            print("登录失败")
        # try_times = 10
        # if self.IsXpathExist('//*[@id="root"]/div/div/div[5]/div/div/form/h2'):
        #     while try_times>0:
        #         try:
        #             # 点击登录按钮
        #             click_sign = self.Click('//*[@id="root"]/div/div/div[5]/div/div/form/button')
        #             if click_sign:
        #                 try_times = 0
        #         except:
        #             try_times -= 1
        #             sleep(2)
        # self.browser.implicitly_wait(5)
    
    def OpenChromeNotLog(self, headless=False):
        '''selenium打开真实chrome,无需登录'''
        os.environ['webdriver.chrome.driver'] = self.chromedriver_path
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless') # 设置option
        if self.download_path != None and os.path.isdir(self.download_path):
            # 指定文件下载路径下载路径
            prefs = {"download.default_directory": self.download_path}
            options.add_experimental_option("prefs", prefs)
        if self.google_data_path is not None and os.path.isdir(self.google_data_path):
            options.add_argument("--user-data-dir=" + self.google_data_path)
        else:
            options.add_argument("--user-data-dir=" + self.chrome_path)

        # options.add_argument('--incognito') # 隐身模式（无痕模式）
        # options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-javascript') 
        self.browser = webdriver.Chrome(self.chromedriver_path, chrome_options=options)
        self.browser.get(self.url)
        self.browser.implicitly_wait(5)
    
    def FindFile(self, download_path, log_name):
        '''查找文件，主要用于判断log是否存在，存在就不用再次下载'''
        if " " not in log_name:
            return download_path + "\\" + log_name
        for file in os.listdir(download_path):
            if not os.path.isfile(file) and " " not in file:
                continue
            if log_name == " ".join(file.split()):
                print(file)
                return download_path + "\\" + file
        return download_path + "\\" + log_name

    def DownLoadLog(self, download_path, log_name, log_link):
        '''下载log，内部使用无线循环的方式保证文件有足够的时间进行下载'''
        source_path = download_path + "\\" + log_name
        if os.path.isfile(source_path):
            return source_path
        self.browser.get(log_link)
        while 1:
            # source_path = self.FindFile(download_path, log_name)
            if not os.path.isfile(source_path):
                sleep(5)
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                continue
            return source_path
    
    def UniformMB(self, file_size):
        '''
        @Time    :   2020/12/24 10:07:58
        @功能    :   统一文件大小为MB
        '''
        file_size_list = file_size.lower().split(" ")
        file_size = float(file_size_list[0])

        if file_size_list[1] == "kb":
            return file_size/1024.0
        elif file_size_list[1] == "mb":
            return file_size
        elif file_size_list[1] == "gb":
            return file_size*1024
        else:
            return 0

    def DownloadTimeOLD(self, file_size:int):
        '''
        @Time    :   2020/12/24 10:09:43
        @功能    :   根据文件大小返回一个文件下载的最长等待时间
        file_size 单位为M
        return download_time单位为 秒
        '''
        download_time = 5
        if file_size <= 1:
            download_time = 5
        elif file_size > 1 and file_size <= 500:
            download_time = 15
        elif file_size > 500 and file_size <= 1024:
            download_time = 25
        elif file_size > 1024 and file_size <= 2048:
            download_time = 35
        elif file_size > 2048 and file_size <= 3096:
            download_time = 40
        else:
            download_time = 180
        return download_time*60

    def DownloadTime(self, file_size:int):
        '''
        @Time    :   2020/12/24 10:09:43
        @功能    :   根据文件大小返回一个文件下载的最长等待时间
        file_size 单位为M
        return download_time单位为 秒
        '''
        download_time = 2
        if file_size <= 10:
            download_time = 2
        elif file_size > 10 and file_size <= 500:
            download_time = 5
        elif file_size > 500 and file_size <= 1024:
            download_time = 10
        elif file_size > 1024 and file_size <= 3096:
            download_time = 15
        else:
            download_time = 20
        return download_time*60

    def DwonloadUrlError(self):
        '''
        @Time    :   2021/01/15 14:02:31
        @功能    :   被下载的log可能存在的两种错误，遇到直接返回
        '''
        try:
            handle = self.GetHandle( xpath='/html/body', attribute_name=By.XPATH)
            info = handle.text
            if info.startswith("An error occurred"):
                return False
        except:pass
        try:
            handle = self.GetHandle(xpath='/html/body/div[2]/span', attribute_name=By.XPATH)
            info = handle.text
            if info.startswith("This XML file does"):
                return False
        except:pass

        return True
    
    def DownLoadLog2(self, download_path, log_name, log_link, log_size):
        '''
        @Time    :   2020/12/24 10:05:34
        @功能    :   下载log，增加log下载时间控制功能
        '''
        '''下载log，内部使用无线循环的方式保证文件有足够的时间进行下载'''
        download_time = self.DownloadTime(self.UniformMB(log_size))
        source_path = download_path + "\\" + log_name
        if os.path.isfile(source_path):
            return source_path
        self.browser.get(log_link)

        if not self.DwonloadUrlError():
            return None
        # return None
        while download_time:
            if not os.path.isfile(source_path):
                sleep(5)
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                download_time -= 5
                continue
            return source_path
        return None
    
    def OpenChromeNotLog(self, headless=False):
        '''selenium打开真实chrome,无需登录'''
        os.environ['webdriver.chrome.driver'] = self.chromedriver_path
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless') # 设置option
        if self.download_path != None and os.path.isdir(self.download_path):
            # 指定文件下载路径下载路径
            prefs = {"download.default_directory": self.download_path}
            options.add_experimental_option("prefs", prefs)
        if self.google_data_path is not None and os.path.isdir(self.google_data_path):
            options.add_argument("--user-data-dir=" + self.google_data_path)
        else:
            options.add_argument("--user-data-dir=" + self.chrome_path)

        # options.add_argument('--incognito') # 隐身模式（无痕模式）
        # options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-javascript') 
        self.browser = webdriver.Chrome(self.chromedriver_path, chrome_options=options)
        self.browser.get(self.url)
        self.browser.implicitly_wait(5)

    def Save(self, save_xpath=None, cancel_xpath=None):
        '''Save 具备点击cancel和save两个功能，由debug_sign控制'''
        self.ScrollBar_TOP()
        if save_xpath == None or cancel_xpath == None:
            self.Back()
            return
        if self.debug:
            self.Click(cancel_xpath)  # cancel
        else:
            self.Click(save_xpath)  # save

    def EditBox(self, click_xpath, send_xpath, info):
        '''编辑box内容'''
        self.Click(click_xpath)
        self.ClearInputText(send_xpath)
        if self.Send( xpath=send_xpath, attribute_name=By.XPATH, send_info=info):
            print("编辑成功")
        else:
            print('编辑失败')
            return False

        self.Save(save_xpath='//*[@id="pg:frm:blk:navBtns:btnSave"]',
                  cancel_xpath='//*[@id="outer"]/div[3]/input')
        return True

    def GetOwnerEmail(self):
        '''owner的名称和email地址'''
        url_t = self.browser.current_url
        try:
            owner = self.GetText('//*[@id="ep"]/div[2]/div[2]/table/tbody/tr[7]/td[2]/a[1]')
            handle = self.GetHandle('//*[@id="ep"]/div[2]/div[2]/table/tbody/tr[7]/td[2]/a[1]')
            handle.click()
        except:
            return "", ""
        email_xpath = '//*[@id="ep"]/div[2]/div[2]/table/tbody/tr[3]/td[2]/a'
        email = self.GetText(email_xpath)
        if url_t != self.browser.current_url:
            self.browser.back()
            self.browser.refresh()
        return owner, email

    def GetCaseStatus(self, xpath='//*[@id="ep"]/div[2]/div[2]/table/tbody/tr[10]/td[2]'):
        '''获得case的状态'''
        case_status = self.GetText(xpath)
        if (case_status == "Closed") or (case_status == 'Closed-Customer Requested'):
            return True
        return False

    def GetCommnets(self, case_id, rows):
        '''获得case的所有comments'''
        comments_list = []
        sign = False
        for row in range(2, rows + 1):
            com_xpath = '//*[@id="{}_RelatedCommentsList_body"]/table/tbody/tr[{}]/td[2]/div'.format(case_id, row)
            if row == 2:
                try:
                    self.browser.find_element(By.XPATH,com_xpath)
                except:
                    sign = True
            if sign:
                com_xpath = com_xpath.replace('/div', "")
            print(com_xpath)
            comment_text = self.GetText_Xpath(com_xpath)
            comments_list.append(comment_text)
        return comments_list

    def FormatComment(self, comment):
        comment = comment.strip()
        comment = "\n".join([com for com in comment.split("\n")])
        comment = comment.replace("\t", " " * 4)
        return comment

    def UpdateComment(self, caseid, comment_info="this is test", public_sign=False,):
        '''更新comment'''
        comment_info = self.FormatComment(comment_info)
        add_com_xpath = '//*[@id="{}_RelatedCommentsList"]/div[1]/div/div[1]/table/tbody/tr/td[2]/input'.format(
            caseid)
        self.Click(add_com_xpath)
        com_xpath = '//*[@id="CommentBody"]'
        self.Send(xpath=com_xpath, attribute_name=By.XPATH, send_info=comment_info)
        if public_sign:
            self.Click('//*[@id="IsPublished"]')
        self.Save(save_xpath='//*[@id="bottomButtonRow"]/input[1]', cancel_xpath='//*[@id="topButtonRow"]/input[2]')

    def SetTag(self, info):
        '''给case打标签'''
        text = self.GetText('//*[@id="ep"]/div[2]/div[14]/table/tbody/tr[12]/td[2]')
        text_list = text.split(",")
        for te in text_list:
            if info == te:
                return
        self.Click('//*[@id="topButtonRow"]/input[1]')
        if (len(text) != 0) and (text != " "):
            info = ",{}".format(info)
        send_xpath = '//*[@id="pg:frm:blk:productData:interOperabilityIOTDeviceId"]'
        if self.Send(xpath=send_xpath, attribute_name=By.XPATH, send_info=info):
            print("修改成功")
        else:
            print("修改失败")
            return False
        self.Save(save_xpath='//*[@id="pg:frm:blk:navBtns:btnSave"]', cancel_xpath='//*[@id="outer"]/div[3]/input')
        return True

    def GetExcelFile(self, path):
        '''获得excel表的名称'''
        reg_ = re.compile("^report(\d+)\.xls$")
        xls_dict = {}
        for fi in os.listdir(path):
            group = re.match(reg_, fi)
            if group:
                xls_dict[group.group(1)[:10]] = fi
        return xls_dict
        
    def DownLoadExcel(self, url):
        '''下载report的数据到excel中'''
        sleep(10)
        # self.browser.get(f"{url}?export=1&enc=UTF-8&xf=xls")
        self.browser.get("{}?export=1&enc=UTF-8&xf=xls".format(url))
        xls_dict, sign = {}, True
        while sign:
            xls_dict = self.GetExcelFile(self.download_path)
            if len(xls_dict):
                sign = False
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            sleep(5)
        max_num = max([int(num) for num in xls_dict.keys()])
        source_file_name = "{}\\{}".format(self.download_path, xls_dict[str(max_num)])
        return source_file_name

    def DownloadReport(self):
        '''
        @Time    :   2022/07/19 15:29:04
        @功能    :   下载report
        '''
        # 点击下拉按钮，根据在class 名称中找到唯一类名
        if self.SwitchToFrame(attribute_name=By.TAG_NAME, frame_name="iframe") == False:
            print("框架切换失败")
            return False
        self.WaitLoading()
        time.sleep(3)
        handle = self.GetHandle(attribute_name=By.CLASS_NAME, xpath='slds-button_last')
        handle.click()

        time.sleep(3)
        # 点击导出按钮按钮，根据在class 名称中找到唯一类名
        handle = self.GetHandle(attribute_name=By.CLASS_NAME, xpath='report-action-ReportExportAction')
        handle.click()

        #切除iframe回到主文档
        self.browser.switch_to.default_content()
        time.sleep(3)
        # 选中details only; 根据在class 名称中找到唯一类名
        export_divs = self.GetHandles(attribute_name=By.CLASS_NAME, xpath="reportsExportVisualPickerOption")
        export_divs[1].click()

        # 切换编码格式
        handles = self.GetHandles(attribute_name=By.CLASS_NAME, xpath='slds-select_container')
        # select_handles = self.GetHandles(attribute_name=By.TAG_NAME, xpath="select", handle=handles[-1])
        # # select_handles = handles[-1].find_elements(By.TAG_NAME, "select")
        # Select(select_handles[-1]).select_by_value("UTF-8")
        self.Selected(xpath="select", attribute_name=By.TAG_NAME, handle=handles[-1], val="UTF-8")
        
        # 点击导出按钮，根据在class 名称中找到唯一类名
        handle = self.GetHandle(attribute_name=By.CLASS_NAME, xpath='uiButton--brand')
        handle.click()
        xls_dict, sign = {}, True
        while sign:
            xls_dict = self.GetExcelFile(self.download_path)
            if len(xls_dict):
                sign = False
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            sleep(5)
        max_num = max([int(num) for num in xls_dict.keys()])
        source_file_name = "{}\\{}".format(self.download_path, xls_dict[str(max_num)])
        return source_file_name

    def MoveAndRename(self, old_file, new_path=None, new_name=None):
        '''移动文件并且重命名'''
        '''移动和修改文件名称'''
        if old_file == None or not os.path.isfile(old_file):
            # print(f"old_file={old_file} 不存在, return")
            print("old_file={} 不存在, return".format(old_file))
            return

        if new_path == None or not os.path.isdir(new_path):
            # print(f"new_path={new_path}, 不移动文件, return")
            print("new_path={}, 不移动文件, return".format(new_path))
            return
        try:
            shutil.move(old_file, new_path)
            file_name = os.path.split(old_file)[1]
            # new_path_file = rf"{new_path}\{file_name}"
            new_path_file = r"{}\{}".format(new_path,file_name)
        except:
            new_path_file = ""

        if new_path_file == None:
            # print(f"new_path_file={new_path_file}, 文件移动失败, return")
            print("new_path_file={}, 文件移动失败, return".format(new_path_file))
            return
        if new_name == None:
            # print(f"new_name={new_name}, 不移动文件, return")
            print("new_name={}, 不移动文件, return".format(new_name))
            return
        try:
            # os.rename(new_path_file, rf"{new_path}\{new_name}")
            os.rename(new_path_file, r"{}\{}".format(new_path,new_name))
        except:
            print("文件名称修改失败")
            return

    def ShowMoreClick(self, xpath):
        '''点击上传log的更多按钮'''
        sign = self.Click(attribute_name=By.XPATH, xpath=xpath)
        sleep(5)  # 有时候系统因为网速的原因会导致加载速度慢，导致获取不全

    def GetLogUrl(self, case_id, name_length=60):
        '''获得所有log的下载地址等相关信息'''
        url_list = []
        record_xpath = '//*[@id="{}_00N300000042No3_body"]/table/tbody'.format(case_id)
        rows1, cols1 = self.GetTableRowsAndCols_xpath(record_xpath, "tr", 'th')
        if rows1 < 2:
            return url_list
        xpath = record_xpath + '/tr[{}]/'
        for index in range(0, rows1 - 1):
            log = {}
            xpath_new = xpath.format(index + 2)
            log["name"] = self.GetText_Xpath(xpath_new + 'th/a')
            log["link"] = self.GetUrl_Xpath(xpath_new + 'th/a')
            log["description"] = self.GetText_Xpath(xpath_new + 'td[{}]'.format(2))
            log["import_date"] = self.GetText_Xpath(xpath_new + 'td[{}]'.format(5))
            log["file_size"] = self.GetText_Xpath(xpath_new + 'td[{}]'.format(6))

            log["owner_alias"] = self.GetText_Xpath(xpath_new + 'td[{}]'.format(4))
            log["uploaded_by"] = self.GetText_Xpath(xpath_new + 'td[{}]'.format(3))
            url_list.append(log)
        url_list = self.CutLogName(url_list, name_length)
        return url_list

    def GetReportsKey(self, cols):
        '''获得report中的标题，用于字典的键'''
        case_info_key = []
        for col in range(1, cols + 1):
            temp_str = self.GetText_Xpath('//*[@id="headerRow_0"]/th[{}]/a'.format(col))
            temp_str = temp_str.strip().replace(" ", "_")
            case_info_key.append(temp_str)
        return case_info_key

    def GetReportsCaseId(self, xpath):
        '''获得report的所有信息，并且生成字典'''
        rows, cols = self.GetTableRowsAndCols_xpath(xpath, "tr", 'th')
        case_info_key = self.GetReportsKey(cols)
        # owner_base_xpath, case_id_list, = f'{xpath}/tr', []
        owner_base_xpath, case_id_list, = '{}/tr'.format(xpath), []
        for row in range(2, rows - 1):
            temp = []
            for index in range(1, cols + 1):
                temp.append(self.GetText_Xpath('{}[{}]/td[{}]'.format(owner_base_xpath, row, index)))
            case_id_list.append(dict(zip(case_info_key, temp)))
        return case_id_list
    
    def ChangeCaseStatus(self):
        Edit_Xpath = '//*[@id="topButtonRow"]/input[1]'
        self.Click(Edit_Xpath)
        self.Selected('//*[@id="pg:frm:blk:title:StatusSection:selStatus"]', 'Hold-Customer Information Required')
        sleep(0.5)
        self.Save(save_xpath='//*[@id="pg:frm:blk:navBtns:btnSave"]', cancel_xpath='//*[@id="outer"]/div[3]/input')

    def CutLogName(self, log_list, name_length=60):
        '''
        @Time    :   2021/10/29 10:54:37
        @功能    :   文件名称超长，需要截断处理，否则容易在存储的时候超出256限制
        '''
        for log in log_list:
            log['description'] = log['description'].replace("/", ">>")
            name_l = os.path.splitext(log['name'])
            if len(name_l[0]) >= name_length:
                log['cut_name'] = name_l[0][:59] + name_l[1]
            else:
                log['cut_name'] = log['name']
        return log_list

    def FitleRecord(self, record_file, log_list):
        '''
        @Time    :   2020/05/22 10:34:42
        @功能   :   过滤loglist去除已经被下载的log信息
        '''
        if not os.path.isfile(record_file):
            return log_list
        f = codecs.open(record_file, "r", encoding="utf-8")
        line_list = f.readline().split(";")
        new_log_list = []
        for log in log_list:
            if operator.eq([log['name'], log['import_date'], log['file_size']], line_list[0:3]):
                return new_log_list
            new_log_list.append(log)
        return new_log_list

    def IsFinishUpdate(self, case):
        '''
        @Time    :   2021/04/19 10:27:42
        @功能    :   检查case是否已经被更新过，不能通过过滤device来确认，因为有的case使用继承
        这是一个特例函数 基本无法被其他程序公用
        '''
        device = self.GetText_Xpath('//*[@id="ep"]/div[2]/div[16]/table/tbody/tr[15]/td[2]')
        parent_case=self.GetText_Xpath('//*[@id="ep"]/div[2]/div[2]/table/tbody/tr[4]/td[2]')
        if "log_check" in device:
            if len(parent_case.strip()) == 8:
                finish_sign = True
                rows, cols = self.GetTableRowsAndCols_xpath(f'//*[@id="{case["Case_ID"]}_RelatedCommentsList_body"]/table/tbody', "tr", "td")
                all_coms = self.GetCommnets(case['Case_ID'], rows)
                for com in all_coms:
                    com_sign = True
                    for key in ["Start:","End:", "captred by default log mask"]:
                        if key not in com:
                            com_sign = False
                            break
                    if com_sign:
                        print("标签存在，case已经更新过comment，该case不再需要被处理")
                        return True
                    else:
                        finish_sign = False
                if finish_sign:
                    print("标签存在（继承自父case），但是没有更新comment，因此该case还需要被继续处理")
                    return False
            else:
                print("标签存在，且没有父case；说明有case已经被解析过")
                return True
        else:
            print("标签 不存在，需要解析case")
            return False

    def NewGetOwnerEmail(self, owner_page_url):
        url = f"https://qualcomm-cdmatech-support.lightning.force.com{owner_page_url}"
        # 打开新页面
        self.browser.execute_script(f"window.open('{url}');")
        # 获取新页面的句柄
        new_window_handle = self.browser.window_handles[-1]
        # 切换到新页面
        self.browser.switch_to.window(new_window_handle)
        # 在新页面上执行操作，例如获取页面标题
        self.browser.switch_to.parent_frame()
        self.browser.implicitly_wait(5)
        email = self.GetHandle(xpath='emailuiFormattedEmail', attribute_name=By.CLASS_NAME)
        email_text = email.text
        owner_name = (email_text.split('@'))[0]
        # 关闭新页面并返回到当前页面
        self.browser.close()
        current_window_handle = self.browser.window_handles[0]
        self.browser.switch_to.window(current_window_handle)
        return email_text,owner_name

    def NewGetOwnerEmailV2(self,name):
        # self.browser.switch_to.frame(self.browser.find_element_by_tag_name("iframe"))
        self.browser.switch_to.parent_frame()
        self.browser.implicitly_wait(5)
        email = self.GetHandle(xpath='emailuiFormattedEmail', attribute_name=By.CLASS_NAME)
        email_text = email.text
        owner_name = (email_text.split('@'))[0]
        count = 0
        while count < 3:
            table = self.GetHandle('//div/div/div/div/ul[2]')
            table_rows = self.GetHandles(xpath='li', attribute_name=By.TAG_NAME, handle=table)
            index = 0
            for i in range(1,len(table_rows)+1):
                handles = self.GetHandles(xpath=f'//div/div/div/div/ul[2]/li[{i}]/a/span[2]')
                for handle in handles:
                    if handle.text == name:
                        index = i
                        break
                if index != 0:
                    break

            button_handles = self.GetHandles(xpath=f'//div/div/div/div/ul[2]/li[{index}]/div[2]/button/lightning-primitive-icon')
            try:
                button_handles[1].click()
                count = 3
            except:
                self.browser.refresh()
                self.browser.implicitly_wait(6)
                count += 1
        self.browser.back()
        self.browser.refresh()
        return email_text,owner_name

    def WaitLoading(self, url_Trye="report"):
        '''
        @Time    :   2022/07/19 15:39:26
        @功能    :   等待页面加载完成
        '''
        if url_Trye == "report":
            while 1:
                try:
                    total_records = self.GetHandles(xpath='metricsElement',attribute_name=By.CLASS_NAME)
                    if total_records != []:
                        break
                except:
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    print(time_str)
                    time.sleep(1)
        elif url_Trye=="case":
            pass

    def SwitchToFrame(self, frame_name, attribute_name=By.XPATH, counts=5):
        '''
        @Time    :   2023/02/20 10:53:06
        @功能    :   切换框架
        '''
        time.sleep(3)
        try_counts = 0
        while 1:
            try:
                handle = self.GetHandle(attribute_name=attribute_name, xpath=frame_name)
                self.browser.switch_to.frame(handle)
                time.sleep(2)
                return True
            except:
                if try_counts == counts:
                    print("框架切换失败")
                    return False
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print(time_str)
                time.sleep(1)
                try_counts += 0.5

    def SwitchOutFrame(self, counts=5):
        '''
        @Time    :   2023/12/12 13:30:17
        @功能    :   切回主框架
        '''
        time.sleep(3)
        try_counts = 0
        while 1:
            try:
                self.browser.switch_to.default_content()
                time.sleep(2)
                return True
            except:
                if try_counts == counts:
                    print("框架切换失败")
                    return False
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print(time_str)
                time.sleep(1)
                try_counts += 0.5
        pass
    
    def GetAttributeValue_Xpath(self,xpath, attr, sign=True, count=0, text=""):
        '''
        @Time    :   2020/04/02 16:31:11
        @功能   :   获得元素的属性值
        #未验证 功能
        '''
        while (sign):
            try:
                count += 0.5
                resolved_during_customer_browser = self.GetHandle(xpath=xpath)
                text = resolved_during_customer_browser.get_attribute(attr)
                sign = False
            except:
                if count == 3:
                    sign = False
                else:
                    sleep(1)
        return text
    
    def GetHandleAttribute(self, handle, attrs:list=[]):
        '''
        @Time    :   2024/07/05 17:22:10
        @功能    :   获得元素的属性
        attrs 为"all"，则获取下面提到的所有属性,未提到的属性也可以加入尝试获取
            ["href", "value", "id" ....]
        attrs 为list则获取list内的所有的属性的值
        attrs 为str则只获取指定的属性值
        '''
        if isinstance(attrs, str):
            if attrs == "all":
                attrs=["href", "value", "id", "class", "type","disabled", "target", "title", "style"]
            else:
                attrs = [attrs]
        attr_dict = {}
        for attr in attrs:
            attr = attr.lower()
            try:
                attr_dict[attr] = handle.get_attribute(attr)
            except:
                attr_dict[attr] = f"{attr} 不存在该属性" 
        return attr_dict
    
    def GetAllComments(self):
        '''
        @Time    :   2024/07/15 09:40:15
        @功能    :   comment 页面一次展开所有comment，因此无需翻页之类的加载操作
        '''
        table_handles = self.GetHandles(".//*[self::table[@class='slds-table forceRecordLayout slds-table_header-fixed slds-table--header-fixed slds-table_edit slds-table--edit slds-table_bordered slds-table--bordered resizable-cols slds-table--resizable-cols uiVirtualDataTable']]")
        if len(table_handles) != 1:
            print("table应该只有一个，但是这里出现了两个请手动查看源html确定tables的选取")

        # 获得comment的标题
        title_handles = self.GetHandles(".//*[self::thead]//*[self::th]", handle=table_handles[0])
        titles = []
        for index, title in enumerate(title_handles):
            if index == 0: continue
            info_list = title.text.split("\n")
            info = info_list[1]
            titles.append(info.strip())
            if info == "Comment": break

        # 获得comment的每个字段的信息
        tr_handles = self.GetHandles(".//*[self::tbody]//*[self::tr]", handle=table_handles[0])
        comments = []
        for tr in tr_handles:
            comment = []
            a_handle = self.GetHandle(".//*[self::th]//*[self::a]", handle=tr)
            if a_handle != None:
                attr_dict = self.GetHandleAttribute(a_handle, attrs=["title", "href"])
                comment.append(attr_dict)
            td_handles = self.GetHandles(".//*[self::td]", handle=tr)
            for index, td in enumerate(td_handles):
                if index == 0 or index == len(td_handles)-1: continue
                if index == 1:
                    img_handle = self.GetHandle(".//*[self::img]", handle=td)
                    public = self.GetHandleAttribute(img_handle, attrs=['alt'])["alt"]
                    comment.append(public)
                else:
                    comment.append(td.text.strip())
            comments.append(dict(zip(titles, comment)))
        return comments
    
    def NewUpdateComment(self,caseid, comment_info="this is test", public_sign=False):
        """更新comment"""
        sign = False
        comment_info = self.FormatComment(comment_info)
        #点击Communications
        self.Click('//*[@id="customTab__item"]')
        #New_xpath
        self.WaitLoadingInfo('//lst-list-view-manager-header/div/div[1]/div[3]/div/ul/li/a')
        count = 0
        while count < 3:
            try:
                handels = self.browser.find_elements(By.XPATH, '//lst-list-view-manager-header/div/div[1]/div[3]/div/ul/li/a')
                handels[0].click()
                # 点击new之后出现的页面中的cancel按钮
                self.WaitLoadingInfo(
                    '/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[2]/section[1]/div/div/section[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/button[1]')
                Body_xpath = '/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[2]/section[1]/div/div/section[2]/div/div[2]/div/div/div/div[1]/div/article/div[3]/div/div/div/div/div[1]/div/div/div/div/textarea'
                self.browser.find_element(By.XPATH, Body_xpath).send_keys(comment_info)
                public_xpath = '/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[2]/section[1]/div/div/section[2]/div/div[2]/div/div/div/div[1]/div/article/div[3]/div/div/div/div/div[2]/div/div/div/div/input'
                if public_sign:
                    self.Click(public_xpath)
                save_xpath = '/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[2]/section[1]/div/div/section[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/button[2]'
                cancel_xpath = '/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[2]/section[1]/div/div/section[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/button[1]'
                self.Save(save_xpath=save_xpath, cancel_xpath=cancel_xpath)
                count = 3
                sign = True
            except:
                self.browser.refresh()
                # self.WaitLoadingInfo('//div/div[2]/div/div/div/div[1]/div/article/h2') #New Case Comment
                self.WaitLoadingInfo('//lst-list-view-manager-header/div/div[1]/div[3]/div/ul/li/a')
                count += 1
        return sign

    def NewUpdateComment2(self, comment_info, public_sign=False, save:bool=True):
        """更新comment"""
        comment_info = self.FormatComment(comment_info)
        comments = self.GetAllComments()
        for comment_dict in comments:
            if comment_info.replace(" ","") == comment_dict['Comment'].replace(" ",""):
                print("comment已经更新 无需再次更新")
                return True
        # 点击新建comment按钮
        self.Click(".//*[self::a[@title='New']]")
        time.sleep(5)

        add_comment_page_title = self.GetText(".//*[self::h2[@class='inlineTitle slds-p-top--large slds-p-horizontal--medium slds-p-bottom--medium slds-text-heading--medium']]")
        if add_comment_page_title == "":
            print("添加新comment失败")
            return None
        
        self.Send(".//*[self::textarea[@role='textbox']]", send_info=comment_info)

        if public_sign:
            self.Click(".//*[self::input[@type='checkbox']]")

        if save:
            # 保存按钮
            self.Click(".//*[self::button[@class='slds-button slds-button_neutral uiButton--brand uiButton forceActionButton']]")
        else:
            # 取消按钮
            self.Click(".//*[self::button[@class='slds-button slds-button_neutral uiButton--neutral uiButton forceActionButton']]")
        print("comment更新成功")
        return True

    def NewSetTag(self,info,old_tag=None):
        self.Click('//*[@id="detailTab__item"]')
        time.sleep(5)
        #device edit button
        self.WaitLoadingInfo(
            '//records-record-layout-block/slot/records-record-layout-section[10]/div/div/div/slot/records-record-layout-row[1]/slot/records-record-layout-item[1]/div/div/div[2]/button')
        self.browser.implicitly_wait(5)
        sign = False
        count = 0
        while count < 3:
            try:
                handles = self.browser.find_elements(By.XPATH, 
                    '//records-record-layout-block/slot/records-record-layout-section[10]/div/div/div/slot/records-record-layout-row[1]/slot/records-record-layout-item[1]/div/div/div[2]/span/slot[1]/lightning-formatted-text')
                text = handles[0].text.strip()
                text_list = text.split(",")
                if info in text_list:
                    # 标签已经存在
                    return
                if old_tag and old_tag in text_list:
                    # 存在需要被删除的标签
                    text_list.remove(old_tag)
                #点击编辑按钮
                edit_handles = self.browser.find_elements(By.XPATH, 
                    '//records-record-layout-block/slot/records-record-layout-section[10]/div/div/div/slot/records-record-layout-row[1]/slot/records-record-layout-item[1]/div/div/div[2]/button')
                self.browser.execute_script("arguments[0].scrollIntoView()", edit_handles[0])
                self.browser.execute_script("window.scrollBy(0,-200)")
                edit_handles[0].click()
                #清空编辑框
                input_handles = self.browser.find_elements(By.XPATH, 
                    '//records-record-layout-block/slot/records-record-layout-section[10]/div/div/div/slot/records-record-layout-row[1]/slot/records-record-layout-item[1]/div/span/slot/records-record-layout-base-input/lightning-input/lightning-primitive-input-simple/div/div/input')
                input_handles[0].clear()
                if text != '' and len(text_list):
                    #存在多个标签则连接生成新标签串
                    text_list.append(info)
                    info = ",".join(text_list)
                try:
                    input_handles[0].send_keys(info)
                except:
                    return
                cancel_handles = self.browser.find_elements(By.XPATH, 
                    '//records-form-footer/div/div/div/runtime_platform_actions-actions-ribbon/ul/li[1]/runtime_platform_actions-action-renderer/runtime_platform_actions-executor-lwc-headless/slot[1]/slot/lightning-button/button')
                save_handles = self.browser.find_elements(By.XPATH, 
                    '//records-form-footer/div/div/div/runtime_platform_actions-actions-ribbon/ul/li[2]/runtime_platform_actions-action-renderer/runtime_platform_actions-executor-lwc-headless/slot[1]/slot/lightning-button/button')
                time.sleep(3)
                if self.debug:
                    cancel_handles[0].click()
                else:
                    save_handles[0].click()
                count = 3
                sign = True
            except:
                self.browser.refresh()
                self.Click('//*[@id="detailTab__item"]')
                self.WaitLoadingInfo('//records-record-layout-block/slot/records-record-layout-section[10]/div/div/div/slot/records-record-layout-row[1]/slot/records-record-layout-item[1]/div/div/div[2]/button')
                count += 1

        return sign
    
    def UpdateReasonForCase(self):
        '''
        @Time    :   2024/07/18 15:23:56
        @功能    :   更新Reason for case
        '''
        xpath = "//records-record-layout-block/slot/records-record-layout-section[4]/div/div/dl/slot/records-record-layout-row[5]/slot/records-record-layout-item[1]/div/span/slot/records-record-picklist/records-form-picklist/lightning-picklist/lightning-combobox/div/div[1]/lightning-base-combobox/div/div/div[1]/button/span"

        # 定位下拉列表看
        # handle = self.browser.find_element(By.XPATH, xpath)
        handle = self.GetHandle(xpath)
        self.browser.execute_script("arguments[0].scrollIntoView()", handle)
        self.browser.execute_script("window.scrollBy(0,-200)")
        # 获得下拉列表看内容
        reason_for_case_text = self.GetText(xpath)
        if reason_for_case_text != "--None--":
            return
        # 点击 Reason for case 下拉框
        self.Click("//records-record-layout-block/slot/records-record-layout-section[4]/div/div/dl/slot/records-record-layout-row[5]/slot/records-record-layout-item[1]/div/span/slot/records-record-picklist/records-form-picklist/lightning-picklist/lightning-combobox/div/div[1]/lightning-base-combobox/div/div/div[1]/button")
        time.sleep(1)

        # 选择 Complex issue that requires input from multiple teams
        self.Click('//records-record-layout-block/slot/records-record-layout-section[4]/div/div/dl/slot/records-record-layout-row[5]/slot/records-record-layout-item[1]/div/span/slot/records-record-picklist/records-form-picklist/lightning-picklist/lightning-combobox/div/div[1]/lightning-base-combobox/div/div/div[2]/lightning-base-combobox-item[4]')
        time.sleep(1)
        
    def NewSetTag2(self, new_tag, del_tag=None):
        '''
        @Time    :   2024/07/18 13:10:56
        @功能    :   添加和删除tag
        del_tag:   需要被删除的tag
        '''
        #device edit button xpath
        edit_btn_xpath = '//records-record-layout-block/slot/records-record-layout-section[10]/div/div/dl/slot/records-record-layout-row[1]/slot/records-record-layout-item[1]/div/div/dd/div/button'
        
        def LocateDeviceButton():
            '''
            @Time    :   2024/07/18 13:24:19
            @功能    :   定位到需要的编辑按钮
            '''
            self.Click('//*[@id="detailTab__item"]')
            time.sleep(5)
            #device edit button
            self.WaitLoadingInfo(edit_btn_xpath)
            self.browser.implicitly_wait(5)
            pass
        
        LocateDeviceButton()
        sign, count = False, 0
        while count < 3:
            try:
                handle = self.browser.find_element(By.XPATH, 
                    '//records-record-layout-block/slot/records-record-layout-section[10]/div/div/dl/slot/records-record-layout-row[1]/slot/records-record-layout-item[1]/div/div/dd/div/span/slot/lightning-formatted-text')
                device_info = handle.text.strip()
                text_list = [tmp.strip() for tmp in device_info.split(",")]
                if new_tag in text_list:
                    # 标签已经存在
                    return
                
                # 更新tag
                if del_tag and del_tag in text_list:
                    # 存在需要被删除的标签
                    text_list.remove(del_tag)

                if device_info != '' and len(text_list):
                    #存在多个标签则连接生成新标签串
                    text_list.append(new_tag)
                    new_tag = ",".join(text_list)
                
                #点击编辑按钮
                edit_handles = self.browser.find_elements(By.XPATH, edit_btn_xpath)
                self.browser.execute_script("arguments[0].scrollIntoView()", edit_handles[0])
                self.browser.execute_script("window.scrollBy(0,-200)")
                edit_handles[0].click()
                time.sleep(3)

                #更新device 编辑内容 
                try:
                    input_handle = self.browser.find_element(By.XPATH, 
                        '//records-record-layout-block/slot/records-record-layout-section[10]/div/div/dl/slot/records-record-layout-row[1]/slot/records-record-layout-item[1]/div/span/slot/records-record-layout-base-input/lightning-input/lightning-primitive-input-simple/div/div/input')
                    input_handle.clear()
                    input_handle.send_keys(new_tag)
                    time.sleep(3)
                except: 
                    print("更新编辑内容失败, 直接退出该case")
                    return None
                
                self.UpdateReasonForCase()
                # 保存或者取消修改
                xpath_header = "//records-form-footer/div/div/div/runtime_platform_actions-actions-ribbon/ul/li"
                xpath_end = "runtime_platform_actions-action-renderer/runtime_platform_actions-executor-lwc-headless/slot[1]/slot/lightning-button/button"
                # self.debug = True
                if self.debug:
                    cancel_handle = self.browser.find_element(By.XPATH,f'{xpath_header}[1]/{xpath_end}')
                    cancel_handle.click()
                else:
                    save_handle = self.browser.find_element(By.XPATH, f'{xpath_header}[2]/{xpath_end}')
                    save_handle.click()
                return True
            except:
                print("点击Details失败, 加载失败或者details地址变更.重新尝试")
                self.browser.refresh()
                LocateDeviceButton()
                count += 1
        if not sign:
            print("始终无法点击Details, 加载失败或者details地址变更")
        return sign
    
    def SFLoadingError(self):
        '''
        @Time    :   2024/07/11 09:40:07
        @功能    :   网页加载失败显示的内容
        可能现在处理的情况不是唯一出现的情况
        进入每一个case之前应该做一次判断
        '''
        
        load_error = self.GetHandle(".//*[self::span[@jsselect='heading']]")
        if load_error is None:
            return False
        if load_error.text == "无法访问此网站":
            print("网页加载失败")
            return True
        else:
            return False

# Multiple issues being raised on parent case