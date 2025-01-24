# -*- encoding: utf-8 -*-
#python>=3.6
'''
@File    :   WeChatRead.py
@Time    :   2025/01/07 17:39:48
@Author  :   sunyan
@Version :   1.0
@email   :   c_yansun
@Desc    :   从微信阅读中提取书本内容
'''
# here put the import lib
import codecs
import time
from time import sleep
from BaseInfo import BaseInfo
from selenium_qti7 import selenium_qti
import base64
import io
from PIL import Image
import requests
from bs4 import BeautifulSoup
import re
import os
import traceback


BIC = BaseInfo().base_info_dict
chrome_handle_dict = {}

def SaveImage(base64_image):
    '''
    @Time    :   2025/01/15 15:44:32
    @功能    :   保存canvas中获得的图片
    '''
    # 处理Base64编码的图片
    if base64_image:
        # 去掉DataURL的前缀
        image_data = base64_image.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # 保存图片到文件
        with open('canvas_image.png', 'wb') as f:
            f.write(image_bytes)
        
        # 或者使用PIL库处理图片
        image = Image.open(io.BytesIO(image_bytes))
        image.show()
    pass

def GetwereadQQBookAllUrl(qti,  begin_url, save_file, begin_index=None, max_url_length=None):
    '''
    @Time    :   2025/01/07 13:09:12
    @功能    :   获得微信读书中，某本书的所有的url
    '''
    qti.browser.get(begin_url)
    url_list = []
    while 1:
        next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
        if next_handle is None:
            break
        next_handle.click()
        sleep(1)
        url_list.append(qti.browser.current_url)
        if max_url_length is not None and len(url_list) == max_url_length:
            break
        pass

    with codecs.open(save_file, "w", "utf-8") as fw:
        fw.write("\n".join(url_list))
    pass

def GetwereadQQBookAllUrlV2(qti,  begin_url, save_file, begin_index=0, max_url_length=None):
    '''
    @Time    :   2025/01/07 13:09:12
    @功能    :   获得微信读书中，某本书的所有的url
    '''
    qti.browser.get(begin_url)
    if begin_index == 0:
        with codecs.open(save_file, "a+", "utf-8") as fw:
            fw.write(f"{begin_index};{begin_url}\n")
        begin_index = 1
    index, url_list =begin_index, []
    while 1:
        next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
        if next_handle is None: break
        next_handle.click()
        sleep(1)
        url_list.append(qti.browser.current_url)
        with codecs.open(save_file, "a+", "utf-8") as fw:
            fw.write(f"{index};{qti.browser.current_url}\n")
        index += 1
        if max_url_length is not None and len(url_list) == max_url_length:
            break
    return 

def GetwereadQQBookAllUrlV3(qti,  begin_url, save_file, begin_index=0, max_url_length=None):
    '''
    @Time    :   2025/01/07 13:09:12
    @功能    :   获得微信读书中，某本书的所有的url
    这里需要区分：下一页和下一章的区别，从现有的目录结构来看下一章需要切换url，但是下一页不需要切换url
    '''
    qti.browser.get(begin_url)
    if begin_index == 0:
        with codecs.open(save_file, "a+", "utf-8") as fw:
            fw.write(f"{begin_index};{begin_url}\n")
        begin_index = 1
    index, url_list =begin_index, []
    sleep(1)
    while 1:
        next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
        if next_handle is None: 
            break
        next_handle.click()
        sleep(1)
        update_url = False
        if qti.browser.current_url not in url_list:
            update_url = True
            url_list.append(qti.browser.current_url)
        with codecs.open(save_file, "a+", "utf-8") as fw:
            if not update_url:
                fw.write(f"{index};与上一个url形同。需要通过点击下一页/下一章 查看下一页/下一章内容\n")
            else:
                fw.write(f"{index};{qti.browser.current_url}\n")
        index += 1
        if max_url_length is not None and len(url_list) == max_url_length:
            break
    return 

def GetwereadQQBookAllUrlV4(qti,  begin_url, save_file, begin_index=0, max_url_length=None):
    '''
    @Time    :   2025/01/07 13:09:12
    @功能    :   获得微信读书中，某本书的所有的url
    这里需要区分：下一页和下一章的区别，从现有的目录结构来看下一章需要切换url，但是下一页不需要切换url
    新的目录模式：点击下一页页面没有跳转只是
    '''
    qti.browser.get(begin_url)
    if begin_index == 0:
        with codecs.open(save_file, "a+", "utf-8") as fw:
            fw.write(f"{begin_index};{begin_url}\n")
        begin_index = 1
    index, url_list =begin_index, []
    while 1:
        next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
        if next_handle is None: 
            break
        next_handle.click()
        sleep(1)
        update_url = False
        if qti.browser.current_url not in url_list:
            update_url = True
            url_list.append(qti.browser.current_url)
        with codecs.open(save_file, "a+", "utf-8") as fw:
            if not update_url:
                fw.write(f"{index};与上一个url形同。需要通过点击下一页/下一章 查看下一页/下一章内容\n")
            else:
                fw.write(f"{index};{qti.browser.current_url}\n")
        index += 1
        if max_url_length is not None and len(url_list) == max_url_length:
            break
    return 

def MainDemo():
    '''
    @Time    :   2022/10/31 09:50:22
    @功能    :    
    '''

    # qti = selenium_qti(
    #                    url='https://weread.qq.com/web/reader/a57325c05c8ed3a57224187',
    #                    chromedriver_path=BIC['chromedriver_path'])
    # qti.OpenChrome()
    # 下一章
    # # next_handle = qti.GetHandle(".//self::button[@class='readerFooter_button']")
    # next_handle = qti.GetHandles(xpath=".//self::div[@class='renderTarget_pager']//button")[1].click()
    # next_handle.click()
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Cookie":"wr_avatar=; wr_fp=2426543452; wr_gid=296512876; wr_vid=914251122; wr_rt=web%40ZxXPwZxXQT9ft4HpyvT_AL; wr_localvid=36d32d708367e5d7236d613; wr_name=%E5%BE%AE%E4%BF%A1%E7%94%A8%E6%88%B7; wr_gender=0; wr_pf=NaN; wr_skey=jz3HBZfZ"
    }
    url = "https://weread.qq.com/web/reader/a57325c05c8ed3a57224187k8f132430178f14e45fce0f7"
    # qti = selenium_qti(
    #                    url='https://weread.qq.com/web/reader/a57325c05c8ed3a57224187',
    #                    chromedriver_path=BIC['chromedriver_path'])
    qti = selenium_qti(browser=None,
                       url='https://weread.qq.com/web/reader/a57325c05c8ed3a57224187',
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                       debug=False)
    qti.OpenChrome()

    begin_url = "https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180"
    save_file = "url_list.txt"
    GetwereadQQBookAllUrl(qti, begin_url, save_file)

    with codecs.open(save_file, "r", "utf-8") as fr:
        lines = fr.readlines()
    
    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    // 存储绘制的文本内容及其位置信息
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });

    // 调用原始方法继续正常渲染
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    // 存储绘制的文本内容及其位置信息
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });

    // 调用原始方法继续正常渲染
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    // 按照 y 坐标排序，模拟自然阅读顺序
    const sortedText = capturedText.sort((a, b) => {
        // 首先按 y 坐标排序
        if (Math.abs(a.y - b.y) > 10) { // 允许 10px 的误差范围
            return a.y - b.y;
        }
        // y 坐标相近时按 x 坐标排序
        return a.x - b.x;
    });

    // 将文本内容提取出来
    return sortedText.map(item => item.text).join(' ');
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};
'''
    
    print(canvas_info)
    for index in range(len(lines)):
    # for index, line in enumerate(lines):
        # 注入js之后需要更换页面内容才可以使用 getCapturedText 获得最新的内容，因此需要向上翻一页之后再点击下一章才可以获得当前章节内容
        # 所以url才需要向下面一样向上取一个
        if index == 0:  url = begin_url
        else:           url =  lines[index-1].strip()
        qti.browser.get(url)
        # 注入js
        qti.browser.execute_script(script)
        # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
        next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
        if next_handle is None:
            break
        next_handle.click()
        # 获取内容
        canvas_info = qti.browser.execute_script("return getCapturedText();")

        # 清除捕获的文本内容
        qti.browser.execute_script("clearCapturedText();")

        # 恢复原始方法
        qti.browser.execute_script("restoreOriginalMethods();")


    # 打开微信读书网页版并登录
    qti.browser.get(url)

    # # 等待用户手动登录完成

    # # 关闭浏览器
    # qti.browser.quit()

    # import io
    # import base64
    # from PIL import Image
    # canvas = qti.GetHandles(xpath=".//self::canvas")
    # canvas_base64 = qti.browser.execute_script("return arguments[0].toDataURL('image/png').substring(22);", canvas[0])
    # image_bytes = base64.b64decode(canvas_base64)
    # image = Image.open(io.BytesIO(image_bytes))
    # # 保存图像到本地文件
    # image.save('canvas_image.png')


    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    // 存储绘制的文本内容及其位置信息
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });

    // 调用原始方法继续正常渲染
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    // 存储绘制的文本内容及其位置信息
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });

    // 调用原始方法继续正常渲染
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    // 按照 y 坐标排序，模拟自然阅读顺序
    const sortedText = capturedText.sort((a, b) => {
        // 首先按 y 坐标排序
        if (Math.abs(a.y - b.y) > 10) { // 允许 10px 的误差范围
            return a.y - b.y;
        }
        // y 坐标相近时按 x 坐标排序
        return a.x - b.x;
    });

    // 将文本内容提取出来
    return sortedText.map(item => item.text).join(' ');
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};
'''
    # 注入js
    qti.browser.execute_script(script)
    
    # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容

    # 获取内容
    canvas_info = qti.browser.execute_script("return getCapturedText();")

    # 清除捕获的文本内容
    qti.browser.execute_script("clearCapturedText();")

    # 恢复原始方法
    qti.browser.execute_script("restoreOriginalMethods();")

    print(canvas_info)
    # 获得所有的章节url列表
 
    qti.Close()

