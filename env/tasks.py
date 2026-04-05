from typing import Dict


#  EASY TASK
def evaluate_daily(plan: Dict[str, float]) -> float:
    subjects = ["DSA", "DBMS", "OS"]
    total_hours = 6

    reward = 0.0

    # All subjects included
    if all(sub in plan for sub in subjects):
        reward += 0.3

    values = list(plan.values())

    # Balanced distribution
    if max(values) - min(values) <= 1:
        reward += 0.4

    # Total time correct
    if sum(values) == total_hours:
        reward += 0.3

    # Penalty: overload
    if sum(values) > total_hours:
        reward -= 0.2

    return max(0.0, min(1.0, reward))


#  MEDIUM TASK
def evaluate_weekly(plan: Dict[str, float]) -> float:
    reward = 0.0

    # Priority: DSA > DBMS > OS
    dsa = plan.get("DSA", 0)
    dbms = plan.get("DBMS", 0)
    os = plan.get("OS", 0)

    # Check priority
    if dsa >= dbms >= os:
        reward += 0.4

    # Balanced (not extreme difference)
    values = [dsa, dbms, os]
    if max(values) - min(values) <= 3:
        reward += 0.3

    # Reasonable total
    if sum(values) <= 42:  # 7 days * 6 hrs
        reward += 0.3

    return max(0.0, min(1.0, reward))


#  HARD TASK
def evaluate_adaptive(plan: Dict[str, float]) -> float:
    reward = 0.0

    total = sum(plan.values())

    # Recover missed tasks (assume >4 hrs = recovery effort)
    if total >= 4:
        reward += 0.4

    # Avoid overload
    if total <= 6:
        reward += 0.3
    else:
        reward -= 0.3

    # Smart distribution
    values = list(plan.values())
    if max(values) - min(values) <= 2:
        reward += 0.3

    return max(0.0, min(1.0, reward))