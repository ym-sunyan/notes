import React from 'react';
import { Form, Input, InputNumber, Button, Space, message, Select, Tooltip, Row, Col } from 'antd';

export function FormItemRange({label, item_name, required=true, number_min=0, number_max=100}) {
  // 处理值范围的form item组件
  return (
    <Form.Item
        label={label}
        style={{ marginBottom: 0 }}
        rules={[
          {
            validator: (_, value) => {
            if(required){
              debugger
              if (!value || value.min === undefined || value.max === undefined) {
                return Promise.reject(new Error('请填写完整的数值范围'));
              }
              if (value.min >= value.max) {
                return Promise.reject(new Error('最小值必须小于最大值'));
              }
              return Promise.resolve();
            }
            },
          },
        ]}
      >
        <Space>
          <Form.Item
            name={Array.isArray(item_name)?item_name.concat(['min']):[item_name, 'min']}
            noStyle
            rules={[{ required: true, message: '请输入最小值' }]}
          >
            <InputNumber placeholder="最小值" min={number_min} max={number_max} />
          </Form.Item>
          到
          <Form.Item
            name={Array.isArray(item_name)?item_name.concat(['max']):[item_name, 'max']}
            noStyle
            rules={[{ required: true, message: '请输入最大值' }]}
          >
            <InputNumber placeholder="最大值"  min={number_min} max={number_max} />
          </Form.Item>
        </Space>
      </Form.Item>
  )
}

const MyFormComponent = () => {
  const onFinish = (values) => {
    console.log('Success:', values);
  };

  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
    message.error('请填写完整的数值范围');
  };
  const initialValues = {
    range: {
      min: null,
      max: 100,
    },
    month_range: {
      min: null,
      max: null,
    },
  };

  return (
    <Form
      name="range_form"
      initialValues={initialValues}
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
    >
      <Form.Item
        label="数值范围"
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
            name={['range', 'min']}
            noStyle
            rules={[{ required: false, message: '请输入最小值' }]}
          >
            <InputNumber placeholder="最小值" />
          </Form.Item>
          到
          <Form.Item
            name={['range', 'max']}
            noStyle
            rules={[{ required: false, message: '请输入最大值' }]}
          >
            <InputNumber placeholder="最大值" />
          </Form.Item>
        </Space>
      </Form.Item>
      {/* <FormItemRange label={"月份范围"} item_name={"month_range"} required={false}/> */}
      <Form.Item>
        <Button type="primary" htmlType="submit">
          提交
        </Button>
      </Form.Item>
    </Form>
  );
};

export default MyFormComponent;