// 添加/更新个人信息
import React, { useState, useRef, useEffect } from 'react';
import { Space, Modal, InputNumber, Tooltip, Radio, message, Card } from 'antd';
import { Button, Select, Form, Input, Row, Col, Upload } from 'antd';
import * as fetch_api from "../fetch_data"
import { MinusCircleOutlined, PlusOutlined, MinusOutlined } from '@ant-design/icons';
const { Option } = Select;
const sex_arr = ["男", "女"]

// 控制上下两个Form.item之间的间距
const item_style = {  marginTop:2,marginBottom:4}
function InitSelectOptions(items){
  let options = []
  for(var i=0; i<items.length; i++){
    options.push(<Select.Option value={items[i]}>{items[i]}</Select.Option>)
  }
  return options
}

export function FormInput({label, name, message="", placeholder="", tooltip_title="", required=false}) {
  // label：    类型：string  描述：表单项的标签文本，显示在输入框旁边。
  // name：     类型：string  描述：表单项的名称，用于在表单提交时标识对应的数据字段。
  // message：  类型：string  默认值：""  描述：当表单项为必填且未被填写时，显示的验证错误消息。
  // placeholder：    类型：string  默认值：""  描述：输入框的占位符文本。
  // tooltip_title：  类型：string  默认值：""  描述：可选参数，用于设置表单项旁边的提示工具条（Tooltip）的标题。
  // required：       类型：boolean  默认值：false  描述：表示该表单项是否为必填项。如果为true，则在表单提交时会进行必填验证。
  return (
    <Tooltip title={tooltip_title}>
      <Form.Item label={label} name={name} rules={[{required: required, message: message }]} style={item_style}>
        <Input placeholder={placeholder}/>
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

function UpdateData(url, form, values){
    fetch_api.post(url, values)
    .then(data=>{
      console.log(data)
      if (data.status === -1){
        message.error(data.msg)
      }else if(data.status === 0){
        message.warning(data.msg)
      }else if(data.status === 1){
        message.success(data.msg)
        form.resetFields()
      }
    }).catch(error=>{
      console.log(error)
      debugger
    })
}

function UpdateDataV2(form, values){
  fetch_api.put("http://10.233.202.137:7767/information", values)
  .then(data=>{
    console.log(data)
    if (data.status === -1){
      message.error(data.msg)
    }else if(data.status === 0){
      message.warning(data.msg)
    }else if(data.status === 1){
      message.success(data.msg)
      form.resetFields()
    }
  }).catch(error=>{
    console.log(error)
    debugger
  })
}
const AddInformation = ({initialValues_obj=null}) => {
    const [form] = Form.useForm()
    const [options_obj, setOptionsObj] = useState(null) //获得所有的下拉列表选项
    const [fastapi_func, setFaseApiFunc] = useState(initialValues_obj===null?"post":"put")
    const [data_backpu, setDataBackup] = useState(initialValues_obj)
    useEffect(()=>{
      if (options_obj !== null){ return }
      fetch_api.get("http://10.233.202.137:7767/get/select_options")
      .then(data => {
        // console.log(data)
        // debugger
        setOptionsObj(data.select_options)
      })
      .catch(error => {console.error(error)});
    },[])

    const initialValues = {
      house_info: [{ is_loan: undefined, is_me:"", city:"", address: '' }],
      cars:[{is_loan:undefined, is_me:"", brand:""}],
      childrens_number:0,
      parents:[
        {health_status:undefined,monthIncome:undefined,yearIncome:undefined,work_status:undefined},
        { health_status:undefined,monthIncome:undefined,yearIncome:undefined,work_status:undefined},
      ]
    }
    const [birthDate, setBirthDate] = useState(null)

    useEffect(()=>{
      if (initialValues_obj === null){ 
        setFaseApiFunc("put")
        fetch_api.get('http://10.233.202.137:7767/information/?name=张长啸')
        .then((results)=>{
          // 设置form值
          setDataBackup(results.datas[0])
          for(let information_obj of results.datas){
            Object.keys(information_obj).forEach(key=>{
              if (key === "birthDate"){
                setBirthDate(information_obj[key])
                setAge(information_obj["age"])
              }else if (key === "childrens_number" && information_obj[key]!==0 && information_obj[key]!==null){
                setShowSon(true)
              }
              form.setFieldsValue({[key]:information_obj[key]})
            })
          }
        })
        .catch((error)=>{
          console.error(error)
        })
        return 
      }
      // 设置form值
      Object.keys(information_obj).forEach(key=>{
        form.setFieldsValue({[key]:information_obj[key]})
      })
    },[initialValues_obj])

    const handleCancel = () => {
        setPreviewVisible(false)
    };
    // cancel 操作
    const onFinish = (values) => {
      // 提交表单
      if(fastapi_func === "put"){
        // 后期整个put的整个if判断都需要独立出来成为一个独立的组件或者函数，这是更新，现在只是为了方便测试才写在一起
        const all_keys = Object.keys(values)
        values["only_key"] = data_backpu['only_key']
        for(let key of all_keys){
          console.log(key)
          if (Array.isArray(values[key])){
            // 判断类型
            // 首先判断长度是否相同,不相同则更新
            if(values[key].length !== data_backpu[key].length){
              console.log(`${values[key].length}`.trim())
              console.log(`${data_backpu[key].length}`.trim())
              UpdateDataV2(form, values)
              return 
            }
            for(let i=0; i<values[key].length; i++){
              if (typeof values[key][i] === 'string') {
                values[key][i] = values[key][i].trim()
              } 
              if (JSON.stringify(values[key][i]) !== JSON.stringify(data_backpu[key][i])){
                UpdateDataV2(form, values)
                return
              }
            }
          }else{
            // 非obj和list类型
            console.log(`${values[key]}`.trim())
            console.log(`${data_backpu[key]}`.trim())
            if (`${values[key]}`.trim() !== `${data_backpu[key]}`.trim()){
              UpdateDataV2(form, values)
              return
            }
          }
        }
        message.warning("数据未修改，无需提交更新")
        debugger
        return
      }
        console.log(values)
        debugger
        // 修正资产信息
        for(let i=0; i<=1; i++){
          values.parents[i]["maritalStatus"] = "已婚"
          values.parents[i]["relations"] = i===0?"父亲":"母亲"
        }

        // 补充子女信息
        if("childrens" in values === false){
          values["childrens"] = []
        }
        if (values.childrens === undefined){
          values.childrens = []
        }
        for(let i=0; i<values.childrens.length; i++){
          if (values.childrens[i].sex === "男"){
            values.childrens[i]["relations"] = "子"
          }else{
            values.childrens[i]["relations"] = "女"
          }
        }
        console.log(values)
        debugger
        UpdateData("http://10.233.202.137:7767/information", form, values)
      };

    const onFinishFailed = (errorInfo) => {
      // 表单提交失败
      message.error(`Failed:${errorInfo}`)
    };
    
    const [age, setAge] = useState('') //根据出生日期 计算年龄
    const calculateAge = (birthDate) => {
        const today = new Date();
        const birthDateObj = new Date(birthDate);
        let age = today.getFullYear() - birthDateObj.getFullYear();
        const monthDiff = today.getMonth() - birthDateObj.getMonth();
        
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDateObj.getDate())) {
            age--;
        }
        
        return age;
    };
   
    const BirthDateHandleBlur = (e) => {
        const birthDate = e.target.value;
        if (birthDate) {
          const calculatedAge = calculateAge(birthDate);
          setAge(calculatedAge);
          setBirthDate(birthDate)
        }
    };
    
    const BirthDateChange = (e) => {
      setBirthDate(e.target.value)
    };

    const [previewVisible, setPreviewVisible] = useState(false);
    const [previewImage, setPreviewImage] = useState('');
    const [previewTitle, setPreviewTitle] = useState('');
  
    const handlePreview = async (file) => {
      if (!file.url && !file.preview) {
        file.preview = await getBase64(file.originFileObj);
      }
  
      setPreviewImage(file.url || file.preview);
      setPreviewVisible(true);
      setPreviewTitle(file.name || file.url.substring(file.url.lastIndexOf('/') + 1));
    };

    const getBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
    };

  const [show_son, setShowSon] = useState(false) //控制是否显示子女信息补充组件
  const maritalStatusChange=(e)=>{
    if (e.target.value != "未婚") {
      setShowSon(true)
    }
    else {
      setShowSon(false)
    }
  }

  const ChildrenNumberChange=(value)=>{
    // 根据孩子的数量来生成form_list的数量
    form.setFieldsValue({
      childrens: Array.from({ length: value }, (_, index) => ({
        sex:"",
        age:"",
        children_around:"",
        children_support_payment:"",
        other:""
      })),
    });
  }
  return (
      <div style={{backgroundColor:"#50758B", paddingTop:10}}>
        {options_obj!==null&&<Form
          form={form}
          name="basic"
          layout="horizontal"
          labelCol={{ span: 8 }}
          wrapperCol={{ span: 16 }}
          style={{maxWidth: 1200,textAlign:"left"}}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
          autoComplete="off"
          initialValues={initialValues}
        >
            <FormInput label={"姓名"} name={"name"} required={true} message={"输入姓名"} placeholder={"输入姓名"}/>
            <SelectForm label={"性别"} name={"sex"} items={sex_arr}/>
            <Form.Item label="出生日期" name="birthDate" rules={[{required: true, message: '输入出生日期!'}]}>
                <Space>
                    <Input placeholder={"格式:2000-01-01"} style={{width:200}} value={birthDate} onChange ={BirthDateChange} onBlur={BirthDateHandleBlur}/>&nbsp;
                    <Tooltip title="年龄根据输入的出生日期自动生成">年龄: 
                        <span style={{backgroundColor:"yellow", color:"red", fontSize:20}}><b> {age} </b></span> 岁
                    </Tooltip>
                </Space>
            </Form.Item>
            <FormInput label={"住址"} name={"address"} required={true} message={"现在居住的地方"} placeholder={"现在居住的地方"}/>
            <FormInput label={"希望安家城市"} name={"Hope_settle_city"} required={true} message={"输入姓名"} placeholder={"现在居住的地方"}/>

            <SelectForm label={"外貌"} name={"appearance"} items={options_obj.appearance_arr} required={true} message={"选择外貌自评"}/>

            <Form.Item label="婚姻状况" name="maritalStatus"rules={[{required: true, message: '输入婚姻状况!'}]} style={item_style}>
              <Radio.Group onChange={maritalStatusChange}>
                {options_obj.marital_status_arr.map((item, index)=>{
                  return <Radio value={item}>{item}</Radio>
                })}
            </Radio.Group>
            </Form.Item>
            {show_son&&<>
            <Form.Item label="几个孩子" name="childrens_number"rules={[{required: true, message: '输入几个孩子!'}]} style={item_style}>
              <InputNumber min={0} max={5} style={{width:300}} onChange={ChildrenNumberChange} placeholder="输入几个孩子"/>
            </Form.Item>
            <ChildrenComponent />
            </>}
            {/* <Form.Item 
                label="照片" 
                name="photos"
                rules={[{message: '请上传照片!' }]}
                style={item_style}
            >
                <div style={{ height: '200px', border: '1px solid #d9d9d9', borderRadius: '2px', overflow: 'hidden', position: 'relative' }}>
                <div style={{ height: 'calc(100% - 50px)', overflowY: 'auto', padding: '8px' }}>
                    <Form.Item name="photos" noStyle  style={item_style}>
                    <Upload
                        listType="picture-card"
                        multiple
                        beforeUpload={() => false}
                        onPreview={handlePreview}
                    >
                        {form.getFieldValue('photos')?.length >= 8 ? null : (
                        <div>
                            <PlusOutlined />
                            <div style={{ marginTop: 8 }}>上传</div>
                        </div>
                        )}
                    </Upload>
                    </Form.Item>
                </div>
                </div>
            </Form.Item> */}
            {/* <Form.Item label="是否公开照片" name="photosPublic" style={item_style}>
              <Radio.Group>
                {["公开","不公开"].map((item, index)=>{
                  return <Radio value={item}>{item}</Radio>
                })}
              </Radio.Group>
            </Form.Item> */}
            <FormInputNumbner label={"身高"} name={"height"} min={100} max={226} required={true} message={"输入身高"} placeholder={"单位:厘米"}/>
            <FormInputNumbner label={"体重"} name={"weight"} min={40} max={150} required={true} message={"输入体重"} placeholder={"单位:公斤"}/>
            <FormInputNumbner label={"月收入"} name={"monthIncome"} min={3000} max={100000} required={true} message={"输入月收入,单位:元"} placeholder={"输入月收入"}/>
            <FormInputNumbner label={"年收入"} name={"yearIncome"} min={3} max={200} required={true} message={"输入年收入单位:万元"} placeholder={"输入年收入"}/>
            <FormInputNumbner label={"存款"} name={"bank_deposit"} min={0} max={200} required={true} message={"输入年收入单位:万元"} placeholder={"输入年收入"}/>
            <SelectForm label={"是否喝酒"} name={"drinking"} items={options_obj.drinking_arr} required={true}/>
            <SelectForm label={"是否吸烟"} name={"smorking"} items={options_obj.smorking_arr}  required={true}/>
            <FormInput label={"工作类型"} name={"workType"} required={true} message={"输入工作类型"} placeholder={"输入工作类型"}/>
            <FormInput label={"工作城市"} name={"workCity"} required={true} message={"输入工作城市"} placeholder={"输入工作城市"}/>
            <FormInput label={"工作单位"} name={"workUnit"} required={true} message={"输入工作单位名称"} placeholder={"输入工作单位名称"}/>
            <SelectForm label={"教育程度"} name={"education"} items={options_obj.academic_qualifications_arr} />
            <FormInput label={"专业"} name={"major"} message={"输入所学专业"} placeholder={"输入所学专业"}/>
            <Form.Item label="学校名称" name="school" rules={[{required: true, message: '输入学校名称!'}]}>
              <Input.TextArea rows={2} style={{width:440}} placeholder="可以写学历+学校或者直接写学校，用换行分割。比如：&#10;高中，xxx高中&#10;大学：yyy大学"/>
            </Form.Item>
            <Form.Item label="教育补充" name="educational_supplements" rules={[{message: '输入教育补充信息!'}]}>
              <Input.TextArea rows={2} style={{width:440}} placeholder="输入教育补充信息。&#10;高中，xxx高中&#10;大学：yyy大学"/>
            </Form.Item>
            <Assets form={form} form_list_label={"房子"} item_name={"is_loan"} item_message={"格式：城市+小区+具体的单元门牌号"} form_list_name={"house_info"} select_options={options_obj.asset_loan_arr} Input_addonBefore={"地址"} select_default_value={"无"}/>
            <Assets form={form} form_list_label={"车子"} item_name={"is_loan"} item_message={"请输入品牌"} form_list_name={"cars"} select_options={options_obj.asset_loan_arr} Input_addonBefore={"品牌"} select_default_value={"无"}/>
            <Form.Item label="兴趣爱好" name="hobbies" style={item_style}>
              <Select mode="multiple">
              {InitSelectOptions(options_obj.hobbies_arr)}
              </Select>  
            </Form.Item>
            <Form.Item label="性格" name="temperament" style={item_style}>
              <Select mode="multiple">
              {InitSelectOptions(options_obj.temperament_arr)}
              </Select>  
            </Form.Item>
            <Form.Item label="其他" name="other" rules={[{message:'输入其他!'}]} ><Input.TextArea rows={2} style={{width:440}}/></Form.Item>
            <ParentComponent options_obj={options_obj} />
            <BrotherComponent options_obj={options_obj}/>
            <Form.Item wrapperCol={{offset: 8,span: 16,}} >
            <Space size={150} style={{paddingBottom:10}}>
                <Button type="primary" htmlType="submit" style={{width:100, height:60}}> 保存 </Button>
                <Button type="primary" htmlType="reset" style={{width:100, height:60}}> 取消 </Button>
            </Space>
            </Form.Item>
            <ModalShow open={previewVisible} title={previewTitle} footer_arr={null} closeable_func={handleCancel} modal_info={<img alt="example" style={{ width: '100%' }} src={previewImage} />}/>
        </Form>}
      </div>
  );
};
export default AddInformation;

