
// router.js
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import AppLayout from './router_components/AppLayout';
import AddInformation from './components/information/AddInfo';
import AgGridTable from './components/AgGridTable';
import FilterInfo from './components/FilterInfo';
import ShowBaseInfo from './components/ShowBaseInfo';
import MyGridComponent from './MyGridComponent';
import MyFormComponent from './components/MyFormComponent';
import FormListDemo from './components/FormListDemo';
import DynamicForm from './components/Demo';
import AddRequirements from './components/information/AddRequirements.jsx';
import SelectDemo from './components/SelectDemo';
import { SettingLayout } from './components/Setting.jsx';

const ErrorPage = () => {
  return (
    <div>
      <h1>404 - 页面未找到</h1>
      <p>抱歉，您访问的页面不存在。</p>
    </div>
  );
};

// export default ErrorPage;

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    errorElement: <ErrorPage />, // 添加错误页面
    children:[
      {
        path: '/',
        element: <div>
          <FilterInfo />
          <ShowBaseInfo />
        </div>,
      },
      {
        path: '/home',
        element: <AddInformation/>,
      },
      {
        path: '/managerial',
        element: <AgGridTable />,
      },
      {
        path: '/add',
        element: <AddInformation />,
      },
      {
        path: '/request_add',
        element: <AddRequirements />,
      },
      {
        path:"/setting",
        element:<SettingLayout />
      },
      {
        path: '/test',
        element: <div>
          <MyGridComponent />
          <MyFormComponent />
          <FormListDemo />
          <DynamicForm />
          <SelectDemo />
        </div>,
      },
      {
        path: '*', // 匹配所有未定义的路由
        element: <ErrorPage />,
      },
    ]
  },
  // {
  //   path: '/dashboard',
  //   element: <Dashboard />,
  //   // 嵌套路由
  //   children: [
  //     {
  //       path: 'profile',
  //       element: <Profile />, // 假设这是另一个组件
  //       // 可以继续嵌套更多路由
  //     },
  //   ],
  // },
  // 404 未找到页面
  // {
  //   path: '*',
  //   element: <NotFound />, // 假设这是另一个组件
  // },
]);
const App = () => {
  return <RouterProvider router={router} />;
};
export default App;