from typing import Literal, Optional

from pydantic import BaseModel


class SynthesizeQuery(BaseModel):
    lang: Literal['auto', 'zh', 'ja', 'en', 'mix'] = 'auto'
    text: str
    accent: Literal['中文', '日本語', 'English', 'Mix', 'no-accent'] = 'no-accent'
    prompt_name: Optional[str] = None

class SynthesizeQueryResult(BaseModel):
    base64_audio: str

class MakePromptQuery(BaseModel):
    prompt_name: str
    base64_audio: str
    transcript: Optional[str] = None

class MakePromptResult(BaseModel):
    result: Literal['success', 'failed']
    prompt_name: str