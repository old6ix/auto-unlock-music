#!/bin/bash

# 检查Selenium服务是否成功启动
while ! `nc -z selenium-server 4444`; do sleep 3; done

python main.py
