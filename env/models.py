from pydantic import BaseModel
from typing import Dict, List


#  What agent sends (ACTION)
class StudyAction(BaseModel):
    plan: Dict[str, float]
    # Example:
    # {
    #   "DSA": 2,
    #   "DBMS": 2,
    #   "OS": 2
    # }


#  What environment returns (OBSERVATION)
class StudyObservation(BaseModel):
    message: str
    current_plan: Dict[str, float]
    remaining_hours: float


#  Reward model
class StudyReward(BaseModel):
    score: float  # must be between 0 and 1