// 控制应用生命周期和创建原生浏览器窗口的模块
const { app, BrowserWindow } = require('electron')
const path = require('node:path')

function createWindow () {
  // 创建浏览器窗口
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })

  //加载应用的 index.html。 界面中显示的具体内容
  mainWindow.loadFile('index.html')

  // 打开开发者工具
  // mainWindow.webContents.openDevTools()
}

// 当 Electron 完成初始化并准备创建浏览器窗口时调用此方法
// 一些 API 只能在此事件发生后使用
app.whenReady().then(() => {
  createWindow()

  app.on('activate', function () {
    // 在 macOS 上，当点击 dock 图标并且没有其他窗口打开时，
    // 通常会重新创建一个窗口
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// 当所有窗口关闭时退出应用，除非在 macOS 上
// 在 macOS 上，应用及其菜单栏通常会保持活动状态，直到用户按 Cmd + Q 显式退出
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

// 在此文件中可以包含应用程序的其他主进程代码
// 你也可以将它们放在单独的文件中并在这里导入