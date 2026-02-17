# 🚛 Fuel Distribution Logistics: Local Search Optimization

This repository contains the project developed for the **Artificial Intelligence (ABIA)** course at **UPC** (Academic Year 2025/26). The goal is to solve a complex vehicle routing and fuel distribution problem using Local Search techniques to maximize operational profit and efficiency.

### 🧠 Project Overview

The project addresses a logistics challenge where a fleet of tankers must supply a network of gas stations. The system manages constraints such as vehicle capacity, maximum daily travel distance, and time windows, while prioritizing supply requests based on urgency and economic impact.

### 🚀 Optimization Strategies

We implemented and compared two primary local search metaheuristics:
- **Hill Climbing:** Focusing on rapid convergence through steepest-ascent and first-choice variations.
- **Simulated Annealing:** Employed to escape local optima and explore the solution space more robustly through controlled stochastic movement.

**Key Technical Components:**
- **State Representation:** Efficient data structures to track truck assignments, remaining capacities, and pending requests.
- **Heuristic Design:** Multi-objective cost functions incorporating travel expenses, delivery income, and penalties for unfulfilled high-priority requests.
- **Custom Operators:** Implementation of swap, move, and reorder operators to navigate the search space effectively.

### 📈 Results & Analysis

The project includes an extensive experimental suite analyzing:
- **Initial Solution Impact:** Comparing greedy vs. random initialization performance.
- **Algorithm Comparison:** Evaluating the trade-off between execution time and solution quality (Profit vs. Distance).
- **Scalability:** Stress-testing the system with increasing numbers of distribution centers and gas stations.

### 🧱 Project Structure

- `implementacio/`: Core Python source code for state management, operators, and problem formulation.
- `experiments/`: Dedicated scripts for running performance benchmarks and scalability tests.
- `resultats/`: Generated data files and comparative charts.
- `INFORME.pdf`: Comprehensive technical report detailing heuristic justifications and experimental findings.

### 💻 Installation & Usage

Ensure you have Python 3.12+ and the required dependencies installed:
```bash
pip install numpy matplotlib pandas aima3
```

To run the main problem or specific experiments from the root directory:
```bash
python -m implementacio.camions
python -m experiments.experiments3
```
