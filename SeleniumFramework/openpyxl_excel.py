# -*- encoding: utf-8 -*-
#python>=3.6
'''
@File    :   openpyxl_excel.py
@Time    :   2023/11/27 10:22:26
@Author  :   sunyan
@Version :   1.0
@email   :   c_yansun
@Desc    :   使用openpyxl操作excel
实现创建excel；创建sheet；渲染title；写入title；修改cell value；写入cell value等功能
'''
# here put the import lib
import re
import os, sys
import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Border, Side, Alignment
from openpyxl.utils.exceptions import IllegalCharacterError
base_path = os.path.dirname(sys.argv[0])

def ReplaceIllegalCharacters(string, char=""):
    '''
    @Time    :   2023/12/18 17:31:30
    @功能    :   替换excel不能写入的所有特殊字符
    '''
    # pattern = re.compile(r'[\U0001000 - \U001ffff]')
    pattern = re.compile(r'[\U00000000-\U0010FFFF]')
    return pattern.sub(string, char)

class OpenpyxlExcel(object):
    '''
    @Time    :   2023/11/27 10:25:25
    @Author  :   sunyan
    @Desc    :   None'''
    def __init__(self, excel_name=None):
        self.excel_name = excel_name
        self.wb = None
        self.sheet = None
        if self.excel_name is None:
            print(f"{self.excel_name} =None，请提供excel文件全路径名称")
            return
        excel_file_path = os.path.dirname(excel_name)
        if not os.path.isdir(excel_file_path):
            os.makedirs(excel_file_path)
    
    def CreateExcel(self):
        '''
        @Time    :   2022/01/10 10:16:39
        @功能    :   加载或者创建新表
        True表示表已经存在； False 表示创建的新表
        '''
        if os.path.isfile(self.excel_name):
            self.wb = openpyxl.load_workbook(self.excel_name)
            return True
        else:
            print(f"{self.excel_name} 不存在，将创建为新表")
            self.wb = openpyxl.Workbook()
            return False
        
    def ReadExcel(self, sheet_list=[]):
        '''
        @Time    :   2022/04/14 15:40:36
        @功能    :   读取excel所有sheet内容
        '''
        # 获得title
        all_keys = []
        datas_dict = {}
        for sheet in sheet_list:
            row, column = sheet.max_row+1, sheet.max_column+1
            tmp_datas = {}
            title = sheet.title
            all_keys.append(title)
            for i in range(1,row):
                if sheet.cell(i,1).value == None:
                    break
                line_data = []
                for j in range(1, column):
                    value = sheet.cell(i,j).value
                    if value is None:
                        value = ""
                    value = rf"{value}"
                    line_data.append(value)
                line_data.append(rf"{i};{column}")
                # tmp_datas.append({line_data[0]:line_data})
                tmp_datas[line_data[0]] = line_data
            datas_dict[title] = tmp_datas
        return all_keys, datas_dict

    def GetSheetAllDatas(self, sheet):
        '''
        @Time    :   2022/01/10 09:37:44
        @功能    :   获得所有数据
        '''
        datas_l = []
        for row in sheet.iter_rows():
            tmp = [cell.value for cell in row]
            datas_l.append(tmp)
        return datas_l

    def UpdateData(self, sheet, datas):
        '''
        @Time    :   2022/01/10 09:43:51
        @功能    :   不同方法提供不同的键值
        该方法同ChangeCellValue()
        '''
        if datas == []:
            return False
        try:
            sheet.cell(datas["key"][0], datas['key'][1]).value=datas["value"] #修改第二行第二列的值
            return True
        except:
            return None
        # # 方法1
        # datas = {
        #     "key":"A2",
        #     "value":"111111"
        # }
        # sheet[datas['key']].value='1111111' #修改第二行第二列的值
        # 方法2
        # datas = {
        #     "key":[2,2],
        #     "value":"111111"
        # }
        # sheet.cell(datas["key"][0], datas['key'][1]).value=datas["value"] #修改第二行第二列的值

        # # 方法3
        # datas = {
        #     "key":[2,3],
        #     "value":"111111"
        # }
        # sheet.cell(datas["key"][0], datas['key'][1],datas["value"]) #修改第二行第二列的值
        pass

    def ChangeCellValue(self, sheet, change_value_list):
        '''
        @Time    :   2023/11/27 11:59:20
        @功能    :   修改单元格内容
        '''
        for value_obj in change_value_list:
            for key, value in value_obj.items():
                sheet[f"{key}"].value=value
        pass

    def GetAllSheetName(self):
        '''
        @Time    :   2023/11/27 11:01:20
        @功能    :   获得表格中所有的sheet name
        '''
        return self.wb.sheetnames #方法一
    
    def GetAllSheets(self):
        '''
        @Time    :   2022/01/10 10:19:56
        @功能    :   获得表格中所有的sheet句柄以及sheet name
        不用字典存储方法存储的原因是
        ecxel表中大小写不敏感 sheet1 Sheet1是不能共同存储的
        但是python中对大小写敏感 sheet1 Sheet1是能共同存储的
        因此需要让python也大小写不敏感才行
        '''
        sheet_list = [{"sheet_name":sheet.title, "sheet":sheet} for sheet in self.wb.worksheets] #方法一
        return sheet_list

    def CreateSheet(self, sheet_name, index=0):
        '''
        @Time    :   2023/11/27 11:04:29
        @功能    :   创建新的sheet
        '''
        try:
            return self.wb.create_sheet(index=index, title=sheet_name)
        except:
            return None
    
    def LoadOrCreateSheet(self, sheet_name, index=0):
        '''
        @Time    :   2022/01/10 10:21:10
        @功能    :   加载或者创建新的sheet
        创建新表的时候指定位置，默认为第一页
        '''
        sheet_list = self.GetAllSheets()
        for sheet in sheet_list:
            if sheet["sheet_name"].lower() == sheet_name.lower():
                return sheet["sheet"]
        sheet = self.CreateSheet(index=index, sheet_name=sheet_name)
        return sheet
    
    def InsertData(self, sheet, datas, row=2, col=1):
        '''
        @Time    :   2022/04/14 15:43:53
        @功能    :   插入数据
        datas格式
        [["a","b"],["a","b"],["a","b"],["a","b"],....]
        row:数据插入的开始位置。如果不提供则默认从第二行开始，第一行留给title
        '''
        
        # 填充样式设置
        # fill = PatternFill(fill_type='darkUp',start_color='FFFF00',end_color='FF0000')
        # fill = PatternFill(start_color ='FFFF00', end_color = 'FFFF00', fill_type = 'solid')  #填充黄色
        # sheet.cell(row,i+1).fill=fill
        for i, value_list in enumerate(datas):
            for j, value in enumerate(value_list):
                # if value.isdigit():
                #     sheet.cell(row+i, j+col).value=int(value) 
                # else:
                #     sheet.cell(row+i, j+col).value=value
                try:
                    sheet.cell(row+i, j+col).value=value
                except IllegalCharacterError:
                    sheet.cell(row+i, j+col).value=ReplaceIllegalCharacters(value)
                    pass
        pass

    def RendererTitle(self, sheet, title_list, font=None,):
        '''
        @Time    :   2022/01/10 12:11:19
        @功能    :   渲染并且写入title
        title_list:所有标题，该字段一旦提供则默认从A1开始渲染
        font：单元格样式
        '''
        cols = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","I","S","T","U","V","W","X","Y","Z"]

        if font is None:
            # 默认字体设置
            font = Font(name='微软雅黑', size=14, bold=False, italic=False, vertAlign=None,
                        underline='none', strike=False, color='FF000000')
        for i, title in enumerate(title_list):
            sheet[f"{cols[i]}1"].font=font
            sheet[f"{cols[i]}1"].value=title
        pass

    def InsertHyperlink(self, sheet, dict_list):
        '''
        @Time    :   2023/11/30 10:28:58
        @功能    :   给单元格插入超链接
        dict_list=[
            {"pos":"a1","link":"https://www.baidu.com","value":"百度", "style":"Hyperlink"},
            {"pos":"a2","link":"https://www.baidu.com","value":"百度", "style":"Hyperlink"},
            ...
            ]
        其中pos可以是A1,也可以是[1,1]
        '''
        if isinstance(dict_list[0]["pos"], list):
            for cell_dict in dict_list:
                cell = sheet.cell(cell_dict['pos'][0], cell_dict['pos'][1])
                cell.value = cell_dict['value']
                cell.hyperlink = cell_dict['link']
                cell.style = cell_dict['style']
        else:
            for cell_dict in dict_list:
                cell = sheet[cell_dict['pos']]
                cell.value = cell_dict['value']
                cell.hyperlink = cell_dict['link']
                cell.style = cell_dict['style']
        pass

    def RendererCell(self, sheet, cell_position_list, font=None,):
        '''
        @Time    :   2023/11/27 11:58:29
        @功能    :   渲染单元格
        cell_position_list：表示需要渲染的特定的单元格位置。如果title——list存在则该参数无效
            如：cell_position_list=["A5","C9","D10","E15",]
        font：单元格样式
        '''
        if font is None:
            # 默认字体设置
            font = Font(name='微软雅黑', size=14, bold=False, italic=False, vertAlign=None,
                        underline='none', strike=False, color='FF000000')

        for cell_pos in cell_position_list:
            sheet[cell_pos].font = font
        pass

    def RenderRow(self, row_number_list=[], row_fill=None):
        '''
        @Time    :   2023/11/30 12:29:15
        @功能    :   对excel整行进行渲染
        注意这里的渲染只是针对有数据的行区域
        row_number_list=[5, 7, 9] 对5，7，9三行渲染
        '''
        if row_number_list == []:
            print("必须提供行数据")
            return
        ws = self.wb.active
        if row_fill is None:
            # 设置单元格的背景颜色
            row_fill = PatternFill(start_color='91AA9D', end_color='91AA9D', fill_type='solid')
        for i, row_number in enumerate(row_number_list):
            for cell in ws[f'{row_number}:{row_number}']:
                cell.fill = row_fill
        pass

    def RenderRowV2(self, min_row=1, max_row=1, min_col=1, max_col=1, fill=None):
        '''
        @Time    :   2023/11/30 12:39:05
        @功能    :   None
        min_row=1, 从第几行开始
        max_row=1, 到第几行结束
        min_col=1, 从第几列开始
        max_col=1 到第几列结束
        fill 颜色.不提供默认黄色
        '''
        # 创建一个PatternFill对象
        if fill is None:
            fill = PatternFill(start_color='fff000', end_color='fff000', fill_type='solid')
        # 设置数据区域单元格的背景颜色
        ws = self.wb.active
        for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
            for cell in row:
                cell.fill = fill
        pass

    def setColWidth(self, sheet, colunm_number=1, width=60):
        '''
        @Time    :   2023/11/30 12:48:11
        @功能    :   设置列宽
        colunm_number 列位置
            colunm_number=1, 则为A
            colunm_number=2, 则为B
            以此类推
            get_column_letter函数根据数字得出A B C .... 
        '''
        colunm = get_column_letter(colunm_number)
        sheet.column_dimensions[colunm].width= width
        pass

    def SetRowHeight(self, sheet, row_number_list, height):
        '''
        @Time    :   2023/11/30 13:00:45
        @功能    :   设置行高
        '''
        for row_number in row_number_list:
            sheet.row_dimensions[row_number].height= height #设置行高
        pass

    def SetTextAlignment(self, sheet, cell_pos_list=[], rows_list=[], horizontal="left", vertical="center"):
        '''
        @Time    :   2023/12/04 11:59:17
        @功能    :   设置文本对齐方式
        cell_pos_list:设置某一组单元格的文本样式
        rows_list：表示设置某一个的文本样式
        # horizontal参数：单元格文本水平对齐方式：
        # 'left'：左对齐
        # 'right'：右对齐
        # 'center'：居中对齐
        # 'centerContinuous'：跨列居中对齐
        # 'distributed'：分散对齐
        # 'fill'：填充对齐
        # 'general'：常规对齐
        # 'justify'：两端对齐
        # vertical参数，文本垂直对齐方式：
        # 'center'：居中对齐
        # 'distributed'：分散对齐
        # 'justify'：两端对齐
        # 'bottom': 底部对齐
        # 'top': 顶部对齐
        horizontal=['left', 'right', 'center', 'centerContinuous',
                     'distributed', 'fill', 'general', 'justify',], 
         vertical=['center', 'top', 'distributed', 'bottom', 'justify',]
        '''
        align = Alignment(horizontal=horizontal, vertical=vertical)
        for cell_pos in cell_pos_list:
            sheet[cell_pos].alignment = align
        if rows_list != []:
            ws = self.wb.active
        # 设置整行单元格文本水平对齐方式
        for row in rows_list:
            for cell in ws[row]:
                cell.alignment = align
        pass
    
    def MergeCellLine(self, sheet, row, begin, end, info):
        '''
        @Time    :   2022/02/16 11:20:19
        @功能    :   合并单元格并写入
        '''
        sheet.merge_cells(f'{begin}{row}:{end}{row}')
        sheet.cell(row, 1).value=info
        pass
    
    def Save(self):
        '''
        @Time    :   2023/11/27 11:21:39
        @功能    :   None
        '''
        self.wb.save(self.excel_name)
        pass
    
