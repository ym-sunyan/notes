import React, { useState } from 'react';
import 'ag-grid-enterprise';

import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

const MyGridComponent = () => {
    const [rowData, setRowData] = useState([
        { name: '张三', age: 25, birthday: '1998-01-01', gender: '男' },
        { name: '李四', age: 30, birthday: '1993-05-15', gender: '女' },
    ]);

    const columnDefs = [
        { headerName: "姓名", field: "name", filter: 'agTextColumnFilter' },
        { headerName: "年龄", field: "age", filter: 'agNumberColumnFilter' },
        { headerName: "生日", field: "birthday", filter: 'agDateColumnFilter' },
        { headerName: "性别", field: "gender", filter: 'agSetColumnFilter', filterParams: { values: ['男', '女'] } }
    ];
    return (
        <div className="ag-theme-alpine" style={{ height: 400, width: 600 }}>
            <AgGridReact
                columnDefs={columnDefs}
                rowData={rowData}
                defaultColDef={{ sortable: true, resizable: true, filter: true }}
            />
        </div>
    );
};

export default MyGridComponent;