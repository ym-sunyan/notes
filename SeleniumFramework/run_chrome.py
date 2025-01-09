# -*- encoding: utf-8 -*-
#python>=3.6
'''
@File    :   run.py
@Time    :   2024/02/23 13:04:56
@Author  :   sunyan
@Version :   1.0
@email   :   c_yansun
@Desc    :   None
'''

# here put the import lib
import os
import shutil
import logging
import traceback
from BaseInfo import BaseInfo
from ClassSendEmail import SendEmailC
from selenium_qti7 import SeleniumBaseClass, selenium_qti

BIC = BaseInfo().base_info_dict

logging.basicConfig(level = logging.DEBUG,
        # filename=logpath, # **** 需指定logpath的存储地址
        # filemode='a',
        # datefmt='%a, %d %b %Y %H:%M:%S',
        # stream=sys.stdout,
           encoding='utf-8',                   #不设置编码可能乱码
        format = '%(asctime)s - %(name)s - [%(funcName)s]-%(module)s-logger: %(name)s- %(lineno)d - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#logging 用例如下
#logger.info('流程输出与信息，观察整体执行')
#logger.debug('输出调试信息，信息更加全面')
#logger.warning('某种原因已发的警告信息，但是系统可以正常的运行')
#logger.error('程序异常自我修复，不能正常运行')
#logger.fatal('比error错误更加严重的错误')

def log_exceptions_to_file(file_name=rf'{os.getcwd()}\error_info.log'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                with open(file_name, 'a') as f:
                    traceback.print_exception(type(e), e, e.__traceback__, file=f)
                    traceback.print_tb(e.__traceback__, file=f)
                    traceback.print_exc(file=f)
        return wrapper
    return decorator
# #  使用装饰器 demo
# @log_exceptions_to_file()
# def divide(x, y):
#     return x / y
# #  调用函数，模拟出现异常
# divide(1,  0)

def VirtualChromeMain():
    '''
    @Time    :   2023/11/29 17:54:53
    @功能    :   打开虚拟浏览器
    '''
    qti = SeleniumBaseClass(browser=None,
                    url=BIC["base_url"],
                    chromedriver_path=BIC['chromedriver_path'])
    qti.OpenBaseChrome(virtual_browser=True)
    qti.Close()

    pass

def CopyChromeMain():
    '''
    @Time    :   2023/11/29 17:54:53
    @功能    :   打开基于真实浏览器数据的虚拟浏览器
    '''

    qti = selenium_qti(browser=None,
                    url="https://qualcomm-cdmatech-support.lightning.force.com/lightning/r/Report/00O4V000008pGEoUAM/view",
                    chromedriver_path=BIC['chromedriver_path'],
                    google_data_path=BIC['google_data_path'],
                    debug=True)
    qti.OpenChrome()
    qti.Close()
    # 删除user_data
    shutil.rmtree(BIC['google_data_path'])
    pass

def ChromeMain():
    '''
    @Time    :   2023/11/29 17:54:53
    @功能    :   运行真实浏览器
    此时chorme浏览器不可以打开，必须关闭
    '''
    qti = SeleniumBaseClass(browser=None,
                    url="https://qualcomm-cdmatech-support.lightning.force.com/lightning/r/Report/00O4V000008pGEoUAM/view",
                    chromedriver_path=BIC['chromedriver_path'],)
    qti.OpenBaseChrome()
    qti.Close()
    pass


if __name__ == '__main__':
    VirtualChromeMain() #运行虚拟chrome 
    CopyChromeMain()    #运行基于真实chorme use data的chrome
    ChromeMain()        #运行真实chrome
    try:
        VirtualChromeMain() #运行虚拟chrome 
        CopyChromeMain()    #运行基于真实chorme use data的chrome
        ChromeMain()        #运行真实chrome
    except:
        title = f'python selenium 程序运行异常'
        email_info = rf'''python auto copilot 程序运行异常: {os.getcwd} '''
        sec = SendEmailC(BIC['from_'], BIC['to_'], BIC['cc_'], title=title,email_info=email_info)
        sec.SendEamilText()
    pass

