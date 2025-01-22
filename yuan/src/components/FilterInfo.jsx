import React, { useEffect, useState } from 'react'
import { Col, Input, Button, Form, InputNumber, Row, Select, Space, Tooltip, Divider, AutoComplete } from 'antd'
import { MinusCircleOutlined, PlusOutlined, MinusOutlined } from '@ant-design/icons';
const { Search } = Input;
const academic_qualifications_arr= ["初中","高中","大专","本科","研究生","博士","博士后"] //学历
const house_loan_arr= ["有房无贷款","有房有贷款","随时可以买房","无房"]
const car_loan_arr= ["有车无贷款","有车有贷款","随时可以买车","无车"]
const work_type_arr= ["务农","公务员","教师","医生","护士","独立创业者","科技工作者","金融工作者","希望增加自定义输入功能"] //工作类型
const parents_work_status = ["退休","教师","公职人员","医护人员","打工","个体户","务农","不便透露"]

const brothers_arr= ["哥哥","姐姐","弟弟","妹妹"] //兄弟姐妹
const marital_status= ["未婚","离异","丧偶"] //婚姻状况

function InitSelectOptions(items){
  let options = []
  for(var i=0; i<items.length; i++){
    options.push(<Select.Option value={(i+1).toString()}>{items[i]}</Select.Option>)
  }
  return options
}
export default function FilterInfo({name="赵某某",sex="男"}) {
  const [form] = Form.useForm()
  const [sex_input_disabled, setSexInputDisabled] = useState(true)
  useEffect(()=>{
    if (sex===null){
      setSexInputDisabled(false)
    }
  },[])
  const onReset=(value)=>{
        
  }

  const onFinish = (values) => {
      const last_data_id = parseInt(rowData[rowData.length-1].id, 10)
    };
  const onFinishFailed = (errorInfo) => {
      console.log('Failed:', errorInfo);
  };
  const initialValues = {    };

  const [select_value_obj, setSelectValueObj] = useState({
    //婚姻状况
    "marital_status": {"value": "未婚","index": "1","col": 0},
    //学历
    "academic_qualifications": {"value": "高中","index": "3","col": 0},
    "house": {"value": "有房无贷款","index": "1","col": 7},
    "car": {"value": "有车无贷款","index": "1","col": 7},
    "father": {"value": "健康","index": "1","col": 0},
    "mother": {"value": "健康","index": "1","col": 0},
  })

  const SelectChange=(value, e, index_of_arr,type)=>{
    console.log(select_value_obj)
    // 更新状态
    const updateValueObj = (prevState) => {
      const col = index_of_arr.indexOf(e.children)!==-1 ? 0 : 7
      return {
        ...prevState,
        [type]: {
          value: e.children,
          index: value,
          col:col,
        },
      };
    };
    setSelectValueObj(updateValueObj);
  }

  const [input_value_obj, setInputValueObj] = useState({})


  const InputNumberChange=(value, type)=>{
    setInputValueObj(prev => ({
      ...prev,
      [type]: value,
    }));
    console.log(input_value_obj)
  }

  const InputChange=(e, type)=>{
    console.log()
    setInputValueObj(prev => ({
      ...prev,
      [type]: e.target.value,
    }));
    console.log(input_value_obj)
  }

  const SaveBtn=()=>{
    console.log(input_value_obj)
    console.log(select_value_obj)
  }

  const onSearch=(value)=>{
    alert(value)
  }

  return (
    <div style={{minWidth:900,maxWidth:1080,paddingTop:5, paddingBottom:5}}>
      <span style={{fontSize:20}}><b>过滤数据</b></span>
      <div style={{textAlign:"left", paddingLeft:20, paddingRight:20}}>
        <div style={{padding:10,paddingLeft:100, paddingRight:100}}>
          <AutoCompleteSearch />
        </div>
        <Row style={{paddingBottom:5}}>
        <Col span={8}>
            <Tooltip title="根据搜素人的性别自动匹配,如果被搜索的人不在数据库中则可以输入">
              <Space>
                <div style={{width:80}}>姓名:</div>
                <Input value={name} disabled={sex_input_disabled} onChange={(e)=>InputChange(e, "name")}/>
              </Space>
            </Tooltip>
          </Col>
          <Col span={6}>
            <Tooltip title="根据搜素人的性别自动匹配,如果被搜索的人不在数据库中则可以输入">
              <Space>
                <div style={{width:80}}>性别:</div>
                <Input value={sex} disabled={sex_input_disabled} onChange={(e)=>InputChange(e, "sex")}/>
              </Space>
            </Tooltip>
          </Col>
          <Col span={2}></Col>
          <Col span={6}>
            <Tooltip title="保存个人搜索条件，再次搜索只需输入用户名称，即可直接一键导入">
              <Button type="primary" htmlType="submit" style={{width:200}} onClick={SaveBtn}> <b>保存个人筛选条件</b> </Button>
            </Tooltip>
          </Col>
        </Row>

        <Row style={{paddingBottom:5}}>
          <Col span={7}>
            <Tooltip title="老祖宗说过: 人靠衣装马靠鞍!">
              <Space>
                <div style={{width:80}}>相 貌 :</div>
                <Select defaultValue={"1"} style={{width:120}}>
                  {InitSelectOptions(["一般","姣好","无要求"])}
                </Select>
              </Space>
            </Tooltip>
          </Col>
          <Col span={1} />
          <Col span={7}>
            <Tooltip title="">
              <Space>
                <div style={{width:80}}>婚姻状况:</div>
                <Select id="marital_status" defaultValue={"1"} style={{width:120}} 
                  onChange={(value, e)=>SelectChange(value, e, ["未婚"],"marital_status")}
                >
                  {InitSelectOptions(["未婚","离异","丧偶"])}
                </Select>
              </Space>
            </Tooltip>
          </Col>
          <Col span={select_value_obj.marital_status.col} style={{paddingBottom:5}} >
            <Tooltip title="请如实填写子女情况">
              <Input.TextArea placeholder='请如实填写子女情况' onChange={(value)=>InputChange(value, "zinv")}/>
            </ Tooltip>
          </Col>
        </Row>

        <Row style={{paddingBottom:5}}>
          <Col span={7}>
            <Tooltip title="将根据自己的年龄前浮动2岁，后浮动3岁。可以不填写">
              <Space>
                <div style={{width:80}}>年龄范围:</div>
                <InputNumber min={18} max={100} defaultValue={20} style={{width:60}} onChange={(value)=>InputNumberChange(value, "min_age")}/> 
                - 
                <InputNumber min={18} max={100} defaultValue={25} style={{width:60}} onChange={(value)=>InputNumberChange(value, "max_age")}/>
                岁
              </Space>
            </Tooltip>
          </Col>
          <Col span={8}>
            <Tooltip title="可以不填写">
              <Space>
                <div style={{width:60, textAlign:"right"}}>身高:</div>
                <InputNumber min={18} max={100} style={{width:60}} onChange={(value)=>InputNumberChange(value, "min_shengao")}/> 
                - 
                <InputNumber min={18} max={100} style={{width:60}} onChange={(value)=>InputNumberChange(value, "max_shengao")}/>
                厘米
              </Space>
            </Tooltip>
          </Col>
          <Col span={8}>
            <Tooltip title="可以不填写">
              <Space>
                <div style={{width:60, textAlign:"right"}}>体重:</div>
                <InputNumber min={18} max={100} style={{width:60}} onChange={(value)=>InputNumberChange(value, "min_tizhong")}/> 
                - 
                <InputNumber min={18} max={100} style={{width:60}} onChange={(value)=>InputNumberChange(value, "max_tizhong")}/>
                公斤
              </Space>
            </Tooltip>
          </Col>
        </Row>

        <Row style={{paddingBottom:5}}>
          <Col span={7}>
            <Tooltip title="将根据自己的学历自动匹配相同的学历">
              <Space>
                <div style={{width:80}}>学 历 :</div>
                <Select id="academic_qualifications" defaultValue={"1"} style={{width:120}} 
                onChange={(value, e)=>SelectChange(value, e, ["无要求","初中","高中"],"academic_qualifications")}
                >
                  {InitSelectOptions(["无要求"].concat(academic_qualifications_arr))}
                </Select>
              </Space>
            </Tooltip>
          </Col>
          <Col span={select_value_obj.academic_qualifications.col}>
            <Tooltip title="不建议填写，要求太过严苛，不利于匹配">
              <Space>
                <div style={{width:60, textAlign:"right"}}>专 业 :</div>
                <Input placeholder='专业名称，不建议填写' onChange={(e)=>InputChange(e, "专业")}/>
              </Space>
            </Tooltip>
          </Col>
          <Col span={select_value_obj.academic_qualifications.col}>
            <Tooltip title="不建议填写，要求太过严苛，不利于匹配">
              <Space>
                <div style={{width:60, textAlign:"right"}}>学 校 :</div>
                <Input placeholder='学校名称，不建议填写'  onChange={(e)=>InputChange(e, "学校")}/>
              </Space>
            </Tooltip>
          </Col>
        </Row>

        <Row style={{paddingBottom:5}}>
          <Col span={7}>
            <Tooltip title="">
              <Space>
                <div style={{width:80}}>房产 :</div>
                <Select id="house" defaultValue={"1"} style={{width:120}} 
                onChange={(value, e)=>SelectChange(value, e, ["无房"], "house")}
                >
                  {InitSelectOptions(house_loan_arr)}
                </Select>
              </Space>
            </Tooltip>
          </Col>
          <Col span={select_value_obj.house.col}>
            <Tooltip title="">
              <Space>
                <div style={{width:60, textAlign:"right"}}>所在城市:</div>
                <Input placeholder='房子在哪个城市' onChange={(e)=>InputChange(e, "房产所在城市")}/>
              </Space>
            </Tooltip>
          </Col>
          <Col span={select_value_obj.house.col}>
            <Tooltip title="不建议填写，要求太过严苛，不利于匹配">
              <Space>
                <div style={{width:60, textAlign:"right"}}>小区名称:</div>
                <Input placeholder='小区名称' onChange={(e)=>InputChange(e, "房产小区名称")}/>
              </Space>
            </Tooltip>
          </Col>
        </Row>

        <Row style={{paddingBottom:5}}>
          <Col span={7}>
            <Tooltip title="">
              <Space>
                <div style={{width:80}}>车 :</div>
                <Select id="car" defaultValue={"1"} style={{width:120}} 
                onChange={(value, e)=>SelectChange(value, e, ["无车"], "car")}>
                  {InitSelectOptions(car_loan_arr)}
                </Select>
              </Space>
            </Tooltip>
          </Col>
          <Col span={select_value_obj.car.col}>
            <Tooltip title="">
              <Space>
                <div style={{width:60, textAlign:"right"}}>车子品牌:</div>
                <Input placeholder='车子品牌，可以不写' onChange={(e)=>InputChange(e, "车子品牌")}/>
              </Space>
            </Tooltip>
          </Col>
        </Row>

        <Row style={{paddingBottom:5}}>
          <Col span={7}>
            <Tooltip title="填写工资范围，单位元">
              <Space>
                <div style={{width:80}}>月工资:</div>
                <InputNumber min={300} max={100000} defaultValue={1500} style={{width:80}} onChange={(value)=>InputNumberChange(value, "min_yuegongzi")}/> 
                - 
                <InputNumber min={300} max={100000} defaultValue={1500} style={{width:80}} onChange={(value)=>InputNumberChange(value, "max_yuegongzi")}/> 
                元
              </Space>
            </Tooltip>
          </Col>
          <Col span={2}></Col>
          <Col span={9}>
          <Tooltip title="填写工资范围，单位万元">
              <Space>
                <div style={{width:80}}>年工资:</div>
                <InputNumber min={3} max={100} defaultValue={5} style={{width:80}} onChange={(value)=>InputNumberChange(value, "min_niangongzi")}/> 
                - 
                <InputNumber min={3} max={100} defaultValue={5} style={{width:80}} onChange={(value)=>InputNumberChange(value, "max_niangongzi")}/> 
                万元
              </Space>
            </Tooltip>
          </Col>
        </Row>

        <Row style={{paddingBottom:5}}>
          <Col span={7}>
            <Tooltip title="">
              <Space>
                <div style={{width:80}}>工作城市:</div>
                <Input  placeholder='工作城市，可以不写' onChange={(e)=>InputChange(e, "工作所在城市")}/> 
              </Space>
            </Tooltip>
          </Col>
          <Col span={7}>
            <Tooltip title="">
              <Space>
                <div style={{width:80, textAlign:"right"}}>工作类型:</div>
                <Input  placeholder='工作类型，可以不写' onChange={(e)=>InputChange(e, "工作类型")}/> 
              </Space>
            </Tooltip>
          </Col>
          <Col span={7}>
          <Tooltip title="">
              <Space>
                <div style={{width:80, textAlign:"right"}}>工作单位:</div>
                <Input placeholder='工作单位，可以不写' onChange={(e)=>InputChange(e, "工作单位")}/> 
              </Space>
            </Tooltip>
          </Col>
        </Row>
        <Divider style={{borderColor: '#7cb305', height:2}} orientation="left"><b>家庭情况</b></Divider>
        <Divider style={{height:2}} ><b>父亲:</b></Divider>
        <Row style={{paddingBottom:5}}>
          <Col span={5}>
            <Tooltip title="">
              <Space>
                <div style={{width:80}}>健康状况:</div>
                <Select defaultValue={"1"} style={{width:90}} 
                onChange={(value, e)=>SelectChange(value, e, ["已故"], "father")}
                >
                  {InitSelectOptions(["健康", "不健康","已故"])}
                </Select>
              </Space>
            </Tooltip>
          </Col>
          <Col span={select_value_obj.father.index==="3"?0:6}>
            <Tooltip title="">
              <Space>
                <div style={{width:80, textAlign:"right"}}>职业:</div>
                <Select defaultValue={"3"} style={{width:100}}>
                  {InitSelectOptions(parents_work_status)}
                </Select>
              </Space>
            </Tooltip>
          </Col>
          <Col span={select_value_obj.father.index==="3"?0:5}>
            <Tooltip title="填写工资范围，单位万元">
                <Space>
                  <div style={{width:60, textAlign:"right"}}>退休:</div>
                  <Select defaultValue={"1"} style={{width:80}}>
                    {InitSelectOptions(["未退", "已退"])}
                </Select>
                </Space>
              </Tooltip>
          </Col>
          <Col span={select_value_obj.father.index==="3"?0:7}>
            <Tooltip title="填写工资范围，单位万元">
              <Space>
                <div style={{width:60, textAlign:"right"}}>年工资:</div>
                <InputNumber min={3} max={100} defaultValue={5} style={{width:50}} onChange={(value)=>InputNumberChange(value, "min_fuqin_niangongzi")}/> 
                - 
                <InputNumber min={3} max={100} defaultValue={5} style={{width:50}} onChange={(value)=>InputNumberChange(value, "max_fuqin_niangongzi")}/> 
                万元
              </Space>
            </Tooltip>
          </Col>
        </Row>
        <Divider style={{height:2}} ><b>母亲:</b></Divider>
        <Row style={{paddingBottom:5}}>
          <Col span={5}>
            <Tooltip title="">
              <Space>
                <div style={{width:80}}>健康状况:</div>
                <Select defaultValue={"1"} style={{width:90}} 
                onChange={(value, e)=>SelectChange(value, e, ["已故"], "mother")}>
                  {InitSelectOptions(["健康", "不健康","已故"])}
                </Select>
              </Space>
            </Tooltip>
          </Col>
          <Col span={select_value_obj.mother.index==="3"?0:6}>
            <Tooltip title="">
              <Space>
                <div style={{width:80, textAlign:"right"}}>职业:</div>
                <Select defaultValue={"3"} style={{width:100}}>
                  {InitSelectOptions(parents_work_status)}
                </Select>
              </Space>
            </Tooltip>
          </Col>
          <Col span={select_value_obj.mother.index==="3"?0:5}>
            <Tooltip title="填写工资范围，单位万元">
                <Space>
                  <div style={{width:60, textAlign:"right"}}>退休:</div>
                  <Select defaultValue={"1"} style={{width:80}}>
                    {InitSelectOptions(["未退", "已退"])}
                </Select>
                </Space>
              </Tooltip>
          </Col>
          <Col span={select_value_obj.mother.index==="3"?0:7}>
            <Tooltip title="填写工资范围，单位万元">
              <Space>
                <div style={{width:60, textAlign:"right"}}>年工资:</div>
                <InputNumber min={3} max={100} defaultValue={5} style={{width:50}} onChange={(value)=>InputNumberChange(value, "min_muqin_niangongzi")}/> 
                - 
                <InputNumber min={3} max={100} defaultValue={5} style={{width:50}} onChange={(value)=>InputNumberChange(value, "max_muqin_niangongzi")}/> 
                万元
              </Space>
            </Tooltip>
          </Col>
        </Row>
        <Divider style={{height:2}} orientation="left"></Divider>
        <Row style={{paddingBottom:5}}>
          <Col span={24}>
            <Form
              form={form}
              name="AddRequirements"
              layout="horizontal"
              labelCol={{ span: 8 }}
              wrapperCol={{ span: 16 }}
              style={{maxWidth: 1200,textAlign:"left"}}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
              onReset={onReset}
              autoComplete="off"
              initialValues={initialValues}
            >
              <BrotherComponent/>
            </Form>
          </Col>
        </Row>
        <Divider style={{borderColor: '#7cb305', height:2}} orientation="left"></Divider>
      </div>
    </div>
  )
}
function BrotherComponent(){
  // 添加兄弟姐妹信息的组件
  return <Form.List name="brothers">
    {(fields, { add, remove }) => (
      <div>
        {fields.map((field, index) => (
          <Form.Item>
          <div key={field.key}>
            <Row>
              <Col span={8}>
                <Form.Item
                  {...field}
                  name={[field.name, 'kinship']}
                  label={"关系"}
                  fieldKey={[field.fieldKey, 'kinship']}
                  rules={[{ required: true, message: '亲属关系不能为空!' }]}
                >
                  <Select defaultValue={"1"} style={{width:100}}>
                    {InitSelectOptions(brothers_arr)}
                  </Select>  
                </Form.Item>
              </Col>
              <Col span={7}>
                <Form.Item
                  {...field}
                  name={[field.name, 'kinship_marital_status']}
                  label={"婚姻状况"}
                  fieldKey={[field.fieldKey, 'kinship_marital_status']}
                  rules={[{ required: true, message: '婚姻状况不能为空!' }]}
                >
                  <Select defaultValue={"1"} style={{width:100}}>
                    {InitSelectOptions(["已婚"].concat(marital_status))}
                  </Select>  
                </Form.Item>
              </Col>
              <Col span={1}></Col>
              <Col span={8}>
                <Tooltip title={"您可以不填写，不强求"}>
                  <Form.Item
                  {...field}
                  name={[field.name, 'kinship_work']}
                  label={"工作情况:"}
                  fieldKey={[field.fieldKey, 'kinship_work']}
                  rules={[{message: 'Value is required!' }]}
                >
                  <Select defaultValue={"1"} >
                  {InitSelectOptions(["不便透露"].concat(work_type_arr))}
                  </Select>  
                </Form.Item>
                </Tooltip>
              </Col>
            </Row>
            <Button type="dashed" onClick={() => remove(field.name)} block icon={<MinusOutlined />} >删除关系</Button>
          </div>
          </ Form.Item>
        ))}
        <Form.Item >
          <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />} >添加兄弟姐妹</Button>
        </Form.Item>
      </div>
    )}
  </Form.List>
}

