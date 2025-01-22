import React, { useState } from 'react';
import { Form, Input, Button, Select, Space, Tooltip, Upload, Modal, Row, Col } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

const YourFormComponent = () => {
  const [form] = Form.useForm();
  const [age, setAge] = useState('XX');
  const [previewVisible, setPreviewVisible] = useState(false);
  const [previewImage, setPreviewImage] = useState('');
  const [previewTitle, setPreviewTitle] = useState('');

  const BirthDateHandleBlur = (e) => {
    // 实现出生日期失焦时的年龄计算逻辑
  };

  const handlePreview = async (file) => {
    // 实现图片预览逻辑
  };

  const handleCancel = () => setPreviewVisible(false);

  return (
    <Form
      form={form}
      name="basic"
      layout="horizontal"
      labelCol={{ span: 6 }}
      wrapperCol={{ span: 18 }}
      style={{maxWidth: 800, textAlign:"left"}}
      autoComplete="off"
    >
      <Row>
        <Col span={24}>
          <Form.Item label="姓名" name="name" rules={[{ required: true, message: 'Please input your name!', }]}>
            <Input />
          </Form.Item>
          <Form.Item label="性别" name="sex" rules={[{ required: true, message: 'Please select your gender!', }]}>
            <Select>
              <Select.Option value="1">男</Select.Option>
              <Select.Option value="2">女</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item label="出生日期" name="birth_date" rules={[{ required: true, message: 'Please input your birth date!', }]}>
            <Space>
              <Input placeholder={"格式:2000-01-01"} style={{width:200}} onBlur={BirthDateHandleBlur}/>
              <Tooltip title="年龄根据输入的出生日期自动生成">
                年龄: <span style={{backgroundColor:"yellow", color:"red", fontSize:20}}><b> {age} </b></span> 岁
              </Tooltip>
            </Space>
          </Form.Item>
          <Form.Item label="照片" name="photos" rules={[{ required: true, message: '请上传照片!' }]}>
            <div style={{ height: '200px', border: '1px solid #d9d9d9', borderRadius: '2px', overflow: 'hidden', position: 'relative' }}>
              <div style={{ height: '100%', overflowY: 'auto', padding: '8px' }}>
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
              </div>
            </div>
          </Form.Item>
          <Form.Item label="工作类型" name="work_type" rules={[{ required: true, message: 'Please input your work type!', }]}>
            <Input />
          </Form.Item>
          <Form.Item label="工作城市" name="work_city" rules={[{ required: true, message: 'Please input your work city!', }]}>
            <Input />
          </Form.Item>
          <Form.Item label="工作单位" name="work_unit" rules={[{ required: true, message: 'Please input your work unit!', }]}>
            <Input />
          </Form.Item>
          <Form.Item wrapperCol={{offset: 6, span: 18}}>
            <Space size={100}>
              <Button type="primary" htmlType="submit"> Update </Button>
              <Button type="primary" htmlType="reset"> Cancel </Button>
            </Space>
          </Form.Item>
        </Col>
      </Row>
      <Modal
        visible={previewVisible}
        title={previewTitle}
        footer={null}
        onCancel={handleCancel}
      >
        <img alt="example" style={{ width: '100%' }} src={previewImage} />
      </Modal>
    </Form>
  );
};

export default YourFormComponent;