export function ModalShow({open, title, footer_arr, closeable_func, modal_info}) {
  const [footer, setFooter] = useState(null); // 初始时没有 footer
  useEffect(()=>{
    if (footer_arr === null){ return }
    let new_footer = []
    for(let obj of footer_arr){
      new_footer.push(<Button key={obj.title} type={"btn_type" in obj?obj.btn_type:"primary"} onClick={obj.func}>{obj.title}</Button>)
    }
    setFooter(new_footer)
  },[footer_arr, open])
  return (
    <Modal 
        title={title} 
        // closable={false}
        open={open} 
        footer={footer}
        onCancel={closeable_func}
        >
          {modal_info}
      </Modal>
  )
}

export function Assets({
  form,                // Ant Design 的 Form 实例，用于操作表单数据
  form_list_label,     // 表单列表的标签，会显示在每个列表项的前面，如 "城市 1", "城市 2" 等
  item_name,           // 列表项中主要输入字段的名称，如 "city"
  item_message,        // 输入框的提示信息，当输入框为空时显示
  form_list_name,      // Form.List 的 name 属性，用于在表单数据中标识这个列表
  select_options = [], // Select 组件的选项数组，如 ["北京", "成都"]
  Input_addonBefore,   // Input 组件的前缀标签，如 "地址"
  select_default_value // Select 组件的默认值，通常是第一个选项的值
}) {
  // house_info: [{ is_loan: undefined, address: '' }],
  // 注意:::::::::::::这里有一个优化点：这里匹配的第二个值一定是address，并且初始化form表单初始化的时候一定要使用address这个字段，后去将会优化
  const [disableAdd, setDisableAdd] = useState(true);

  const handleChange = (value, name) => {
    debugger
    const formValues = form.getFieldValue(form_list_name);
    if (value === select_default_value) {
      debugger
      const newAddress = formValues.length === 1
        ? '总会有的，继续努力!!!'
        : '很好，其实你可以不加这一条!!!';
      form.setFieldsValue({
        [form_list_name]: formValues.map((item, index) =>
          index === name ? { ...item, address: newAddress } : item
        )
      });
    } else {
      form.setFieldsValue({
        [form_list_name]: formValues.map((item, index) =>
          index === name ? { ...item, address: '' } : item
        )
      });
    }
    checkAddButtonStatus();
  };

  const handleAddressChange = () => {
    checkAddButtonStatus();
  };

  const checkAddButtonStatus = () => {
    const formValues = form.getFieldValue(form_list_name);
    const lastAddress = formValues[formValues.length - 1];
    const allAddressesFilled = formValues.every(addr => addr[item_name] && addr.address);
    const lastAddressIsDefault = lastAddress[item_name] === select_default_value;
    setDisableAdd(!allAddressesFilled || lastAddressIsDefault);
  };

  useEffect(() => {
    checkAddButtonStatus();
  }, [form.getFieldValue(form_list_name)]);

  return (
    <Form.List name={form_list_name}>
      {(fields, { add, remove }) => (
        <>
          {fields.map(({ key, name, ...restField }) => (
            <Form.Item
              {...restField}
              label={`${form_list_label} ${name + 1}`}
              required={true}
              key={key}
              style={item_style}
            >
              <Row gutter={8}>
                <Col span={8}>
                  <Form.Item
                    {...restField}
                    name={[name, item_name]}
                    noStyle
                    rules={[{ required: true, message: '请选择一项' }]}
                    style={item_style}
                  >
                    <Select 
                      placeholder=""
                      onChange={(value) => handleChange(value, name)}
                    >
                      {/* {options} */}
                      {InitSelectOptions(select_options)}
                    </Select>
                  </Form.Item>
                </Col>
                <Col span={16}>
                  <Form.Item
                    {...restField}
                    name={[name, form_list_name==="house_info"?'address':'brand']}
                    noStyle
                    rules={[{ required: true, message: item_message }]}
                    style={item_style}
                  >
                    <Input 
                      addonBefore={`${Input_addonBefore}: `}
                      placeholder={item_message}
                      disabled={form.getFieldValue(form_list_name)[name]?.[item_name] === select_default_value}
                      onChange={handleAddressChange}
                    />
                  </Form.Item>
                </Col>
                {form_list_name==="house_info"&&<Col span={6}>
                  <Form.Item
                    {...restField}
                    label="城市:"
                    name={[name, 'city']}
                    required={true}
                    key={key}
                    style={item_style}
                  >
                    <Input 
                      placeholder={item_message}
                      disabled={form.getFieldValue(form_list_name)[name]?.[item_name] === select_default_value}
                      onChange={handleAddressChange}
                    />
                  </Form.Item>
                </Col>}
                <Col span={12}>
                  <Form.Item
                    {...restField}
                    label="在我名下:"
                    name={[name, 'is_me']}
                    required={true}
                    key={key}
                    style={item_style}
                  >
                    <Select 
                      placeholder=""
                      disabled={form.getFieldValue(form_list_name)[name]?.[item_name] === select_default_value}
                    >
                      {InitSelectOptions(["在我名下","不在我名下"])}
                    </Select>
                  </Form.Item>
                </Col>
                <Col span={2}>
                  {fields.length > 1 && (
                    <MinusCircleOutlined onClick={() => {
                      remove(name);
                      checkAddButtonStatus();
                    }} />
                  )}
                </Col>
              </Row>
            </Form.Item>
          ))}
          <Form.Item wrapperCol={{ offset: 8, span: 16 }} style={item_style}>
            <Button 
              type="dashed" 
              onClick={() => {
                add();
                checkAddButtonStatus();
              }} 
              block 
              icon={<PlusOutlined />}
              disabled={disableAdd}
            >
              添加地址
            </Button>
          </Form.Item>
        </>
      )}
    </Form.List>
  );
}

