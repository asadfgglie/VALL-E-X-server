import base64
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
import os
os.chdir(os.getcwd() + '/vall_e_x')
import time

import numpy as np
import uvicorn
from fastapi import FastAPI
from scipy.io.wavfile import write

from schemas import SynthesizeQuery, SynthesizeQueryResult
from vall_e_x.utils.generation import generate_audio, SAMPLE_RATE, generate_audio_from_long_text, preload_models

app = FastAPI()

@app.get("/")
def hello_world():
    return "This is a vall-e-x server."

@app.post('/synthesize', response_model=SynthesizeQueryResult)
def synthesize(query: SynthesizeQuery):
    t1 = time.time()
    data = (generate_audio(query.text, query.prompt, query.lang, query.accent) * 32767).astype(np.int16)
    write('output.wav', SAMPLE_RATE, data)
    logging.info(f'Time cost: {time.time() - t1}')
    with open('output.wav', 'rb') as f:
        return dict(base64_data=base64.b64encode(f.read()).decode())

@app.post('/synthesize_long', response_model=SynthesizeQueryResult)
def synthesize_long(query: SynthesizeQuery):
    t1 = time.time()
    data = (generate_audio_from_long_text(query.text, query.prompt, query.lang, query.accent) * 32767).astype(np.int16)
    write('output.wav', SAMPLE_RATE, data)
    logging.info(f'Time cost: {time.time() - t1}')
    with open('output.wav', 'rb') as f:
        return dict(base64_data=base64.b64encode(f.read()).decode())

if __name__ == "__main__":
    logging.info('Loading model...')
    preload_models()
    logging.info('model loaded done.')
    uvicorn.run(app, host="0.0.0.0")