def 微信读书Main(begin_url, book_name=None):
    '''
    @Time    :   2022/10/31 09:50:22
    @功能    :    该函数只能获取所有已经绘制在canvas中的文本内容，
    以及穿插在文本中的上传的图片
    '''
    qti = selenium_qti(browser=None,
                       url='https://weread.qq.com/',
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                    #    virtual_chrome=True, # 使用虚拟浏览器
                       debug=False)
    qti.OpenChrome()
    # qti.OpenBaseChrome(virtual_browser=True)
    # 最大化浏览器窗口
    qti.browser.maximize_window()

    if book_name is None:
        time_str = time.strftime('%Y_%m_%d',time.localtime(time.time()))
        book_name = f"微信阅读_{time_str}"

    save_file = rf"{BIC['base_path']}\url_list_{book_name}.txt"
    save_book = rf"{BIC['base_path']}\{book_name}.md"

    try:
        # 中途异常退出
        with codecs.open(save_file, "r", "utf-8") as fr:
            url_lines = fr.readlines()
    except:
        # 首次执行
        url_lines = []

    qti.browser.get(begin_url)
    sleep(5)
    # 使用包含类名 isHorizontalReader 的 XPath 定位元素
    # 类中包含 isHorizontalReader 表示处于双页阅读；isNormalReader 表示处于滚动阅读
    read_model_handle = qti.GetHandle(".//self::button[contains(@class, 'isHorizontalReader')]")
    if read_model_handle is not None:
        read_model_handle.click()
    # # 如果要获得目录的标题需要先展开目录才行
    # qti.Click(".//self::button[@class='readerControls_item catalog']")
    # sleep(1)
    # 获取目录数量. 包含匹配的方式获取

    begin_index = 0
    # if url_lines == []:
    #     GetwereadQQBookAllUrlV3(qti, begin_url, save_file, begin_index=begin_index)
    # else:
    #     contents_handles = qti.GetHandles(".//self::li[contains(@class, 'readerCatalog_list_item')]")
    #     # for index, content in enumerate(contents_handles):
    #     #     # 如果没有登录账号，那么只能获取免费的目录
    #     #     print(f"{index}; {content.text}") #content.text 需要先展开书的目录
    #     if contents_handles is not None:
    #         # 获取书所有的章节url
    #         last_url = url_lines[-1].split(";")[-1].strip()
    #         begin_index = len(url_lines)

    #     if begin_index != len(contents_handles):
    #         GetwereadQQBookAllUrlV3(qti, last_url, save_file, begin_index=begin_index)


    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法， 在调用时将文本内容及其位置、样式等信息存储到 capturedText 数组中，然后调用原始的 fillText 方法。
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline,
            fontSize: this.font.split('px')[0], // 字体大小
            lineHeight: this.font.split('px')[0] * 1.2, // 行高
            textWidth: this.measureText(text).width, // 文本宽度
            textLines: text.split('\\n').length // 文本行数
        }
    });
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法，功能与 fillText 方法类似，将文本内容及其相关信息存储到 capturedText 数组中，然后调用原始的 strokeText 方法。
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    debugger
    console.log(capturedText)
    const sortedText = capturedText.sort((a, b) => {
        if (Math.abs(a.y - b.y) > 10) {
            return a.y - b.y;
        }
        return a.x - b.x;
    });

    let result = '';
    let contents_arr = [];
    let lastY = null;
    let last_style = null;
    sortedText.forEach(item => {
        if (lastY !== null && Math.abs(item.y - lastY) > 40) {
            result += '\\n'; // 插入换行符
            //result += "YYY:"+lastY+'\\n'; // 插入换行符
            contents_arr.push({
                "Y":lastY,
                "content":result,
                "item":last_style
            })
            result = ""
        }
        result += item.text + '';
        lastY = item.y;
        last_style = item
    });
    if (result !== "" && last_style !== null){
        contents_arr.push({
            "Y":lastY,
            "content":result,
            "item":last_style
        })
    }
    

    // return result.trim();
    return contents_arr
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};'''

#     script = '''
# // 存储捕获的文本内容和矩形框信息
# let capturedText = [];
# let capturedRects = [];

# // 保存原始的 fillText, strokeText 和 rect 方法
# const originalFillText = CanvasRenderingContext2D.prototype.fillText;
# const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
# const originalRect = CanvasRenderingContext2D.prototype.rect;

# // 重写 fillText 方法
# CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
#     capturedText.push({
#         text: text,
#         x: x,
#         y: y,
#         maxWidth: maxWidth,
#         type: 'fill',
#         style: {
#             font: this.font,
#             fillStyle: this.fillStyle,
#             textAlign: this.textAlign,
#             textBaseline: this.textBaseline,
#             fontSize: this.font.split('px')[0], // 字体大小
#             lineHeight: this.font.split('px')[0] * 1.2, // 行高
#             textWidth: this.measureText(text).width, // 文本宽度
#             textLines: text.split('\\n').length // 文本行数
#         }
#     });
#     return originalFillText.apply(this, arguments);
# };

# // 重写 strokeText 方法
# CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
#     capturedText.push({
#         text: text,
#         x: x,
#         y: y,
#         maxWidth: maxWidth,
#         type: 'stroke',
#         style: {
#             font: this.font,
#             strokeStyle: this.strokeStyle,
#             textAlign: this.textAlign,
#             textBaseline: this.textBaseline
#         }
#     });
#     return originalStrokeText.apply(this, arguments);
# };

# // 重写 rect 方法
# CanvasRenderingContext2D.prototype.rect = function(x, y, width, height) {
#     capturedRects.push({
#         x: x,
#         y: y,
#         width: width,
#         height: height,
#         type: 'rect',
#         isRounded: false, // 默认为非圆角矩形
#         style: {
#             strokeStyle: this.strokeStyle,
#             fillStyle: this.fillStyle,
#             lineWidth: this.lineWidth
#         }
#     });
#     return originalRect.apply(this, arguments);
# };

# // 获取捕获的文本内容和矩形框信息
# window.getCapturedTextAndRects = function() {
#     const sortedText = capturedText.sort((a, b) => {
#         if (Math.abs(a.y - b.y) > 10) {
#             return a.y - b.y;
#         }
#         return a.x - b.x;
#     });

#     let result = '';
#     let contents_arr = [];
#     let lastY = null;
#     let last_style = null;
#     sortedText.forEach(item => {
#         if (lastY !== null && Math.abs(item.y - lastY) > 40) {
#             result += '\\n'; // 插入换行符
#             contents_arr.push({
#                 "Y": lastY,
#                 "content": result,
#                 "item": last_style
#             });
#             result = "";
#         }
#         result += item.text + '';
#         lastY = item.y;
#         last_style = item;
#     });
#     if (result !== "" && last_style !== null) {
#         contents_arr.push({
#             "Y": lastY,
#             "content": result,
#             "item": last_style
#         });
#     }

#     return {
#         text: contents_arr,
#         rects: capturedRects
#     };
# };

# // 清除已捕获的文本内容和矩形框信息
# window.clearCapturedTextAndRects = function() {
#     capturedText = [];
#     capturedRects = [];
# };

