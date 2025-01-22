@echo off
    @REM FormatXlsmToHtml

@echo off
@REM 本套程序首次在新电脑上执行的时候 执行以下代码 *****开始*****
rem 设置虚拟环境名称
set "venv_name=vent1"

rem 设置需要安装的库
set "libraries=-r pip_list.txt"

rem 判断是否存在虚拟环境
if exist %venv_name% (
    echo Virtual environment already exists. Exiting...
) else (
    echo Creating virtual environment...
    python -m venv %venv_name%
    rem 激活虚拟环境
    echo Activating virtual environment...
    call %venv_name%\Scripts\activate
    rem 安装相关库
    echo Installing libraries...
    pip install %libraries%
    echo Process completed.
)
@REM 本套程序首次在新电脑上执行的时候 执行以下代码 *****结束*****



@REM start /MIN "FormatXlsmToHtml" "%~dp0vent\Scripts\python.exe" "%~dp0FormatXlsmToHtml.py"
"%~dp0vent\Scripts\python.exe" "%~dp0FormatXlsmToHtml.py"
@REM echo "FormatXlsmToHtml" "%~dp0vent\Scripts\python.exe"
@REM echo 输入任意键退出...
@REM pause > nul
exit