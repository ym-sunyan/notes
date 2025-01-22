import React, { useEffect, useState } from 'react'
import { Card, Col, Image, Row, Space, Divider, Select } from 'antd';

export function CardTitle({name, sex, age, car, house, first,status}) {
  return (
    <div style={{fontSize:15, textAlign:"left"}}>
        <span >{name}</span>&nbsp;&nbsp;&nbsp;
        <span >{sex}</span>&nbsp;&nbsp;&nbsp;
        <span >{age}岁</span>&nbsp;&nbsp;&nbsp;
        <span >{house!==null?"有房":"无房"} {car!==null?"有车":"无车"}</span>&nbsp;&nbsp;&nbsp;
        <span >{first===true?"首首":"非首"}</span>&nbsp;&nbsp;&nbsp;
        <span style={{fontSize:18,color:'red'}}>{status===true?"匹配中":"等待中"}</span>
    </div>
  )
}

export function ShowImages({images}){
    // 显示个人照片
    // 如果不不提供图片，就显示默认的商户log
    const [imgs, setImgs] = useState(images)
    useEffect(()=>{
        if(images.length===0){
            let new_images=['https://gw.alipayobjects.com/zos/antfincdn/LlvErxo8H9/photo-1503185912284-5271ff81b9a8.webp']
            setImgs(new_images)
        }
    },[])
    return(
        <Image.PreviewGroup items={imgs} >
            <Image width={150} height={220} src={imgs[0]} />
        </Image.PreviewGroup>
    )
}

export function BasicPersonalInformation({birthDate, monthIncome, yearIncome, house=null, car=null, jobType, jobCity, jobCompany}){
    // 个人基本信息
    return (
        <div>
            <div>出生: {birthDate}</div>
            <span style={{width:120, display:"inline-block"}}>月收入: {monthIncome}</span>
            <span>年收入: {yearIncome}万</span>
            {house!==null&&<div>房子: {house.number} 套,{house.loan}</div>}
            {car!==null&&<div>车子: {car.number} 辆,{car.loan}</div>}
            <Divider
                    orientation="left"
                    style={{
                        borderColor: '#7cb305',
                        margin: '1px 0',
                        fontSize:10,
                        paddingLeft:2,
                        paddingRight:5
                    }}
                    >
                    <b>工作</b>
                </Divider>
            <span style={{width:120, display:"inline-block"}}>类型: {jobType}</span>
            <span>城市: {jobCity}</span>
            <div>单位: {jobCompany}</div>
            <div style={{height:2}}></div>
        </div>
    )
}

export function FamilySituation({father=null, mother=null, brothers=[]}){
    const [div_height, setDivHeight] = useState(180)
    useEffect(()=>{
        if(father===null&&mother===null&&brothers.length===0) setDivHeight(0)
    },[])

    const div_block =(info_obj)=>{
        if (info_obj===null) return null
        return (
        <div>
            <Space>
            <div style={{color:"red"}}><b>{info_obj.name}</b></div>
            <div>{info_obj.jobStatus}</div>
            <div>婚姻状况:{info_obj.maritalStatus}</div>
            <div>月收入:{info_obj.monthIncome}</div>
            <div>年收入:{info_obj.yearIncome}万</div>
            </Space><br/>
            <span>工作:{info_obj.jobCity}</span>&nbsp;&nbsp;&nbsp;&nbsp;
            <span>工作地点:{info_obj.jobCompany}</span>
        </div>
        )
    }
    // 家庭情况
    return (
        <div style={{
            height:{div_height},
            paddingLeft:5,
            fontSize:12,
            paddingRight:5,
            textAlign:"left",
            backgroundColor:"#F5F5F5"}}
        >
           {div_block(father)}
           {div_block(mother)}
           {brothers.map((brother, index)=>{return div_block(brother)})}
    </div>
    )
}

