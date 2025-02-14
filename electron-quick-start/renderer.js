/**
 * This file is loaded via the <script> tag in the index.html file and will
 * be executed in the renderer process for that window. No Node.js APIs are
 * available in this process because `nodeIntegration` is turned off and
 * `contextIsolation` is turned on. Use the contextBridge API in `preload.js`
 * to expose Node.js functionality from the main process.
 */
const {ipcRenderer} = require("electron")

window.addEventListener("DOMContentLoaded",()=>{
    let btn = document.getElementById("btn")
    btn.addEventListener("click",()=>{
        ipcRenderer.send("open-new-window")
    })

    let close_btn = document.getElementById("close_btn")
    close_btn.addEventListener("click",()=>{
        ipcRenderer.send("click","close_btn")
    })
    let max_btn = document.getElementById("max_btn")
    max_btn.addEventListener("click",()=>{
        ipcRenderer.send("click","max_btn")
    })
    let min_btn = document.getElementById("min_btn")
    min_btn.addEventListener("click",()=>{
        ipcRenderer.send("click","min_btn")
    })
})

window.addEventListener('contextmenu', (event) => {
    event.preventDefault()
    ipcRenderer.send('show-context-menu')
})

window.onload=function(){
    ipcRenderer.on("msg_click",(event, data)=>{
        console.log(data)
    })

    let send = document.getElementById("send")
    send.addEventListener("click",()=>{
        ipcRenderer.sendSync("sendSync", "发送同步消息")
    })
}