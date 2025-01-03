import os
import time
import PySimpleGUI as sg
# import PySimpleGUIQt as sg

# sg.theme('DarkBlue3') # 设置主题
placeholder = '''添加需要翻译的头部信息
将 "文本内容："后面的【】内的文本仅仅翻译为中文，不要做其他任何和额外的事情.
比如：
【PySimpleGUI Generating a minimal GUI interface】
输出：
【PySimpleGUI 生成一个最简单的GUI界面】
文本内容：
'''
# 文本内容：【In Elasticsearch, in addition to the default text processing, you may consider adding the following text processing methods to enhance your search and analysis capabilities】

# 设置窗口布局
menu_def = [['文件', ['打开', '另存为', '退出']],
            ['设置', ['设置界面颜色']],
            ['关于', '关于']] 

toolbar = [
    # sg.Button('打开'), sg.Button('保存'), sg.Button('另存为')
    ]

tab1_layout = [
    [sg.Frame('', [
        [
            sg.Radio("中 译 英", "trans", key='英文', pad=(10, 10)), 
            sg.Radio("英 译 中", "trans", key='中文', pad=(10, 10), default=True),
        ],
        ], 
        element_justification='center', 
        background_color="white", 
        expand_x=True, 
        border_width=0)
    ],
    # [sg.Text('翻译文件路径', background_color="white", text_color="black")]
    # +[sg.In(key="file_path", expand_x=True)]
    # +[sg.FileBrowse('导入文件', file_types=(("Text Files", "*.txt"), ("INI Files", "*.ini"), ("JSON Files", "*.json")), key="load_file")],
    [
        sg.Text('翻译文件路径', background_color="white", text_color="black"),
        sg.In(key="file_path", enable_events=True, expand_x=True),
        sg.FileBrowse('导入文件', file_types=(("Text Files", "*.txt"), ("INI Files", "*.ini"), ("JSON Files", "*.json")), key="load_file")
    ],
    [
        sg.ProgressBar(100, orientation='h', expand_x=True, size=(20, 20),  key='-PBAR-',visible=False), 
    ],
    [
        sg.Text('', key='-OUT-', size=(20 , 1), enable_events=True, font=('Arial Bold', 16), justification='center', expand_x=True,visible=False),
    ],
    [sg.Frame('', [
        [
            sg.Pane([
                sg.Column([
                    [sg.Multiline(default_text=placeholder,size=(60, 33), key='multiline', autoscroll=True, enable_events=True, expand_x=True, expand_y=True)]
                ], expand_x=True, expand_y=True)
            ], orientation='vertical', expand_x=True, expand_y=True)
        ]
        ],
        element_justification='center', 
        background_color="white", 
        expand_x=True, 
        border_width=0)
    ],
    [sg.Button('翻译', key="translate", size=(30 , 3), expand_x=True,font=('Helvetica', 16))],
]

tab2_layout = [[sg.Button('B Demo')]]
tab3_layout = [[sg.Button('C Demo')]]

layout = [
    [sg.Menu(menu_def)],
    [toolbar],
    [sg.TabGroup(
        [[
            sg.Tab('Copilot 翻译', tab1_layout, background_color="white"), 
            sg.Tab('Copilot 搜索', tab2_layout), 
            sg.Tab('其他', tab3_layout)
        ]], 
        expand_x=True, 
        expand_y=True, 
        background_color="white"
        )
    ],
    [sg.Text('版本信息：1.0.0', 
        size=(60, 1), 
        justification='center', 
        background_color='white',
        text_color='#808080',
        expand_x=True)
    ]
]

# 创建窗口
window = sg.Window('Copilot GUI', 
                   layout, 
                   size=(1000, 800), 
                   background_color='white', 
                   resizable=False #禁止修改窗口大小
                   )

def clear_placeholder(window, key, placeholder):
    if window[key].get() == placeholder:
        window[key].update('')

def restore_placeholder(window, key, placeholder):
    if window[key].get() == '':
        window[key].update(placeholder)

# 事件循环
while True:
    try:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '退出':
            break
        elif event == 'multiline':
            clear_placeholder(window, 'multiline', placeholder)
        elif event == sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED:
            restore_placeholder(window, 'multiline', placeholder)
        elif event == 'multilineFocusOut':
            restore_placeholder(window, 'multiline', placeholder)
        elif event == '关于':
            sg.popup('这是一个使用 PySimpleGUI 创建的示例应用。')
        elif event == '设置界面颜色':
            sg.popup('设置界面颜色功能尚未实现。')
        elif event == '打开':
            sg.popup('打开文件功能尚未实现。')
        elif event == '另存为':
            sg.popup('另存为功能尚未实现。')
        elif event == '保存':
            sg.popup('保存文件功能尚未实现。')
        elif event =="translate":
            if values['load_file'].strip() == "" and values['multiline'].strip() == placeholder.strip():
                sg.popup('''
                         加载翻译文件
                         或者 
                         在文本框中输入需要翻译的内容
                         ''', title="错误警告")
            else:
                window['translate'].update(disabled=True)  #设置翻译按钮：不可操作
                # 控制进度条的显示
                window['-PBAR-'].update(visible=True)       #显示进度条
                # window['-OUT-'].update(visible=True)        #显示进度信息
                # window['multiline'].update(size=(20, 28))   # 设置多行文本框的高度
                for i in range(1, 11):
                    window['-PBAR-'].update(current_count=i*10)
                    # window['-OUT-'].update(str((i+1)*10))
                    if i*10 == 100: break
                    time.sleep(1)
                sg.popup(r'''
                         翻译已经完成，文件存储在
                         \\10.233.202.137\Dropbox\zhiguo\小说
                         ''', title="提示信息"
                )
                window['translate'].update(disabled=False)  #设置翻译按钮：可操作
                window['-PBAR-'].update(visible=False)      #隐藏进度条
                # window['-OUT-'].update(visible=False)       #隐藏进度信息
                # window['multiline'].update(size=(20, 33))   #设置多行文本框的高度
        elif event == 'load_file':
            file_path = values['load_file']
            window['file_path'].update(file_path)
        # if values['英文']:
        #     sg.popup('你选择了：中 译 英')
        # elif values['中文']:
        #     sg.popup('你选择了：英 译 中')


        # if values['file_path'].strip() != "":
        #     # window['multiline'].update(disabled=True) #禁用某个元素

        if event == 'Cancel':
            window['-PBAR-'].update(max=100)
        
    except Exception as e:
        print(f"错误信息: {e}")
window['multiline'].bind('<FocusOut>', 'FocusOut')

window.close()
