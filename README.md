# Documentação do Transcritor e Incorporador de Legendas

Este projeto automatiza o processo de transcrição de áudio de vídeos para texto, tradução desses textos para o português, geração de arquivos de legendas no formato `.srt`, e a opção de incorporar essas legendas diretamente nos vídeos. O script suporta uma variedade de formatos de vídeo, incluindo `.mp4`, `.avi`, e `.mkv`.

## Pré-requisitos

Antes de utilizar o script, é necessário preparar o ambiente com as seguintes dependências:

### Python

O script é escrito para Python 3.8 ou superior. Se não tiver o Python instalado, você pode baixá-lo e instalá-lo do [site oficial do Python](https://www.python.org/downloads/).

### FFmpeg

FFmpeg é uma ferramenta gratuita e de código aberto essencial para processar os vídeos. É usado aqui para incorporar as legendas nos vídeos. Siga os passos abaixo para instalá-lo:

#### Windows:

1. Baixe o FFmpeg do [site oficial do FFmpeg](https://ffmpeg.org/download.html).
2. Extraia o arquivo baixado em uma pasta de sua escolha.
3. Adicione a pasta `bin` dentro da pasta extraída ao PATH do sistema:
   - Pesquise por "Editar as variáveis de ambiente do sistema" no menu Iniciar.
   - Clique em "Variáveis de Ambiente".
   - Na seção "Variáveis do Sistema", encontre e selecione a variável `Path` e clique em "Editar".
   - Clique em "Novo" e adicione o caminho para a pasta `bin` do FFmpeg.
   - Clique em "OK" para fechar todas as janelas.

#### Linux:

Em sistemas baseados em Debian (como Ubuntu), você pode instalar o FFmpeg usando o seguinte comando:

```bash
sudo apt update && sudo apt install ffmpeg
```

#### macOS:

Você pode instalar o FFmpeg usando o [Homebrew](https://brew.sh/) com o comando:

```bash
brew install ffmpeg
```

### Translate-Shell

Translate-Shell é um tradutor de linha de comando que o script usa para traduzir os textos. Instale-o conforme abaixo:

#### Linux (Debian-based):

```bash
sudo apt-get install translate-shell
```

#### Outros sistemas:

Veja as instruções específicas para seu sistema operacional na [página do GitHub do Translate-Shell](https://github.com/soimort/translate-shell).

### Dependências do Python

O projeto utiliza o Poetry para gerenciar as dependências do Python. Instale o Poetry seguindo as instruções na [documentação oficial do Poetry](https://python-poetry.org/docs/#installation).

Após a instalação do Poetry, navegue até o diretório do projeto e execute o comando abaixo para instalar as dependências do Python:

```bash
poetry install
```

## Uso

### Transcrição e Tradução de Legendas

Para transcrever e traduzir legendas sem incorporá-las nos vídeos, execute:

```bash
python main.py "caminho_do_diretorio"
```

O script processará todos os arquivos de vídeo no diretório especificado, gerando arquivos `.srt` com as legendas traduzidas para o português.

### Incorporação de Legendas nos Vídeos

Para incorporar as legendas traduzidas diretamente nos vídeos:

```bash
python main.py "caminho_do_diretorio" true
```

Isso gerará uma cópia de cada vídeo com as legendas incorporadas, mantendo os arquivos originais inalterados. Os vídeos modificados terão `_com_legendas` adicionado ao seu nome.

## Estrutura do Script

O script é composto por várias funções chave, como `transcrever_audio_para_texto` para a transcrição do áudio, `formatar_tempo` para formatar os tempos de início e fim dos segmentos transcritos, `gerar_srt` para gerar o arquivo de legendas, `traduzir_texto` para a tradução, `incorporar_legendas` para adicionar as legendas ao vídeo, e `processar_videos_no_diretorio` para processar todos os vídeos em um diretório.

## Notas Finais

- Verifique se os caminhos dos diretórios e arquivos não contêm espaços ou caracteres especiais que possam ser mal interpretados pelo seu sistema operacional.
- O processo de transcrição, tradução e incorporação de

 legendas pode ser demorado, dependendo do tamanho e da quantidade de vídeos processados.

Para problemas na instalação de dependências ou execução do script, consulte as documentações oficiais das ferramentas e bibliotecas mencionadas.


---

# Documentação da API de Transcrição e Incorporação de Legendas

Esta seção documenta a extensão do projeto anterior para incluir uma API construída com FastAPI, permitindo o upload de vídeos para transcrição, tradução, e opcionalmente, a incorporação de legendas. Além disso, detalha a configuração necessária para executar a aplicação em um container Docker.

## API com FastAPI

A API fornece endpoints para upload de vídeos e execução das funcionalidades de transcrição e tradução de forma assíncrona, com a opção de retornar o vídeo com legendas incorporadas ou apenas o arquivo de legendas.

### Endpoints da API

- `POST /upload/`: Recebe um arquivo de vídeo e uma flag opcional `incorporar`. Se `incorporar` for verdadeiro, o vídeo com legendas incorporadas será retornado. Caso contrário, apenas o arquivo de legendas será retornado.
- `GET /transcrever-audio-para-texto`: Recebe o caminho de um vídeo e retorna a transcrição do áudio em texto.
- `GET /traduzir-texto`: Recebe um texto e retorna o texto traduzido.

### Uso

Para fazer upload de um vídeo e obter o arquivo de legendas:

```curl
curl -X 'POST' \
  'http://localhost:8000/upload/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@caminho_do_seu_video;type=video/mp4'
```

Para incorporar legendas no vídeo:

```curl
curl -X 'POST' \
  'http://localhost:8000/upload/?incorporar=true' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@caminho_do_seu_video;type=video/mp4'
```

## Docker

A aplicação pode ser executada em um container Docker, facilitando a configuração e execução do ambiente.

### Dockerfile

O `Dockerfile` incluído configura o ambiente necessário, instala dependências e prepara a aplicação para ser executada dentro do container.

### Docker Compose

Um arquivo `docker-compose.yml` é fornecido para facilitar a construção e execução da aplicação em containers Docker. Ele configura o serviço `app` para ser construído com base no `Dockerfile` e expõe a porta 8000 para acesso à API.

### Executando a Aplicação com Docker

Para construir a imagem e iniciar o serviço:

```bash
docker-compose up --build
```

A API estará acessível em `http://localhost:8000`.

## Notas Importantes

- A API utiliza diretórios temporários para processar os vídeos. Esses diretórios são limpos após a conclusão das tarefas.
- As funcionalidades de verificação de FFmpeg e Translate-Shell estão comentadas, mas podem ser habilitadas para diagnóstico.
- Assegure-se de que o Docker e o Docker Compose estejam instalados em seu sistema para utilizar a aplicação em um ambiente containerizado.

Esta documentação complementa a seção anterior, fornecendo instruções para a utilização da API e execução da aplicação via Docker, oferecendo uma interface flexível e acessível para transcrição, tradução, e incorporação de legendas em vídeos.

Créditos: Marcelo programador
Github: [link](https://github.com/MarceloFullStack)