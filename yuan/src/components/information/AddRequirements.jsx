import React, { useState, useEffect } from 'react';
import { Space, InputNumber, Tooltip, Radio, message, Checkbox } from 'antd';
import { Button, Select, Form, Input, Row, Col } from 'antd';
import * as fetch_api from "../fetch_data"
import { MinusCircleOutlined, PlusOutlined, MinusOutlined } from '@ant-design/icons';
import { FormItemRange } from '../MyFormComponent';
const { Option } = Select;

function FormSelectComm({label, name, message, style, mode, required=false, items=[], onChange=null}){

  return (
    <Form.Item label={label} name={name} rules={[{required: required, message: {message}}]} style={style} >
      <Select mode={mode} onChange={onChange}>
        {items.map((item, index)=>{
          return <Select.Option key={index} value={item}>{item}</Select.Option>
        })}
      </Select> 
    </Form.Item>
  )
}
// 控制上下两个Form.item之间的间距
const item_style = {  marginTop:2,marginBottom:4}
function InitSelectOptions(items){
  let options = []
  for(var i=0; i<items.length; i++){
    options.push(<Select.Option value={items[i]}>{items[i]}</Select.Option>)
  }
  return options
}

export function FormInput({form_item_obj, input_obj, tooltip_title="", style=null}) {
  const {label, name, message, required} = form_item_obj
  const {placeholder, text_color, disabled} = input_obj

  // label：  类型：string  描述：表单项的标签文本，显示在输入框旁边。
  // name：  类型：string  描述：表单项的名称，用于在表单提交时标识对应的数据字段。
  // message：  类型：string  默认值：""  描述：当表单项为必填且未被填写时，显示的验证错误消息。
  // placeholder：  类型：string  默认值：""  描述：输入框的占位符文本。
  // tooltip_title：  类型：string  默认值：""  描述：可选参数，用于设置表单项旁边的提示工具条（Tooltip）的标题。
  // required：  类型：boolean  默认值：false  描述：表示该表单项是否为必填项。如果为true，则在表单提交时会进行必填验证。
  return (
    <Tooltip title={tooltip_title}>
      <Form.Item label={label} name={name} rules={[{required: required, message: message }]} style={style}>
        <Input style={{color:text_color}} placeholder={placeholder} disabled={disabled}/>
      </Form.Item>
    </Tooltip>
  )
}

export function FormInputNumbner({label, name, min, max, message="", placeholder="", tooltip_title="", required=false}) {
  // label：  类型：string  描述：表单项的标签文本，显示在输入框旁边。
  // name：  类型：string  描述：表单项的名称，用于在表单提交时标识对应的数据字段。
  // min：  类型：number  描述：InputNumber组件的最小值。
  // max：  类型：number  描述：InputNumber组件的最大值。
  // message：  类型：string  默认值：""  描述：当表单项为必填且未被填写时，显示的验证错误消息。
  // placeholder：  类型：string  默认值：""  描述：输入框的占位符文本。
  // tooltip_title：  类型：string  默认值：""  描述：可选参数，用于设置表单项旁边的提示工具条（Tooltip）的标题。
  // required：  类型：boolean  默认值：false  描述：表示该表单项是否为必填项。如果为true，则在表单提交时会进行必填验证。
  return (
    <Tooltip title={tooltip_title}>
      <Form.Item label={label} name={name} rules={[{required:required, message: message }]} style={item_style}>
        <InputNumber min={min} max={max} placeholder={placeholder} style={{width:300}}/>
      </Form.Item>
    </Tooltip>
  )
}

