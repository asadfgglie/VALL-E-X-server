from pathlib import Path
from typing import Literal, Union

from pydantic import BaseModel


class SynthesizeQuery(BaseModel):
    lang: Literal['auto', 'zh', 'ja', 'en', 'mix'] = 'auto'
    text: str
    accent: Literal['zh', 'ja', 'en', 'no-accent'] = 'no-accent'
    prompt: Union[Path, str, None] = None

class SynthesizeQueryResult(BaseModel):
    base64_data: str