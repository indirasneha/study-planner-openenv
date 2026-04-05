---
title: Study Planner Env
emoji: 📚
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---
# Study Planner OpenEnv

## Description
This project implements a real-world OpenEnv environment where an AI agent learns to create and optimize study schedules for students.

The environment simulates planning tasks such as daily scheduling, weekly planning, and adaptive adjustments.

---

## Tasks

### 1. Daily Planner (Easy)
Create a balanced 1-day study plan using 6 hours across subjects (DSA, DBMS, OS).

### 2. Weekly Planner (Medium)
Create a 7-day study schedule while respecting subject priorities.

### 3. Adaptive Planner (Hard)
Adjust the study plan when disruptions occur (missed days, fatigue, deadlines).

---

## Action Space
The agent provides a study plan:

Example:
{
  "DSA": 2,
  "DBMS": 2,
  "OS": 2
}

---

## Observation Space
The environment returns:
- message
- current plan
- remaining hours

---

## Reward System
The reward is based on:
- balanced distribution
- correct total time usage
- priority handling
- avoiding overload

Rewards are normalized between 0 and 1.

---

## Setup Instructions

1. Install dependencies:
pip install openenv-core openai

2. Run inference:
python inference.py

---

## Project Structure

- env/
  - study_env.py
  - models.py
  - tasks.py
- inference.py
- openenv.yaml
- Dockerfile
- README.md

---

## Baseline Score
The baseline agent generates a balanced study plan and achieves a moderate score.

---

## Notes
This environment demonstrates a real-world application of reinforcement learning for planning and optimization tasks.