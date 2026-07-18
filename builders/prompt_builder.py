class PromptBuilder:

    @staticmethod
    def first_question(session):

        return f"""
You are an expert technical interviewer.

Candidate Name:
{session.candidate_name}

Role:
{session.role}

Experience:
{session.experience}

Difficulty:
{session.difficulty}

Interview Type:
{session.interview_type}

Generate ONLY the first interview question.

Rules:

- Ask only one question.
- Do not explain.
- Do not greet.
- No markdown.
- Keep it concise.
"""