FROM python:3.8

COPY poetry.lock /
COPY pyproject.toml .
RUN pip install poetry==1.0.9 && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi && \
    rm -rf /var/cache/pypoetry

COPY . /

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]