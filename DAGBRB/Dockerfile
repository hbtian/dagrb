# 使用官方的 Python 镜像作为基础镜像，指定版本号
FROM python:3.9

# 设置工作目录，这里使用 /app
WORKDIR /app

# 复制项目文件到容器的工作目录
COPY . /app

# 安装项目依赖，如果有 requirements.txt 文件的话
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y iproute2



