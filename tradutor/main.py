import whisper
import sys
import subprocess
import os

def transcrever_audio_para_texto(caminho_do_video):
    model = whisper.load_model("small")
    resultado = model.transcribe(caminho_do_video)
    return resultado["segments"]

def formatar_tempo(segundos):
    ms = int((segundos - int(segundos)) * 1000)
    segundos = int(segundos)
    horas = segundos // 3600
    segundos %= 3600
    minutos = segundos // 60
    segundos %= 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d},{ms:03d}"

def gerar_srt(segments, caminho_arquivo_srt):
    with open(caminho_arquivo_srt, 'w', encoding='utf-8') as arquivo_srt:
        for i, segment in enumerate(segments, start=1):
            inicio = formatar_tempo(segment["start"])
            fim = formatar_tempo(segment["end"])
            texto = segment["text"]
            texto_traduzido = traduzir_texto(texto)
            arquivo_srt.write(f"{i}\n{inicio} --> {fim}\n{texto_traduzido}\n\n")

def traduzir_texto(texto):
    processo = subprocess.run(["trans", "-b", ":pt-BR", texto], capture_output=True, text=True, encoding='utf-8')
    return processo.stdout.strip()

def incorporar_legendas(caminho_do_video, caminho_arquivo_srt):
    caminho_video_saida = os.path.splitext(caminho_do_video)[0] + "_com_legendas.mp4"
    comando_ffmpeg = [
        "ffmpeg", "-i", caminho_do_video, "-vf", f"subtitles={caminho_arquivo_srt}",
        "-codec:a", "copy", caminho_video_saida
    ]
    subprocess.run(comando_ffmpeg)
    print(f"Vídeo com legendas gerado: {caminho_video_saida}")

def processar_videos_no_diretorio(diretorio, incorporar_legendas_opcao=False):
    for raiz, diretorios, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if arquivo.lower().endswith(('.mp4', '.avi', '.mkv')):
                caminho_completo = os.path.join(raiz, arquivo)
                print(f"Processando vídeo: {caminho_completo}")
                try:
                    segments = transcrever_audio_para_texto(caminho_completo)
                    nome_arquivo_srt_traduzido = os.path.splitext(caminho_completo)[0] + ".srt"
                    gerar_srt(segments, nome_arquivo_srt_traduzido)
                    print(f"Subtítulo traduzido gerado: {nome_arquivo_srt_traduzido}")
                    if incorporar_legendas_opcao:
                        incorporar_legendas(caminho_completo, nome_arquivo_srt_traduzido)
                except Exception as e:
                    print(f"Erro ao processar vídeo {caminho_completo}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_do_diretorio> [incorporar_legendas]")
        sys.exit(1)

    caminho = sys.argv[1]
    incorporar_legendas_opcao = len(sys.argv) > 2 and sys.argv[2].lower() == "true"
    if os.path.isdir(caminho):
        processar_videos_no_diretorio(caminho, incorporar_legendas_opcao)
    else:
        print("O caminho fornecido não é um diretório.")