# // 恢复原始方法
# window.restoreOriginalMethods = function() {
#     CanvasRenderingContext2D.prototype.fillText = originalFillText;
#     CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
#     CanvasRenderingContext2D.prototype.rect = originalRect;
# };
# '''

    img_script='''
    //    .//self::img[contains(@class, 'wr_absolute wr_readerImage_opacity')]
    //iMg 元素 会随着网页动态显示而发生变化
// function getAllImgs(){
window.getAllImgs = function(){
    // 获取 <img> 元素
    const imgElement = document.getElementsByTagName('img');

    let imgs = []
    for(let handle of imgElement){
        const classes = handle.className;
        // width60 wr_absolute wr_readerImage_opacity
        // width80 wr_absolute wr_readerImage_opacity
        if (classes.indexOf("wr_absolute wr_readerImage_opacity") ===-1)continue
        console.log("className",classes)
        // 获取坐标和长宽信息
        const rect = handle.getBoundingClientRect();
        const imgWidth = rect.width;
        const imgHeight = rect.height;
        const imgTop = rect.top;
        const imgLeft = rect.left;

        // 输出信息
        console.log(`Width: ${imgWidth}, Height: ${imgHeight}`);
        console.log(`Top: ${imgTop}, Left: ${imgLeft}`);

        // 获取样式信息
        const style = handle.style;
        

        // 解析坐标和尺寸
        const transform = style.transform;
        const width = style.width;
        const height = style.height;

        // 提取坐标值
        const translateX = transform.match(/translate\((\d+)px, (\d+)px\)/)[1];
        const translateY = transform.match(/translate\((\d+)px, (\d+)px\)/)[2];

        console.log(`X坐标: ${translateX}px`);
        console.log(`Y坐标: ${translateY}px`);
        console.log(`宽度: ${width}`);
        console.log(`高度: ${height}`);
        imgs.push({
        "src":handle.src,
        "X坐标":parseInt(translateX),
        "Y坐标":parseFloat(translateY),
        "宽度":width,
        "高度":height,
        "className":classes,
        })
    }
    return imgs
}
'''

    pre_code_script='''
    //.//self::pre[contains(@class, 'wr_absolute hljs')]
    //pre 元素 不会随着网页动态显示而发生变化
// function getAllImgs(){
window.getAllPres = function(){
    // 获取 <img> 元素
    const imgElement = document.getElementsByTagName('pre');

    let pre_arr = []
    for(let handle of imgElement){
        const classes = handle.className;
        // wr_absolute hljs language-routeros
        // wr_absolute hljs language-llvm
        if (classes.indexOf("wr_absolute hljs") ===-1)continue
        console.log("className",classes)
        // 获取坐标和长宽信息
        const rect = handle.getBoundingClientRect();
        const imgWidth = rect.width;
        const imgHeight = rect.height;
        const imgTop = rect.top;
        const imgLeft = rect.left;

        // 输出信息
        console.log(`Width: ${imgWidth}, Height: ${imgHeight}`);
        console.log(`Top: ${imgTop}, Left: ${imgLeft}`);
        // 获取样式信息
        const style = handle.style;

        // 解析坐标和尺寸
        const transform = style.transform;
        const width = style.width;
        const height = style.height;

        // 提取坐标值
        const translateX = transform.match(/translate\((\d+)px, (\d+)px\)/)[1];
        const translateY = transform.match(/translate\((\d+)px, (\d+)px\)/)[2];

        console.log(`X坐标: ${translateX}px`);
        console.log(`Y坐标: ${translateY}px`);
        console.log(`宽度: ${width}`);
        console.log(`高度: ${height}`);
        pre_arr.push({
        "pre_outer_html":handle.outerHTML, //获得包含该元素的所有元素内容
        "X坐标":parseInt(translateX),
        "Y坐标":parseFloat(translateY),
        "宽度":width,
        "高度":height,
        "className":classes,
        })
    }
    return pre_arr
}
'''

    # 获得已经存储的book的最后一个章节位置
    try:
        with codecs.open(save_book, "r", "utf-8") as fr:
            book_lines = fr.readlines()
        begin = int(book_lines[-1].split(r"\t")[0].strip())
    except:
        begin = 0

    # 再读一次完整的url——list
    with codecs.open(save_file, "r", "utf-8") as fr:
        url_lines = fr.readlines()
    book_content = []
    begin = 3
    try:
        for index in range(begin, len(url_lines)):
        # for index, line in enumerate(url_lines):
            # 注入js之后需要更换页面内容才可以使用 getCapturedText 获得最新的内容，因此需要向上翻一页之后再点击下一章才可以获得当前章节内容
            # 所以url才需要向下面一样向上取一个
            # if index == 0:  url = begin_url
            if index == 0:  url = url_lines[index+1].split(";")[-1].strip()
            else:           url =  url_lines[index].split(";")[-1].strip()
            qti.browser.get(url)
            sleep(5)
            # 注入js
            qti.browser.execute_script(script)
            if index == 0:
                # 首页需要使用点击上一章才能获取完整
                next_handle = qti.GetHandle(xpath=".//self::button[@class='readerHeaderButton']")
            else:
                # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
                next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
            if next_handle is None:
                break
            next_handle.click()
            sleep(5)
            # 获取内容
            qti.browser.execute_script(img_script) #注入获取图片的脚本
            qti.browser.execute_script(pre_code_script) #注入获取代码的脚本
            canvas_info = qti.browser.execute_script("return getCapturedText();")
            new_canvas_info = {data_dict["Y"]:data_dict["content"] for data_dict in canvas_info}
            
            # 获得所有的图片信息
            img_dict_list = qti.browser.execute_script("return getAllImgs();")
            article_title=canvas_info[0]['content'].strip()
            # 保存图片到本地,并且返回本地地址
            image_dict_list = DownloadImage(book_name, index, article_title, img_dict_list)
            new_img_dict = {int(img_dict['Y坐标']):img_dict for img_dict in image_dict_list}

            # 获得所有的pre元素
            pre_html_list = qti.browser.execute_script("return getAllPres();")
            pre_html_dict = {data_dict["Y坐标"]:data_dict["pre_outer_html"] for data_dict in pre_html_list}

            combined_sorted_keys = sorted(list(new_canvas_info.keys()) + list(new_img_dict.keys())+list(pre_html_dict.keys()))
            new_content = []
            for key in combined_sorted_keys:
                if key in list(new_canvas_info.keys()):
                    if new_content == []:
                        new_content.append(f"# {new_canvas_info[key]}")
                    else:
                        new_content.append(new_canvas_info[key])
                elif key in list(pre_html_dict.keys()):
                    output_string = remove_transform_translate(pre_html_dict[key])
                    new_content.append(f"{output_string}\n")
                else:
                    # new_content.append(f"{str(new_img_dict[key])}\n") #这个用来检测地址
                    image_path = None
                    if new_img_dict[key]["image"] is not None:
                        image_path = new_img_dict[key]["image"].replace("\\","/")
                    # ('\n') #换行顶格写，否则会变成文本
                    # (rf'<img src={image_path} alt="测试图片" width="500" height="350">')
                    # ('\n\n') #必须给两个换行
                    # # 完整的img拼接实例
                    # <img src="testdd.jpg" alt="测试图片" width="200" height="200" onerror="this.onerror=null; this.alt='图片加载失败。网络地址: C:/Dropbox/YAN/D/2025/zhiguol/WeChatRead/对赌_test/5_幸运箱_80_756.jpg';">
                    onerror = f'''this.onerror=null; this.alt='本地图片加载失败。网络地址: {new_img_dict[key]["src"]}';'''
                    image_md = '\n'+rf'''<img src={image_path} alt="测试图片" width="{new_img_dict[key]['width']}" height="{new_img_dict[key]['heigth']}"  onerror="{onerror}">'''+'\n\n'
                    new_content.append(image_md)
                    pass
            new_content.insert(1, f'{url_lines[index+1].split(";")[-1]}') #存储url到章节开头
            canvas_content = "".join(new_content)

            # 获得所有动态渲染的内容，动态渲染的内容都在网页的最下面
            dynamic_web_content = 获取渲染到网页的动态内容(qti)
            if dynamic_web_content.strip() != "":
                canvas_content = f"{canvas_content}\n{dynamic_web_content}"

            book_content.append(canvas_content)
            with codecs.open(save_book, "a+", "utf-8") as fa:
                fa.write(f"{canvas_content}\n{index+1}\t\n")
            # 清除捕获的文本内容
            qti.browser.execute_script("clearCapturedText();")

            # 恢复原始方法
            qti.browser.execute_script("restoreOriginalMethods();")
            # print(1/0)
    except Exception as e:
        print(e)
        pass
    qti.Close()

def 微信读书MainV2(begin_url, book_name=None):
    '''
    @Time    :   2022/10/31 09:50:22
    @功能    :    该函数只能获取所有已经绘制在canvas中的文本内容，
    以及穿插在文本中的上传的图片
    除了上面的功能还具有：
    获得已经渲染在网页上切实乱序的网站的内容
    '''
    qti = selenium_qti(browser=None,
                       url='https://weread.qq.com/',
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                       virtual_chrome=True, # 使用虚拟浏览器
                       debug=False)
    # qti.OpenChrome()
    qti.OpenBaseChrome(virtual_browser=True)
    # 最大化浏览器窗口
    qti.browser.maximize_window()

    if book_name is None:
        time_str = time.strftime('%Y_%m_%d',time.localtime(time.time()))
        book_name = f"微信阅读_{time_str}"

    save_file = rf"{BIC['base_path']}\url_list_{book_name}.txt"
    save_book = rf"{BIC['base_path']}\{book_name}.txt"

    try:
        # 中途异常退出
        with codecs.open(save_file, "r", "utf-8") as fr:
            url_lines = fr.readlines()
    except:
        # 首次执行
        url_lines = []

    qti.browser.get(begin_url)
    sleep(5)
    # 使用包含类名 isHorizontalReader 的 XPath 定位元素
    # 类中包含 isHorizontalReader 表示处于双页阅读；isNormalReader 表示处于滚动阅读
    read_model_handle = qti.GetHandle(".//self::button[contains(@class, 'isHorizontalReader')]")
    if read_model_handle is not None:
        read_model_handle.click()
    # # 如果要获得目录的标题需要先展开目录才行
    # qti.Click(".//self::button[@class='readerControls_item catalog']")
    # sleep(1)
    # 获取目录数量. 包含匹配的方式获取
    # begin_index = 0
    # if url_lines == []:
    #     GetwereadQQBookAllUrlV3(qti, begin_url, save_file, begin_index=begin_index)
    # else:
    #     contents_handles = qti.GetHandles(".//self::li[contains(@class, 'readerCatalog_list_item')]")
    #     # for index, content in enumerate(contents_handles):
    #     #     # 如果没有登录账号，那么只能获取免费的目录
    #     #     print(f"{index}; {content.text}") #content.text 需要先展开书的目录
    #     if contents_handles is not None:
    #         # 获取书所有的章节url
    #         last_url = url_lines[-1].split(";")[-1].strip()
    #         begin_index = len(url_lines)
    #     # if begin_index != len(contents_handles):
    #     #     GetwereadQQBookAllUrlV3(qti, last_url, save_file, begin_index=begin_index)

    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法， 在调用时将文本内容及其位置、样式等信息存储到 capturedText 数组中，然后调用原始的 fillText 方法。
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline,
            fontSize: this.font.split('px')[0], // 字体大小
            lineHeight: this.font.split('px')[0] * 1.2, // 行高
            textWidth: this.measureText(text).width, // 文本宽度
            textLines: text.split('\\n').length // 文本行数
        }
    });
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法，功能与 fillText 方法类似，将文本内容及其相关信息存储到 capturedText 数组中，然后调用原始的 strokeText 方法。
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    debugger
    console.log(capturedText)
    const sortedText = capturedText.sort((a, b) => {
        if (Math.abs(a.y - b.y) > 10) {
            return a.y - b.y;
        }
        return a.x - b.x;
    });

    let result = '';
    let contents_arr = [];
    let lastY = null;
    let last_style = null;
    sortedText.forEach(item => {
        if (lastY !== null && Math.abs(item.y - lastY) > 40) {
            result += '\\n'; // 插入换行符
            //result += "YYY:"+lastY+'\\n'; // 插入换行符
            contents_arr.push({
                "Y":lastY,
                "content":result,
                "item":last_style
            })
            result = ""
        }
        result += item.text + '';
        lastY = item.y;
        last_style = item
    });
    if (result !== "" && last_style !== null){
        contents_arr.push({
            "Y":lastY,
            "content":result,
            "item":last_style
        })
    }
    

    // return result.trim();
    return contents_arr
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};'''

#     script = '''
# // 存储捕获的文本内容和矩形框信息
# let capturedText = [];
# let capturedRects = [];

