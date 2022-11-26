FROM python:3.9.15-slim-bullseye

LABEL maintainer="jiabh"

# 设置时区
ENV TZ="Asia/Shanghai"

WORKDIR /app

# apt换源+安装依赖
RUN sed -i s/deb.debian.org/mirrors.aliyun.com/g /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y netcat-openbsd && \
    apt-get clean

# pip依赖
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制运行相关文件
COPY . .
COPY docker.env .env


ENTRYPOINT ["bash"]
CMD ["./entrypoint.sh"]
