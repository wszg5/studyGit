FROM python:2.7.11

ENV TZ "Asia/Shanghai"

RUN pip install -i https://pypi.douban.com/simple/ rethinkpool 
RUN pip install -i https://pypi.douban.com/simple/ rethinkdb 
RUN pip install -i https://pypi.douban.com/simple/ requests 
RUN pip install -i https://pypi.douban.com/simple/ redis
RUN pip install -i https://pypi.douban.com/simple/ pillow
RUN pip install -i https://pypi.douban.com/simple/ six



# Work in app dir by default.
WORKDIR /app

COPY . /app

RUN rm -rf /app/modules
RUN rm -rf /app/plugins

ENV ANDROID_HOME /app/adb/
ENV PATH /app:$PATH

# Export default app port, not enough for all processes but it should do
# for now.
USER root
ENTRYPOINT ["python","MainTask.py"] 
CMD [""]  