# // 保存原始的 fillText, strokeText 和 rect 方法
# const originalFillText = CanvasRenderingContext2D.prototype.fillText;
# const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
# const originalRect = CanvasRenderingContext2D.prototype.rect;

# // 重写 fillText 方法
# CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
#     capturedText.push({
#         text: text,
#         x: x,
#         y: y,
#         maxWidth: maxWidth,
#         type: 'fill',
#         style: {
#             font: this.font,
#             fillStyle: this.fillStyle,
#             textAlign: this.textAlign,
#             textBaseline: this.textBaseline,
#             fontSize: this.font.split('px')[0], // 字体大小
#             lineHeight: this.font.split('px')[0] * 1.2, // 行高
#             textWidth: this.measureText(text).width, // 文本宽度
#             textLines: text.split('\\n').length // 文本行数
#         }
#     });
#     return originalFillText.apply(this, arguments);
# };

# // 重写 strokeText 方法
# CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
#     capturedText.push({
#         text: text,
#         x: x,
#         y: y,
#         maxWidth: maxWidth,
#         type: 'stroke',
#         style: {
#             font: this.font,
#             strokeStyle: this.strokeStyle,
#             textAlign: this.textAlign,
#             textBaseline: this.textBaseline
#         }
#     });
#     return originalStrokeText.apply(this, arguments);
# };

# // 重写 rect 方法
# CanvasRenderingContext2D.prototype.rect = function(x, y, width, height) {
#     capturedRects.push({
#         x: x,
#         y: y,
#         width: width,
#         height: height,
#         type: 'rect',
#         isRounded: false, // 默认为非圆角矩形
#         style: {
#             strokeStyle: this.strokeStyle,
#             fillStyle: this.fillStyle,
#             lineWidth: this.lineWidth
#         }
#     });
#     return originalRect.apply(this, arguments);
# };

# // 获取捕获的文本内容和矩形框信息
# window.getCapturedTextAndRects = function() {
#     const sortedText = capturedText.sort((a, b) => {
#         if (Math.abs(a.y - b.y) > 10) {
#             return a.y - b.y;
#         }
#         return a.x - b.x;
#     });

#     let result = '';
#     let contents_arr = [];
#     let lastY = null;
#     let last_style = null;
#     sortedText.forEach(item => {
#         if (lastY !== null && Math.abs(item.y - lastY) > 40) {
#             result += '\\n'; // 插入换行符
#             contents_arr.push({
#                 "Y": lastY,
#                 "content": result,
#                 "item": last_style
#             });
#             result = "";
#         }
#         result += item.text + '';
#         lastY = item.y;
#         last_style = item;
#     });
#     if (result !== "" && last_style !== null) {
#         contents_arr.push({
#             "Y": lastY,
#             "content": result,
#             "item": last_style
#         });
#     }

#     return {
#         text: contents_arr,
#         rects: capturedRects
#     };
# };

# // 清除已捕获的文本内容和矩形框信息
# window.clearCapturedTextAndRects = function() {
#     capturedText = [];
#     capturedRects = [];
# };

# // 恢复原始方法
# window.restoreOriginalMethods = function() {
#     CanvasRenderingContext2D.prototype.fillText = originalFillText;
#     CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
#     CanvasRenderingContext2D.prototype.rect = originalRect;
# };
# '''

    img_script='''
// function getAllImgs(){
window.getAllImgs = function(){
    // 获取 <img> 元素
    const imgElement = document.getElementsByTagName('img');

    let imgs = []
    for(let handle of imgElement){
        const classes = handle.className;
        // width60 wr_absolute wr_readerImage_opacity
        // width80 wr_absolute wr_readerImage_opacity
        if (classes.indexOf("wr_absolute wr_readerImage_opacity") ===-1)continue
        console.log("className",classes)
        // 获取坐标和长宽信息
        const rect = handle.getBoundingClientRect();
        const imgWidth = rect.width;
        const imgHeight = rect.height;
        const imgTop = rect.top;
        const imgLeft = rect.left;

        // 输出信息
        console.log(`Width: ${imgWidth}, Height: ${imgHeight}`);
        console.log(`Top: ${imgTop}, Left: ${imgLeft}`);

        // 获取样式信息
        const style = handle.style;
        

        // 解析坐标和尺寸
        const transform = style.transform;
        const width = style.width;
        const height = style.height;

        // 提取坐标值
        const translateX = transform.match(/translate\((\d+)px, (\d+)px\)/)[1];
        const translateY = transform.match(/translate\((\d+)px, (\d+)px\)/)[2];

        console.log(`X坐标: ${translateX}px`);
        console.log(`Y坐标: ${translateY}px`);
        console.log(`宽度: ${width}`);
        console.log(`高度: ${height}`);
        imgs.push({
        "src":handle.src,
        "X坐标":parseInt(translateX),
        "Y坐标":parseFloat(translateY),
        "宽度":width,
        "高度":height,
        "className":classes,
        })
    }
    return imgs
}
'''

    # 获得已经存储的book的最后一个章节位置
    try:
        with codecs.open(save_book, "r", "utf-8") as fr:
            book_lines = fr.readlines()
        begin = int(book_lines[-1].split(r"\t")[0].strip())
    except:
        begin = 0

    # 再读一次完整的url——list
    with codecs.open(save_file, "r", "utf-8") as fr:
        url_lines = fr.readlines()
    book_content = []
    try:
        for index in range(begin, len(url_lines)):
        # for index, line in enumerate(url_lines):
            # 注入js之后需要更换页面内容才可以使用 getCapturedText 获得最新的内容，因此需要向上翻一页之后再点击下一章才可以获得当前章节内容
            # 所以url才需要向下面一样向上取一个
            # if index == 0:  url = begin_url
            if index == 0:  url = url_lines[index+1].split(";")[-1].strip()
            else:           url =  url_lines[index].split(";")[-1].strip()
            # 测试使用，这是运行需要关闭 begin
            url = "https://weread.qq.com/web/reader/cf132e10813ab92e9g018088kc81322c012c81e728d9d180"
            # 测试使用，这是运行需要关闭 end 
            qti.browser.get(url)
            sleep(5)
            # 注入js
            qti.browser.execute_script(script)
            if index == 0:
                # 首页需要使用点击上一章才能获取完整
                next_handle = qti.GetHandle(xpath=".//self::button[@class='readerHeaderButton']")
            else:
                # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
                next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
            if next_handle is None:
                break
            next_handle.click()
            sleep(5)
            # 获取内容
            qti.browser.execute_script(img_script) #注入获取图片的脚本
            canvas_info = qti.browser.execute_script("return getCapturedText();")
            img_dict_list = qti.browser.execute_script("return getAllImgs();")
            new_canvas_info = {data_dict["Y"]:data_dict["content"] for data_dict in canvas_info}
            new_img_dict = {int(img_dict['Y坐标']):img_dict for img_dict in img_dict_list}
            combined_sorted_keys = sorted(list(new_canvas_info.keys()) + list(new_img_dict.keys()))
            new_content = []
            for key in combined_sorted_keys:
                if key in list(new_canvas_info.keys()):
                    new_content.append(new_canvas_info[key])
                else:
                    # new_content.append(f"{str(new_img_dict[key])}\n")
                    pass
            canvas_info = "".join(new_content)
            print(canvas_info)
            book_content.append(canvas_info)
            with codecs.open(save_book, "a+", "utf-8") as fa:
                fa.write(f"{canvas_info}\n{index+1}\t\n")
            # 清除捕获的文本内容
            qti.browser.execute_script("clearCapturedText();")

            # 恢复原始方法
            qti.browser.execute_script("restoreOriginalMethods();")
            # print(1/0)
    except Exception as e:
        print(e)
        pass
    qti.Close()

