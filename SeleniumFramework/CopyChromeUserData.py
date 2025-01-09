'''
@File    :   BaseChromeThread.py
@Time    :   2021/08/31 10:04:16
@Author  :   sunyan
@Version :   1.0
@email   :   c_yansun
@Desc    :   copy user data
'''
'将路径导入系统环境变量'
import os
import codecs
import shutil
import getpass

class CopyUserData(object):
    '''
    @Time    :   2021/10/28 10:31:54
    @Author  :   sunyan
    @Desc    :   user data 自动化拷贝和更新'''
    def __init__(self, from_path, to_path=None, auto_copy=False, del_userdata=False):
        self.from_path = from_path
        self.to_path = to_path
        self.del_userdata = del_userdata
        self.download_path = "LOG" #存储下载文件的文件夹
        self.finish_copy_sign_file = "finish_copy.user_data" #完整copy user data将会生成该文件
        self.auto_copy = auto_copy #True,类调用直接拷贝，无需明显调用copy函数；False则需要明确调用copy函数
        self.Check()
        self.ReadMe()
        self.DelUserData()
        if self.auto_copy:
            self.CopyChrome()

    def Check(self):
        '''
        @Time    :   2021/10/28 10:45:34
        @功能    :   类传入的变量检测
        '''
        if not os.path.isdir(self.from_path):
            print(rf"user data path: {self.from_path} error")
            exit()

        if self.to_path == None:
            print(rf"copy user data 的目的地址: {self.from_path} error")
            exit()

        if not os.path.isdir(self.to_path):
            os.makedirs(self.to_path)

    def DelUserData(self, del_sign=None):
        '''
        @Time    :   2021/10/28 11:21:18
        @功能    :   删除已经存在的to_path
        '''
        if del_sign != None or self.del_userdata == True:
            try:
                shutil.rmtree(self.to_path)
            except:
                print(f"del {self.del_userdata} error")
        pass
    
    def ReadMe(self):
        '''
        @Time    :   2021/10/28 10:59:33
        @功能    :   None
        '''
        print("""
        类参数说明：
        from_path: user data地址
        to_path：user data copy的目标地址
        del_userdata：默认值False，不删除已经存在的to_path；True表示每次copy之前都强制删除原有to_path文件夹
        download_path #在userdata下创建下载文件夹
        inish_copy_sign_file #完整copy user data将会生成该文件
        auto_copy #True,类调用直接拷贝，无需明显调用copy函数；False则需要明确调用copy函数""")
        pass
        
    def CopyUserData(self, chrome_userdata_path, user_data_folder):
        '''
        @Time    :   2021/07/29 13:26:04
        @功能    :   copy user data
        '''
        if not os.path.isdir(user_data_folder):
            os.makedirs(user_data_folder)
        copy_list = [rf"{chrome_userdata_path}\{folder}" for folder in os.listdir(chrome_userdata_path) if folder != "Default"]
        folder_list, file_list = [], []
        for folder in copy_list:
            if os.path.isdir(folder):
                folder_list.append(folder)
            else:
                file_list.append(folder)
        for folder in folder_list:
            tmp = os.path.split(folder)[1]
            try:
                shutil.copytree(folder, rf"{user_data_folder}\{tmp}")
            except:
                print("主chrome浏览器处于启动中，虽然不影响copy结果，但是还是建议关闭")
        for file in file_list:
            new_path = file.replace(chrome_userdata_path, user_data_folder)
            path = os.path.split(new_path)[0]
            try:
                shutil.copy2(file, path)
            except:
                print("主chrome浏览器处于启动中，虽然不影响copy结果，但是还是建议关闭")

    def CopyDefault(self, chrome_userdata_path, user_data_folder):
        '''
        @Time    :   2021/07/29 13:26:04
        @功能    :   copy user data/Default
        '''
        default_path = rf"{chrome_userdata_path}\Default"
        copy_list = [rf"{default_path}\{folder}" for folder in os.listdir(default_path) if folder not in ["Cache", "Code Cache", "Service Worker"]]
        folder_list, file_list = [], []
        for folder in copy_list:
            if os.path.isdir(folder):
                folder_list.append(folder)
            else:
                file_list.append(folder)
        new_default_path = rf"{user_data_folder}\Default"
        if not os.path.isdir(new_default_path):
            os.makedirs(new_default_path)
        for folder in folder_list:
            tmp = os.path.split(folder)[1]
            try:
                shutil.copytree(folder, rf"{new_default_path}\{tmp}")
            except:
                print("主chrome浏览器处于启动中，虽然不影响copy结果，但是还是建议关闭")
        for file in file_list:
            tmp_file = file.replace(default_path, new_default_path)
            path = os.path.split(tmp_file)[0]
            try:
                shutil.copy2(file, path)
            except:
                print("主chrome浏览器处于启动中，虽然不影响copy结果，但是还是建议关闭")
        # with codecs.open(rf"{user_data_folder}\{self.finish_copy_sign_file}", "w", "utf-8") as f:
        #     f.write("finish copy")
        self.CreateAndReadSignFile(rf"{user_data_folder}\{self.finish_copy_sign_file}", "w")

    def CreateAndReadSignFile(self, sign_file, model=None):
        '''
        @Time    :   2022/12/27 09:08:25
        @功能    :   创建或者读取标记文件
        model参数值为None 表示每次必须强制更新UserData
        '''
        import time
        now_time = time.time()
        if model == "w":
            with codecs.open(sign_file, model, "utf-8") as f:
                f.write(f"finish copy\n{now_time}")
        elif model == "w":
            with codecs.open(sign_file, model, "utf-8") as fr:
                lines = fr.readlines()
            copy_time = int(lines[1])
            if now_time-copy_time>=12*60*60:
                return True
            return False
        else:
            print("Force Update chrome userData")
            return None
    
    def CopyChrome(self, from_path=None, to_path=None):
        '''
        @Time    :   2021/09/01 13:19:58
        @功能    :   None
        '''
        if to_path == None:
            to_path=self.to_path
        if from_path == None:
            from_path = self.from_path

        # user data; copy完成后生成finish_copy_sign_file参数指定的文件
        if not os.path.isfile(rf"{to_path}\{self.finish_copy_sign_file}"):
            self.CopyUserData(from_path, to_path)
            self.CopyDefault(from_path, to_path)

        download_path = rf"{to_path}\{self.download_path}"
        if not os.path.isdir(download_path):
            os.makedirs(download_path)

        if not os.path.isfile(rf"{to_path}\{self.finish_copy_sign_file}"):
            print("copy user data failed")
            exit()
            
        chrome_path = to_path
        return chrome_path, download_path
    pass

# if __name__ == '__main1__':
#     from_path = rf"C:\Users\{getpass.getuser()}\AppData\Local\Google\Chrome\User Data"
#     to_path = rf"C:\SY_QTI_2021\yan\SeleniumAutoFramework_4.0\user_data"
#     cud = CopyUserData(from_path=from_path, to_path=to_path, del_userdata=True)
#     print(cud.CopyChrome())
#     pass
