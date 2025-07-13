FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

# Diretório de trabalho no container
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adiciona o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Copia os arquivos de dependência primeiro
COPY pyproject.toml poetry.lock ./

# Desativa venv isolada e instala dependências
RUN poetry config virtualenvs.create false && poetry install --no-root

WORKDIR /app

# Copia o restante da aplicação
COPY . .

WORKDIR /app/curso

# Expõe a porta do app

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Comando final: roda Gunicorn apontando para o WSGI dentro da pasta curso/
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