// 自定义Select组件
export function SelectForm ({ label, name, items, tooltip_title="",required=false,message="", onchange=null, add_item_sign=false }) {
    // label：    类型：string    描述：表单项的标签文本，显示在输入框旁边。
    // name：    类型：string    描述：表单项的名称，用于在表单提交时标识对应的数据字段。
    // items：    类型：array    描述：一个数组，包含下拉列表中的选项内容。数组的每个元素都将被转换为一个下拉选项。
    // tooltip_title：    类型：string    描述：可选参数，用于设置表单项旁边的提示工具条（Tooltip）的标题。
    // required：    类型：boolean    默认值：false    描述：表示该表单项是否为必填项。如果为true，则在表单提交时会进行必填验证。
    // message：    类型：string    描述：当required为true且该字段未被填写时，显示的验证错误消息。
    // onchange：    类型：function    描述：一个回调函数，当选择的值发生变化时被调用。通常用于处理用户选择的值。
    // add_item_sign：    类型：boolean    默认值：false    描述：控制是否允许用户输入不在下拉列表中的新值。如果为true，则启用搜索和自定义值添加功能。

    const [value, setValue] = useState(null);
    const [options, setOptions] = useState([]);
    const [old_options_length, setOldOtionsLength] = useState(null)

    useEffect(()=>{
        let new_options = []
        for(let i=0; i<items.length; i++){
            new_options.push({
                value: items[i], label: items[i]
            })
        }
        setOptions(new_options)
        setOldOtionsLength(new_options.length)
    },[])

    const SelecthandleSearch = (inputValue) => {
        // 如果输入值不在选项中，可以在这里进行处理，例如添加到选项中
        if (!options.find(option => option.value === inputValue)) {
            debugger
            if (options.length === old_options_length){
                setOptions([...options, { value: inputValue, label: inputValue }]);
            }else{
                let newOptions = [...options]
                newOptions[old_options_length]={ value: inputValue, label: inputValue }
                setOptions(newOptions)
            }
        }
      };
    
      const SelecthandleChange = (inputValue) => {
        // 设置选中值为用户输入的值
        setValue(inputValue);
      };

    return (
        <Tooltip title={tooltip_title}>
            <Form.Item label={label} name={name}
                rules={[ { required: required, message:message, }]}
                style={item_style}
                >
                {add_item_sign===true?
                    <Select
                        showSearch
                        value={value}
                        placeholder="您可以任选一个也可以写一个新的内容"
                        optionFilterProp="label"
                        onChange={SelecthandleChange}
                        onSearch={SelecthandleSearch}
                        style={{width:300}}
                        filterOption={(input, option) => option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0}
                        >
                        {options.map(option => (
                            <Option key={option.value} value={option.value}>
                            {option.label}
                            </Option>
                        ))}
                    </Select>
                :
                <Select onChange={onchange}>
                    {options.map(option => (
                        <Option key={option.value} value={option.value}>
                        {option.label}
                        </Option>
                    ))}
                </Select>
                }
                </Form.Item>
        </Tooltip>
    );
};

// 自定义Select组件
export function SelectFormV2 ({items, tooltip_title="", onchange=null, add_item_sign=false }) {
  // items：        类型：array    描述：一个数组，包含下拉列表中的选项内容。数组的每个元素都将被转换为一个下拉选项。
  // tooltip_title  类型：string    描述：可选参数，用于设置表单项旁边的提示工具条（Tooltip）的标题。
  // onchange：     类型：function    描述：一个回调函数，当选择的值发生变化时被调用。通常用于处理用户选择的值。
  // add_item_sign：类型：boolean    默认值：false    描述：控制是否允许用户输入不在下拉列表中的新值。如果为true，则启用搜索和自定义值添加功能。
  const [value, setValue] = useState(null);
  const [options, setOptions] = useState([]);
  const [old_options_length, setOldOtionsLength] = useState(null)

  useEffect(()=>{
      let new_options = []
      for(let i=0; i<items.length; i++){
          new_options.push({
              value: items[i], label: items[i]
          })
      }
      setOptions(new_options)
      setOldOtionsLength(new_options.length)
  },[])

  const SelecthandleSearch = (inputValue) => {
      // 如果输入值不在选项中，可以在这里进行处理，例如添加到选项中
      if (!options.find(option => option.value === inputValue)) {
          debugger
          if (options.length === old_options_length){
              setOptions([...options, { value: inputValue, label: inputValue }]);
          }else{
              let newOptions = [...options]
              newOptions[old_options_length]={ value: inputValue, label: inputValue }
              setOptions(newOptions)
          }
      }
    };
  
    const SelecthandleChange = (inputValue) => {
      // 设置选中值为用户输入的值
      setValue(inputValue);
    };

  return (
      <Tooltip title={tooltip_title}>
        {add_item_sign===true?
            <Select
                showSearch
                value={value}
                placeholder="您可以任选一个也可以写一个新的内容"
                optionFilterProp="label"
                onChange={SelecthandleChange}
                onSearch={SelecthandleSearch}
                style={{width:300}}
                filterOption={(input, option) => option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0}
                >
                {options.map(option => (
                    <Option key={option.value} value={option.value}>
                    {option.label}
                    </Option>
                ))}
            </Select>
        :
        <Select onChange={onchange}>
            {options.map(option => (
                <Option key={option.value} value={option.value}>
                {option.label}
                </Option>
            ))}
        </Select>
        }
      </Tooltip>
  );
};