export function AutoCompleteSearch() {
  const name_arr = ["尹凯","倪雨婷","俞秀","左丘思敏","戚楠","葛宇","赵泽","端木涵","范宇轩","严磊","卞磊","罗桐","司寇红","元梓豪",
  "陆汪诚","范荣","邹洋","薛梓睿","云皓","袁洋","唐瑞","窦成","平欣然","严柏","沈章梓萱","吕瑾瑜","马庆",
  "叶诗涵","漆雕柏","赵云"]
  const searchResult = (query) =>{
    let new_name_arr = []
    for(let name of name_arr){
      if(name.indexOf(query) !== -1){
        new_name_arr.push({
          value: name,
          label: (
            <div style={{display: 'flex',justifyContent: 'space-between',}}>
              <span>找到 <span style={{color:"red"}}><b>{name}</b></span></span>
              <span>导入筛选条件</span>
            </div>
          ),
        })
      }
    }

    if(new_name_arr.length === 0){
      new_name_arr.push({
        // value: "没有该用户",
        label: (
          <div style={{display: 'flex',justifyContent: 'space-between',}}>
            <span style={{color:"red"}}><b>没有该用户</b></span>
            <span>请逐项填写并保存</span>
          </div>
        ),
      })
    }
    return new_name_arr
  };
  const [options, setOptions] = useState([]);
  const handleSearch = (value) => {
    setOptions(value ? searchResult(value) : []);
  };
  const onSelect = (value) => {
    console.log('onSelect', value);
  };
  return (
    <div>
    <AutoComplete
      popupMatchSelectWidth={440}
      style={{width: 500}}
      options={options}
      onSelect={onSelect}
      onSearch={handleSearch}
      size="large"
      // allowClear
    >
      <Input.Search size="large" placeholder="输入姓名" enterButton="搜索" />
    </AutoComplete>
    </div>
  )
}
