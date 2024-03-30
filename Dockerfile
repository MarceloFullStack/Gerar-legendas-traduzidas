# Use uma imagem base que permite a instalação de novos pacotes.
FROM python:3.12-slim

# Define o diretório de trabalho no container.
WORKDIR /app

# Copia o conteúdo do diretório atual para o diretório de trabalho no container.
COPY . /app

# Atualiza os pacotes e instala wget, ffmpeg, gawk, curl e bsdmainutils (para hexdump).
RUN apt-get update && \
    apt-get install -y ffmpeg gawk wget curl bsdmainutils

# Baixa e instala o translate-shell.
RUN wget git.io/trans -O /usr/local/bin/trans && \
    chmod +x /usr/local/bin/trans

# Instala o Poetry para gerenciamento de dependências do Python.
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

RUN poetry install --no-dev


# Define o comando padrão para executar a aplicação usando Uvicorn.
CMD poetry run uvicorn .App.main_api:app --host 0.0.0.0 --port 8000

# CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000"]
