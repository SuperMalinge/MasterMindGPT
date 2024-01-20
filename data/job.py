from typing import Optional

class Job:
    def __init__(self, team, description, status='not solved', subjob=None):
        self.team = team
        self.description = description
        self.status = status
        self.subjob = subjob
        team: str
        description: str
        status: str = 'not solved'
        subjob: Optional[str] = None
        question: Optional[str] = None
        ask_question: Optional[str] = None
        suggestion1: Optional[str] = None
        suggestion2: Optional[str] = None
        own_suggestion: Optional[str] = None
        scratch_question: Optional[str] = None
