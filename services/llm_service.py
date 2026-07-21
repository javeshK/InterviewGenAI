"""
llm_service.py

Responsible ONLY for communicating with Gemini.

Responsibilities:
- Send prompts to Gemini
- Parse responses
- Return clean Python objects
- Handle API failures

Prompt generation is handled by PromptService.
"""

import json
import logging
from typing import Any

from google import genai

from config import Config
from services.prompt_service import PromptService

from models.candidate import Candidate
from models.interview_question import InterviewQuestion


logger = logging.getLogger(__name__)


class LLMService:

    def __init__(self):

        self.client = genai.Client(
            api_key=Config.GEMINI_API_KEY
        )

        self.model = Config.GEMINI_MODEL

    # --------------------------------------------------
    # Internal helper
    # --------------------------------------------------

    def _generate(self, prompt: str) -> str:
        """
        Sends a prompt to Gemini and returns plain text.
        """

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            return response.text.strip()

        except Exception as e:

            logger.exception(e)

            raise RuntimeError(
                f"Gemini request failed:\n{e}"
            )

    # --------------------------------------------------
    # Interview Question Generation
    # --------------------------------------------------

    def generate_first_question(
        self,
        candidate: Candidate
    ) -> str:

        prompt = PromptService.build_first_question_prompt(
            candidate
        )

        return self._generate(prompt)

    def generate_followup_question(
        self,
        candidate: Candidate,
        history: list[InterviewQuestion]
    ) -> str:

        prompt = (
            PromptService.build_followup_question_prompt(
                candidate,
                history
            )
        )

        return self._generate(prompt)

    # --------------------------------------------------
    # Answer Evaluation
    # --------------------------------------------------

    def evaluate_answer(
        self,
        question: str,
        answer: str,
        candidate: Candidate
    ) -> dict:

        prompt = (
            PromptService.build_answer_evaluation_prompt(
                question,
                answer,
                candidate
            )
        )

        response = self._generate(prompt)
        print("\n========== GEMINI RESPONSE ==========")
        print(response)
        print("=====================================\n")

        try:

            return json.loads(response)

        except json.JSONDecodeError:

            logger.exception(
                "Gemini returned invalid JSON:\n%s",
                response
            )

            raise RuntimeError(
                "Gemini returned invalid evaluation JSON."
            )
        

    

    # --------------------------------------------------
    # Final Interview Report
    # --------------------------------------------------

    def generate_final_report(
        self,
        candidate: Candidate,
        history: list[InterviewQuestion]
    ) -> dict:

        prompt = (
            PromptService.build_final_report_prompt(
                history,
                candidate
            )
        )

        response = self._generate(prompt)

        try:

            return json.loads(response)

        except json.JSONDecodeError:

            logger.exception(response)

            raise RuntimeError(
                "Gemini returned invalid report JSON."
            )

    # --------------------------------------------------
    # Resume Based Interview (Future)
    # --------------------------------------------------

    def generate_resume_question(
        self,
        resume_text: str
    ) -> str:

        prompt = (
            PromptService.build_resume_interview_prompt(
                resume_text
            )
        )

        return self._generate(prompt)

    # --------------------------------------------------
    # Behavioural Interview
    # --------------------------------------------------

    def generate_behavioral_question(
        self,
        candidate: Candidate
    ) -> str:

        prompt = (
            PromptService.build_behavioral_prompt(
                candidate
            )
        )

        return self._generate(prompt)