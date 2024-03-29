from fastapi import BackgroundTasks, FastAPI, UploadFile, File, HTTPException
import shutil
import uuid
import os
from fastapi.responses import FileResponse
from Actions.translateActions.main import processar_videos_no_diretorio, transcrever_audio_para_texto, traduzir_texto, limpar_diretorio_temporario

app = FastAPI()

@app.post("/upload/")
async def create_upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...), incorporar: bool = False):
    temp_dir = f"temp/{str(uuid.uuid4())}/"
    try:
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = temp_dir + file.filename
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        processar_videos_no_diretorio(temp_dir, incorporar_legendas_opcao=incorporar)

        if incorporar:
            video_com_legendas = os.path.splitext(temp_file_path)[0] + "_com_legendas.mp4"
            response = FileResponse(path=video_com_legendas, filename=os.path.basename(video_com_legendas))
        else:
            arquivo_srt = os.path.splitext(temp_file_path)[0] + ".srt"
            response = FileResponse(path=arquivo_srt, filename=os.path.basename(arquivo_srt))

        # Adiciona a tarefa de limpeza para ser executada após a resposta
        background_tasks.add_task(limpar_diretorio_temporario, temp_dir)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/transcrever-audio-para-texto")
def api_transcrever_audio_para_texto(caminho_do_video: str):
    # Chama a função importada e retorna o resultado
    return transcrever_audio_para_texto(caminho_do_video)

@app.get("/traduzir-texto")
def api_traduzir_texto(texto: str):
    # Chama a função importada e retorna o resultado
    return traduzir_texto(texto)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# @app.get("/verificar-ffmpeg/")
# def verificar_ffmpeg():
#     resultado = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     return {"stdout": resultado.stdout, "stderr": resultado.stderr}

# @app.get("/verificar-translate/")
# def verificar_translate():
#     resultado = subprocess.run(["trans", "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     return {"stdout": resultado.stdout, "stderr": resultado.stderr}