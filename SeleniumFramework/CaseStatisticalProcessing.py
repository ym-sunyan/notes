# -*- encoding: utf-8 -*-
#python>=3.6
'''
@File    :   CaseStatisticalProcessing.py
@Time    :   2023/11/29 17:54:49
@Author  :   sunyan
@Version :   1.0
@email   :   c_yansun
@Desc    :   None
'''

# here put the import lib
import os
import re
import time
import shutil
import datetime
import argparse
from BaseInfo import BaseInfo
from selenium_qti7 import selenium_qti
from openpyxl_excel import OpenpyxlExcel
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment
BIC = BaseInfo().base_info_dict

def GetVersion():
    return "1.0.0"

def GetXls(args):
    '''
    @Time    :   2022/12/14 14:03:40
    @功能    :   从命令行第二个参数中获取xls文件,如果没有则程序自动下载最新的xls文件
    返回值
    cmd_xls_sign=True表示是从命令行传入的参数;False表示不是从命令行传入可以理解为debug模式
    这个参数控制后面需要修改传入的文件名称
    '''
    xls_file = args.xls_file
    cmd_xls_sign = False
    if xls_file is None:
        return xls_file, False

    if os.path.dirname(xls_file) == "":
        xls_file = rf"{BIC['base_path']}\{xls_file}"
        if os.path.isfile(xls_file):
            return xls_file, True
    if os.path.isfile(xls_file):
        return xls_file, True
    
    return None, False

def FormatArparse():
    '''
    @Time    :   2022/12/21 14:38:44
    @功能    :   None
    '''
    parser = argparse.ArgumentParser(description="weeklyreport")
    parser.add_argument("-xls", "--xls_file",type=str, help="add xls file")
    parser.add_argument("-qdn", "--add_qdn",type=str,choices=["true","false"],help="Add a chart of statistical results")
    parser.add_argument("-v", "--version", action="version", version=GetVersion(), help="display version")
    parser.add_argument("-V", action="version", version=GetVersion(), help="display version")
    return parser

def InsertChart(xlsx_file, active_case_list):
    '''
    @Time    :   2023/11/30 14:53:56
    @功能    :   插入同级数据图表，原数据在图标的下面
    '''
    owner_counts_dict = {}
    for case_dict in active_case_list:
        try:
            owner_counts_dict[case_dict['Case_Owner']] += 1
        except:
            owner_counts_dict[case_dict['Case_Owner']] = 1

    # 插入统计图
    oe = OpenpyxlExcel(xlsx_file)
    oe.CreateExcel()
    sheet = oe.LoadOrCreateSheet("ActiveCases")
    rows = [[key, value] for key, value in owner_counts_dict.items()]
    rows.insert(0, ["onwer","counts"])
    oe.InsertData(sheet, rows, row=3,col=13)
    ws = oe.wb.active
    # 创建柱状图
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Owner Case Counts"
    chart.y_axis.title = 'Case Counts'
    # chart.x_axis.title = 'Sample length (mm)'

    # 设置数据
    # data = Reference(sheet, min_row=3, max_row=12, min_col=14, max_col=14)
    data = Reference(sheet, min_row=3, min_col=14, max_row=len(rows)+2, max_col=15)
    # data = Reference(ws,  min_row=1, min_col=2,  max_row=7, max_col=3)


    # 设置类别
    cats = Reference(sheet, min_col=13, min_row=4, max_row=len(rows)+2)
    # cats = Reference(ws, min_col=1, min_row=2, max_row=7)

    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)

    chart.legend = None # 隐藏图表的图例,图最右侧显示的内容

    # 设置图表的大小
    chart.width = 25
    chart.height = 15
    # 添加柱状图到工作表
    sheet.add_chart(chart, f"{get_column_letter(13)}{3}")

    oe.Save()