export default function AddRequirements({only_key=null}) {
  // 添加另一半要求
  // 这里需要注意有两个地方可以触发数据的修改:
  // 一个是在填写完个人信息之后
  // 另一个是在主页的筛选条件中进行修改或者添加
    const [form] = Form.useForm()
    const [options_obj, setOptionsObj] = useState(null) //获得所有的下拉列表选项
    const [initialValues, setInitialValues] = useState(null)  //FORM初始化
    const [open_children, setOpenChildren] = useState(false)  //控制子女详细信息显示组件
    const [url_type, setUrlType] = useState("post") //向后台发送数据的方式

    useEffect(()=>{
      if (options_obj !== null){ return }
      // 获得所有下拉列表的items
      fetch_api.get("http://10.233.202.137:7767/get/select_options")
      .then(data => {
        // console.log(data)
        setOptionsObj(data.select_options)
      })
      .catch(error => {console.error(error)});

      // 获得个人要求数据
      fetch_api.get("http://10.233.202.137:7767/request/request/?name=张长啸_1996-04-08_2024-12-03")
      .then(data => {
        // console.log(data)
        for(let value of ["离异", "丧偶"]){
          if (data.initialValues.maritalStatus.indexOf(value) !== -1){
            setOpenChildren(true)
            break
          }
        }
        message.info(`发送将会以${data.url_type}的方式执行`)
        setInitialValues(data.initialValues)
        setUrlType(data.url_type)
        message.info(data.msg)
      })
      .catch(error => {console.error(error)});
    },[])

    const onFinish = (values) => {
      console.log(values)
      if(url_type === "put"){
        values['only_key'] = initialValues.only_key
        values['house_info']["id"] = initialValues.house_info.id
        values['car']["id"] = initialValues.car.id
        debugger
        fetch_api.put(`http://10.233.202.137:7767/request/put`, values)
        .then(data =>{  
          console.log(data) 
          for(let msg of data.msgs){
            message.success(msg)
          }
        })
        .catch(error => { console.error(error) });
        
      }else if (url_type === "post"){
        values['only_key'] = initialValues.only_key
        fetch_api.post(`http://10.233.202.137:7767/request/add`, values)
        .then(data =>{  
          console.log(data) 
          message.success()
        })
        .catch(error => { console.error(error) });
      }
    };
    const onFinishFailed = (errorInfo) => {
        console.log('Failed:', errorInfo);
    };
    
    const MaritalStatusChange=(values, type)=>{
      for(let value of ["离异","丧偶"]){
        if (values.indexOf(value)!== -1){
          setOpenChildren(true)
          return
        }
      }
      form.setFieldsValue({
        childrens: Array.from({ length: 0 }, (_, index) => ({
          sex:"",
          age_range:"",
          children_around:"",
          children_support_payment:"",
          other:""
        })),
      });
      setOpenChildren(false)
    }

    const ChildrenNumberChange=(value)=>{
      form.setFieldsValue({
        childrens: Array.from({ length: value }, (_, index) => ({
          sex:"",
          age_range:"",
          children_around:"",
          children_support_payment:"",
          other:""
        })),
      });
    }

    // Model 所有操作 结束
    return (
        <div style={{minWidth:1000,backgroundColor:"#50758B", paddingTop:10}}>
          <div style={{fontSize:15}}><b>根据某个用户的信息自动填写一部分信息</b></div>
          <div style={{fontSize:15}}><b>创建个人要求，修改个人要求，修改所有涉及的要求表</b></div>
        {initialValues&&<Form
            form={form}
            name="AddRequirements"
            layout="horizontal"
            labelCol={{ span: 6 }}
            wrapperCol={{ span: 16 }}
            style={{maxWidth: 1200,textAlign:"left"}}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
            initialValues={initialValues}
        >
            <FormInput style={item_style} tooltip_title={""}
              form_item_obj={{ label:"性别", name:"sex", required:true, message:"", }}
              input_obj={{ placeholder:"", text_color:"red", disabled:true }}
            />
            <FormSelectComm label={"婚姻状况"} name={"maritalStatus"} required={true} message={'输入婚姻状况!'} style={item_style} mode={"multiple"} items={["无要求","首婚","离异","丧偶"]} onChange={(values)=>{MaritalStatusChange(values, "maritalStatus")}}/>
            {open_children!==false&&<>
              <Form.Item label="几个孩子" name="childrens_number"rules={[{required: true, message: '输入几个孩子!'}]} style={item_style}>
                <InputNumber min={0} max={5} style={{width:300}} onChange={ChildrenNumberChange} placeholder="输入几个孩子"/>
              </Form.Item>
            </>}
            <ChildrenComponent  options_obj={options_obj}/>
            <FormSelectComm label={"相貌"} name={"appearance"} required={false} message={'输入婚姻状况!'} style={item_style} mode={"multiple"} items={["无要求"].concat(options_obj.appearance_arr)}/>
            <AntdFormItemRange label={"年龄范围"} item_name={"age_range"} number_min={20} number_max={55}/>
            <AntdFormItemRange label={"身高范围(厘米)"} item_name={"height_range"} number_min={145} number_max={226}/>
            <AntdFormItemRange label={"体重范围(公斤)"} item_name={"weight_range"} number_min={40} number_max={150}/>
            <FormSelectComm label={"性格"} name={"temperament"} required={false} message={'性格!'} style={item_style} mode={"multiple"} items={["无要求"].concat(options_obj.temperament_arr)}/>
            <FormSelectComm label={"爱好"} name={"hobbies"} required={false} message={'性格!'} style={item_style} mode={"multiple"} items={["无要求"]}/>
            <FormSelectComm label={"吸烟"} name={"smorking"} required={false} message={'性格!'} style={item_style} mode={"multiple"} items={["无要求"]}/>
            <FormSelectComm label={"喝酒"} name={"drinking"} required={false} message={'性格!'} style={item_style} mode={"multiple"} items={["无要求"]}/>
            <FormSelectComm label={"希望定居城市"} name={"Hope_settle_city"} required={false} message={'性格!'} style={item_style} mode={"multiple"} items={["沭阳"]}/>
            <FormSelectComm label={"是否公开照片"} name={"photos_public"} required={false} message={'性格!'} style={item_style} mode={"multiple"} items={["无要求","公开","不公开"]}/>
            <AntdFormItemRange label={"月收入范围(元)"} item_name={"monthIncome_range"} number_min={3000} number_max={100000}/>
            <AntdFormItemRange label={"年收入范围(万元)"} item_name={"yearIncome_range"} number_min={3} number_max={200}/>
            <AntdFormItemRange label={"存款范围(万元)"} item_name={"bank_deposit_range"} number_min={0} number_max={200}/>
            <FormSelectComm label={"工作类型"} name={"workType"} required={false} message={'工作类型!'} style={item_style} mode={"multiple"} items={["无要求"].concat(options_obj.work_type_arr)}/>
            <Form.Item label="工作城市" name="workCity" style={item_style}><Input placeholder={"请放心填写,随时可以修改"}/></Form.Item>
            <Form.Item label="工作单位" name="workUnit" style={item_style}><Input placeholder={"请放心填写,随时可以修改"}/></Form.Item> 
            <FormSelectComm label={"教育程度"} name={"academic_qualifications"} required={true} message={'教育程度!'} style={item_style} mode={"multiple"} items={["无要求"].concat(options_obj.academic_qualifications_arr)}/>
            <FormSelectComm label={"专业"} name={"major"} required={true} message={'教育程度!'} style={item_style} mode={"multiple"} items={["无要求"]}/>
            <Form.Item label="学校名称" name="school" style={item_style}><Input placeholder={"可以不填写"}/></Form.Item>

            <AssetItem label={"房子"} item_name={"house_info"} options_obj={options_obj}/>
            <AssetItem label={"车子"} item_name={"car"} options_obj={options_obj}/>
            <Form.Item label="其他" name="other" style={item_style}><Input.TextArea rows={2} style={{width:440}} placeholder={"请放心填写,随时可以修改"}/></Form.Item>
            <RequestParentComponent options_obj={options_obj} />
            <BrotherComponent options_obj={options_obj}/>
            <Form.Item wrapperCol={{offset: 6,span: 16,}} style={item_style} >
              <Space size={100} style={{paddingBottom:10}}>
                  <Button type="primary" htmlType="submit"> 保存 </Button>
                  <Button type="primary" htmlType="reset"> 取消 </Button>
              </Space>
            </Form.Item>
        </Form>}
        </div>
    );
}