function BrotherComponent({options_obj}){
  // 添加兄弟姐妹信息的组件
  const {marital_status_arr, brothers_arr, work_type_arr, health_status_arr} = options_obj

  return <Form.List name="brothers">
  {(fields, { add, remove }) => (
    <div>
      {fields.map((field, index) => (
        <Form.Item wrapperCol={{ offset: 7, span: 16 }} style={item_style}>
        <div key={field.key}>
          <Row gutter={8}>
            <Col span={4}>
              <Form.Item
                {...field}
                name={[field.name, 'relations']}
                label={"关系"}
                fieldKey={[field.fieldKey, 'relations']}
                rules={[{ required: true, message: 'Value is required!' }]}
                style={item_style}
              >
                <Select>
                  {InitSelectOptions(brothers_arr)}
                </Select>
              </Form.Item>
            </Col>
            <Col span={6}>
              <Form.Item
                {...field}
                name={[field.name, 'health_status']}
                label={"健康状况"}
                fieldKey={[field.fieldKey, 'health_status']}
                rules={[{ required: true, message: 'Value is required!' }]}
                style={item_style}
              >
                <Select>
                  {InitSelectOptions(health_status_arr)}
                </Select>  
              </Form.Item>
            </Col>
            <Col span={6}>
              <Form.Item
                {...field}
                name={[field.name, 'maritalStatus']}
                label={"婚姻状况"}
                fieldKey={[field.fieldKey, 'maritalStatus']}
                rules={[{ required: true, message: 'Value is required!' }]}
                style={item_style}
              >
                <Select>
                {InitSelectOptions(["已婚"].concat(marital_status_arr))}
                </Select>  
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={8}>
            <Col span={7}>
              <Tooltip title={"您可以不填写，不强求"}>
                <Form.Item
                {...field}
                name={[field.name, 'work_type']}
                label={"工作类型:"}
                fieldKey={[field.fieldKey, 'work_type']}
                rules={[{message: 'Value is required!' }]}
                style={item_style}
              >
                <Select>
                {InitSelectOptions(["不便透露"].concat(work_type_arr))}
                </Select>  
              </Form.Item>
              </Tooltip>
            </Col>
            <Col span={7}>
              <Form.Item
                {...field}
                name={[field.name, 'monthIncome']}
                label={"月收入"}
                fieldKey={[field.fieldKey, 'monthIncome']}
                style={item_style}
              >
                {/* <Input placeholder='您可以不用填写'/> */}
                <InputNumber min={300} max={100000} style={{width:"100%"}}/>
              </Form.Item>
            </Col>
            <Col span={7}>
              <Form.Item
                {...field}
                name={[field.name, 'yearIncome']}
                label={"年收入"}
                fieldKey={[field.fieldKey, 'yearIncome']}
                style={item_style}
              >
                {/* <Input placeholder='您可以不用填写'/> */}
                <InputNumber min={0} max={200} style={{width:"100%"}}/>
              </Form.Item>
            </Col>
          </Row>
          <Button type="dashed" onClick={() => remove(field.name)} block icon={<MinusOutlined />} >删除关系</Button>
        </div>
        </ Form.Item>
      ))}
      <Form.Item wrapperCol={{ offset: 8, span: 16 }} style={item_style}>
        <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />} >添加兄弟姐妹</Button>
      </Form.Item>
    </div>
  )}
