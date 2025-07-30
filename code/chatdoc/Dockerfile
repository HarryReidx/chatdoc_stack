FROM python:3.9

RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone

RUN mkdir -p "/app"
RUN mkdir -p /data/parse/catalog /data/parse/doc-paser /data/parse/extract /data/file /data/parse/structure /data/parse/title

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /app
ENTRYPOINT ["python", "main.py"]