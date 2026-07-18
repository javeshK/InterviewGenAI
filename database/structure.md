FINAL STRUCTURE of database

Candidate
──────────────
id
name
email
created_at

        │

        ▼

Interview
──────────────
id
candidate_id
role
experience
difficulty
type
status
started_at
ended_at
overall_score

        │

 ┌──────┴────────┐

 ▼               ▼

Questions      Report