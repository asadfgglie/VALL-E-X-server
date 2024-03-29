import base64
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
import os
os.chdir(os.getcwd() + '/vall_e_x')
import time

import numpy as np
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from scipy.io.wavfile import write

from schemas import SynthesizeQuery, SynthesizeQueryResult, MakePromptQuery, MakePromptResult, SynthesizeLongQuery
from vall_e_x.utils.generation import generate_audio, SAMPLE_RATE, generate_audio_from_long_text, preload_models
from vall_e_x.utils.prompt_making import make_prompt as mpt

app = FastAPI()
TMP_DIR = Path('../tmp')
TMP_AUDIO = TMP_DIR / 'audio.wav'

@app.get("/")
def hello_world():
    return "This is a vall-e-x server."

@app.post('/synthesize', response_model=SynthesizeQueryResult)
def synthesize(query: SynthesizeQuery):
    try:
        t1 = time.time()
        data = (generate_audio(query.text, query.prompt_name, query.lang, query.accent) * 32767).astype(np.int16)
        write('output.wav', SAMPLE_RATE, data)
        logging.info(f'Time cost: {time.time() - t1}')
        return FileResponse('output.wav')
    except Exception as e:
        return SynthesizeQueryResult(result='failed', detail=str(e))

@app.post('/synthesize_long', response_model=SynthesizeQueryResult)
def synthesize_long(query: SynthesizeLongQuery):
    try:
        t1 = time.time()
        data = (generate_audio_from_long_text(query.text, query.prompt_name, query.lang, query.accent, query.mode) * 32767).astype(np.int16)
        write('output.wav', SAMPLE_RATE, data)
        logging.info(f'Time cost: {time.time() - t1}')
        return FileResponse('output.wav')
    except Exception as e:
        return SynthesizeQueryResult(result='failed', detail=str(e))

@app.post('/make_prompt', response_model=MakePromptResult)
def make_prompt(query: MakePromptQuery):
    try:
        os.makedirs(TMP_DIR, exist_ok=True)
        with open(TMP_AUDIO, 'wb') as f:
            f.write(base64.b64decode(query.base64_audio))

        mpt(query.prompt_name, TMP_AUDIO, query.transcript)
        return MakePromptResult(prompt_name=query.prompt_name)
    except Exception as e:
        return MakePromptResult(result='failed', detail=str(e))

if __name__ == "__main__":
    logging.info('Loading model...')
    preload_models()
    logging.info('model loaded done.')
    uvicorn.run(app, host="0.0.0.0", port=6666)