def 微信读书MainV3(begin_url, book_name=None):
    '''
    @Time    :   2022/10/31 09:50:22
    @功能    :    该函数只能获取所有已经绘制在canvas中的文本内容，
    以及穿插在文本中的上传的图片
    文本元素滚动渲染到页面，并且图片也是滚动渲染到页面的处理方法
    '''
    qti = selenium_qti(browser=None,
                       url='https://weread.qq.com/',
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                    #    virtual_chrome=True, # 使用虚拟浏览器
                       debug=False)
    qti.OpenChrome()
    # qti.OpenBaseChrome(virtual_browser=True)
    # 最大化浏览器窗口
    qti.browser.maximize_window()
    
    if book_name is None:
        time_str = time.strftime('%Y_%m_%d',time.localtime(time.time()))
        book_name = f"微信阅读_{time_str}"

    save_file = rf"{BIC['base_path']}\url_list_{book_name}.txt"
    save_book = rf"{BIC['base_path']}\{book_name}.md"

    try:
        # 中途异常退出
        with codecs.open(save_file, "r", "utf-8") as fr:
            url_lines = fr.readlines()
    except:
        # 首次执行
        url_lines = []

    qti.browser.get(begin_url)
    sleep(5)
    # li_handles = qti.GetHandles(".//self::ul[@class='readerCatalog_list']//li")
    # url_list = []
    # last_url = None
    # for index in range(len(li_handles)):
    #     li_handle = li_handles[index]
    #     qti.Click(".//self::button[@class='readerControls_item catalog']")
    #     li_handle.click()
    #     new_url = qti.browser.current_url
    #     if last_url is None:
    #         url_list.append(new_url)
    #     if new_url == last_url:
    #         url_list.append("与上一个url形同。需要通过点击下一页/下一章 查看下一页/下一章内容")
    #         pass
    #     else:
    #         url_list.append(new_url)
    #         last_url = new_url
    #     if len(url_list) == 13:
    #         break
    #     sleep(2)
    # with codecs.open(save_file, "w", "utf-8") as fw:
    #     for index, url in enumerate(url_list):
    #         fw.write(f"{index};{url}\n")
    # 使用包含类名 isHorizontalReader 的 XPath 定位元素
    # 类中包含 isHorizontalReader 表示处于双页阅读；isNormalReader 表示处于滚动阅读
    read_model_handle = qti.GetHandle(".//self::button[contains(@class, 'isHorizontalReader')]")
    if read_model_handle is not None:
        read_model_handle.click()
    # # 如果要获得目录的标题需要先展开目录才行
    # qti.Click(".//self::button[@class='readerControls_item catalog']")
    # sleep(1)
    # 获取目录数量. 包含匹配的方式获取

    begin_index = 0
    if url_lines == []:
        GetwereadQQBookAllUrlV3(qti, begin_url, save_file, begin_index=begin_index)
    else:
        contents_handles = qti.GetHandles(".//self::li[contains(@class, 'readerCatalog_list_item')]")
        # for index, content in enumerate(contents_handles):
        #     # 如果没有登录账号，那么只能获取免费的目录
        #     print(f"{index}; {content.text}") #content.text 需要先展开书的目录
        if contents_handles is not None:
            # 获取书所有的章节url
            last_url = url_lines[-1].split(";")[-1].strip()
            begin_index = len(url_lines)

    #     if begin_index != len(contents_handles):
    #         GetwereadQQBookAllUrlV3(qti, last_url, save_file, begin_index=begin_index)


    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法， 在调用时将文本内容及其位置、样式等信息存储到 capturedText 数组中，然后调用原始的 fillText 方法。
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline,
            fontSize: this.font.split('px')[0], // 字体大小
            lineHeight: this.font.split('px')[0] * 1.2, // 行高
            textWidth: this.measureText(text).width, // 文本宽度
            textLines: text.split('\\n').length // 文本行数
        }
    });
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法，功能与 fillText 方法类似，将文本内容及其相关信息存储到 capturedText 数组中，然后调用原始的 strokeText 方法。
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    debugger
    console.log(capturedText)
    const sortedText = capturedText.sort((a, b) => {
        if (Math.abs(a.y - b.y) > 10) {
            return a.y - b.y;
        }
        return a.x - b.x;
    });

    let result = '';
    let contents_arr = [];
    let lastY = null;
    let last_style = null;
    sortedText.forEach(item => {
        if (lastY !== null && Math.abs(item.y - lastY) > 40) {
            result += '\\n'; // 插入换行符
            //result += "YYY:"+lastY+'\\n'; // 插入换行符
            contents_arr.push({
                "Y":lastY,
                "content":result,
                "item":last_style
            })
            result = ""
        }
        result += item.text + '';
        lastY = item.y;
        last_style = item
    });
    if (result !== "" && last_style !== null){
        contents_arr.push({
            "Y":lastY,
            "content":result,
            "item":last_style
        })
    }
    

    // return result.trim();
    return contents_arr
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};'''

    img_script='''
// function getAllImgs(){
window.getAllImgs = function(){
    // 获取 <img> 元素
    const imgElement = document.getElementsByTagName('img');

    let imgs = []
    for(let handle of imgElement){
        const classes = handle.className;
        // width60 wr_absolute wr_readerImage_opacity
        // width80 wr_absolute wr_readerImage_opacity
        if (classes.indexOf("wr_absolute wr_readerImage_opacity") ===-1)continue
        console.log("className",classes)
        // 获取坐标和长宽信息
        const rect = handle.getBoundingClientRect();
        const imgWidth = rect.width;
        const imgHeight = rect.height;
        const imgTop = rect.top;
        const imgLeft = rect.left;

        // 输出信息
        console.log(`Width: ${imgWidth}, Height: ${imgHeight}`);
        console.log(`Top: ${imgTop}, Left: ${imgLeft}`);

        // 获取样式信息
        const style = handle.style;
        

        // 解析坐标和尺寸
        const transform = style.transform;
        const width = style.width;
        const height = style.height;

        // 提取坐标值
        const translateX = transform.match(/translate\((\d+)px, (\d+)px\)/)[1];
        const translateY = transform.match(/translate\((\d+)px, (\d+)px\)/)[2];

        console.log(`X坐标: ${translateX}px`);
        console.log(`Y坐标: ${translateY}px`);
        console.log(`宽度: ${width}`);
        console.log(`高度: ${height}`);
        imgs.push({
        "src":handle.src,
        "X坐标":parseInt(translateX),
        "Y坐标":parseFloat(translateY),
        "宽度":width,
        "高度":height,
        "className":classes,
        })
    }
    return imgs
}
'''

    pre_code_script='''
