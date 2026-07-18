from google import genai

from config import Config

from builders.prompt_builder import PromptBuilder


class LLMService:

    def __init__(self):

        self.client = genai.Client(
            api_key=Config.GEMINI_API_KEY
        )

        self.model = Config.GEMINI_MODEL

    def generate_first_question(self, session):

        prompt = PromptBuilder.first_question(session)

        response = self.client.models.generate_content(

            model=self.model,

            contents=prompt
        )

        return response.text.strip()