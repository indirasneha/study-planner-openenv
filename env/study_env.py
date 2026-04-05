from typing import Dict
from env.models import StudyAction, StudyObservation

class StudyEnv:

    def __init__(self):
        self.total_hours = 6
        self.subjects = ["DSA", "DBMS", "OS"]
        self.current_plan: Dict[str, float] = {}
        self.done = False

    #  Reset environment
    def reset(self):
        self.current_plan = {}
        self.done = False

        return StudyObservation(
            message="Start planning your study schedule",
            current_plan=self.current_plan,
            remaining_hours=self.total_hours
        )

    #  Step function (core logic)
    def step(self, action: StudyAction):
        plan = action.plan
        self.current_plan = plan

        total_time = sum(plan.values())

        # --- Reward Calculation ---
        reward = 0.0

        # Check all subjects present
        if all(sub in plan for sub in self.subjects):
            reward += 0.3

        # Check balance (simple logic)
        values = list(plan.values())
        if max(values) - min(values) <= 1:
            reward += 0.4

        # Check total time usage
        if total_time == self.total_hours:
            reward += 0.3

        # Penalty: overload
        if total_time > self.total_hours:
            reward -= 0.2

        # Clamp reward
        reward = max(0.0, min(1.0, reward))

        self.done = True

        return {
            "observation": StudyObservation(
                message="Plan evaluated",
                current_plan=plan,
                remaining_hours=max(0, self.total_hours - total_time)
            ),
            "reward": reward,
            "done": self.done,
            "info": {}
        }

    #  State function
    def state(self):
        return {
            "current_plan": self.current_plan,
            "done": self.done
        }
from fastapi import FastAPI
from openenv import OpenEnvApp

app = FastAPI()
env = StudyEnv()

openenv_app = OpenEnvApp(env)
app.mount("/", openenv_app)