function BrotherComponent({options_obj}){
  // 添加兄弟姐妹信息的组件
  // const work_type_arr= ["公务员","教师","医生","护士","独立创业者","科技工作者","金融工作者","希望增加自定义输入功能"] //工作类型
  // const brothers_arr= ["哥哥","姐姐","弟弟","妹妹"] //兄弟姐妹
  // const marital_status= ["未婚","离异","丧偶"] //婚姻状况
  // const health_status_arr = ["健康","亚健康","有疾","已故"]
  const {marital_status, brothers_arr, work_type_arr, health_status_arr} = options_obj

  let new_work_type_arr = ["无要求"].concat(work_type_arr)
  let siblingsHealthy_arr = ["不便透露"].concat(health_status_arr)


  return <Form.List name="brothers">
  {(fields, { add, remove }) => (
    <div>
      {fields.map((field, index) => (
        <Form.Item wrapperCol={{ offset: 5, span: 16 }} style={item_style}>
        <div key={field.key}  style={{backgroundColor:"#ecfaf4"}}>
          <Row gutter={8}>
            <Col span={5}>
              <Form.Item
                {...field}
                name={[field.name, 'relations']}
                label={"关系"}
                fieldKey={[field.fieldKey, 'relations']}
                rules={[{ required: true, message: 'Value is required!' }]}
                style={item_style}
              >
                <Select style={{minWidth:70}} >
                  {InitSelectOptions(brothers_arr)}
                </Select>  
              </Form.Item>
            </Col>
            <Col span={6}>
              <Form.Item
                {...field}
                name={[field.name, 'health_status']}
                label={"健康"}
                fieldKey={[field.fieldKey, 'health_status']}
                rules={[{ required: true, message: 'Value is required!' }]}
                style={item_style}
              >
                <Select mode={"multiple"} style={{minWidth:100}}>
                  {InitSelectOptions(['无要求'].concat(siblingsHealthy_arr))}
                </Select>  
              </Form.Item>
            </Col>
            <Col span={1}></Col>
            <Col span={5}>
              <Form.Item
                {...field}
                name={[field.name, 'maritalStatus']}
                label={"婚姻"}
                fieldKey={[field.fieldKey, 'maritalStatus']}
                rules={[{ required: true, message: 'Value is required!' }]}
                style={item_style}
              >
                <Select mode={"multiple"} style={{minWidth:70}}>
                {InitSelectOptions(["已婚"].concat(marital_status))}
                </Select>  
              </Form.Item>
            </Col>
            <Col span={6}>
              <Tooltip title={"您可以不填写，不强求"}>
                <Form.Item
                {...field}
                name={[field.name, 'work_type']}
                label={"工作"}
                fieldKey={[field.fieldKey, 'work_type']}
                rules={[{required: true, message: 'Value is required!' }]}
                style={item_style}
              >
                <Select mode={"multiple"} style={{minWidth:120}}>
                {InitSelectOptions(new_work_type_arr)}
                </Select>  
              </Form.Item>
              </Tooltip>
            </Col>
          </Row>
          <Row gutter={8}>
          <Col span={2}></Col>
            <Col span={10}>
              <AntdFormItemRange label={"月收入"} item_name={[field.name, 'monthIncome_range']} number_min={3000} number_max={100000} />
            </Col>
            <Col span={2}></Col>
            <Col span={10}>
              <AntdFormItemRange label={"年收入"} item_name={[field.name, 'yearIncome_range']} number_min={0} number_max={200} />

            </Col>
          </Row>
          <Button type="dashed" onClick={() => remove(field.name)} block icon={<MinusOutlined />} >删除关系</Button>
        </div>
        </ Form.Item>
      ))}
      <Form.Item wrapperCol={{ offset: 5, span: 16 }} style={item_style}>
        <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />} >添加兄弟姐妹</Button>
      </Form.Item>
    </div>
  )}