// function getAllImgs(){
window.getAllPres = function(){
    // 获取 <img> 元素
    const imgElement = document.getElementsByTagName('pre');

    let pre_arr = []
    for(let handle of imgElement){
        const classes = handle.className;
        // wr_absolute hljs language-routeros
        // wr_absolute hljs language-llvm
        if (classes.indexOf("wr_absolute hljs") ===-1)continue
        console.log("className",classes)
        // 获取坐标和长宽信息
        const rect = handle.getBoundingClientRect();
        const imgWidth = rect.width;
        const imgHeight = rect.height;
        const imgTop = rect.top;
        const imgLeft = rect.left;

        // 输出信息
        console.log(`Width: ${imgWidth}, Height: ${imgHeight}`);
        console.log(`Top: ${imgTop}, Left: ${imgLeft}`);
        // 获取样式信息
        const style = handle.style;

        // 解析坐标和尺寸
        const transform = style.transform;
        const width = style.width;
        const height = style.height;

        // 提取坐标值
        const translateX = transform.match(/translate\((\d+)px, (\d+)px\)/)[1];
        const translateY = transform.match(/translate\((\d+)px, (\d+)px\)/)[2];

        console.log(`X坐标: ${translateX}px`);
        console.log(`Y坐标: ${translateY}px`);
        console.log(`宽度: ${width}`);
        console.log(`高度: ${height}`);
        pre_arr.push({
        "pre_outer_html":handle.outerHTML, //获得包含该元素的所有元素内容
        "X坐标":parseInt(translateX),
        "Y坐标":parseFloat(translateY),
        "宽度":width,
        "高度":height,
        "className":classes,
        })
    }
    return pre_arr
}
'''

    # 获得已经存储的book的最后一个章节位置
    try:
        with codecs.open(save_book, "r", "utf-8") as fr:
            book_lines = fr.readlines()
        begin = int(book_lines[-1].split(r"\t")[0].strip())
    except:
        begin = 0

    # 再读一次完整的url——list
    with codecs.open(save_file, "r", "utf-8") as fr:
        url_lines = fr.readlines()
    book_content = []
    # begin = 3
    try:
        for index in range(begin, len(url_lines)):
        # for index, line in enumerate(url_lines):
            # 注入js之后需要更换页面内容才可以使用 getCapturedText 获得最新的内容，因此需要向上翻一页之后再点击下一章才可以获得当前章节内容
            # 所以url才需要向下面一样向上取一个
            # if index == 0:  url = begin_url
            if index == 0:  url = url_lines[index+1].split(";")[-1].strip()
            else:           url = url_lines[index-1].split(";")[-1].strip()

            
            # 当前url如果不是一个正在的url，需要逐层向上找到一个完整的url，并且需要记住向上的次数，这个次数和后面的js注入位置有重要关系
            url_index = 0
            while 1:
                if url == "与上一个url形同。需要通过点击下一页/下一章 查看下一页/下一章内容":
                    url_index += 1
                    url = url_lines[index-url_index].split(";")[-1].strip()
                else:
                    break
            qti.browser.get(url)
            sleep(5)

            # # 注入js
            # qti.browser.execute_script(script)
            # if index == 0:
            #     # 首页需要使用点击上一章才能获取完整
            #     next_handle = qti.GetHandle(xpath=".//self::button[@class='readerHeaderButton']")
            # else:
            #     # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
            #     next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
            # if next_handle is None:
            #     break
            # next_handle.click()
            # sleep(5)

            # 因为url中现在存储了， 
            # "与上一个url形同。需要通过点击下一页/下一章 查看下一页/下一章内容"，
            # 这样的使用相同url的情况。
            # 因此下面的点击 就会因为上面的while 1 的循环得出的url_index值来确定需要连续点击下一页/下一章的次数
            # 为了满足最少点击一次，一次url_index 需要默认+1

            # 并且注入js的时间点也需要进行更改
            # 根据上面逐次向上找到真正url的次数，来判断js注入的位置，需要在倒数第二次的时候注入
            if url_index == 0:
                # 需要确保 js注入和点击下一页或者下一章至少执行一次
                qti.browser.execute_script(script)
                if index == 0:
                    # 首页需要使用点击上一章才能获取完整
                    next_handle = qti.GetHandle(xpath=".//self::button[@class='readerHeaderButton']")
                else:
                    # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
                    next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
                if next_handle is None:
                    break
                next_handle.click()
                sleep(5)

            for i in range(url_index):
                if i == url_index-1:
                    # 在导数第二次click的时候注入js
                    qti.browser.execute_script(script)
                if index == 0:
                    # 首页需要使用点击上一章才能获取完整
                    next_handle = qti.GetHandle(xpath=".//self::button[@class='readerHeaderButton']")
                else:
                    # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
                    next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
                if next_handle is None:
                    break
                next_handle.click()
                sleep(5)
            # 获取内容
            qti.browser.execute_script(img_script) #注入获取图片的脚本
            qti.browser.execute_script(pre_code_script) #注入获取代码的脚本
            canvas_info = qti.browser.execute_script("return getCapturedText();")
            new_canvas_info = {data_dict["Y"]:data_dict["content"] for data_dict in canvas_info}
            
            # # 获得所有的图片信息
            # img_dict_list = qti.browser.execute_script("return getAllImgs();")
            article_title = "无文本内容"
            if canvas_info != []:
                article_title=canvas_info[0]['content'].strip()
            # # 保存图片到本地,并且返回本地地址
            # image_dict_list = DownloadImage(book_name, index, article_title, img_dict_list)
            # new_img_dict = {int(img_dict['Y坐标']):img_dict for img_dict in image_dict_list}

            # # 获得所有的pre元素
            # pre_html_list = qti.browser.execute_script("return getAllPres();")
            # pre_html_dict = {data_dict["Y坐标"]:data_dict["pre_outer_html"] for data_dict in pre_html_list}

            # 获取动态内容：文本，图片，代码
            dynamic_content_dict, new_img_dict, pre_html_dict = 获取渲染到网页的动态内容V2(qti)
            imags_dict = DownloadImage(book_name, index, article_title, new_img_dict)

            combined_sorted_keys = sorted(list(new_canvas_info) + list(imags_dict)+list(dynamic_content_dict)+ list(pre_html_dict))
            new_content = []
            for key in combined_sorted_keys:
                if key in list(new_canvas_info):
                    if new_content == []:
                        # 通过判断当前页面的url是否为独立的url来判断是否应该在markdown中生成一级目录结构
                        next_index = index + 1
                        if next_index < len(url_lines) and "与上一个url形同" in url_lines[index]:
                            # 非独立章节
                            new_content.append(new_canvas_info[key])
                        else:
                            # 独立章节
                            new_content.append(f"# {new_canvas_info[key]}")
                    else:
                        new_content.append(new_canvas_info[key])
                elif key in list(pre_html_dict):
                    output_string = remove_transform_translate(pre_html_dict[key])
                    new_content.append(f"{output_string}\n")
                elif key in list(dynamic_content_dict):
                    output_string = remove_transform_translate(dynamic_content_dict[key]["content"])
                    if dynamic_content_dict[key]["x"] != 0:
                        output_string = f"&nbsp;&nbsp;&nbsp;&nbsp;{output_string}"
                    new_content.append(f"{output_string}\n")
                else:
                    # new_content.append(f"{str(imags_dict[key])}\n") #这个用来检测地址
                    image_path = None
                    if imags_dict[key]["image"] is not None:
                        # 使用相对地址
                        route_list = imags_dict[key]["image"].split("\\")
                        image_path = "/".join(route_list[-2:])
                        # # 绝对地址
                        # image_path = imags_dict[key]["image"].replace("\\","/")
                    # ('\n') #换行顶格写，否则会变成文本
                    # (rf'<img src={image_path} alt="测试图片" width="500" height="350">')
                    # ('\n\n') #必须给两个换行
                    # # 完整的img拼接实例
                    # <img src="testdd.jpg" alt="测试图片" width="200" height="200" onerror="this.onerror=null; this.alt='图片加载失败。网络地址: C:/Dropbox/YAN/D/2025/zhiguol/WeChatRead/对赌_test/5_幸运箱_80_756.jpg';">
                    onerror = f'''this.onerror=null; this.alt='本地图片加载失败。网络地址: {imags_dict[key]["src"]}';'''
                    image_md = '\n'+rf'''<img src={image_path} alt="测试图片" width="{imags_dict[key]['width']}" height="{imags_dict[key]['heigth']}"  onerror="{onerror}">'''+'\n\n'
                    new_content.append(image_md)
                    pass
            new_content.insert(1, f'{url_lines[index].split(";")[-1]}') #存储url到章节开头
            canvas_content = "".join(new_content)

            # # 获得所有动态渲染的内容，动态渲染的内容都在网页的最下面
            # if dynamic_web_content.strip() != "":
            #     canvas_content = f"{canvas_content}\n{dynamic_web_content}"

            book_content.append(canvas_content)
            with codecs.open(save_book, "a+", "utf-8") as fa:
                fa.write(f"{canvas_content}\n{index+1}\t\n")
            # 清除捕获的文本内容
            qti.browser.execute_script("clearCapturedText();")

            # 恢复原始方法
            qti.browser.execute_script("restoreOriginalMethods();")
            # print(1/0)
    except Exception as e:
        print(e)
        traceback.print_exc()
        pass
    qti.Close()

def 微信读书_一章Main(begin_url=None, url_list=None):
    '''
    @Time    :   2022/10/31 09:50:22
    @功能    :    
    '''
    qti = selenium_qti(browser=None,
                       url='https://weread.qq.com/',
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                       debug=False)
    qti.OpenChrome()

    if begin_url is None:
        begin_url = "https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180"
    book_name = "明朝那些事"
    save_file = rf"{BIC['base_path']}\url_list_{book_name}.txt"
    save_book = rf"{BIC['base_path']}\{book_name}.txt"

    # 获取书所有的章节url
    # GetwereadQQBookAllUrl(qti, begin_url, save_file)

    with codecs.open(save_file, "r", "utf-8") as fr:
        url_lines = fr.readlines()
    
    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    const sortedText = capturedText.sort((a, b) => {
        if (Math.abs(a.y - b.y) > 10) {
            return a.y - b.y;
        }
        return a.x - b.x;
    });

    let result = '';
    let lastY = null;
    sortedText.forEach(item => {
        if (lastY !== null && Math.abs(item.y - lastY) > 10) {
            result += '\\n'; // 插入换行符
        }
        result += item.text + ' ';
        lastY = item.y;
    });

    return result.trim();
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};'''
    
    # 获得已经存储的book的最后一个章节位置
    try:
        with codecs.open(save_book, "r", "utf-8") as fr:
            book_lines = fr.readlines()
        begin = int(book_lines[-1].split(r"\t")[0].strip())
    except:
        begin = 0
    book_content = []
    try:
        for index in range(begin, len(url_lines)):
        # for index, line in enumerate(url_lines):
            # 注入js之后需要更换页面内容才可以使用 getCapturedText 获得最新的内容，因此需要向上翻一页之后再点击下一章才可以获得当前章节内容
            # 所以url才需要向下面一样向上取一个
            if index == 0:  url = begin_url
            else:           url =  url_lines[index-1].strip()
            qti.browser.get(url)
            sleep(2)
            # 注入js
            qti.browser.execute_script(script)
            # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
            next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
            if next_handle is None:
                break
            next_handle.click()
            sleep(3)
            # 获取内容
            canvas_info = qti.browser.execute_script("return getCapturedText();")
            canvas_info ="".join(canvas_info.split(" ")) #去除内部多余的空格
            book_content.append(rf"{index+1}\t{canvas_info}@@@***@@@***")
            # 清除捕获的文本内容
            qti.browser.execute_script("clearCapturedText();")

            # 恢复原始方法
            qti.browser.execute_script("restoreOriginalMethods();")
            # print(1/0)
    except:
        with codecs.open(save_book, "a+", "utf-8") as fa:
            fa.write("\n".join(book_content))
            fa.write("\n")


    qti.Close()

import re
def is_chinese_punctuation(char):
    # 中文标点符号的Unicode范围
    chinese_punctuation = r'[\u3000-\u303F\uFF00-\uFFEF]'
    return re.match(chinese_punctuation, char) is not None

def check_last_char_is_chinese_punctuation(s):
    if not s:
        return False
    return is_chinese_punctuation(s[-1])

def 测试获取文本和图片的信息():
    '''
    @Time    :   2025/01/15 16:54:26
    @功能    :   None
    '''
    qti = selenium_qti(browser=None,
                       url="https://weread.qq.com/web/reader/77e326b072922e9177e6cb1kc7432af0210c74d97b01b1c",
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                       debug=False)
    qti.OpenChrome()
    sleep(2)
    
    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法， 在调用时将文本内容及其位置、样式等信息存储到 capturedText 数组中，然后调用原始的 fillText 方法。
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline,
            fontSize: this.font.split('px')[0], // 字体大小
            lineHeight: this.font.split('px')[0] * 1.2, // 行高
            textWidth: this.measureText(text).width, // 文本宽度
            textLines: text.split('\\n').length // 文本行数
        }
    });
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法，功能与 fillText 方法类似，将文本内容及其相关信息存储到 capturedText 数组中，然后调用原始的 strokeText 方法。
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    debugger
    console.log(capturedText)
    const sortedText = capturedText.sort((a, b) => {
        if (Math.abs(a.y - b.y) > 10) {
            return a.y - b.y;
        }
        return a.x - b.x;
    });

    let result = '';
    let contents_arr = [];
    let lastY = null;
    let last_style = null;
    sortedText.forEach(item => {
        if (lastY !== null && Math.abs(item.y - lastY) > 40) {
            result += '\\n'; // 插入换行符
            //result += "YYY:"+lastY+'\\n'; // 插入换行符
            contents_arr.push({
                "Y":lastY,
                "content":result,
                "item":last_style
            })
            result = ""
        }
        result += item.text + '';
        lastY = item.y;
        last_style = item
    });
    contents_arr.push({
        "Y":lastY,
        "content":result,
        "item":last_style
    })

    // return result.trim();
    return contents_arr
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};'''

    img_script='''
