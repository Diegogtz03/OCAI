import google.generativeai as genai
from collections.abc import Iterable
from google.generativeai.types import content_types
from google.generativeai.types import generation_types
from google.generativeai import protos
from google.generativeai.types import helper_types
from google.generativeai.types import safety_types


_USER_ROLE = "user"
_MODEL_ROLE = "model"

class modelOCAI(genai.GenerativeModel):
    def _init_(self, model_name, system_instruction=None):
        super()._init_(model_name=model_name, system_instruction=system_instruction)
        self.history = []
        self.chat = self.startChatOCAI()
        
    def startChatOCAI(
        self,
        *,
        history: Iterable[content_types.StrictContentType] | None = None,
        enable_automatic_function_calling: bool = False,
    ) -> genai.ChatSession:
        if self._generation_config.get("candidate_count", 1) > 1:
            raise ValueError(
                "Invalid configuration: The chat functionality does not support candidate_count greater than 1."
            )
        return ChatOCAI(
            model=self,
            history=history,
            enable_automatic_function_calling=self._generation_config.get("enable_automatic_function_calling", False),
        )

class ChatOCAI(genai.ChatSession):
    def __init__(
        self,
        model: modelOCAI,
        history: Iterable[content_types.StrictContentType] | None = None,
        enable_automatic_function_calling: bool = False,
        session_id: str = "",
    ):
        self.model: modelOCAI = model
        self._history: list[protos.Content] = content_types.to_contents(history)
        self._last_sent: protos.Content | None = None
        self._last_received: generation_types.BaseGenerateContentResponse | None = None
        self.enable_automatic_function_calling = enable_automatic_function_calling
        self.session_id = session_id
        
    def send_message(self,
        content: content_types.ContentType,
        *,
        generation_config: generation_types.GenerationConfigType = None,
        safety_settings: safety_types.SafetySettingOptions = None,
        stream: bool = False,
        tools: content_types.FunctionLibraryType | None = None,
        tool_config: content_types.ToolConfigType | None = None,
        request_options: helper_types.RequestOptionsType | None = None,
        session_id: str,
    ) -> generation_types.GenerateContentResponse:
        if request_options is None:
            request_options = {}

        if self.enable_automatic_function_calling and stream:
            raise NotImplementedError(
                "Unsupported configuration: The `google.generativeai` SDK currently does not support the combination of `stream=True` and `enable_automatic_function_calling=True`."
            )

        tools_lib = self.model._get_tools_lib(tools)

        content = content_types.to_content(content)

        if not content.role:
            content.role = _USER_ROLE

        history = self.history[:]
        history.append(content)

        generation_config = generation_types.to_generation_config_dict(generation_config)
        if generation_config.get("candidate_count", 1) > 1:
            raise ValueError(
                "Invalid configuration: The chat functionality does not support `candidate_count` greater than 1."
            )

        response = self.model.generate_content(
            contents=history,
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=stream,
            tools=tools_lib,
            tool_config=tool_config,
            request_options=request_options,
        )

        self._check_response(response=response, stream=stream)

        if self.enable_automatic_function_calling and tools_lib is not None:
            self.history, content, response = self._handle_afc(
                response=response,
                history=history,
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=stream,
                tools_lib=tools_lib,
                request_options=request_options,
            )

        self._last_sent = content
        self._last_received = response

        return response

genai.configure(api_key="AIzaSyCg-nr4gR-TOJ27425B8OaZmvDIiktcT-E")

model = modelOCAI("gemini-1.5-flash")
chat = model.startChatOCAI()

user = ""
while user != "bye":
    user = input("write: ")
    response = chat.send_message(user, session_id="1234")
    print(response.text)

print(chat.history)