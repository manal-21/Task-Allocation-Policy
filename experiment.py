import random
import csv
import numpy as np
import matplotlib.pyplot as plt

# =========================
# GLOBAL PARAMETERS
# =========================

NUM_HUMANS = 2
NUM_ROBOTS = 2
SIM_TIME = 500   # Increased simulation time

ROBOT_PAYLOAD = 25
HUMAN_SPEED = 1.0
ROBOT_SPEED = 1.5

ALPHA = 0.002   # fatigue accumulation rate
BETA = 0.01     # fatigue recovery rate


# =========================
# AGENT CLASSES
# =========================

class Human:
    def __init__(self, id):
        self.id = id
        self.available_time = 0
        self.fatigue = 0.0

    def assign_task(self, duration, weight, current_time):
        self.available_time = current_time + duration
        self.fatigue += ALPHA * weight * duration
        self.fatigue = min(1.0, self.fatigue)

    def recover(self):
        self.fatigue -= BETA
        self.fatigue = max(0.0, self.fatigue)


class Robot:
    def __init__(self, id):
        self.id = id
        self.available_time = 0
        self.max_payload = ROBOT_PAYLOAD

    def assign_task(self, duration, current_time):
        self.available_time = current_time + duration


# =========================
# TASK
# =========================

class Task:
    def __init__(self, weight, distance):
        self.weight = weight
        self.distance = distance


# =========================
# HELPER FUNCTIONS
# =========================

def assign_human(task, humans, time):
    for h in humans:
        if h.available_time <= time and h.fatigue < 0.8:
            return h
    return None


def assign_robot(task, robots, time):
    for r in robots:
        if r.available_time <= time and task.weight <= r.max_payload:
            return r
    return None


# =========================
# POLICIES
# =========================

def weight_fatigue_policy(task, humans, robots, time):
    if task.weight <= 5:
        return assign_human(task, humans, time)

    if task.weight <= 10:
        for h in humans:
            if h.available_time <= time and h.fatigue < 0.6:
                return h
        return assign_robot(task, robots, time)

    return assign_robot(task, robots, time)


def human_centered(task, humans, robots, time):
    return assign_human(task, humans, time) or assign_robot(task, robots, time)


def robot_centered(task, humans, robots, time):
    return assign_robot(task, robots, time) or assign_human(task, humans, time)


def greedy_policy(task, humans, robots, time):
    available = [a for a in humans + robots if a.available_time <= time]
    return random.choice(available) if available else None


# =========================
# SIMULATION
# =========================

def run_simulation(policy_function, arrival_prob):

    humans = [Human(i) for i in range(NUM_HUMANS)]
    robots = [Robot(i) for i in range(NUM_ROBOTS)]

    completed_tasks = 0
    total_completion_time = 0

    for t in range(SIM_TIME):

        # Human recovery
        for h in humans:
            if h.available_time <= t:
                h.recover()

        # Task arrival
        if random.random() < arrival_prob:

            weight = random.uniform(1, 20)
            distance = random.uniform(5, 20)
            task = Task(weight, distance)

            agent = policy_function(task, humans, robots, t)

            if agent:

                if isinstance(agent, Human):
                    duration = distance / HUMAN_SPEED
                    agent.assign_task(duration, weight, t)

                else:
                    duration = distance / ROBOT_SPEED
                    agent.assign_task(duration, t)

                completed_tasks += 1
                total_completion_time += duration

    avg_fatigue = np.mean([h.fatigue for h in humans])
    max_fatigue = max([h.fatigue for h in humans])
    throughput = completed_tasks / SIM_TIME
    avg_completion = (
        total_completion_time / completed_tasks if completed_tasks > 0 else 0
    )

    return {
        "throughput": throughput,
        "avg_completion_time": avg_completion,
        "avg_fatigue": avg_fatigue,
        "max_fatigue": max_fatigue,
    }


# =========================
# EXPERIMENT RUNNER
# =========================

def run_experiments(policy_function, arrival_prob, runs=50):

    results = []

    for seed in range(runs):
        random.seed(seed)
        np.random.seed(seed)

        result = run_simulation(policy_function, arrival_prob)
        results.append(result)

    metrics = {}

    for key in results[0].keys():
        values = [r[key] for r in results]
        metrics[key] = (np.mean(values), np.std(values))

    return metrics


# =========================
# CLEAN PRINTING
# =========================

def print_clean_results(results):

    for policy, metrics in results.items():
        print("\n==============================")
        print(f"Policy: {policy}")
        print("==============================")

        for metric_name, (mean, std) in metrics.items():
            print(f"{metric_name:25s}: {mean:.4f} ± {std:.4f}")

def save_results_to_csv(all_results, filename="results.csv"):

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Header row
        writer.writerow([
            "Workload",
            "Policy",
            "Throughput_Mean", "Throughput_Std",
            "Completion_Mean", "Completion_Std",
            "AvgFatigue_Mean", "AvgFatigue_Std",
            "MaxFatigue_Mean", "MaxFatigue_Std"
        ])

        # Write rows
        for workload, policies in all_results.items():
            for policy_name, metrics in policies.items():

                writer.writerow([
                    workload,
                    policy_name,
                    metrics["throughput"][0], metrics["throughput"][1],
                    metrics["avg_completion_time"][0], metrics["avg_completion_time"][1],
                    metrics["avg_fatigue"][0], metrics["avg_fatigue"][1],
                    metrics["max_fatigue"][0], metrics["max_fatigue"][1],
                ])

    print(f"\nResults saved to {filename}")


# =========================
# MAIN EXPERIMENT
# =========================

if __name__ == "__main__":

    policies = {
        "Weight-Fatigue": weight_fatigue_policy,
        "Human-Centered": human_centered,
        "Robot-Centered": robot_centered,
        "Greedy": greedy_policy,
    }

    arrival_levels = [0.2, 0.4, 0.6]

    all_results = {}

    for arrival in arrival_levels:
        print("\n\n####################################")
        print(f"WORKLOAD LEVEL (Arrival Prob): {arrival}")
        print("####################################")

        results = {}

        for name, policy in policies.items():
            metrics = run_experiments(policy, arrival, runs=50)
            results[name] = metrics

        print_clean_results(results)

        all_results[arrival] = results

    # Save everything to CSV
    save_results_to_csv(all_results)