// 极简模式
export function MiniBaseInfo({data}) {
    // 极简模式
    const {name, sex, age, first, status, cars, images, houses, familySituation} = data
    const [house_loan, setHouseLoan] = useState("")
    const [car_loan, setCarLoan] = useState("")

    const GetLoan=(arrs)=>{
        if (arrs.length === 0) return ""
        let loan = []
        arrs.forEach((obj)=>{
            loan.push(obj.loan)
        })
        let loan1 = loan.indexOf("无贷款")
        let loan2 = loan.indexOf("有贷款")
        if(loan1!==-1 && loan2!==-1){
            return "部分无贷款"
        }else if(loan1 === -1){
            return "全部有贷款"
        }else if(loan2 === -1){
            return "全部无贷款"
        }
    }
    useEffect(()=>{
        setHouseLoan(GetLoan(houses))
        setCarLoan(GetLoan(cars))
    },[])
  return (
    <div> 
        <Card
            title={<CardTitle 
                name={name}
                sex={sex}
                age={age}
                car={cars.length===0?null:"有"} 
                house={houses.length===0?null:"有"} 
                first={first} 
                status={status}/>}
            size="small"
            bordered={false}
            hoverable
            extra={<a href="#">详情</a>}
            style={{width: 400,height:300}}
        >
            <Row style={{backgroundColor:"#F5F5F5"}}>
                <Col span={10}>
                    {<ShowImages images={images} />}
                </Col>
                <Col span={14} style={{textAlign:"left", fontSize:12, paddingRight:2,paddingTop:2}}>
                    <BasicPersonalInformation birthDate={data.birthDate} monthIncome={data.monthIncome} yearIncome={data.yearIncome} house={{number:houses.length, loan:house_loan}} car={{number:cars.length, loan:car_loan}} jobType={data.jobType} jobCity={data.jobCity} jobCompany={data.jobCompany}/>
                    <Divider
                          orientation="left"
                          style={{
                              borderColor: '#7cb305',
                              margin: '1px 0',
                              fontSize:10,
                              paddingLeft:2,
                              paddingRight:5
                          }}
                          >
                          <b>家庭情况</b>
                      </Divider>
                    <span style={{color:"red",width:30, display:"inline-block"}}><b>父亲</b></span>
                    <span>年收入:<b style={{color:"red"}}>{familySituation.father.yearIncome}万</b></span>&nbsp;&nbsp;
                    <span>工作:{familySituation.father.jobType}</span><br/>
                    <span style={{color:"red",width:30, display:"inline-block"}}><b>母亲</b></span>
                    <span>年收入:<b style={{color:"red"}}>{familySituation.mother.yearIncome}万</b></span>&nbsp;&nbsp;
                    <span>工作:{familySituation.mother.jobType}</span><br/>
                    {familySituation.brothers.map((brother)=>{
                        return <span style={{color:"red",width:100, display:"inline-block"}}><b>{brother.name}:{brother.maritalStatus}</b></span>
                    })}
                    <div>中间人:喜笑颜开</div>
                </Col>
            </Row>
        </Card>
    </div>
  )
}

// 普通模式
export function PlainBaseInfo({data}) {
    const {name, sex, age, first, images, status, cars, houses, familySituation} = data
    // 普通模式
    return (
      <div> 
          <Card
              title={<CardTitle 
                    name={name}
                    sex={sex}
                    age={age}
                    car={cars.length===0?null:"有"} 
                    house={houses.length===0?null:"有"} 
                    first={first} 
                    status={status}/>}
              size="small"
              bordered={false}
              hoverable
              extra={<a href="#">详情</a>}
              style={{width: 400,height:500}}
          >
              <Row style={{backgroundColor:"#F5F5F5"}}>
                  <Col span={10}>
                      {<ShowImages images={images} />}
                  </Col>
                  <Col span={14} style={{textAlign:"left", fontSize:12, paddingRight:2,paddingTop:2}}>
                      
                  <BasicPersonalInformation birthDate={data.birthDate} monthIncome={data.monthIncome} yearIncome={data.yearIncome} jobType={data.jobType} jobCity={data.jobCity} jobCompany={data.jobCompany}/>

                    {houses.map((house, index)=>{
                        return <div style={{backgroundColor:"#DBE0FF"}}>房子: {index+1} <span style={{color:"red"}}>{house.loan}</span>, 地址:<span>{house.address}</span></div>
                    })}

                    {cars.map((car, index)=>{
                        return <div style={{backgroundColor:"#DBE0FF"}}>车子: {index+1} <span>{car.loan}</span>, 品牌:<span><b>{car.address}</b></span></div>
                    })}
                  </Col>
              </Row>
              <div style={{height:10}}></div>
                {<FamilySituation 
                father={familySituation.father}
                mother={familySituation.mother}
                brothers={familySituation.brothers}
                />}
          </Card>
      </div>
    )
}