</Form.List>
}

function RequestParentComponent({options_obj}){
  // 添加兄父母信息的组件
  const {health_status_arr, parents_work_status_arr} = options_obj
  return <Form.List name="parents">
  {(fields) => (
    <>
      {fields.map((field, index) => (
        <Form.Item wrapperCol={{ offset: 5, span: 16 }} style={item_style}>
        <div key={field.key} style={{backgroundColor:"#fff5ea"}}>
          {index===0?<div ><p>爸爸</p></div>:<div ><p>妈妈</p></div>}
          <Row gutter={8}>
            <Col span={8}>
              <Form.Item
                {...field}
                name={[field.name, 'health_status']}
                label={"健康"}
                fieldKey={[field.fieldKey, 'health_status']}
                rules={[{ required: true, message: 'Value is required!' }]}
                style={item_style}
              >
                <Select mode={"multiple"}>
                  {InitSelectOptions(['无要求'].concat(health_status_arr))}
                </Select>  
              </Form.Item>
            </Col>
            <Col span={14}>
              <Form.Item
                {...field}
                name={[field.name, 'work_type']}
                label={"工作类型"}
                fieldKey={[field.fieldKey, 'work_type']}
                style={item_style}
              >
                <Select mode={"multiple"}>
                  {InitSelectOptions(parents_work_status_arr)}
                </Select>  
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={8}>
          <Col span={8}>
              <Tooltip title={"请注意单位：【元】。输入10000:表示月收入10000元"}>
                <AntdFormItemRange label={"月收入"} item_name={[field.name, 'monthIncome_range']} number_min={3000} number_max={100000} />
              </Tooltip>
            </Col>
            <Col span={2}></Col>
            <Col span={10}>
              <Tooltip title={"请注意单位：【元】。输入12:表示年收入12万元"}>
              <AntdFormItemRange label={"年收入"} item_name={[field.name, 'yearIncome_range']} number_min={0} number_max={200} />
              </Tooltip>
            </Col>
          </Row>
        </div>
        </ Form.Item>
      ))}
    </>
  )}
</Form.List>
}

