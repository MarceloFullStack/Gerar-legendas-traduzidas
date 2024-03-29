# import whisper
# import sys

# def transcrever_audio_para_texto(caminho_do_video):
#     model = whisper.load_model("base")
#     resultado = model.transcribe(caminho_do_video)
#     return resultado["text"]

# def gerar_srt(texto_transcrito, nome_arquivo_srt):
#     with open(nome_arquivo_srt, 'w') as arquivo_srt:
#         # Dividindo o texto em partes para simular legendas
#         partes = texto_transcrito.split('. ')
#         inicio = 0
#         for i, parte in enumerate(partes, start=1):
#             inicio_str = f"00:00:{inicio:02d},000"
#             fim_str = f"00:00:{inicio + 5:02d},000"  # Asumindo cada parte com duração de 5 segundos
#             arquivo_srt.write(f"{i}\n{inicio_str} --> {fim_str}\n{parte}\n\n")
#             inicio += 6  # Aumentando o início para a próxima parte

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Uso: python main.py <caminho_do_video>")
#         sys.exit(1)
    
#     caminho_do_video = sys.argv[1]
#     texto_transcrito = transcrever_audio_para_texto(caminho_do_video)
#     nome_arquivo_srt = "subtitulo.srt"
#     gerar_srt(texto_transcrito, nome_arquivo_srt)
#     print(f"Subtítulo gerado: {nome_arquivo_srt}")

import whisper
import sys
import subprocess

def transcrever_audio_para_texto(caminho_do_video):
    model = whisper.load_model("base")
    resultado = model.transcribe(caminho_do_video)
    return resultado["segments"]

def formatar_tempo(segundos):
    """ Formata o tempo em horas, minutos, segundos e milissegundos para SRT. """
    ms = int((segundos - int(segundos)) * 1000)
    segundos = int(segundos)
    horas = segundos // 3600
    segundos %= 3600
    minutos = segundos // 60
    segundos %= 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d},{ms:03d}"

def gerar_srt(segments, nome_arquivo_srt):
    with open(nome_arquivo_srt, 'w', encoding='utf-8') as arquivo_srt:
        for i, segment in enumerate(segments, start=1):
            inicio = formatar_tempo(segment["start"])
            fim = formatar_tempo(segment["end"])
            texto = segment["text"]
            texto_traduzido = traduzir_texto(texto)
            arquivo_srt.write(f"{i}\n{inicio} --> {fim}\n{texto_traduzido}\n\n")

def traduzir_texto(texto):
    """ Traduz texto do inglês para português usando o translate-shell. """
    processo = subprocess.run(["trans", "-b", ":pt", texto], capture_output=True, text=True, encoding='utf-8')
    return processo.stdout.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_do_video>")
        sys.exit(1)

    caminho_do_video = sys.argv[1]
    segments = transcrever_audio_para_texto(caminho_do_video)
    nome_arquivo_srt_traduzido = "subtitulo_traduzido.srt"
    gerar_srt(segments, nome_arquivo_srt_traduzido)
    print(f"Subtítulo traduzido gerado: {nome_arquivo_srt_traduzido}")