def Main():
    '''
    @Time    :   2023/11/27 13:07:42
    @功能    :   None
    '''
    excel_file = rf"{base_path}\test.xlsx"
    oe = OpenpyxlExcel(excel_file)
    oe.CreateExcel()
    sheet_list = oe.GetAllSheets()
    sheet_name = "sheet5"
    sheet = oe.LoadOrCreateSheet(sheet_name)
    if sheet is None: exit()

    # 获得sheet所有数据
    sheet_all_datas = oe.GetSheetAllDatas(sheet)
    # 渲染并添加title
    oe.RendererTitle(sheet, ["A", "b","c"])

    # 渲染单元格
    oe.RendererCell(sheet, cell_position_list=["A5","C9","D10","E15",])

    # 修改单元格内容
    change_value_list=[
        {"A2":20,},
        {"A5":100,}
    ]
    oe.ChangeCellValue(sheet, change_value_list)
    # 写入数据
    new_datas = [["a1","a2","a3",],
                ["a1","a2","a3",],
                ["a1","a2","a3",],
                ["a1","a2","a3",],
                ["a1","a2","a3",],
                ["a1","a2","a3",],
                ["a1","a2","a3",],
                ]
    oe.InsertData(sheet, new_datas, row=2)
    oe.Save()

if __name__ == '__main__':
    Main()