def CreateChart(xlsx_file, sheet_name, status, owner_counts_dict):
    '''
    @Time    :   2023/11/30 14:53:56
    @功能    :   创建堆叠图
    '''
    all_status = status[:]
    owner_list = []
    for key, status_dict in owner_counts_dict.items():
        # tmp = [key]
        # for status in all_status:
        #     tmp.append(status_dict[status])
        values = [value for value in status_dict.values()]
        tmp = (list(set(values)))
        if len(tmp) == 1 and tmp[0] == 0: continue
        values.insert(0, key)
        owner_list.append(values)
    all_status.insert(0, "owner")

    # 插入统计图
    oe = OpenpyxlExcel(xlsx_file)
    oe.CreateExcel()
    # sheet = oe.LoadOrCreateSheet("All Case")
    sheet = oe.LoadOrCreateSheet(sheet_name)

    oe.RendererTitle(sheet, all_status)
    oe.InsertData(sheet, owner_list)
    ws = oe.wb.active
    # 创建柱状图
    chart = BarChart()
    chart.type = "col"
    chart.style = 12
    chart.overlap = 100
    chart.grouping = "stacked"
    chart.title = "Owner Case Counts"
    chart.x_axis.title = 'owner'
    chart.y_axis.title = 'Case Counts'
    # 设置图表的大小
    chart.width = 38
    chart.height = 15

    data = Reference(ws, min_col=2, min_row=1, max_row=len(owner_list)+1, max_col=len(all_status))
    cats = Reference(ws, min_col=1, min_row=2, max_row=len(owner_list)+1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.shape = 4
    ws.add_chart(chart, f"A{len(owner_list)+2}")

    oe.Save()

def InsertData(xlsx_file, new_xlsx_fields, active_case_list, sheet_name):
    '''
    @Time    :   2023/12/01 16:51:22
    @功能    :   将数据写入excel
    '''
    oe = OpenpyxlExcel(xlsx_file)
    oe.CreateExcel()
    sheet = oe.LoadOrCreateSheet(sheet_name)

    # 默认字体设置
    font = Font(name='微软雅黑', size=10, bold=True, italic=False, vertAlign=None,
                underline='none', strike=False, color='ffffff')
    field_list = [field.replace("_", " ") for field in new_xlsx_fields]

    # 渲染Field顔色和樣式
    oe.RendererTitle(sheet, field_list, font)

    # 设置文本样式
    oe.SetTextAlignment(sheet, rows_list=[1], horizontal="center", vertical="center")

    # 渲染行顔色
    title_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    oe.RenderRow([1], title_fill)
    #設置行高度
    oe.SetRowHeight(sheet, [1], 35)

    # 格式化需要插入的数据
    row_datas = []
    for row_dict in active_case_list:
        tmp = []
        for key, value in row_dict.items():
            if key == "Days_Open":
                tmp.append(float(value))
            else:
                tmp.append(value)
        row_datas.append(tmp)

    # 插入数据
    oe.InsertData(sheet, row_datas)

    # 格式化超链接数据
    cell_link_list = []
    for i, row_dict in enumerate(active_case_list):
        cell_link_list.append(
            {"pos":[i+2, 5],
               "value":row_dict['Case_Number'], 
               "link":f"https://qualcomm-cdmatech-support.lightning.force.com/lightning/r/Case/{row_dict['Case_ID']}/view",
               "style":"Hyperlink"}
               )
    # 插入超链接
    oe.InsertHyperlink(sheet, cell_link_list)
    # 获得需要设置宽度的列
    for i, field in enumerate(new_xlsx_fields):
        if field == "Description":
            oe.setColWidth(sheet, i+1, 60)
        elif field == "Subject":
            oe.setColWidth(sheet, i+1, 30)
        else:
            oe.setColWidth(sheet, i+1, 20)

    # 区分单双号行
    single_number_list, double_number_list = [], []
    for i, row_dict in enumerate(active_case_list):
        row_number = i+2
        if (row_number)%2==0: double_number_list.append(row_number)
        else: single_number_list.append(row_number)

    # # 渲染行颜色
    # single_fill = PatternFill(start_color='B4C6E7', end_color='B4C6E7', fill_type='solid')
    # double_fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
    # oe.RenderRow(single_number_list,single_fill )
    # oe.RenderRow(double_number_list,double_fill )

    #设置元格边框顔色
    # 创建一个新的 Side 对象，设置边框样式为 'thin'，颜色为黑色
    ws = oe.wb.active
    side = Side(border_style='thin', color='ffffff')
    border = Border(left=side, right=side, top=side, bottom=side)
    # 将这个 Border 对象应用到单元格 'A1'
    for row in [1]+single_number_list+double_number_list:
        for cell in ws[row]:
            cell.border = border

    # 设置文本样式
    oe.SetTextAlignment(sheet,rows_list=single_number_list+double_number_list, horizontal="left", vertical="center")

    # 設置行高度
    oe.SetRowHeight(sheet, single_number_list+double_number_list, 35)

    # 设置除title外的字体样式
    ws = oe.wb.active
    font = Font(name='微软雅黑')
    for row in single_number_list+double_number_list:
        for cell in ws[row]:
            cell.font = font

    # 渲染行颜色
    single_fill = PatternFill(start_color='B4C6E7', end_color='B4C6E7', fill_type='solid')
    double_fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
    oe.RenderRow(single_number_list,single_fill )
    oe.RenderRow(double_number_list,double_fill )

    # link样式被冲刷，重新设置
    # 创建一个新的 Font 对象，设置字体颜色为蓝色
    font = Font(color='256FD0', bold=True, underline="single", size=14)
    # # 创建一个新的 Fill 对象，设置背景色为黄色
    # fill = PatternFill(start_color='FFFFFF00', end_color='FFFFFF00', fill_type='solid')
    # 创建一个新的 Alignment 对象，设置文字为居中对齐
    align = Alignment(horizontal='left', vertical='center')
    # 将这三个对象应用到单元格 'A1'
    for cell_dict in cell_link_list:
        cell = sheet.cell(cell_dict['pos'][0], cell_dict['pos'][1])
        # cell.style = cell_dict['style']
        cell.font = font
        # cell.aligment = align

    # 添加自动过滤功能
    # 设置单元格 'A1' 到 'J167' 的自动过滤功能
    # 开始位置
    begin_cell_pos = "A1"
    col_counts = get_column_letter(len(new_xlsx_fields))
    row_counts = 1 + len(active_case_list)
    end_cell_pos = f"{col_counts}{row_counts}"
    ws.auto_filter.ref = f"{begin_cell_pos}:{end_cell_pos}"

    col_list = []
    for i, field in enumerate(field_list):
        if field in ["Case Owner", "Chipset", "Case Number", "Days Open"]:
            col_list.append(get_column_letter(i+1))
    # 遍历列A的所有单元格
    for col in col_list:
        for row in ws[col]:
            # 设置单元格的对齐方式为居中
            row.alignment = Alignment(horizontal="center", vertical="center")
    # 设置文本样式
    oe.SetTextAlignment(sheet, rows_list=[1], horizontal="center", vertical="center")

    oe.Save()
    pass

def ClassifiedCase(all_status, case_info_list):
    '''
    @Time    :   2023/12/07 16:48:38
    @功能    :   None
    '''
    status_counts = [0 for i in range(len(all_status))]
    all_status_dict = dict(zip(all_status, status_counts))

    # 按照状态进行分类
    owner_counts_dict = {}
    for case_dict in case_info_list:
        owner_list = list(owner_counts_dict.keys())
        if case_dict['Case_Owner'] not in owner_list:
            owner_counts_dict[case_dict['Case_Owner']] = all_status_dict.copy()
        for status in owner_counts_dict[case_dict['Case_Owner']].keys():
            if status == case_dict['Status']:
                owner_counts_dict[case_dict['Case_Owner']][status] += 1
                break
    return owner_counts_dict


def Main():
    '''
    @Time    :   2023/11/29 17:54:53
    @功能    :   None
    '''
    parser=FormatArparse()
    args = parser.parse_args()
    BIC['xls_file'], cmd_xls_sign = GetXls(args) #cmd_xls_sign 两个是命令行传入的xls文件程序则
    print(args)
    print(BIC['xls_file'])

    # BIC['xls_file'] = rf"{BIC['base_path']}\report1701084276375.xls"
    BIC['xls_file'] = rf"{BIC['base_path']}\xlsx\report1701084276375.xls"
    
    # 生成需要新的xlsx文件的名称
    if BIC['xls_file'] != None:
        xlsx_path = os.path.dirname(BIC['xls_file'])
        xlsx_name = os.path.basename(BIC['xls_file']).split(".")[0]
        xlsx_file = rf"{xlsx_path}\{xlsx_name}.xlsx"
        
        # 创建转换后的日期时间戳
        time_str = re.findall(r'\d+', os.path.basename(BIC['xls_file']))[0]
        dt = datetime.datetime.fromtimestamp(int(time_str) / 1000)
        date_str = str(dt).split(".")[0].replace(":", "_")
        new_xls_folder = rf"{xlsx_path}\{date_str}"

        # 判断文件重复，则删除最新上传的 文件并退出
        if os.path.isdir(new_xls_folder):
            os.remove(BIC['xls_file'])
            return

    if BIC['xls_file'] is None:
        time_str = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
        google_data_path = rf"{BIC['google_data_path']}_{time_str}"
        qti = selenium_qti(browser=None,
                        url=BIC["base_url"],
                        chromedriver_path=BIC['chromedriver_path'],
                        google_data_path=google_data_path,
                        download_path=BIC['download_path'],
                        debug=True)
        qti.OpenChrome()
        BIC['xls_file'] = qti.DownloadReport()
        qti.Close()
        # 删除user_data
        shutil.rmtree(google_data_path)

    xlsx_path = os.path.dirname(BIC['xls_file'])
    xlsx_name = os.path.basename(BIC['xls_file']).split(".")[0]
    xlsx_file = rf"{xlsx_path}\{xlsx_name}.xlsx"
    
    # 创建转换后的日期时间戳
    time_str = re.findall(r'\d+', os.path.basename(BIC['xls_file']))[0]
    dt = datetime.datetime.fromtimestamp(int(time_str) / 1000)
    date_str = str(dt).split(".")[0].replace(":", "_")
    new_xls_folder = rf"{xlsx_path}\{date_str}"

    
    com_head_list, com_str_list, case_info_list = ReadCSV(BIC['xls_file']).out()
    active_case_list = []
    new_xlsx_fields = [
        "Account_Nick_Name",
        "Case_Owner",
        "Chipset",
        "Status",
        "Case_Number",
        "Days_Open",
        "TAM_Escalate_(L1)",
        "Subject",
        "Description",
        "Case_ID",
        ]

    all_status_case = []
    for case_dict in case_info_list:
        new_case_dict = {field:case_dict[field] for field in new_xlsx_fields}
        all_status_case.append(new_case_dict)
        if case_dict["Status"] in ["Closed", "Closed-Customer Requested"]: 
            continue
        active_case_list.append(new_case_dict)

    all_status = ['Closed', 'Closed-Customer Requested', 'Closed-Pending Your Approval', 'Customer Updated Case', 'Hold-Customer Information Required', 'Research-General', 'Hold-Pending Change Request', 'Open', 'Research-Internal Support']

    active_status = all_status[2:]
    owner_counts_dict = ClassifiedCase(active_status, case_info_list)
    # 绘制所有owenr 不同状态的统计图
    CreateChart(xlsx_file, "Active Case", active_status, owner_counts_dict)

    owner_counts_dict = ClassifiedCase(all_status, case_info_list)
    CreateChart(xlsx_file, "All Case", all_status, owner_counts_dict)

    # 将提取的数据写入excel
    InsertData(xlsx_file, new_xlsx_fields, active_case_list, sheet_name="ActiveCases")

    # 将提取的数据写入excel
    InsertData(xlsx_file, new_xlsx_fields, all_status_case, sheet_name="AllCase")

    # 绘制onwer 非close的统计图
    InsertChart(xlsx_file, active_case_list)   

    
    if not os.path.isdir(new_xls_folder):
        os.makedirs(new_xls_folder)
    
    # 修改文件名称
    new_xls_file = rf"{os.path.dirname(BIC['xls_file'])}\{date_str}.xls"
    shutil.move(BIC['xls_file'], new_xls_file)
    new_xlsx_file = rf"{os.path.dirname(BIC['xls_file'])}\{date_str}.xlsx"
    shutil.move(xlsx_file, new_xlsx_file)

    # 将文件转移到指定目录
    shutil.move(new_xls_file, new_xls_folder)
    shutil.move(new_xlsx_file, new_xls_folder)
    
    shutil.copytree(new_xls_folder, rf'\\10.233.202.137\Dropbox\Qualcomm\zhiguo\CaseStatisticalProcessing\{date_str}')

if __name__ == '__main__':
    Main()
    pass
