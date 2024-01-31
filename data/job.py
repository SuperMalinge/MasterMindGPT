from typing import Optional

class Job:
    def __init__(self, team: str, description: str, status: str = 'not solved', subjob: Optional[str] = None):
        self.team = team
        self.description = description
        self.status = status
        self.subjob = subjob
        self.question = None
        self.ask_question = None
        self.suggestion1 = None
        self.suggestion2 = None
        self.own_suggestion = None
        self.scratch_question = None





