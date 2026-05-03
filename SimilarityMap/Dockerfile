FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python -m compileall .

ENTRYPOINT ["python", "main.py"]
CMD ["--method", "umap"]