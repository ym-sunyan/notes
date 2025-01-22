import React, { useEffect, useRef, useCallback, useState } from 'react';
import { Flex,Layout } from 'antd';
import { useLocation, useNavigate } from 'react-router-dom';
import { Menu, Switch, message } from 'antd';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { Outlet } from 'react-router-dom';
import { Anchor } from 'antd';

const { Sider, Content } = Layout;

const siderStyle = {
    position: 'fixed',
    left: 0,
    width: 200, // px 可以省略，React 会识别为像素单位
    overflowY: 'auto', // React 样式使用 camelCase 命名
    zIndex: 100, // 确保侧边栏在页面其他内容之上
};
const contentStyle = {
    marginLeft: '200px', // 与侧边栏宽度相同
    padding: '24px',
    background: '#fff',
};


export function SettingLayout() {
    const [current, setCurrent] = useState("section1")
    return (
        <Layout hasSider={"auto"} style={{ minHeight: '100vh' }}>
        <Sider style={siderStyle}>
            <Directory item={current}/>
        </Sider>
        <Content style={contentStyle}>
            {/* <ContentItem ChangeItem={setCurrent}/> */}
            <ContentItem />
        </Content>
        </Layout>
    );
}

const Directory = ({item}) => {
    const [current, setCurrent] = useState(null);
    const location = useLocation()
    useEffect(() => {
        setCurrent(location.pathname);
      }, [location]);

    useEffect(()=>{
        setCurrent(item)
    },[item])
    const handleClick = (e) => {
        console.info(e.key)
        debugger
      setCurrent(e.key);
    };
    return (
      <Menu
        onClick={handleClick}
        style={{ width: 200 }}
        defaultSelectedKeys={[current]}
        selectedKeys={current}
        mode="inline"
      >
        <Menu.Item key="section1">
          <a href="#section1">搜索结果的模式设置</a>
        </Menu.Item>
        <Menu.Item key="section2">
          <a href="#section2">表格中初始字段设置</a>
        </Menu.Item>
        <Menu.Item key="section3">
          <a href="#section3">Section 3</a>
        </Menu.Item>
        <Menu.Item key="section4">
          <a href="#section4">Section 4</a>
        </Menu.Item>
        <Menu.Item key="section5">
          <a href="#section5">Section 5</a>
        </Menu.Item>
        <Menu.Item key="section6">
          <a href="#section6">Section 6</a>
        </Menu.Item>
      </Menu>
    );
};

const ContentItem = ({ChangeItem}) => {
    const sections = useRef([]);
    const [visibleSection, setVisibleSection] = useState(null);
  
    useEffect(() => {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              const sectionId = entry.target.id;
              if (sectionId !== visibleSection) {
                setVisibleSection(sectionId);
                console.log(`Entered ${sectionId}`);
                // 在这里触发你想要的事件
                ChangeItem(entry.target.id)
                message.info(entry.target.id)
              }
            }
          });
        },
        { threshold: 0.8 } // 触发的阈值，可以根据需要调整
      );
  
      sections.current.forEach((section) => {
        observer.observe(section);
      });
  
      return () => {
        sections.current.forEach((section) => {
          observer.unobserve(section);
        });
      };
    }, []);
  
    return (
      <div>
        <Anchor affix={false} offsetTop={0}>
          <Anchor.Link href="#section1" />
          <Anchor.Link href="#section2" />
          <Anchor.Link href="#section3" />
          <Anchor.Link href="#section4" />
          <Anchor.Link href="#section5" />
          <Anchor.Link href="#section6" />
        </Anchor>
        {Array.from({ length: 6 }, (_, index) => (
          <div
            key={index}
            id={`section${index + 1}`}
            ref={(el) => (sections.current[index] = el)}
            style={{ marginTop: '64px', padding: '24px', height: 200, backgroundColor:"#ecfaf4" }}
          >
            <h2>Section {index + 1}</h2>
            <p>Content of section {index + 1}...</p>
          </div>
        ))}
      </div>
    );
  };
