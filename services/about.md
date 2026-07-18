This is where almost everything happens.

Think of this folder as your backend brain.


llm_service.py

Only talks to Gemini.
Nothing else.
Methods:
    generate_text(prompt)
    generate_json(prompt)
    stream(prompt)
It shouldn't know anything about interviews.


##Interview_service.py

This is the heart of the application.
Responsibilities:

    Build prompts
    Call LLMService
    Keep interview state
    Store conversation history
    Generate next question

Methods:

    start_interview()
    next_question()
    end_interview()
This is the file you'll spend most of your time in.

whisper_service.py
Only handles

Audio

↓

Whisper

↓

Transcript

Nothing else.


evaluation_service.py

Given:

Question

+

Answer

Return:
    Score
    Feedback
    Ideal Answer
    Weak Areas


report_service.py

Collects all evaluations.

Creates

Final Report

↓

PDF

↓

HTML