from typing import Literal, Optional

from pydantic import BaseModel, Field

class QueryResult(BaseModel):
    result: Literal['success', 'failed'] = Field(default='success')
    detail: Optional[str] = Field(default=None,
    description='When result is failed, it will show the detail, otherwise this will be null.')

class SynthesizeQuery(BaseModel):
    lang: Literal['auto', 'zh', 'ja', 'en', 'mix'] = Field(default='auto', examples=['en'])
    text: str = Field(examples=['Hello, my name is Toku Lili!'])
    accent: Literal['中文', '日本語', 'English', 'Mix', 'no-accent'] = Field(default='no-accent', examples=['English'])
    prompt_name: Optional[str] = Field(default=None, examples=[None])

class SynthesizeLongQuery(SynthesizeQuery):
    mode: Literal['sliding-window', 'fixed-prompt'] = Field(default='sliding-window', examples=['sliding-window'],
    description="""
    For long audio generation, two modes are available.
    * fixed-prompt: This mode will keep using the same prompt the user has provided, and generate audio sentence by sentence.
    * sliding-window: This mode will use the last sentence as the prompt for the next sentence, but has some concern on speaker maintenance.
    """)

class SynthesizeQueryResult(QueryResult):
    base64_audio: Optional[str] = Field(default=None)

class MakePromptQuery(BaseModel):
    prompt_name: str = Field(examples=['test'])
    base64_audio: str
    transcript: Optional[str] = Field(default=None,
    description="If doesn't provide, it will use whisper to transcript prompt audio.")

class MakePromptResult(QueryResult):
    prompt_name: Optional[str] = Field(default=None)