// function getAllImgs(){
window.getAllImgs = function(){
    // 获取 <img> 元素
    const imgElement = document.getElementsByTagName('img');

    let imgs = []
    for(let handle of imgElement){
        const classes = handle.className;
        if (classes.indexOf("width80 wr_absolute wr_readerImage_opacity") ===-1)continue
        console.log("className",classes)
        // 获取坐标和长宽信息
        const rect = handle.getBoundingClientRect();
        const imgWidth = rect.width;
        const imgHeight = rect.height;
        const imgTop = rect.top;
        const imgLeft = rect.left;

        // 输出信息
        console.log(`Width: ${imgWidth}, Height: ${imgHeight}`);
        console.log(`Top: ${imgTop}, Left: ${imgLeft}`);

        // 获取样式信息
        const style = handle.style;
        

        // 解析坐标和尺寸
        const transform = style.transform;
        const width = style.width;
        const height = style.height;

        // 提取坐标值
        const translateX = transform.match(/translate\((\d+)px, (\d+)px\)/)[1];
        const translateY = transform.match(/translate\((\d+)px, (\d+)px\)/)[2];

        console.log(`X坐标: ${translateX}px`);
        console.log(`Y坐标: ${translateY}px`);
        console.log(`宽度: ${width}`);
        console.log(`高度: ${height}`);
        imgs.push({
        "src":handle.src,
        "X坐标":parseInt(translateX),
        "Y坐标":parseFloat(translateY),
        "宽度":width,
        "高度":height,
        "className":classes,
        })
    }
    return imgs
}
'''

    sleep(2)
    # 注入js
    qti.browser.execute_script(script)
    qti.browser.execute_script(img_script)
    # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
    sleep(3)
    # 获取内容
    canvas_info = qti.browser.execute_script("return getCapturedText();")
    img_dict_list = qti.browser.execute_script("return getAllImgs();")
    new_canvas_info = {data_dict["Y"]:data_dict["content"] for data_dict in canvas_info}
    new_img_dict = {int(img_dict['Y坐标']):img_dict for img_dict in img_dict_list}
    combined_sorted_keys = sorted(list(new_canvas_info.keys()) + list(new_img_dict.keys()))
    new_content = []
    for key in combined_sorted_keys:
        if key in list(new_canvas_info.keys()):
            new_content.append(new_canvas_info[key])
        else:
            new_content.append(f"{str(new_img_dict[key])}\n")
    print(canvas_info)
    # 清除捕获的文本内容
    qti.browser.execute_script("clearCapturedText();")
    # 恢复原始方法
    qti.browser.execute_script("restoreOriginalMethods();")
    # print(1/0)
    qti.Close()
    pass

def is_scroll_to_bottom(qti):
    """
    判断滚动条是否已经滚动到底部。
    
    :param driver: Selenium WebDriver实例
    :return: True表示滚动到底部，False表示未到底部
    """
    # 执行JavaScript代码获取页面高度和滚动位置
    scroll_height = qti.browser.execute_script("return document.body.scrollHeight;")
    window_height = qti.browser.execute_script("return window.innerHeight;")
    scroll_position = qti.browser.execute_script("return window.scrollY;")
    # 判断是否滚动到底部
    return scroll_height <= window_height + scroll_position

def 微信读书MainV2测试获取已经被渲染到网页的文本(begin_url, book_name=None):
    '''
    @Time    :   2022/10/31 09:50:22
    @功能    :    该函数只能获取所有已经绘制在canvas中的文本内容，
    以及穿插在文本中的上传的图片
    除了上面的功能还具有：
    获得已经渲染在网页上切实乱序的网站的内容
    '''
    qti = selenium_qti(browser=None,
                       url='https://weread.qq.com/',
                       chromedriver_path=BIC['chromedriver_path'],
                       google_data_path=BIC['google_data_path'],
                       del_userdata=False,
                       virtual_chrome=True, # 使用虚拟浏览器
                       debug=False)
    # qti.OpenChrome()
    qti.OpenBaseChrome(virtual_browser=True)
    qti.browser.get(begin_url)
    # 最大化浏览器窗口
    qti.browser.maximize_window()

    # 使用包含类名 isHorizontalReader 的 XPath 定位元素
    # 类中包含 isHorizontalReader 表示处于双页阅读；isNormalReader 表示处于滚动阅读
    read_model_handle = qti.GetHandle(".//self::button[contains(@class, 'isHorizontalReader')]")
    if read_model_handle is not None:
        read_model_handle.click()
    # # 如果要获得目录的标题需要先展开目录才行
    # qti.Click(".//self::button[@class='readerControls_item catalog']")
    # sleep(1)
    # 获取目录数量. 包含匹配的方式获取
    
    script = '''