function ChildrenComponent({options_obj}){
  // 添加兄父母信息的组件
  const {sex_arr} = options_obj
  return <Form.List name="childrens">
  {(fields) => (
    <>
      {fields.map((field, index) => (
        <Form.Item wrapperCol={{ offset: 5, span: 16 }}  style={item_style}>
        <div key={field.key}>
          <Row gutter={8} style={item_style}>
            <Col span={7}>
              <Form.Item
                {...field}
                name={[field.name, 'sex']}
                label={"性别"}
                fieldKey={[field.fieldKey, 'sex']}
                rules={[{ required: true, message: '孩子性别必须填写!' }]}
              >
                <Select>
                  {InitSelectOptions(['无要求'].concat(sex_arr))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={15} style={{paddingBottom:2}}>
              <AntdFormItemRange label={"年龄"} item_name={[field.name, 'age_range']} number_min={0} number_max={18}/>
            </Col>
          </Row>
          <Row gutter={8} style={{marginTop:-20}}>
          <Col span={7}>
              <Tooltip title={""}>
                <Form.Item
                  {...field}
                  name={[field.name, 'children_around']}
                  label={"在身边?"}
                  rules={[{ required: true, message: '孩子是否在身边必须填写!' }]}
                  fieldKey={[field.fieldKey, 'children_around']}
                >
                  <Select>
                  {InitSelectOptions(["无要求","在身边","不在身边"])}
                </Select>
                </Form.Item>
              </Tooltip>
            </Col>
            <Col span={7}>
              <Tooltip title={""}>
                <Form.Item
                  {...field}
                  name={[field.name, 'children_support_payment']}
                  label={"对方出抚养费"}
                  rules={[{ required: true, message: '对方是否出孩子抚养费必须填写!' }]}
                  fieldKey={[field.fieldKey, 'children_support_payment']}
                >
                  <Select>
                    {InitSelectOptions(["无要求","出","不出"])}
                </Select>
                </Form.Item>
              </Tooltip>
            </Col>
            <Col span={10}>
              <Tooltip title={"其他需要额外补充的信息"}>
                <Form.Item
                {...field}
                name={[field.name, 'other']}
                label={"补充:"}
                fieldKey={[field.fieldKey, 'other']}
                style={item_style}
              >
                <Input.TextArea rows={1} style={{width:440}} placeholder="其他需要额外补充的信息"/>
              </Form.Item>
              </Tooltip>
            </Col>
          </Row>
        </div>
        </ Form.Item>
      ))}
    </>
  )}
</Form.List>
}

export function AntdFormItemRange({label, item_name, required=true, number_min=0, number_max=100}) {
  // 处理值范围的form item组件
  // label: form item在web端显示的内容, 
  // item_name:收集数据的字段名称, 
  // number_min=0: inputNumber的最小值, 
  // number_max=100:inputNumber的最大值
  return (
    <Form.Item
        label={label}
        style={{ marginBottom: 0 }}
        rules={[
          {
            validator: (_, value) => {
              if (!value || value.min === undefined || value.max === undefined) {
                return Promise.reject(new Error('请填写完整的数值范围'));
              }
              if (value.min >= value.max) {
                return Promise.reject(new Error('最小值必须小于最大值'));
              }
              return Promise.resolve();
            },
          },
        ]}
      >
        <Space>
          <Form.Item
            name={Array.isArray(item_name)?item_name.concat(['min']):[item_name, 'min']}
            noStyle
            rules={[{ required: required, message: '请输入最小值' }]}
          >
            <InputNumber placeholder="最小值" min={number_min} max={number_max} />
          </Form.Item>
          到
          <Form.Item
            name={Array.isArray(item_name)?item_name.concat(['max']):[item_name, 'max']}
            noStyle
            rules={[{ required: required, message: '请输入最大值' }]}
          >
            <InputNumber placeholder="最大值"  min={number_min} max={number_max} />
          </Form.Item>
        </Space>
      </Form.Item>
  )
}

export function AssetItem({label, item_name, options_obj, required=true }) {
  // 个人资产信息
  // label = "房子"
  // item_name = "house_info"
  return (
    <Form.Item
        label={label}
        style={{ marginBottom: 0 }}
      >
        <br/>
        <Space>
        
          <AntdFormItemRange label={"资产数量"} item_name={[item_name, "assets_number"]}/>
        <div style={{paddingLeft:10, textAlign:"right"}}>贷款:</div>
          <Form.Item
            name={[item_name, "is_loan"]}
            noStyle
            rules={[{ required: required, message: '请输入相关信息' }]}
          >
            <Select mode="multiple" style={{width:130}}>
                {InitSelectOptions(["无要求"].concat(options_obj.asset_loan_arr))}
            </Select>
          </Form.Item>
        </Space>
        <Space>
          <div style={{paddingLeft:10, textAlign:"right"}}>是否自己名下:</div>
          <Form.Item
            name={[item_name, "is_me"]}
            noStyle
            rules={[{ required: required, message: '请输入相关信息' }]}
          >
            <Select mode="multiple" style={{width:130}}>
                {InitSelectOptions(["无要求","在","不在"])}
            </Select>
          </Form.Item>
          <div style={{paddingLeft:10, textAlign:"right"}}>{item_name==="car"?"汽车品牌":"所在城市"}:</div>
          <Form.Item
            name={[item_name, item_name==="car"?"brand":"city"]}
            noStyle
            rules={[{ message: '请输入相关信息' }]}
          >
            <Input placeholder="最大值" />
          </Form.Item>
        </Space>
      </Form.Item>
  )
}