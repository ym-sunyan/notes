import React, { useEffect, useState } from 'react';
import { Select } from 'antd';
const { Option } = Select;
const SelectDemo = ({items}) => {
  const [value, setValue] = useState(null);
  const [options, setOptions] = useState([]);
  const [old_options_length, setOldOtionsLength] = useState(null)

  useEffect(()=>{
    let new_options = []
    for(let index in items){
        new_options.push({
            value: index+1, label: items[index]
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
  );
};

export default SelectDemo;