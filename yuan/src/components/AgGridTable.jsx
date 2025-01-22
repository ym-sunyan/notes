import React, { useState, useRef, useEffect } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { saveAs } from 'file-saver';
import { Space, Modal, message } from 'antd';
import { Button, Select, Form, Input, AutoComplete } from 'antd';
import * as fetch_api from "./fetch_data"
import ClipboardJS from 'clipboard';
import Password from 'antd/es/input/Password';
{/* 
AgGridReact 设置过滤器的类型
常用的过滤器类型：
1. agTextColumnFilter
作用：用于文本类型的列过滤。
功能：允许用户输入文本进行过滤，可以选择包含、等于、不等于、开始于、结束于等条件。
使用场景：适用于字符串类型的数据列，例如姓名、地址等。
2. agNumberColumnFilter
作用：用于数字类型的列过滤。
功能：允许用户输入数字进行过滤，可以选择等于、不等于、小于、大于、小于等于、大于等于等条件。
使用场景：适用于数值类型的数据列，例如年龄、价格等。
其他常用过滤器类型
agDateColumnFilter
作用：用于日期类型的列过滤。
功能：允许用户选择日期进行过滤，可以选择等于、不等于、在之前、在之后等条件。
使用场景：适用于日期类型的数据列，例如生日、订单日期等。
agSetColumnFilter ：：：：：：：：：：：：：：：：：：这个属于收费功能无法使用
作用：用于枚举类型的列过滤。
功能：允许用户从预定义的值集合中选择进行过滤。
使用场景：适用于具有固定值集合的数据列，例如国家、状态等。
还可以完全自定义过滤器：：：：：：：：：：：：：：：：：：这个属于收费功能无法使用
使用实例
const columnDefs = [
    { headerName: "姓名", field: "name", filter: 'agTextColumnFilter' },
    { headerName: "年龄", field: "age", filter: 'agNumberColumnFilter' },
    { headerName: "生日", field: "birthday", filter: 'agDateColumnFilter' },
];
AgGridReact的调用实例
<AgGridReact
    columnDefs={columnDefs}
    rowData={rowData}
    onGridReady={onGridReady}
    rowSelection="multiple"
    defaultColDef={{ 
        sortable: true, //使所有列都可以排序。用户可以点击列头来对该列的数据进行升序或降序排序
        resizable: true, //使所有列都可以调整宽度。用户可以拖动列头的边缘来改变列的宽度。
        filter: true //每个字段可以搜索，在这里设置的原因是我们可以自定义搜索条件 localeText
    }}
    localeText={localeText} //自定义过滤器的显示内容
/> */}
// table可以显示的总字段

// AgGridReact字段搜索条件的英文到中文切换
const localeText = {
    // 设置本地化文本
    filterOoo: '过滤...',
    applyFilter: '应用过滤',
    blank: '空白', // 替换 blank
    notBlank: '非空白', // 替换 not blank

    // 文本过滤器
    contains: '包含',
    notContains: '不包含',
    equals: '等于',
    notEqual: '不等于',
    startsWith: '开始于',
    endsWith: '结束于',
    // startsWith: '', //无法通过设置空格让其消失
    // 数字过滤器
    lessThan: '小于',
    greaterThan: '大于',
    lessThanOrEqual: '小于等于',
    greaterThanOrEqual: '大于等于',
    inRange: '在范围内',
    // 其他本地化文本...
};

const table_fileds = ["姓名","性别","年龄","住址","出生日期","婚姻状况",
    "外貌","身高","体重","月收入","年收入","希望安家城市",
    "学历","专业","学校",
    "房产(数量)","房贷款","车(数量)","车贷款",
    "工作类型","工作城市","工作单位",
    '性格',"兴趣爱好","是否喝酒","是否吸烟","子女(个)"]

// 初始化时候table显示的字段
const now_show_fields = ["姓名","性别","年龄","住址","出生日期","婚姻状况",
    "外貌","身高","体重","月收入","年收入","希望安家城市",
    "学历","专业","学校",
    "房产(数量)","房贷款","车(数量)","车贷款",
    "工作类型","工作城市","工作单位",
    '性格',"兴趣爱好","是否喝酒","是否吸烟","子女(个)"]
