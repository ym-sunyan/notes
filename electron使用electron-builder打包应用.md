# 打包electron应用
## 安装打包组件
npm install electron-builder -D
## electron-builder的优劣
### 优势
    跨平台支持：
        electron-builder 支持 Windows、macOS 和 Linux 平台的打包1，使得开发者可以轻松地为不同操作系统创建安装包。
    自动更新：
        内置自动更新功能，支持应用程序的自动更新1，减少了用户手动更新的麻烦。
    配置灵活：
        提供丰富的配置选项，可以通过 package.json 或独立的配置文件进行详细配置2，满足不同项目的需求。
    集成度高：
        与 Electron 项目无缝集成，支持常见的打包格式（如 NSIS、DMG、AppImage 等）2，简化了打包流程。
    社区支持：
        拥有活跃的社区和丰富的文档资源，开发者可以方便地找到解决方案和最佳实践2。
### 劣势
    打包体积大：
        由于 Electron 应用包含完整的 Chromium 和 Node.js，打包后的应用体积较大3，可能会影响下载和安装速度。
    学习曲线：
        对于初学者来说，配置和使用 electron-builder 可能需要一定的学习时间2，特别是涉及到复杂的配置选项时。
    性能问题：
        Electron 应用在性能上可能不如原生应用，特别是在资源受限的设备上3。
    依赖管理：
        需要管理大量的依赖库，可能会导致依赖冲突或版本兼容性问题3。
## 配置electron应用的package.json

    package.json 调整如下：
    "scripts": {
            ...
            "build": "electron-builder"
            ...
        },
        ...
        "build": {
            "appId": "com.yourcompany.yourapp", //应用的唯一标识
            <!-- 打包windows平台的安装包的具体配置 -->
            "win": {
                "icon": "build/icon.ico",//应用图标
                "target": [
                    {
                        "target":"nsis", //指定使用nsis作为安装程序的格式。windows的另一种是msi安装程序格式
                        "arch":["x64"] //生成64位安装包
                    }
                ]
            },
            "nsis": {
                "oneClick": false, // 设置为false 使安装程序显示安装向导界面，而不是一键安装
                "perMachine": true, //允许没太机器安装一次，而不是每个用户都安装
                "allowToChangeInstallationDirectory": true, //允许用户在安装过程中选择安装目录
            }
            ...
    
        },
        
# 执行打包
    npm run build
# 打包结果
    在应用的当前目录下生成 dist 文件夹
    dist内的xxxx.exe就是安装文件，独立拿到相应的平台就可以安装使用。