</Form.List>
}

function ParentComponent({options_obj}){
  // 添加兄父母信息的组件
  const {health_status_arr, parents_work_status_arr} = options_obj
  return <Form.List name="parents">
  {(fields) => (
    <>
      {fields.map((field, index) => (
        <Form.Item wrapperCol={{ offset: 7, span: 16 }} style={item_style}>
        <div key={field.key}>
          {index===0?<div ><p>爸爸</p></div>:<div ><p>妈妈</p></div>}
          <Row gutter={8}>
            <Col span={6}>
              <Form.Item
                {...field}
                name={[field.name, 'health_status']}
                label={"健康状况"}
                fieldKey={[field.fieldKey, 'health_status']}
                rules={[{ required: true, message: 'Value is required!' }]}
                style={item_style}
              >
                <Select>
                  {InitSelectOptions(health_status_arr)}
                </Select>  
              </Form.Item>
            </Col>
            <Col span={8}>
              <Tooltip title={"请注意单位：【元】。输入10000:表示月收入10000元"}>
                <Form.Item
                  {...field}
                  name={[field.name, 'monthIncome']}
                  label={"月收入"}
                  fieldKey={[field.fieldKey, 'monthIncome']}
                  style={item_style}
                >
                  <InputNumber min={300} max={100000} style={{width:"100%"}}/>
                </Form.Item>
              </Tooltip>
            </Col>
            <Col span={10}>
              <Tooltip title={"请注意单位：【元】。输入12:表示年收入12万元"}>
                <Form.Item
                {...field}
                name={[field.name, 'yearIncome']}
                label={"年收入:"}
                fieldKey={[field.fieldKey, 'yearIncome']}
                style={item_style}
              >
                <InputNumber min={0} max={200} style={{width:"100%"}}/>
              </Form.Item>
              </Tooltip>
            </Col>
          </Row>
          <Row gutter={8}>
            <Col span={12}>
              <Form.Item
                {...field}
                name={[field.name, 'work_type']}
                label={"工作类型"}
                fieldKey={[field.fieldKey, 'work_type']}
                style={item_style}
              >
                <Select>
                  {InitSelectOptions(parents_work_status_arr)}
                </Select>  
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                {...field}
                name={[field.name, 'work_city']}
                label={"工作城市"}
                fieldKey={[field.fieldKey, 'work_city']}
                style={item_style}
              >
                <Input />
              </Form.Item>
            </Col>
          </Row>
        </div>
        </ Form.Item>
      ))}
    </>
  )}
</Form.List>
}

