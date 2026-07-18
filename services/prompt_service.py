"""
prompt_service.py

Centralized Prompt Engineering Service.

Every prompt sent to Gemini is generated here.

Advantages:
- Keeps prompts consistent
- Easier prompt engineering
- Easier testing
- LLMService only communicates with Gemini
"""

from typing import List

from models.interview_question import InterviewQuestion
from models.candidate import Candidate


class PromptService:

    @staticmethod
    def build_first_question_prompt(
        candidate: Candidate
    ) -> str:
        """
        Prompt for generating the very first interview question.
        """

        return f"""
You are an expert technical interviewer.

Candidate Details

Role:
{candidate.target_role}

Experience:
{candidate.experience}

Interview Type:
{candidate.interview_type}

Difficulty:
{candidate.difficulty}

Instructions:

- Ask ONLY ONE interview question.
- Do not explain the answer.
- Do not greet.
- Do not use markdown.
- Keep the question under 80 words.
- The question should match the candidate's experience.
- The question should be suitable for a real interview.

Return ONLY the interview question.
"""

    @staticmethod
    def build_followup_question_prompt(
        candidate: Candidate,
        history: List[InterviewQuestion]
    ) -> str:
        """
        Prompt for generating the next question.
        """

        conversation = ""

        for item in history:

            conversation += f"""
Question {item.question_number}

{item.question}

Candidate Answer

{item.candidate_answer}
"""

        return f"""
You are an experienced software engineering interviewer.

Candidate

Role:
{candidate.target_role}

Experience:
{candidate.experience}

Difficulty:
{candidate.difficulty}

Interview History

{conversation}

Instructions

- Ask ONLY ONE new question.
- Do NOT repeat previous questions.
- Increase or decrease difficulty based on previous answers.
- Ask a logical follow-up.
- No greetings.
- No markdown.
- Maximum 80 words.

Return ONLY the next question.
"""

    @staticmethod
    def build_answer_evaluation_prompt(
        question: str,
        answer: str,
        candidate: Candidate
    ) -> str:
        """
        Prompt for evaluating an interview answer.

        Gemini MUST return JSON.
        """

        return f"""
You are a Senior Technical Interviewer.

Candidate Role

{candidate.target_role}

Experience

{candidate.experience}

Interview Question

{question}

Candidate Answer

{answer}

Evaluate the answer.

Return ONLY valid JSON.

JSON Format

{{
    "technical_score": 0,
    "communication_score": 0,
    "confidence_score": 0,
    "overall_score": 0,
    "ideal_answer": "",
    "feedback": ""
}}

Scoring

Technical Score:
0-10

Communication Score:
0-10

Confidence Score:
0-10

Overall Score:
0-10

No markdown.

No explanation.

Only JSON.
"""

    @staticmethod
    def build_final_report_prompt(
        history: List[InterviewQuestion],
        candidate: Candidate
    ) -> str:
        """
        Prompt for generating the final interview report.
        """

        interview = ""

        for item in history:

            interview += f"""
Question {item.question_number}

Question:
{item.question}

Answer:
{item.candidate_answer}

Technical:
{item.technical_score}

Communication:
{item.communication_score}

Confidence:
{item.confidence_score}

Feedback:
{item.feedback}

"""

        return f"""
You are an expert hiring manager.

Candidate

Role:
{candidate.target_role}

Experience:
{candidate.experience}

Interview Summary

{interview}

Generate the final report.

Return ONLY valid JSON.

{{
    "strengths": "",
    "weaknesses": "",
    "recommendations": "",
    "final_summary": ""
}}

No markdown.

Only JSON.
"""

    @staticmethod
    def build_resume_interview_prompt(
        resume_text: str
    ) -> str:
        """
        Future extension.

        Generates interview questions directly from resume.
        """

        return f"""
Generate technical interview questions based ONLY on this resume.

Resume

{resume_text}

Return ONLY ONE interview question.
"""

    @staticmethod
    def build_behavioral_prompt(
        candidate: Candidate
    ) -> str:
        """
        Behavioral interview prompt.
        """

        return f"""
Generate ONE behavioural interview question.

Candidate Role

{candidate.target_role}

Experience

{candidate.experience}

Difficulty

{candidate.difficulty}

Return ONLY the question.
"""