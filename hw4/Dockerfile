FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app/app.py .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "app.py"]