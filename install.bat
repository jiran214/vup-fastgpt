@echo off
REM 设置Python环境变量
set PATH=%PATH%;C:\Python27

REM 安装依赖
pip install package1
pip install package2
pip install package3
REM 更多的包...

REM 提示安装完成
echo Python依赖安装完成!
pause