// 存储捕获的文本内容
let capturedText = [];
// 保存原始的 fillText 方法
const originalFillText = CanvasRenderingContext2D.prototype.fillText;
const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
// 重写 fillText 方法， 在调用时将文本内容及其位置、样式等信息存储到 capturedText 数组中，然后调用原始的 fillText 方法。
CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'fill',
        style: {
            font: this.font,
            fillStyle: this.fillStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline,
            fontSize: this.font.split('px')[0], // 字体大小
            lineHeight: this.font.split('px')[0] * 1.2, // 行高
            textWidth: this.measureText(text).width, // 文本宽度
            textLines: text.split('\\n').length // 文本行数
        }
    });
    return originalFillText.apply(this, arguments);
};
// 重写 strokeText 方法，功能与 fillText 方法类似，将文本内容及其相关信息存储到 capturedText 数组中，然后调用原始的 strokeText 方法。
CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
    capturedText.push({
        text: text,
        x: x,
        y: y,
        maxWidth: maxWidth,
        type: 'stroke',
        style: {
            font: this.font,
            strokeStyle: this.strokeStyle,
            textAlign: this.textAlign,
            textBaseline: this.textBaseline
        }
    });
    return originalStrokeText.apply(this, arguments);
};
// 获取捕获的文本内容
window.getCapturedText = function() {
    debugger
    console.log(capturedText)
    const sortedText = capturedText.sort((a, b) => {
        if (Math.abs(a.y - b.y) > 10) {
            return a.y - b.y;
        }
        return a.x - b.x;
    });

    let result = '';
    let contents_arr = [];
    let lastY = null;
    let last_style = null;
    sortedText.forEach(item => {
        if (lastY !== null && Math.abs(item.y - lastY) > 40) {
            result += '\\n'; // 插入换行符
            //result += "YYY:"+lastY+'\\n'; // 插入换行符
            contents_arr.push({
                "Y":lastY,
                "content":result,
                "item":last_style
            })
            result = ""
        }
        result += item.text + '';
        lastY = item.y;
        last_style = item
    });
    if (result !== "" && last_style !== null){
        contents_arr.push({
            "Y":lastY,
            "content":result,
            "item":last_style
        })
    }
    

    // return result.trim();
    return contents_arr
};
// 清除已捕获的文本内容
window.clearCapturedText = function() {
    capturedText = [];
};
// 恢复原始方法
window.restoreOriginalMethods = function() {
    CanvasRenderingContext2D.prototype.fillText = originalFillText;
    CanvasRenderingContext2D.prototype.strokeText = originalStrokeText;
};'''


    book_content = []
    try:
        # 测试使用，这是运行需要关闭 begin
        # url = "https://weread.qq.com/web/reader/cf132e10813ab92e9g018088ka87322c014a87ff679a21ea"
        # # 测试使用，这是运行需要关闭 end 
        # qti.browser.get(url)
        # sleep(5)
        # 注入js
        qti.browser.execute_script(script)
        # 进入下一章，否则此时 qti.browser.execute_script("return getCapturedText();") 无内容
        next_handle = qti.GetHandle(xpath=".//self::button[@class='readerFooter_button']")
        next_handle.click()
        sleep(5)
        # 获取内容
        canvas_info = qti.browser.execute_script("return getCapturedText();")
        html_content = 获取渲染到网页的动态内容(qti)
        print(canvas_info)
        book_content.append(f"{canvas_info}\n{html_content}")
        # 清除捕获的文本内容
        qti.browser.execute_script("clearCapturedText();")

        # 恢复原始方法
        qti.browser.execute_script("restoreOriginalMethods();")
        # print(1/0)
    except Exception as e:
        print(e)
        pass
    qti.Close()


def 获取渲染到网页的动态内容(qti):
    '''
    @Time    :   2025/01/21 17:38:11
    @功能    :   循环获得已经渲染到网页的所有文本
    注意这里的文本是随着滚动条而动态出现和动态消失的，一次滚动条每次不能滚动条太多
    '''
    content_html_list = []
    while 1:
        if is_scroll_to_bottom(qti):
            print("滚动条已经滚动到底部")
            break
        qti.ScrollBar_相对位置(200) #向下滚动100个单位
        handles = qti.GetHandles(".//self::div[@class='passage-wrapper']//div[@class='passage-content']")
        for index, handle in enumerate(handles):
            if index == 0: continue
            content_html = handle.get_attribute("innerHTML")
            if content_html not in content_html_list:
                content_html_list.append(content_html)

        # if len(handles) != 1:
        #     print(handles[1].get_attribute("innerHTML"))
        print(len(handles))
        time.sleep(1)
        pass
    context_list = []
    for index, content_html in enumerate(content_html_list):
        content = [data_dict["content"] for data_dict in 重组文本(content_html)]
        context_list.append("\n".join(content))
    html_content = "\n".join(context_list)
    return html_content

def 获取渲染到网页的动态内容V2(qti):
    '''
    @Time    :   2025/01/21 17:38:11
    @功能    :   循环获得已经渲染到网页的所有文本、图片、代码等
    注意这里的文本是随着滚动条而动态出现和动态消失的，一次滚动条每次不能滚动条太多
    '''
    test = '''<span data-wr-id="wrnbw9r7youki" data-wr-role="text" class="wr_absolute ccn-naikd6yf6x" style="transform: translate(0px, 7975px);width:21.40625px;">车</span>'''

    test2 = '''<span data-wr-id="wrgvnj8vudlo8" data-wr-role="text" class="wr_absolute ccn-naikd6yf6x" style="transform: translate(0px, 8329px);width:23.46875px;">上</span>'''
    content_html_list, img_dict, pre_dict = [], {}, {}
    while 1:
        if is_scroll_to_bottom(qti):
            print("滚动条已经滚动到底部")
            break
        qti.ScrollBar_相对位置(200) #向下滚动100个单位
        # 获得所有的文本
        content_handles = qti.GetHandles(".//self::div[@class='passage-wrapper']//div[@class='passage-content']")
        for index, handle in enumerate(content_handles):
            if index == 0: continue
            content_html = handle.get_attribute("innerHTML")
            if test in content_html:
                print(index)
            if test2 in content_html:
                print(index)
                
            # if content_html.startswith("<pre class=") or content_html.startswith("<img class="): continue
            if content_html not in content_html_list:
                content_html_list.append(content_html)

        # 获得所有的图片信息
        img_dict_list = qti.browser.execute_script("return getAllImgs();")
        for data_dict in img_dict_list:
            y_value = int(data_dict['Y坐标'])
            if y_value not in list(img_dict.keys()):
                img_dict[y_value] = data_dict
        # 获得所有的pre元素
        pre_html_list = qti.browser.execute_script("return getAllPres();")
        for data_dict in pre_html_list:
            y_value = int(data_dict['Y坐标'])
            if y_value not in list(pre_dict.keys()):
                pre_dict[y_value] = data_dict["pre_outer_html"]

        time.sleep(1)
        pass
    # context_list = []
    # for index, content_html in enumerate(content_html_list):
    #     content = [data_dict["content"] for data_dict in 重组文本(content_html)]
    #     context_list.append("\n".join(content))
    # html_content = "\n".join(context_list)
    # return html_content, img_dict, pre_dict 


    content_dict = {}
    for index, content_html in enumerate(content_html_list):
        result_dict = 重组文本(content_html)
        for key, data_dict in result_dict.items():
            if key in list(content_dict):
                continue
            content_dict[key] = data_dict
    return content_dict, img_dict, pre_dict 

def 重组文本(html_body):
    '''
    @Time    :   2025/01/21 16:34:02
    @功能    :   None
    '''
    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html_body, 'html.parser')
    # 获取所有具有data-wr-role属性的span元素
    spans = soup.find_all('span', {'data-wr-role': 'text'})

    # 遍历每个span元素并获取其属性和文本内容
    # 获取y轴数据
    text_dict = {}
    for span in spans:
        data_wr_id = span.get('data-wr-id')
        data_wr_role = span.get('data-wr-role')
        class_name = span.get('class')
        style = span.get('style')
        text_content = span.text
        # # 打印属性和文本内容
        # print('data-wr-id:', data_wr_id)
        # print('data-wr-role:', data_wr_role)
        # print('class:', class_name)
        # print('style:', style)
        # print('textContent:', text_content)
        # print('-------------------------')
        pattern = r"translate\((\d+)px,\s*(\d+)px\)"
        match = re.search(pattern, style)
        if match:
            x_value = int(match.group(1))  # 提取第一个数值
            y_value = int(match.group(2))  # 提取第二个数值
            print(f"X值: {x_value}")
            print(f"Y值: {y_value}")
            if y_value in list(text_dict.keys()):
                text_dict[y_value].append({
                    "x":x_value,
                    "text":span.text
                })
            else:
                text_dict[y_value] = [{
                    "x":x_value,
                    "text":span.text
                }]
        else:
            continue

    # 排序y轴数据
    new_y_list = sorted(list(text_dict.keys()))
    new_text_dict = {}
    for index, key in enumerate(new_y_list):
        new_text_dict[key] = text_dict[key]

    # 排序x轴数据
    for key, data_dict_list in new_text_dict.items():
        sorted_data = sorted(data_dict_list, key=lambda item: item['x'])
        content = [data_dict["text"] for data_dict in sorted_data]
        new_text_dict[key] = {
            "x":sorted_data[0]["x"],
            "content":"".join(content)
        }

    # # 根据y轴差值是否超过40来判定是否属于一行
    # # 初始化结果列表
    # result = []
    # # 遍历排序后的键
    # keys = list(new_text_dict)
    # for i in range(len(keys)):
    #     current_key = keys[i]
    #     current_text = new_text_dict[current_key]
    #     # 如果是第一个键，直接添加到结果列表
    #     if i == 0:
    #         result.append(current_text)
    #     else:
    #         previous_key = keys[i - 1]
    #         # 如果当前键和前一个键的差值不超过40，合并文本
    #         if current_key - previous_key <= 40:
    #             result[-1]["content"] += current_text["content"]  # 合并到上一个文本
    #         else:
    #             result.append(current_text)  # 新增一个文本

    result_dict, last_y = {}, -1
    # 遍历排序后的键
    keys = list(new_text_dict)
    for key, data_dict in new_text_dict.items():
        # 如果是第一个键，直接添加到结果列表
        if result_dict == {}:
            result_dict[key] = data_dict
            last_y = key
        else:
            # 如果当前键和前一个键的差值不超过40，合并文本
            if key-last_y <= 40:
                last_key = list(result_dict)[-1]
                result_dict[last_key]["content"] += data_dict["content"]  # 合并到上一个文本
            else:
                result_dict[key] = data_dict  # 新增一个文本
            last_y = key

    return result_dict

from 通过位置渲染的文本 import html_innerHtml
重组文本(html_innerHtml)
def MarkDownDemo():
    '''
    @Time    :   2025/01/22 11:11:19
    @功能    :   
    # vscode 安装 markdown （Markdown Paste Image To okmd.dev OSS store）插件，
    # 打开markdown笔记方法：
    # 1 在vscode中打开一个markdown 笔记比如（my.md）
    # 2 按下 ctrl+shift+v 就会重新打开一个页面显示笔记
    '''
    def create_markdown_note(note_title, note_content, image_path=None):
        # 创建Markdown文件
        with open(f"{note_title}.md", "a+", encoding="utf-8") as file:
            # 写入标题
            file.write("\n")
            file.write(f"# {note_title}\n\n")
            # 写入内容
            file.write(note_content)
            # 如果提供了图片路径，则将图片添加到Markdown文件中
            if image_path and os.path.exists(image_path):
                # # ![测试图片](C:/Dropbox/YAN/D/2025/zhiguol/WeChatRead/test.jpg "测试图片") #图片存储的格式
                image_path = image_path.replace("\\","/")
                # file.write(f"\n\n![]({image_path})\n")
                file.write('\n') #换行顶格写，否则会变成文本
                file.write(rf'<img src={image_path} alt="测试图片" width="500" height="350">')
                file.write('\n\n') #必须给两个换行

    # 示例用法
    note_title = "My Note"
    note_content = """
This is an example note.

## Section 1
Here is some text for section 1.

## Section 2
Here is some text for section 2.
    """

    # 图片路径（如果有）
    image_path = r"C:\Dropbox\YAN\D\2025\zhiguol\WeChatRead\test.jpg"
    create_markdown_note(note_title, note_content, image_path)
    print(f"Markdown note '{note_title}.md' created successfully.")

def DownloadImage(book_name, article_index, book_article_title, image_url_dict):
    '''
    @Time    :   2025/01/22 12:44:43
    @功能    :   None
    article_index 章节的下标 便于排序
    book_article_title 章节的标题
    image_name 图片的名称
    图片名称的结构：章节的下标_每个url对应的第一行文本_x坐标_y坐标.jpg
    image_url_list 内部结果如下：
    {21:{'X坐标': 39, 'Y坐标': 21, 'className': 'wr_absolute wr_readerImage_opacity', 'src': 'https://res.weread.qq.com/wrepub/CB_22806930_22806930_2.png', '宽度': '719.048px', '高度': '151px'}, ...}
    '''
    
    book_path = rf"{BIC['base_path']}\{book_name}"
    if not os.path.isdir(book_path):
        os.makedirs(book_path)

    # 图片的URL
    # image_url = "https://res.weread.qq.com/wrepub/epub_43134609_5"
    images_dict = {}
    for key, url_dict in image_url_dict.items():
        img_name = rf"{book_path}\{article_index}_{book_article_title}_{url_dict['X坐标']}_{url_dict['Y坐标']}.jpg"
        image_dict = {
                'src':url_dict['src'],
                "image":img_name,
                "width":url_dict['宽度'],
                "heigth":url_dict['高度'],
                'X坐标':url_dict['X坐标'],
                'Y坐标':url_dict['Y坐标'],
        }
        if os.path.isfile(img_name): 
            images_dict[key] = image_dict
            continue
        try:
            # 发起请求获取图片内容
            response = requests.get(url_dict['src'])
            # response = requests.get(image_url)
            response.raise_for_status()  # 检查请求是否成功
            with open(img_name, "wb") as file:
                file.write(response.content)
            print("图片已成功保存到本地！")
        except requests.exceptions.RequestException as e:
            image_dict['image'] = None
            print(f"下载失败，错误信息：{e}")
            print("请检查链接的合法性或稍后重试。")

        images_dict[key] = image_dict

    return images_dict

def remove_transform_translate(input_string):
    # 使用正则表达式找到并移除 transform: translate(...)  和 ❶|❷|❸|❹|❺|❻|❼|❽|❾|❿ 等 部分
    output_string = re.sub(r'transform: translate\(\d+px, \d+px\);', '', input_string)
    output_string = re.sub(r'❶|❷|❸|❹|❺|❻|❼|❽|❾|❿', '', output_string)
    return output_string

if __name__=='__main__':
    # MainDemo()
    # 微信读书Main("https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180")
    # 微信读书Main("https://weread.qq.com/web/reader/77e326b072922e9177e6cb1kecc32f3013eccbc87e4b62e", book_name="对赌_test")

    # 微信读书Main("https://weread.qq.com/web/reader/214327005b6b3621437a4f5k16732dc0161679091c5aeb1", book_name="华尔街英语创始人的幸福成功学")

    # 重组文本(html_innerHtml)
    # 测试获取文本和图片的信息()

    # 微信读书MainV3("https://weread.qq.com/web/reader/19532980715c01921954a54", book_name="Python编程：从入门到实践")
    # 微信读书MainV3("https://weread.qq.com/web/reader/cf132e10813ab92e9g018088ka87322c014a87ff679a21ea", book_name="思辨力35讲：像辩手一样思考")

    微信读书MainV3("https://weread.qq.com/web/reader/cf132e10813ab92e9g018088kc81322c012c81e728d9d180", book_name="思辨力35讲：像辩手一样思考")

    # 微信读书MainV3("https://weread.qq.com/web/reader/214327005b6b3621437a4f5kc81322c012c81e728d9d180", book_name="赢者之心：华尔街英语创始人的幸福成功学")

    # 微信读书MainV3("https://weread.qq.com/web/reader/77e326b072922e9177e6cb1kc81322c012c81e728d9d180", book_name="对赌")

    # 微信读书MainV3("https://weread.qq.com/web/reader/f1e328e072710bfaf1e87e9k0aa32fc02bf0aa1883c60ae", book_name="明朝那些事儿")
    
    



