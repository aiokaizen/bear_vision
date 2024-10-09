FROM python:3.10

RUN pip install --upgrade pip

WORKDIR /bear_vision

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Define environment variable for the container.
ENV PORT=8000
EXPOSE 8000

RUN python manage.py migrate --no-input
RUN python manage.py collectstatic --no-input
RUN python manage.py light_setup

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