let numbers = []
for(var i=0; i<table_fileds.length; i++){
    if (now_show_fields.indexOf(table_fileds[i]) === -1) continue
    numbers.push(i)
}
const btn_css = { height:40, fontSize:"15px"}
const div_css = {
    position:"sticky",
    top:0, //当页面滚动到这个元素的顶部时，它会变成固定定位
    zIndex: 1000, //确保div在页面其他内容之上
}
function InitSelectOptions(items){
    let options = []
    for(var i=0; i<items.length; i++){
      // options.push(<Select.Option value={(i+1).toString()}>{items[i]}</Select.Option>)
      options.push(<Select.Option key={items[i]} value={i}>{items[i]}</Select.Option>)
    }
    return options
  }
function initColumns(table_fileds){
    let fields = []
    for(let item of table_fileds){
        fields.push(item)
    }
    const columns = []
    for(let i=0; i<fields.length; i++){
        // const column = { headerName: fields[i], field: fields[i], sortable: true, filter: true }
        // 设置不同的过滤器 agSetColumnFilter 高级过滤器是收费的，自定义过滤器也是收费的
        const column = {headerName: fields[i],field: fields[i]}
        if((["年龄","身高","体重","月收入","年收入","房产(数量)","车(数量)","子女(个)"].indexOf(fields[i]) !== -1)){
            column["filter"] = "agNumberColumnFilter"
        }else if((["出生日期"].indexOf(fields[i]) !== -1)){
            column["filter"] = "agDateColumnFilter"
            // column["sortable"] = false
        }else{
            column["filter"] = "agTextColumnFilter"
        }
        // column["filter"] = false //暂时不支持单字段搜索
        // column["sortable"] = false //暂时不支持字段排序
        column['width'] = 150

        columns.push(column)
    }
    return columns
}

function formatData(id_value, data_keys){
    const data = {id:id_value}
    for(let i=0; i<data_keys.length; i++){
        data[data_keys[i]] = ""
    }
    return data
}
var items = []


const CopyText = ({textToCopy} ) => {
    const buttonRef = useRef(null)
    useEffect(()=>{
        if (buttonRef.current) {
            debugger
            clipboard = new ClipboardJS(buttonRef.current, {
              text: () => textToCopy,
            });
            debugger
            clipboard.on('success', () => {
              alert('复制成功！');
            });
      
            clipboard.on('error', () => {
              alert('复制失败');
            });
      
            // 组件卸载时销毁 ClipboardJS 实例
            return () => {
              clipboard.destroy();
            };
        }
    },[])
    return (
        <Button ref={buttonRef} type="primary" style={btn_css} >复制文本</Button>
    );
};

