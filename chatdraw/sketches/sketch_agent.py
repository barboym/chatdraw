from chatdraw.sketches.tutorial_structure import LLMOutput
from llama_index.llms.anthropic import Anthropic
from llama_index.core.llms import ChatMessage

from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from opik.integrations.llama_index import LlamaIndexCallbackHandler

opik_callback_handler = LlamaIndexCallbackHandler(project_name="Sketching")
Settings.callback_manager = CallbackManager([opik_callback_handler])



llm = Anthropic(
    model='claude-sonnet-4-20250514', 
    max_tokens=3000,
    temperature=0,
).as_structured_llm(LLMOutput)