// 详情模式
export function DetailsBaseInfo({data}) {
    // 详情模式
    return (
      <div> 详情模式</div>
    )
}
const datas = [
    { name:"花好月圆 ",sex:"男", age:"25", birthDate:"2000-01-01",first:true, status:false,
        monthIncome:"8000", yearIncome:"12", jobType:"数据分析员", jobCity:"南京", jobCompany:"南京巨好数据分析有限公司",jobStatus:"在职",
        images:[
            'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png?x-oss-process=image/blur,r_50,s_50/quality,q_1/resize,m_mfit,h_200,w_200',
            ],
        cars:[
            {loan:"无贷款", address:"XXXX"},
            {loan:"有贷款", address:"XXXX"},
            {loan:"无贷款", address:"XXXX"},
        ], 
        houses:[
            {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
            {loan:"有贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
            {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
        ], 
        familySituation:{
            father:{name:"父亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            mother:{name:"母亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            brothers:[{name:"哥哥", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            {name:"妹妹", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"}
        ]
        }
    },
    { name:"花好月圆 ",sex:"男", age:"25", birthDate:"2000-01-01",first:true, status:false,
        monthIncome:"8000", yearIncome:"12", jobType:"数据分析员", jobCity:"南京", jobCompany:"南京巨好数据分析有限公司",jobStatus:"在职",
        images:[
            'https://gw.alipayobjects.com/zos/antfincdn/LlvErxo8H9/photo-1503185912284-5271ff81b9a8.webp',
            'https://gw.alipayobjects.com/zos/antfincdn/cV16ZqzMjW/photo-1473091540282-9b846e7965e3.webp',
            'https://gw.alipayobjects.com/zos/antfincdn/x43I27A55%26/photo-1438109491414-7198515b166b.webp',
                    ],
        cars:[
            {loan:"无贷款", address:"XXXX"},
            {loan:"无贷款", address:"XXXX"},
            {loan:"无贷款", address:"XXXX"},
        ], 
        houses:[
                {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
            {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
            {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
        ], 
        familySituation:{
            father:{name:"父亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            mother:{name:"母亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            brothers:[{name:"哥哥", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            {name:"妹妹", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"}
        ]
        }
    },
    { name:"花好月圆 ",sex:"男", age:"25", birthDate:"2000-01-01",first:true, status:false,
        monthIncome:"8000", yearIncome:"12", jobType:"数据分析员", jobCity:"南京", jobCompany:"南京巨好数据分析有限公司",jobStatus:"在职",
        images:[
            'https://gw.alipayobjects.com/zos/antfincdn/LlvErxo8H9/photo-1503185912284-5271ff81b9a8.webp',
            'https://gw.alipayobjects.com/zos/antfincdn/cV16ZqzMjW/photo-1473091540282-9b846e7965e3.webp',
            'https://gw.alipayobjects.com/zos/antfincdn/x43I27A55%26/photo-1438109491414-7198515b166b.webp',
                    ],
        cars:[
            {loan:"无贷款", address:"XXXX"},
            {loan:"无贷款", address:"XXXX"},
            {loan:"无贷款", address:"XXXX"},
        ], 
        houses:[
                {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
            {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
            {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
        ], 
        familySituation:{
            father:{name:"父亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            mother:{name:"母亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            brothers:[{name:"哥哥", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            {name:"妹妹", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"}
        ]
        }
    },
    { name:"花好月圆 ",sex:"男", age:"25", birthDate:"2000-01-01",first:true, status:false,
        monthIncome:"8000", yearIncome:"12", jobType:"数据分析员", jobCity:"南京", jobCompany:"南京巨好数据分析有限公司",jobStatus:"在职",
        images:[
            'https://gw.alipayobjects.com/zos/antfincdn/LlvErxo8H9/photo-1503185912284-5271ff81b9a8.webp',
            'https://gw.alipayobjects.com/zos/antfincdn/cV16ZqzMjW/photo-1473091540282-9b846e7965e3.webp',
            'https://gw.alipayobjects.com/zos/antfincdn/x43I27A55%26/photo-1438109491414-7198515b166b.webp',
                    ],
        cars:[
            {loan:"无贷款", address:"XXXX"},
            {loan:"无贷款", address:"XXXX"},
            {loan:"无贷款", address:"XXXX"},
        ], 
        houses:[
                {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
            {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
            {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
        ], 
        familySituation:{
            father:{name:"父亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            mother:{name:"母亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            brothers:[{name:"哥哥", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            {name:"妹妹", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"}
        ]
        }
    },
    { name:"花好月圆 ",sex:"男", age:"25", birthDate:"2000-01-01",first:true, status:false,
        monthIncome:"8000", yearIncome:"12", jobType:"数据分析员", jobCity:"南京", jobCompany:"南京巨好数据分析有限公司",jobStatus:"在职",
        images:[
            'https://gw.alipayobjects.com/zos/antfincdn/LlvErxo8H9/photo-1503185912284-5271ff81b9a8.webp',
            'https://gw.alipayobjects.com/zos/antfincdn/cV16ZqzMjW/photo-1473091540282-9b846e7965e3.webp',
            'https://gw.alipayobjects.com/zos/antfincdn/x43I27A55%26/photo-1438109491414-7198515b166b.webp',
                    ],
        cars:[
            {loan:"无贷款", address:"XXXX"},
            {loan:"无贷款", address:"XXXX"},
            {loan:"无贷款", address:"XXXX"},
        ], 
        houses:[
                {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
            {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
            {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
        ], 
        familySituation:{
            father:{name:"父亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            mother:{name:"母亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            brothers:[{name:"哥哥", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            {name:"妹妹", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"}
        ]
        }
    },
    { name:"花好月圆 ",sex:"男", age:"25", birthDate:"2000-01-01",first:true, status:false,
        monthIncome:"8000", yearIncome:"12", jobType:"数据分析员", jobCity:"南京", jobCompany:"南京巨好数据分析有限公司",jobStatus:"在职",
        images:[
            'https://gw.alipayobjects.com/zos/antfincdn/LlvErxo8H9/photo-1503185912284-5271ff81b9a8.webp',
            'https://gw.alipayobjects.com/zos/antfincdn/cV16ZqzMjW/photo-1473091540282-9b846e7965e3.webp',
            'https://gw.alipayobjects.com/zos/antfincdn/x43I27A55%26/photo-1438109491414-7198515b166b.webp',
            ],
        cars:[], 
        houses:[], 
        familySituation:{
            father:{name:"父亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            mother:{name:"母亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            brothers:[{name:"哥哥", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            {name:"妹妹", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"}
        ]
        }
    },
    { name:"花好月圆 ",sex:"男", age:"25", birthDate:"2000-01-01",first:true, status:false,
        monthIncome:"8000", yearIncome:"12", jobType:"数据分析员", jobCity:"南京", jobCompany:"南京巨好数据分析有限公司",jobStatus:"在职",
        images:[
            'https://gw.alipayobjects.com/zos/antfincdn/LlvErxo8H9/photo-1503185912284-5271ff81b9a8.webp',
            'https://gw.alipayobjects.com/zos/antfincdn/cV16ZqzMjW/photo-1473091540282-9b846e7965e3.webp',
            'https://gw.alipayobjects.com/zos/antfincdn/x43I27A55%26/photo-1438109491414-7198515b166b.webp',
                    ],
        cars:[
            {loan:"无贷款", address:"XXXX"},
            {loan:"无贷款", address:"XXXX"},
            {loan:"无贷款", address:"XXXX"},
        ], 
        houses:[
                {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
            {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
            {loan:"无贷款", address:"江苏省,宿迁市,沭阳县,东方现代城X栋X单元XXXX号"},
        ], 
        familySituation:{
            father:{name:"父亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            mother:{name:"母亲", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            brothers:[{name:"哥哥", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"},
            {name:"妹妹", maritalStatus:"已婚", jobStatus:"未退休", monthIncome:"10000", yearIncome:"12", jobType:"XXXXX",jobCity:"xxxxxxx", jobCompany:"xxxxxxxx"}
        ]
        }
    },
]
export default function ShowBaseInfo() {
    const desc_obj={
        "1":"极简模式: 显示更多的人员，人员只显示重要信息",
        "2":"普通模式: 显示人员相对较少，人员的信息相对较多",
        "3":"详情模式: 显示更少的人员，人员信息最多求全面",
    }

    const [desc, setDesc] = useState(desc_obj["1"])
    const [value, setValue] = useState("1")
    const handleChange = (value) => {
        console.log(`selected ${value}`);
        setDesc(desc_obj[value])
        setValue(value)
        debugger
    };

    const BaseInfoGroup=()=>{
        let groups = [], group = []
        for(let i=0; i<datas.length; i++){
            if (group.length === 2){
                groups.push(<div><Space>{group}</Space></div>)
                group = []
            }
            if(value === "1"){
                group.push(<MiniBaseInfo data={datas[i]} />)
            }else if(value === "2"){
                group.push(<PlainBaseInfo data={datas[i]} />)
            }else if(value === "3"){
                group.push(<DetailsBaseInfo data={datas[i]} />)
            }
        }
        if (group.length > 0) groups.push(<div><Space>{group}</Space></div>)
        return groups
    }
  return (
    <div >
        <Select style={{width: 200,}} 
        defaultValue="1"
        onChange={handleChange}
        options={[{value:"1", label:"极简模式"},{value:"2", label:"普通模式"},{value:"3", label:"详情模式", disabled:true},]} 
        />
        <span style={{paddingLeft:20}}>{desc}</span>
        <div style={{textAlign:"left"}}>
            {value==="1"&&BaseInfoGroup()}
            {value==="2"&&BaseInfoGroup()}
            {value==="3"&&BaseInfoGroup()}
        </div>
    </div>
  )
}
