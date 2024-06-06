FROM python:3.10.6

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code

ADD . /code/


RUN pip install --upgrade pip
    

RUN pip install -r requirements.txt 


CMD python manage.py migrate \ 
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'root')" \
    && python manage.py runserver 0.0.0.0:8000




ENV SECRET_KEY=$SECRET_KEY 
