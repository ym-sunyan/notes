
@REM 进入项目文件夹
cd %~dp0%

@REM 创建python虚拟环境
python -m venv venv 

@REM 激活python虚拟环境
call venv\Scripts\activate
@REM 切换虚拟环境
@REM •	在Windows上：.\venv\Scripts\activate
@REM •	在macOS或Linux上：source venv/bin/activate

@REM @REM 更新pip
@REM @REM python.exe -m pip install --upgrade pip  >nul  2>nul
@REM python.exe -m pip install --upgrade pip

@REM 安装项目需要的基础库
:: pip install -r pip_flask_list.txt >nul  2>nul
:: 在【pip install -r pip_flask_list.txt >nul  2>nul】这个命令中：
:: >nul重定向标准输出（STDOUT）到nul设备，这样就不会显示标准输出。
:: 2>nul重定向标准错误（STDERR）到nul设备，这样就不会显示警告或错误信息。
:: 请注意，这样做会隐藏所有的标准输出和错误信息，包括成功的安装信息和可能的错误信息。
:: 如果你希望在安装过程中保留这些信息，你可能需要考虑其他方法，
:: 如在安装之前检查pip的版本并决定是否升级它
pip install -r pip_flask_list.txt

@REM 初始化db
flask db init

flask db migrate

flask db upgrade

@REM 启动项目
python app.py