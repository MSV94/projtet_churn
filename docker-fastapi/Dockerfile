FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY ./api /api
WORKDIR /api/
EXPOSE 8000
CMD ["uvicorn", "application_churn_v2:api", "--host", "0.0.0.0", "--port", "8000"]
