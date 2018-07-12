FROM vevende/python3
RUN apt-get update \ 
 && apt-get install python3-dev libmysqlclient-dev \
 &&	pip install mysqlclient \
 &&	pip install numpy \
 && cd /home
COPY . /home

CMD ["python","manage.py","runserver"]