const AgGridTable = () => {
    const gridApi = useRef(null);
    const [form] = Form.useForm()
    const [rowData, setRowData] = useState([]);
    const [columnDefs, setColumnDefs] = useState(null);
    const [searchText, setSearchText] = useState(null);
    const [data_keys, setDataKeys] = useState([])
    const [copy_text, setCopyText] = useState(null)
    const [show_fileds, setShowFileds] = useState(table_fileds)
    const [search_fileds, setSearchFileds] = useState({})

    useEffect(()=>{
        // Demo 发送 GET 请求
        fetch_api.post("http://10.233.202.137:7767/information_table")
        .then(res => {
                // console.log(res)
                let new_datas = []
                for(let i=0; i<res.datas.length; i++){
                    let tmp_obj = {}
                    for(let key in res.datas[i]){
                        if(table_fileds.indexOf(key) === -1) continue
                        tmp_obj[key]=res.datas[i][key]
                    }
                    console.log(tmp_obj['性格'])
                    tmp_obj['性格'] = tmp_obj['性格'].toString(",")
                    new_datas.push(tmp_obj)
                }
                setRowData(new_datas)
            })
        .catch(error => {console.error(error)});
        setColumnDefs(initColumns(now_show_fields))

        // 动态获取web和数据库的table映射表
        // fetch_api.get("http://10.233.202.137:7767/get/fieldMapping")
        // .then(data => {
        //         console.log(data['field_mapping'])
        //         debugger
        //         setColumnDefs(initColumns(data['field_mapping']))
        //         setDataKeys(data.table_keys)
        //     })
        // .catch(error => {
        //     console.error(error)
        // });
    },[])

    const onGridReady = (params) => {
        gridApi.current = params.api;
        gridApi.current.sizeColumnsToFit() //表格大小自适应
    };

    const onRowDoubleClicked = (event) => {
        const { node } = event;
        form.setFieldsValue(node.data)
        setOpen(true)
    };
    const addRow = () => {
        showModal()
        form.setFieldsValue(formatData(parseInt(rowData[rowData.length-1].id,10)+1, data_keys))
    };

    const deleteRows = () => {
        const selectedNodes = gridApi.current.getSelectedNodes();
        const selectedData = selectedNodes.map(node => node.data);
        const newData = rowData.filter(row => !selectedData.includes(row));
        setRowData(newData);
        gridApi.current.deselectAll();
        for (let i=0; i<selectedData.length; i++){
            debugger
            fetch_api.del(`http://10.233.202.137:7767/datas/${selectedData[i].id}`)
                .then(() => console.log("Resource deleted"))
                .catch(error => console.error(error));
        }
    };

    const copyRows = () => {
        const selectedData = gridApi.current.getSelectedRows();
        debugger
        
        const copyData = selectedData.map(row => {
            let datas = []
            for(let i=0; i<data_keys.length; i++){
                datas.push(row[data_keys[i]])
            }
            return datas.join(", ")
        }).join('\n');
        // setCopyText(copyData)
        navigator.clipboard.writeText(copyData).then(() => alert('Copied to clipboard!'));
    };

    const downloadRows = () => {
        const selectedData = gridApi.current.getSelectedRows();
        console.log(selectedData)
        if (selectedData.length === 0){
            alert("你没有选择任何数据")
            return
        }
        debugger
        const csvContent = selectedData.map(row => `${row.make},${row.model},${row.price}`).join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        saveAs(blob, 'data.csv');
    };

    const onQuickFilterChanged = (event) => {
        const filterText = event.target.value;
        setSearchText(filterText)
        console.log(filterText)
        debugger
        if (filterText===""){
            setRowData(items)
        }else{
            setRowData(filterText ? [...items].filter(row => Object.values(row).join(' ').toLowerCase().includes(filterText.toLowerCase())) : rowData);
        }
    };

    // Model 所有操作 开始
    const [open, setOpen] = useState(false);
    const showModal = () => setOpen(true)
    const handleCancel = () => setOpen(false);
    // cancel 操作
    const onReset=(value)=>setOpen(false)

    const onFinish = (values) => {
        const last_data_id = parseInt(rowData[rowData.length-1].id, 10)
        // 最后条数据的id比当前id小，则是增加数据
        if (last_data_id < values.id){
            console.log('增加数据:', values);
            setRowData([...rowData, values]);
            values.id = values.id.toString()
            fetch_api.post("http://10.233.202.137:7767/datas", values)
        }else{
            console.log('修改数据:', values);
            let new_rowData = [...rowData]
            new_rowData[values.id] = values
            fetch_api.patch(`http://10.233.202.137:7767/datas/${values.id}`, values)
                .then(data =>{  console.log(data) })
                .catch(error => { console.error(error) });
            setRowData(new_rowData);
        }
        setOpen(false)
      };
    const onFinishFailed = (errorInfo) => {
        console.log('Failed:', errorInfo);
        showModal()
    };
    const ChangeTableShowFileds=(values)=>{
        console.log(values)
        // setShowFileds(values)
        values.sort((a, b) => a - b); //修改顺序，使其有序
        let fields = []
        for(let index of values){
            fields.push(table_fileds[index])
        }
        debugger
        setColumnDefs(initColumns(fields))
    }
    // Model 所有操作 结束
    // 初始化 每页显示的数量， 这个需要添加到配置中
    // 初始化 每页显示量，以及总共有多少个显示量可选，这个需要添加到配置中
    const pageSize = 20
    const paginationPageSizeSelector = [10, 20, 50, 100, 500]

    const onFilterChanged = () => {
        if (gridApi) {
            const filter_obj_arr = gridApi.current.getFilterModel();
            let new_search_fileds = {...search_fileds}
            new_search_fileds["filed_search"] = filter_obj_arr
            setSearchFileds(new_search_fileds)
        }
    };

    const onSortChanged=(params)=>{
        // 捕获排序事件
        // 取最后一次的排序
        const index = params.columns.length-1
        message.info(params.columns[index].colId)
        message.info(params.columns[index].sort)
        let new_search_fileds = {...search_fileds}
        new_search_fileds["sort"] = {
            filed:params.columns[index].colId,
            sort:params.columns[index].sort
        }
        setSearchFileds(new_search_fileds)
    }

    return (
        <div>
            <div style={{textAlign:"left"}}>
                注意这里table中默认显示的字段需要可以通过设置来控制,数据一次返回1790条数据，延迟1秒<br/>
                这张表的功能定位：暂时是快速筛选和删除用户，后续功能待开发
                <div><b>Version: 1.0</b></div><br/>
                <span style={{fontSize:20}}><b>修改表格显示内容</b></span>&nbsp;&nbsp;
                <Select 
                    mode="multiple"
                    maxTagCount={1}
                    defaultValue={numbers}
                    maxTagPlaceholder={(values) => `+${values.length} more`} // 自定义超出时的显示内容
                    onChange={ChangeTableShowFileds}
                    style={{width:250}}>
                        {InitSelectOptions(show_fileds)}
                </Select>
            </div>
            {columnDefs&&
            <div className="ag-theme-alpine" style={{ 
                height: "800px",
                width: '100%'
                }}>
                <div style={div_css}>
                    <div style={{paddingBottom:5, paddingTop:5, textAlign:"center",textAlign:"left"}}>
                        <Space>
                            <Button type="primary" style={btn_css} onClick={addRow}><b>Add Row</b></Button>
                            <Button type="primary" style={btn_css} onClick={copyRows}><b>Copy Selected Rows(功能实现中...)</b></Button>
                            <Button style={btn_css} onClick={deleteRows} type="primary" danger><b>Delete Selected Rows</b></Button>
                        </ Space>
                        
                    </div>
                </div>
                <AgGridReact
                    columnDefs={columnDefs}
                    rowData={rowData}
                    onGridReady={onGridReady}
                    onRowDoubleClicked={onRowDoubleClicked}
                    rowSelection="multiple"
                    // suppressRowDeselection //开启之后选中无法取消
                    gridOptions={{
                        pagination:true,
                        paginationPageSize:pageSize,
                        paginationPageSizeSelector:paginationPageSizeSelector,
                    }}
                    defaultColDef={{ 
                        sortable: true, //使所有列都可以排序。用户可以点击列头来对该列的数据进行升序或降序排序
                        resizable: true, //使所有列都可以调整宽度。用户可以拖动列头的边缘来改变列的宽度。
                        filter: true //每个字段可以搜索，在这里设置的原因是我们可以自定义搜索条件 localeText
                    }}
                    onFilterChanged={onFilterChanged} //捕获用户输入的每个字段的搜索条件
                    localeText={localeText}
                    onSortChanged={onSortChanged}
                />
            </div>
            }
            <Modal title="Update LLM LVM" open={open} onCancel={handleCancel} footer={false} /*false不显示默认按钮 */ >
                <Form
                    form={form}
                    name="basic"
                    labelCol={{span: 8,}}
                    wrapperCol={{span: 16,}}
                    style={{maxWidth: 600,}}
                    onFinish={onFinish}
                    onFinishFailed={onFinishFailed}
                    onReset={onReset}
                    autoComplete="off"
                >
                    <Form.Item label="ID" name="id"
                        rules={[ { required: true, message: 'Please input your username!', }, ]}
                    >
                    <Input disabled />
                    </Form.Item>
                    <Form.Item label="LLM Model" name="llm_model"
                        rules={[ { required: true, message: 'Please input your username!', }, ]}
                    >
                    <Input />
                    </Form.Item>
                    <Form.Item label="CL" name="cl"
                        rules={[{message: 'Please input your username!',},]}
                    >
                    <Input />
                    </Form.Item>
                    <Form.Item label="ARN" name="arn"
                        rules={[ {message: 'Please input your username!', }, ]}
                    >
                    <Input />
                    </Form.Item>
                    <Form.Item label="Feature" name="feature"
                        rules={[ {message: 'Please input your username!', }, ]}
                    >
                    <Input />
                    </Form.Item>
                    <Form.Item label="SoC" name="soc"
                        rules={[{message: 'Please input your username!',},]}
                    >
                    {/* <Input /> */}
                    <Select>
                        <Select.Option value="SM8750">SM8750</Select.Option>
                        {/* <Select.Option value="SM8650">SM8650</Select.Option> */}
                    </Select>
                    </Form.Item>
                    <Form.Item label="Token Rates" name="token_rates"
                        rules={[ {message: 'Please input your username!', }, ]}
                    >
                    <Input />
                    </Form.Item>
                    <Form.Item wrapperCol={{offset: 8,span: 16,}} >
                    <Space size={100}>
                        <Button type="primary" htmlType="submit"> Update </Button>
                        <Button type="primary" htmlType="reset"> Cancel </Button>
                    </Space>
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default AgGridTable;

export function AutoCompleteSearch({GlobalFieldSearch}) {
    // const name_arr = ["尹凯","倪雨婷","俞秀","左丘思敏","戚楠","葛宇","赵泽","端木涵","范宇轩","严磊","卞磊","罗桐","司寇红","元梓豪",
    // "陆汪诚","范荣","邹洋","薛梓睿","云皓","袁洋","唐瑞","窦成","平欣然","严柏","沈章梓萱","吕瑾瑜","马庆",
    // "叶诗涵","漆雕柏","赵云"]
    const [input_value, setInputValue] = useState(null)
    const searchResult = (query=null) =>{
      let new_name_arr = []
      for(let name of name_arr){
        if (query === null){
            new_name_arr.push({
                value: name,
                label: (
                <div style={{display: 'flex',justifyContent: 'space-between',}}>
                    <span>{name}</span>
                </div>
                ),
            })
        }else{
            if(name.indexOf(query) !== -1){
                new_name_arr.push({
                    value: name,
                    label: (
                    <div style={{display: 'flex',justifyContent: 'space-between',}}>
                        <span>{name}</span>
                    </div>
                    ),
                })
            }
        }
      }
      debugger
      return new_name_arr
    };
    const [options, setOptions] = useState([]);
    // useEffect(()=>{
    //     setOptions(searchResult())
    // },[])

    const handleSearch = (value) => {
        // message.info("onSearch")
        setInputValue(value)
      setOptions(value ? searchResult(value) : []);
    };
    const onSelect = (value) => {
        // message.info(`onSelect:${value}`);
        setOptions(value ? searchResult(value) : []);
        setInputValue(value)
        GlobalFieldSearch(value)
    };

    const onClick = (e) => {
        GlobalFieldSearch(input_value)
    };
    const onClear=(e)=>{
        let new_name_arr = searchResult()
        setOptions(new_name_arr)
    }
    return (
      <div>
      <AutoComplete
        popupMatchSelectWidth={440}
        style={{width: 500}}
        options={options}
        onSelect={onSelect}
        onSearch={handleSearch}
        size="large"
        allowClear
        onClear={onClear}
      >
        {/* <Input.Search size="large" placeholder="输入姓名"
            enterButton="搜索" 
            // onClick={onClick}

        /> */}
      </AutoComplete>
      <Button size='large' onClick={onClick} type="primary">搜 索</Button>
      </div>
    )
  }
  