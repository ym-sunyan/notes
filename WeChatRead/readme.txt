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
