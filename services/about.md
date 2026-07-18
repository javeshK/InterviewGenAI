This is where almost everything happens.

Think of this folder as your backend brain.





                Flask Routes
                     │
                     ▼
            InterviewService
                     │
     ┌───────────────┼────────────────┐
     │               │                │
Repositories      AI Services      Utilities
     │               │                │
     ▼               ▼                ▼
CandidateRepo   PromptService     Logger
InterviewRepo   LLMService        Config
QuestionRepo    EvaluationService
ReportRepo      ReportService
     │
     ▼
SQLite Database