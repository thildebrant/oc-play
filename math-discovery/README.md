# Mathematical Discovery Simulator

A simulation where AI agents attempt to discover new mathematical theorems and identities, starting from high school mathematics, while a skeptical naysayer agent tries to disprove or find existing examples.

## Concept

Inspired by mathematical research and the process of conjecture and refutation, this system simulates:
- **Explorer Agents**: Generate new mathematical conjectures
- **Naysayer Agent**: Attempts to disprove or find prior art
- **Validator**: Verifies mathematical correctness
- **Knowledge Base**: Growing repository of discovered theorems

## Features

- Start with fundamental high school identities (algebraic, trigonometric, etc.)
- Agents use various strategies to propose new theorems:
  - Generalization of existing patterns
  - Combination of known results
  - Analogical reasoning
  - Symmetry exploration
- Naysayer agent employs:
  - Counterexample search
  - Database lookup for similar results
  - Triviality detection
  - Proof by contradiction attempts
- Real-time monitoring dashboard showing:
  - Discovery attempts
  - Success/failure rates
  - Novel theorems found
  - Knowledge graph growth

## Quick Start

```bash
# Run the discovery simulation
python3 discovery_sim.py

# Monitor progress in real-time
python3 monitor.py

# View the web dashboard
python3 -m http.server 8080
# Open http://localhost:8080/dashboard.html
```

## Architecture

1. **Knowledge Base** (`knowledge_base.py`)
   - Stores known identities and theorems
   - Semantic search for similar results
   - Categorization by field and difficulty

2. **Explorer Agents** (`explorer.py`)
   - Multiple exploration strategies
   - Hypothesis generation
   - Pattern recognition

3. **Naysayer Agent** (`naysayer.py`)
   - Counterexample generation
   - Prior art detection
   - Proof verification

4. **Simulation Engine** (`discovery_sim.py`)
   - Orchestrates agent interactions
   - Manages discovery pipeline
   - Records progress

5. **Monitoring Dashboard** (`dashboard.html`)
   - Live visualization
   - Discovery timeline
   - Success metrics