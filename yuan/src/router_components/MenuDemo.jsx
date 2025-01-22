import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Menu, Switch } from 'antd';

export default function MenuDemo() {
    const navigate = useNavigate()
    const menus_items = [
      {
        label: '首页',
        key: '/',
        path: '/',
      },
      {
        label: '添加',
        key: '/add',
        path: '/add',
      },
      {
        label: '管理',
        key: '/managerial',
        path: '/managerial',
      },
      {
        label: '添加个人要求',
        key: '/request_add',
        path: '/request_add',
      },
      {
        label: '系统设置',
        key: '/setting',
        path: '/setting',
      },
      {
        label: '测试',
        key: '/test',
        path: '/test',
      },
    ];
    const onMenuClick = (e) => {
      navigate(e.key);
    };
    return (
      <div>
        <Menu
            // defaultSelectedKeys={['1']}
            onClick={onMenuClick}
            mode="horizontal"
            items={menus_items}
          />
      </div>
    )
  }