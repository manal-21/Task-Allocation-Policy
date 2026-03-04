# Task-Allocation-Policy
Weight and fatigue aware task allocation framework simple simulation.

# Weight–Fatigue Aware Task Allocation in Human–Robot Collaborative Warehouses**
# Project Overview
This repository contains the simulation framework developed for the thesis:
"Fatigue-Aware Task Allocation in Human–Robot Collaborative Warehouse Systems"

The project implements a discrete-event simulation to evaluate task allocation strategies that balance operational productivity and human ergonomic sustainability.
The core contribution is a Weight–Fatigue allocation policy, which dynamically assigns tasks to human workers or robotic agents based on task weight and real-time human fatigue levels.

# Research Objective
The objective of this study is to investigate whether fatigue-aware task allocation can:
- Reduce cumulative human fatigue
- Maintain competitive throughput
- Improve system robustness under stochastic workloads
- Balance productivity and worker sustainability

# Features
- Discrete-time simulation framework
- Human fatigue accumulation and recovery model
- Multiple task allocation strategies:
    - Weight–Fatigue Policy (proposed)
    - Human-Centered Policy
    - Robot-Centered Policy
    - Greedy Policy
- Multi-run statistical evaluation (mean and standard deviation)

# Simulation Model Summary
- Time horizon: Configurable
- Task arrivals: Bernoulli process with probability p
- Task attributes:
    - Weight
    - Distance
- Human agents:
    - Fatigue accumulation based on task weight and duration
    - Fatigue recovery during idle periods
- Robot agents:
    - Constant performance (no fatigue)

# Installation
- Clone the repository:
    - git clone https://github.com/manal-21/Task-Allocation-Policy.git
    - cd Task-Allocation-Policy
- Install dependencies:
    - pip install -r requirements.txt

# Running the Simulation
- To run the experimental evaluation:
    - python experiment.py
- This will:
    - Execute all allocation policies
    - Run multiple independent simulations
    - Compute mean and standard deviation metrics
    - Export results to a CSV file

# Output
The simulation generates:
  - Throughput (mean ± std)
  - Average completion time (mean ± std)
  - Average fatigue (mean ± std)
  - Maximum fatigue (mean ± std)
Results are saved as:
  - results.csv
These outputs can be used for visualization in Excel or other statistical tools.

CSV export of experimental results
