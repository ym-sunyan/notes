import os
# vscode 安装 markdown （Markdown Paste Image To okmd.dev OSS store）插件，
# 打开markdown笔记方法：
# 1 在vscode中打开一个markdown 笔记比如（my.md）
# 2 按下 ctrl+shift+v 就会重新打开一个页面显示笔记

def MarkDownDemo():
    '''
    @Time    :   2025/01/22 11:50:41
    @功能    :   None
    '''
    # 创建一个Markdown文件并写入内容
    file_name = "example.md"
    image_path = "图片地址"

    with open(file_name, "w", encoding="utf-8") as file:
        file.write("# 这是一个Markdown标题\n")
        file.write("## 这是一个二级标题\n")
        file.write("\n")
        file.write("这是一个段落。\n")
        file.write("\n")
        file.write("### 列表示例\n")
        file.write("- 第一项\n")
        file.write("- 第二项\n")
        file.write("- 第三项\n")
        file.write("\n")
        file.write("### 表格示例\n")
        file.write("| 表头1 | 表头2 | 表头3 |\n")
        file.write("|-------|-------|-------|\n")
        file.write("| 内容1 | 内容2 | 内容3 |\n")
        file.write("| 内容4 | 内容5 | 内容6 |\n")
        image_path = image_path.replace("\\","/")
        # file.write(f"\n\n![]({image_path})\n")
        file.write('\n')    #换行顶格写，否则会变成文本
        file.write(rf'<img src={image_path} alt="测试图片" width="500" height="350">')
        file.write('\n\n') #必须给两个换行
        file.write("| 表头1 | 表头2 | 表头3 |\n")
        file.write("|-------|-------|-------|\n")
        file.write("| 内容1 | 内容2 | 内容3 |\n")
        file.write("| 内容4 | 内容5 | 内容6 |\n")

    print(f"Markdown文件 {file_name} 已生成。")
    pass

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

def MarkDown():
    '''
    @Time    :   2025/01/22 11:11:19
    @功能    :   None
    '''
    
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
    note_content = """
This is an example note.

## Section 1
Here is some text for section 1.

## Section 2
Here is some text for section 2.
    """
    create_markdown_note(note_title, note_content, image_path)
    note_content = """
This is an example note.

## Section 1
Here is some text for section 1.

## Section 2
Here is some text for section 2.
    """
    create_markdown_note(note_title, note_content, image_path)

    print(f"Markdown note '{note_title}.md' created successfully.")