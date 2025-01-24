现有程序的限制：
    1 只能获取一本书的所有内容
        因为js的注入动作，不能被刷新打断否则注入的代码失效
    2 这里只能通过下一章的方式 翻页进行才能保证js注入始终有效

1 执行 WeChatRead.bat 
    自动创建虚拟环境并且安装需要的包
2 提供一本书的主目录
    如：https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180
    微信读书Main(begin_url="https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180")
3 必须在程序运行之后将阅读模型手动修改为“上下滚动阅读”
4  可以提前中断获取章节的url函数
    max_url_length 
    GetwereadQQBookAllUrl(qti, begin_url, save_file, max_url_length=10) 
    章节获取完成之后，需要关闭这个函数，再次执行程序


2025/01/08 10:58:37
1 自动将双排阅读切换为滚动阅读
    类中包含 isHorizontalReader 表示处于双页阅读；isNormalReader 表示处于滚动阅读
2 浏览器最大化
    canvas中的内容是绘制所得，一次js获得的内容就是绘制的copy，
    浏览器打开太小"\n"符号会非常多，且内容不能充满全屏导致出现大量换行
    # 最大化浏览器窗口
    qti.browser.maximize_window()
    有可能触发报错，让程序停止但是为了阅读内容的阅读性，不规避这个错误，触发则重启程序
3 获取目录中断后续处理
    再次获取根据最后的获取位置接着处理
4 获取目录的标题
5 目录缺少第一页的链接和信息（该bug后续修改，暂时时间不够）
    修改完成后，需要将 if begin_index+1 != len(contents_handles):
    修改为：if begin_index != len(contents_handles):


2025/01/23 17:57:11
微信阅读 这套程序解决了哪些问题
1 获得使用canvas渲染的文本
2 获得静态加载和动态加载的img 图片，并且根据y轴的值插入到文本的相应位置
    使用滚动条逐次向下滚动的方式
    图片本存储到本地和书名相同的文件夹中，图片存储的格式如下：
        图片名称的结构：章节的下标_每个url对应的第一行文本_x坐标_y坐标.jpg
        如:C:\Dropbox\YAN\D\2025\zhiguol\WeChatRead\Python编程：从入门到实践\4_第1章起步_86_5292.jpg

3 获得pre的code内容，并且根据y轴的值插入到文本的相应位置
    直接获取pre源码，并且去除相关的属性
4 获得动态加载的文本，并给根据x轴的值让文本左右有序，根据y轴的值让文本上下有序
    使用滚动条逐次向下滚动的方式
5 将获得的文本，图片，code 写入markdown文件中
6 去除原有的通过点击下一章的方式获取所有的url，然后通过open url来逐个获取文本内容
    因为 《赢者之心：华尔街英语创始人的幸福成功学》 这本书的url通过点击下一章部分章节内的url没有，
        导致程序结构性异常
    书链接： https://weread.qq.com/web/reader/214327005b6b3621437a4f5kc81322c012c81e728d9d180
    异常触发位置：
        目录：  第一章 如何确定你的人生使命
        内部章节没有各自的url
    上面的数导致的bug：将永远卡死在下面代码位置
    if begin_index != len(contents_handles):
        GetwereadQQBookAllUrlV3(qti, last_url, save_file, begin_index=begin_index)
    修改后的方法：
        1 需要确保获得所有url地址的方法一次完成，如果完成不了直接退出程序，再次获取
        2 使用公用的url 在url链接中使用 "与上一个url形同。需要通过点击下一页/下一章 查看下一页/下一章内容" 这句话代替
        如下：
        ...
        4;https://weread.qq.com/web/reader/214327005b6b3621437a4f5k16732dc0161679091c5aeb1
        5;与上一个url形同。需要通过点击下一页/下一章 查看下一页/下一章内容
        6;与上一个url形同。需要通过点击下一页/下一章 查看下一页/下一章内容
        ...

7 生成的markdown基本的目录结构，暂时看来生成的目录结构已不是完整正确，有的可能需要手动修改一下
8 过滤了部分特殊符合和字符串
9 暂时只能使用虚拟的浏览器，然后手动登录微信，否则会触发bug >>> 找不到元素
10 程序根据书的名称生成url链接和书的markdown文件
    书的url链接文件名称格式：url_list_书名称.txt
    书的markdown文件名称格式:书名称.md

2025/01/24 10:18:12
BUG 1:页面纯图片导致canvas内容为空触发bug。
     bug位置：article_title=canvas_info[0]['content'].strip()
修改：将Markdown中的图片的绝对地址改为相对地址