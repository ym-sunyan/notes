# -*- encoding: utf-8 -*-
#python>=3.6
'''
@File    :   监控.py
@Time    :   2025/01/13 16:09:14
@Author  :   sunyan
@Version :   1.0
@email   :   c_yansun
@Desc    :   监控桌面所有的程序
1 监控某些网页、某些应用是否打开 缺点需要知道应用和网站的名称才可以
    不允许特定的网站、应用外其他应用打开
2 阻止应用的安装
'''
import os
import time
import win32api
import win32gui
import win32con
import win32security
import win32event
import win32file
import win32process
import win32service
import win32serviceutil
import tkinter as tk
from tkinter import messagebox

def enum_windows_callback(hwnd, results):
    if win32gui.IsWindowVisible(hwnd):
        window_title = win32gui.GetWindowText(hwnd)
        if window_title:
            results.append((hwnd, window_title))

def get_open_windows():
    open_windows = []
    win32gui.EnumWindows(enum_windows_callback, open_windows)
    return open_windows

def close_window_by_title(window_title):
    open_windows = get_open_windows()
    for hwnd, title in open_windows:
        if title == window_title:
            # win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0) #关闭窗口，则会提示是否退出
            win32gui.PostMessage(hwnd, win32con.WM_QUIT, 0, 0)  #发送 WM_QUIT 消息可以结束消息循环，从而关闭应用程序，但不会弹出确认对话框。
            print(f"关闭窗口: {title}")
            return True
    print(f"未找到窗口: {window_title}")
    return False


AUTHORIZED_SOFTWARE = ["chrome", "firefox", "python", "vscode"]

def monitor_software_installation():
    # 获取当前安装的软件列表
    installed_software = get_installed_software()
    # 将已安装软件的名称存储到一个集合中，方便后续快速查找
    # installed_software_names = {software["DisplayName"]["name"] for software in installed_software if software["DisplayName"]["name"]}
    installed_software_names = [software["DisplayName"]["name"] for software in installed_software if software["DisplayName"]["name"]]

    # 监控注册表或文件系统的变化
    while True:
        # 再次获取当前安装的软件列表
        new_installed_software = get_installed_software()
        # 检查是否有新软件安装
        for software in new_installed_software:
            software_name = software["DisplayName"]["name"]
            if software_name and software_name not in installed_software_names and software_name.lower() not in [s.lower() for s in AUTHORIZED_SOFTWARE]:
                # 弹出提示框让用户确认是否安装
                root = tk.Tk()
                root.withdraw()  # 隐藏主窗口
                response = messagebox.askyesno("软件安装确认", f"是否允许安装软件：{software_name}？")
                if not response:
                    # 如果用户选择不允许安装，则阻止安装
                    block_installation(software_name)
                # 更新已安装软件名称集合
                installed_software_names.add(software_name)
        
        # 每隔一段时间检查一次
        time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(time_str)
        time.sleep(1)

def 获得安装软件的信息(name, software_info, sub_key, info):
    '''
    @Time    :   2025/01/13 16:45:58
    @功能    :   获得软件的name字段信息
    '''
    tmp = {"name":None, "description":info}
    try:
         tmp["name"] =  win32api.RegQueryValueEx(sub_key, name)[0] if win32api.RegQueryValueEx(sub_key, name) else None
    except: pass
    software_info[name] = tmp

def get_installed_software():
    """
    获取当前系统中已安装的软件列表及其详细信息。
    返回一个包含软件信息的字典列表。
    """
    installed_software = []
    try:
        # 打开注册表中的Uninstall键
        reg_key = win32api.RegOpenKey(
            win32con.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            0, win32con.KEY_READ
        )
        
        # 遍历所有子键
        for i in range(win32api.RegQueryInfoKey(reg_key)[0]):
            sub_key_name = win32api.RegEnumKey(reg_key, i)
            sub_key = win32api.RegOpenKey(reg_key, sub_key_name)
            software_info = {}
            获得安装软件的信息("DisplayName", software_info, sub_key, "软件的名称，显示在控制面板的“程序和功能”中。")

            获得安装软件的信息("DisplayVersion", software_info, sub_key, "软件的版本号，通常为x.y.z格式。")

            获得安装软件的信息("Publisher", software_info, sub_key, "软件的发布者或开发商名称。")
            
            获得安装软件的信息("InstallLocation", software_info, sub_key, "软件的安装路径，通常是程序的主目录。")

            获得安装软件的信息("UninstallString", software_info, sub_key, "用于卸载该软件的命令行或可执行文件路径。")

            获得安装软件的信息("InstallDate", software_info, sub_key, "软件的安装日期，格式通常为YYYYMMDD。")

            获得安装软件的信息("EstimatedSize", software_info, sub_key, "软件的估计大小，以KB为单位。")

            获得安装软件的信息("DisplayIcon", software_info, sub_key, "软件的图标路径，通常用于在控制面板中显示。")

            获得安装软件的信息("HelpLink", software_info, sub_key, "软件的帮助或支持链接，通常指向官方网站。")

            获得安装软件的信息("URLUpdateInfo", software_info, sub_key, "软件的更新信息链接，通常指向更新服务器。")

            获得安装软件的信息("ModifyPath", software_info, sub_key, "用于修改软件安装的命令行或可执行文件路径。")

            获得安装软件的信息("QuietUninstallString", software_info, sub_key, "用于静默卸载软件的命令行或可执行文件路径。")

            获得安装软件的信息("RepairPath", software_info, sub_key, "用于修复软件安装的命令行或可执行文件路径。")

            installed_software.append(software_info)
    except Exception as e:
        print(f"Error reading registry: {e}")
    
    return installed_software

def block_installation(software_name):
    # 阻止软件安装的逻辑
    # 这里只是一个简单的示例，实际应用中需要更复杂的逻辑
    print(f"阻止安装: {software_name}")
    # 你可以尝试终止安装进程或删除安装文件
    # 例如：查找并终止与软件安装相关的进程
    try:
        for proc in win32process.EnumProcesses():
            try:
                hProcess = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, proc)
                exe_name = win32process.GetModuleFileNameEx(hProcess, 0)
                if software_name.lower() in exe_name.lower():
                    win32api.TerminateProcess(hProcess, 0)
                    print(f"已终止进程: {exe_name}")
            except Exception as e:
                pass
    except Exception as e:
        print(f"Error terminating process: {e}")

# if __name__ == "__main__":
#     monitor_software_installation()


if __name__ == "__main__":
    print("获得当前已经打开的所有网站和应用，并且关闭不允许打开的网站")
    # 可以控制安装进程，但是需要注意不同的安装场景
    open_windows = get_open_windows()
    open_names_list = [window[1] for window in open_windows]
    while 1:
        new_open_windows = get_open_windows()
        print(len(new_open_windows))
        for index, window in enumerate(new_open_windows):
            if window[1] not in open_names_list:
                print(f"index: {index}:{window[1]}")
                # 弹出提示框让用户确认是否安装
                window_title_to_close = window[1]  # 替换为您想要关闭的窗口标题
                close_window_by_title(window_title_to_close)


        # 每隔一段时间检查一次
        time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(time_str)
        time.sleep(10)

    # 关闭特定窗口
    window_title_to_close = "'Anaconda3 2024.06-1 (64-bit) Setup'"  # 替换为您想要关闭的窗口标题
    close_window_by_title(window_title_to_close)

