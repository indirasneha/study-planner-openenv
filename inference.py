import asyncio
import os
from typing import List

from openai import OpenAI

from env.study_env import StudyEnv
from env.models import StudyAction

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

MAX_STEPS = 1


def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: str | None):
    err = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={err}", flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


def get_action_from_model(client: OpenAI) -> str:
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Create a balanced study plan for DSA, DBMS, OS within 6 hours."},
                {"role": "user", "content": "Give hours for each subject."},
            ],
            temperature=0.3,
            max_tokens=100,
        )
        return completion.choices[0].message.content.strip()
    except Exception:
        return "DSA:2, DBMS:2, OS:2"


def parse_action(text: str):
    try:
        parts = text.split(",")
        plan = {}
        for p in parts:
            k, v = p.split(":")
            plan[k.strip()] = float(v.strip())
        return plan
    except Exception:
        return {"DSA": 2, "DBMS": 2, "OS": 2}


async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    env = StudyEnv()

    rewards = []
    steps_taken = 0

    log_start(task="daily_planner", env="study_env", model=MODEL_NAME)

    try:
        obs = env.reset()

        for step in range(1, MAX_STEPS + 1):
            action_text = get_action_from_model(client)
            plan = parse_action(action_text)

            result = env.step(StudyAction(plan=plan))

            reward = result["reward"]
            done = result["done"]

            rewards.append(reward)
            steps_taken = step

            log_step(step, action_text, reward, done, None)

            if done:
                break

        score = max(0.0, min(1.0, sum(rewards)))
        success = score > 0.5

    finally:
        log_end(success, steps_taken, score, rewards)


if __name__ == "__main__":
    asyncio.run(main())