function ChildrenComponent(){
  // 添加子女信息的组件
  const [select_title, setSelectTitle] = useState("对方是否出抚养费:")
  const SelectChange=(e)=>{
    // console.log(e)
    // if (e==="在身边"){
    //   setSelectTitle("对方是否出抚养费:")
    // }else{
    //   setSelectTitle("我是否出抚养费:")
    // }
    // debugger
  }
  return <Form.List name="childrens">
  {(fields) => (
    <>
      {fields.map((field, index) => (
        <Form.Item wrapperCol={{ offset: 7, span: 16 }}  style={item_style}>
        <div key={field.key}>
          <Row gutter={8} style={item_style}>
            <Col span={4}>
              <Form.Item
                {...field}
                name={[field.name, 'sex']}
                label={"性别"}
                fieldKey={[field.fieldKey, 'sex']}
                rules={[{ required: true, message: '孩子性别必须填写!' }]}
              >
                <Select>
                  {InitSelectOptions(sex_arr)}
                </Select>  
              </Form.Item>
            </Col>
            <Col span={5}>
              <Tooltip title={""}>
                <Form.Item
                  {...field}
                  name={[field.name, 'age']}
                  label={"年龄"}
                  rules={[{ required: true, message: '孩子年龄必须填写!' }]}
                  fieldKey={[field.fieldKey, 'age']}
                >
                  <InputNumber min={0} max={18}  style={{width:100}}/>
                </Form.Item>
              </Tooltip>
            </Col>
            <Col span={6}>
              <Tooltip title={""}>
                <Form.Item
                  {...field}
                  name={[field.name, 'children_around']}
                  label={"是否在身边"}
                  rules={[{ required: true, message: '孩子是否在身边必须填写!' }]}
                  fieldKey={[field.fieldKey, 'children_around']}
                >
                  <Select onChange={SelectChange}>
                  {InitSelectOptions(["在身边","不在身边"])}
                </Select>
                </Form.Item>
              </Tooltip>
            </Col>
            <Col span={7}>
              <Tooltip title={""}>
                <Form.Item
                  {...field}
                  name={[field.name, 'children_support_payment']}
                  label={select_title}
                  rules={[{ required: true, message: '对方是否出孩子抚养费必须填写!' }]}
                  fieldKey={[field.fieldKey, 'children_support_payment']}
                >
                  <Select>
                    {InitSelectOptions(["出","不出"])}
                </Select>
                </Form.Item>
              </Tooltip>
            </Col>
          </Row>
          <Row gutter={8} style={{marginTop:-20}}>
            <Col span={14}>
              <Tooltip title={"其他需要额外补充的信息"}>
                <Form.Item
                {...field}
                name={[field.name, 'other']}
                label={"是否有其他补充"}
                fieldKey={[field.fieldKey, 'other']}
                rules={[{ required: false, message: '其他需要额外补充的信息!' }]}
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
