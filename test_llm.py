from services.llm_service import LLMService

llm = LLMService()

question = llm.generate_question(
    role="Python Backend Developer",
    experience="Student",
    interview_type="Technical",
    difficulty="Easy"
)

print(question)