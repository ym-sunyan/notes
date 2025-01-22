import React, { useState } from 'react';
import { Form, Input, Button, Select, Tooltip, Row, Col, Space, InputNumber } from 'antd';

const FormListDemo = () => {
  const [form] = Form.useForm();

  const onFinish = (values) => {
    console.log('Received values of form:', values);
  };

  return (
    <Form
      form={form}
      name="static_list"
      onFinish={onFinish}
      initialValues={{
        items: [
            { value: '1',monthIncome:"t",health_status:"1" },
            { value: '2',monthIncome:"t",health_status:"1" },
            { value: '3',monthIncome:"t",health_status:"1" },
        ],
        items1: [
            { value: '1',monthIncome:"1000",health_status:"1" },
            { value: '2',monthIncome:1000,health_status:"1" },
            { value: '3',monthIncome:1000,health_status:"1" },
        ],
        parents:[
            {health_status:"1",monthIncome:"10001",yearIncome:"12",work_status:"2"},
            {health_status:"1",monthIncome:"3000",yearIncome:"4000",work_status:"7"},
        ]
      }}
    >
      <Form.List name="items">
        {(fields) => (
          <>
            {fields.map((field, index) => (
              <>
              <Form.Item
                key={field.key}
                {...field}
              label="test1"
                name={[field.name, 'value']}
                fieldKey={[field.fieldKey, 'value']}
                rules={[{ required: true, message: 'Please input the value!' }]}
              >
                <Input placeholder="Enter something" />
              </Form.Item>
              <Form.Item
              key={field.key}
              {...field}
              label="test2"
              name={[field.name, 'monthIncome']}
            //   fieldKey={[field.fieldKey, 'monthIncome']}
              rules={[{ required: true, message: 'Please input the value!' }]}
            >
              <Input placeholder="Enter something"/>
            </Form.Item>
            <Form.Item
                {...field}
                name={[field.name, 'health_status']}
                label={"健康状况"}
                fieldKey={[field.fieldKey, 'health_status']}
                rules={[{ required: true, message: 'Value is required!' }]}
            >
                <Select>
                <Select.Option value="1">健康</Select.Option>
                <Select.Option value="2">已故</Select.Option>
                </Select>  
            </Form.Item>
            </>
            ))}
          </>
        )}
      </Form.List>
      <Form.List name="parents">
        {(fields) => (
        <>
            {fields.map((field, index) => (
            <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <div key={field.key}>
                {/* {index===0?<div ><p>爸爸</p></div>:<div ><p>妈妈</p></div>} */}
                <Row gutter={8}>
                <Col span={6}>
                    {/* <Form.Item
                    {...field}
                    name={[field.name, 'health_status']}
                    label={"健康状况"}
                    fieldKey={[field.fieldKey, 'health_status']}
                    rules={[{ required: true, message: 'Value is required!' }]}
                    >
                    <Select>
                        <Select.Option value="1">健康</Select.Option>
                        <Select.Option value="2">已故</Select.Option>
                    </Select>  
                    </Form.Item> */}
                </Col>
                <Col span={8}>
                    <Tooltip title={"您可以不填写，不强求"}>
                    <Form.Item
                        {...field}
                        name={[field.name, 'monthIncome']}
                        label={"月收入"}
                        fieldKey={[field.fieldKey, 'monthIncome']}
                    >
                        <Input placeholder='请输入'/>
                    </Form.Item>
                    </Tooltip>
                </Col>
                <Col span={10}>
                    <Tooltip title={"您可以不填写，不强求"}>
                    <Form.Item
                    {...field}
                    name={[field.name, 'yearIncome']}
                    label={"年收入:"}
                    fieldKey={[field.fieldKey, 'yearIncome']}
                    >
                        <Input placeholder='请输入'/>
                    </Form.Item>
                    </Tooltip>
                </Col>
                {/* <Col span={24}>
                    <Form.Item
                    {...field}
                    name={[field.name, 'work_status']}
                    label={"工作类型"}
                    fieldKey={[field.fieldKey, 'work_status']}
                    >
                    <Select>
                        <Select.Option value="0">退休</Select.Option>
                        <Select.Option value="1">个体户</Select.Option>
                        <Select.Option value="2">教师</Select.Option>
                        <Select.Option value="3">公职人员</Select.Option>
                        <Select.Option value="4">医护人员</Select.Option>
                        <Select.Option value="5">打工</Select.Option>
                        <Select.Option value="6">个体户</Select.Option>
                        <Select.Option value="7">务农</Select.Option>
                        <Select.Option value="8">不便透露</Select.Option>
                    </Select>  
                    </Form.Item>
                </Col> */}
                </Row>
            </div>
            </ Form.Item>
            ))}
        </>
        )}
    </Form.List>

    <Form.List name="items1">
        {(fields) => (
        <>
            {fields.map((field, index) => (
            <div key={field.key}>
                <Tooltip title={"请注意单位：【元】。输入10000:表示月收入10000元"}>
                <Form.Item
                    {...field}
                    name={[field.name, 'monthIncome']}
                    label={"月收入"}
                    fieldKey={[field.fieldKey, 'monthIncome']}
                >
                    <InputNumber min={1000} max={100000} style={{width:"100%"}}/>
                </Form.Item>
                </Tooltip>
                <Tooltip title={"请注意单位：【元】。输入12:表示年收入12万元"}>
                    <Form.Item
                    {...field}
                    name={[field.name, 'health_status']}
                    label={"年收入:"}
                    fieldKey={[field.fieldKey, 'health_status']}
                    >
                        <Input placeholder='请输入'/>
                    </Form.Item>
                </Tooltip>
            </div>
            ))}
        </>
        )}
    </Form.List>

    </Form>
  );
};

export default FormListDemo;