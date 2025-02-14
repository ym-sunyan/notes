const {app, BrowserWindow, ipcMain, Menu} = require("electron")
let mainWin
// 创建窗口
function createWindow(){
  mainWin = new BrowserWindow({
    // x, y 设置窗口的显示位置，相对于屏幕的左上角
    x:50,
    y:50,

    //防止窗口加载和内容加载不同步导致的窗口短时间内白屏的情况
    //切记 一旦show设置为false窗口将不显示，需要使用ready-to-show主动触发显示
    //详见下面的 mainWin.on("ready-to-show"....
    show:false, 
    width:800, 
    height:400,

    // 窗口最大，最小尺寸的设置
    maxWidth:1000, 
    maxHeight:600,
    minWidth:200,
    minHeight:300,

    // resizable:false, //设置属性设置为false之后，则不允许修改窗口尺寸的大小

    title:"在主进程中修改窗口title，但是需要将index.html的title去除才可以",
    // icon:"", 修改窗口左上角的图标
    // frame:false, //false时，窗口将不显示标题和菜单栏只有纯窗口，且无法被拖动
    transparent:false, //true窗体为透明，参数没有效果！！！！
    // autoHideMenuBar:true, //true 隐藏默认的菜单

    webPreferences:{
      nodeIntegration:true, //允许渲染进程使用node
      contextIsolation: false, // 关闭上下文隔离，但是关闭是不安全的
    }
  })

  // 自定义菜单
  let menuTemp = [
    {label:"文件",
      submenu:[
        {
          label:"打开文件",
          click(){
            console.log("测试打开文件")
          }
        },
        {label:"关闭文件"},
        {type:"separator"},  //添加分割符
        {
          label:"关于",
          role:"about" //预定义值，详情见electron官网中的菜单部分
        },
      ]
    },
    {label:"编辑"},
    {
      label:"角色",
      submenu:[
        {label:"复制", role:"copy"},
        {label:"剪切", role:"cut"},
        {label:"粘贴", role:"paste"},
        {type:"separator"},  //添加分割符
        {label:"最小化", role:"minimize"},
      ]
    },
    {
      label:"类型",
      submenu:[
        {label:"选项1", type:"checkbox"},
        {label:"选项2", type:"checkbox"},
        {label:"选项3", type:"checkbox"},
        {type:"separator"},  //添加分割符
        {label:"item1", type:"radio"},
        {label:"item2", type:"radio"},
        {label:"item3", type:"radio"},
        {type:"separator"},  //添加分割符
        {label:"windows", type:"submenu",role:"windowMenu"},
      ]
    },
    {
      label:"其他",
      submenu:[
        {
          label:"打开", 
          icon:"", 
          accelerator:"ctrl + o",

          click(){
            console.log("open 操作")
          }
        },
        
      ]
    },
  ]

  // 利用上述的模板生成菜单项
  let menu = Menu.buildFromTemplate(menuTemp)

  // autoHideMenuBar:true, //属性需要关闭或者设置为 false
  // 将上述的自定义菜单添加到应用里
  Menu.setApplicationMenu(menu)


  mainWin.loadFile("index.html")

  // show:false 需要捕捉 ready-to-show 主动显示
  mainWin.on("ready-to-show", ()=>{
    mainWin.show()
  })

  mainWin.webContents.on("did-finish-load",()=>{
    console.log("3333 -> did-finish-load")
  })

  mainWin.webContents.on("dom-ready", ()=>{
    console.log("2222 -> dom-ready")
  })

  mainWin.on("close", ()=>{
    console.log("8888 -> this window is clonsed")
    mainWin = null
  })

  // 打开开发者工具
  mainWin.webContents.openDevTools()
}

app.on("ready", ()=>{
  console.log("1111 -> ready")
  createWindow()
})

app.on("window-all-closed", ()=>{
  console.log("4444 -> window-all-closed")
  app.quit()
})

app.on("before-quit", ()=>{
  console.log("5555 -> before-quit")
})

app.on("will-quit", ()=>{
  console.log("6666 -> will-quit")
})

app.on("quit",()=>{
  console.log("7777 -> quit")
})

ipcMain.on("open-new-window",(event, arg)=>{
  let newWindow = new BrowserWindow({
    parent:mainWin, //指定父窗口，此时可以通过父窗口按钮创建多个子窗口，父窗口和子窗口都可以独立操作
    modal:true,   //指定模式为模态窗口，则只能创建一个子窗口，并且此时父窗口不可以操作
    width: 400,
    height: 300
  })
  newWindow.loadFile("test.html")
  newWindow.on("closed",()=>{
    // newWindow.quit()
    newWindow = null
  })
})
ipcMain.on("click",(event, arg)=>{
  console.log(event)
  console.log(arg)
  if (arg === "close_btn"){
    app.quit()
  }else if(arg === "max_btn"){
    console.log("max_btn")
    event.sender.send("msg_click","这是来自主进程的异步消息")
    if (! mainWin.isMaximized()){
      mainWin.maximize()
    }else{
      mainWin.restore()
    }
  }else if(arg === "min_btn"){
    console.log("max_btn")
    mainWin.minimize()
  }
  console.log("渲染进程发送的请求")
})

// 处理右键菜单的 IPC 消息
ipcMain.on('show-context-menu', (event) => {
  const template = [
    { label: '复制', role: 'copy' },
    { label: '粘贴', role: 'paste' },
    { type: 'separator' },
    { label: '自定义操作', click: () => { console.log('自定义操作') } }
  ]
  const menu = Menu.buildFromTemplate(template)
  menu.popup(BrowserWindow.fromWebContents(event.sender))
})