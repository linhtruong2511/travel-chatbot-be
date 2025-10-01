# Sử dụng python slim để nhẹ
FROM python:3.11-slim

# Set env
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Tạo thư mục làm việc
WORKDIR /app

# Cài dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

EXPOSE 8000

# Migrate + runserver (chạy qua docker-compose command)
CMD python manage.py migrate  && gunicorn travel_chatbot_app.wsgi:application --bind 0.0.0.0:8000

#Dev
#CMD python manage.py runserver 0.0.0.0:8000