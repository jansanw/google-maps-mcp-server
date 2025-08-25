FROM docker.1ms.run/python:3.11.13

ENV TZ=Asia/Shanghai
ENV FASTMCP_TRANSPORT=streamable-http

#RUN apt-get update && \
#         DEBIAN_FRONTEND="noninteractive" \
#         apt-get install -y --no-install-recommends \
#         build-essential \
#         cmake && \
#         apt-get autoremove -y && \
#         apt-get clean -y && \
#    rm -rf /var/lib/apt/lists/*

# 设置pip镜像源
# RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN python -m pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /app
COPY ./ /app

CMD ["python", "server.py"]