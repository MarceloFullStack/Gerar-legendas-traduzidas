import whisper
import sys
import subprocess
import tempfile

def transcrever_audio_para_texto(caminho_do_video):
    model = whisper.load_model("base", FP16=False)
    resultado = model.transcribe(caminho_do_video)
    return resultado["segments"]

def formatar_tempo(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos = int(segundos % 60)
    milissegundos = int((segundos % 1) * 1000)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d},{milissegundos:03d}"

def traduzir_texto(texto):
    processo = subprocess.run(["trans", "-b", ":pt", texto], capture_output=True, text=True, encoding='utf-8')
    return processo.stdout.strip()

def gerar_srt(segments, nome_arquivo_srt):
    with open(nome_arquivo_srt, 'w', encoding='utf-8') as arquivo_srt:
        for i, segment in enumerate(segments, start=1):
            inicio = formatar_tempo(segment["start"])
            fim = formatar_tempo(segment["end"])
            texto = segment["text"]
            texto_traduzido = traduzir_texto(texto)
            arquivo_srt.write(f"{i}\n{inicio} --> {fim}\n{texto_traduzido}\n\n")

def sintetizar_audio_de_srt(nome_arquivo_srt, nome_arquivo_audio):
    with open(nome_arquivo_srt, 'r', encoding='utf-8') as arquivo_srt:
        texto = arquivo_srt.read()
    linhas_de_texto = [linha for linha in texto.split('\n') if linha and not linha.isdigit() and '-->' not in linha]
    texto_limpo = ' '.join(linhas_de_texto)
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as tmp_file:
        tmp_file.write(texto_limpo)
        tmp_file.flush()
        subprocess.run(['gtts-cli', '-f', tmp_file.name, '-l', 'pt', '-o', nome_arquivo_audio])

def adicionar_audio_ao_video(caminho_do_video, caminho_do_audio, caminho_do_video_final):
    subprocess.run(['ffmpeg', '-i', caminho_do_video, '-i', caminho_do_audio, '-c:v', 'copy', '-map', '0:v:0', '-map', '1:a:0', '-shortest', caminho_do_video_final])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_do_video>")
        sys.exit(1)
    
    caminho_do_video = sys.argv[1]
    segments = transcrever_audio_para_texto(caminho_do_video)
    nome_arquivo_srt = "subtitulo_traduzido.srt"
    gerar_srt(segments, nome_arquivo_srt)
    
    nome_arquivo_audio = "audio_traduzido.mp3"
    sintetizar_audio_de_srt(nome_arquivo_srt, nome_arquivo_audio)
    
    caminho_do_video_final = "video_final.mp4"
    adicionar_audio_ao_video(caminho_do_video, nome_arquivo_audio, caminho_do_video_final)
    
    print(f"Vídeo com áudio traduzido: {caminho_do_video_final}")
