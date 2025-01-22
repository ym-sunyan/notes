import React from 'react';
import { Flex,Layout } from 'antd';

import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { Outlet } from 'react-router-dom';
import MenuDemo from './MenuDemo.jsx';
const { Header, Footer, Sider, Content } = Layout;

const AppLayout=()=> {
  const headerStyle = {textAlign: 'center',backgroundColor: '#4096ff',};
  const contentStyle = {textAlign: 'center',minHeight: 1000};
  const siderStyle = {textAlign: 'center',backgroundColor: '#fff',};
  const footerStyle = { textAlign: 'center', backgroundColor: '#4096ff',};
  return (
    <Flex>
      <Layout>
        <Header style={headerStyle}>
          <MenuDemo />
        </Header>
        <Layout>
        <Sider width={200} style={siderStyle}>
          </Sider>
          <Content style={contentStyle}>
            <Outlet /> 
          </Content>
          <Sider width={200} style={siderStyle}>
            Sider
          </Sider>
        </Layout>
        <Footer style={footerStyle}><b>信息管理</b></Footer>
      </Layout>
    </Flex>
  );
}
export default AppLayout;
