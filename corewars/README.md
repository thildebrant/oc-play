# Core Wars AI Battle Arena

A Python implementation of Core Wars where AI agents generate and evolve Redcode warriors to battle in the MARS (Memory Array Redcode Simulator).

## Features

- Full Redcode '88 instruction set implementation
- MARS virtual machine with configurable core size
- AI agents that generate and evolve warriors
- Real-time battle visualization
- Battle statistics and analysis

## Quick Start

```bash
# Run a single battle with visualization
python battle.py

# Run a tournament between AI-generated warriors
python tournament.py

# Watch battles in the terminal
python battle.py --visualize
```

## Components

- `mars.py` - The MARS virtual machine and Redcode interpreter
- `warrior.py` - Warrior generation and mutation logic
- `ai_agent.py` - AI agents that create and evolve warriors
- `battle.py` - Battle runner and visualization
- `tournament.py` - Tournament system for multiple battles

## Redcode Instructions Supported

- **Data Movement**: MOV, DAT
- **Arithmetic**: ADD, SUB, MUL, DIV, MOD
- **Comparison**: CMP, SEQ, SNE, SLT
- **Jumps**: JMP, JMZ, JMN, DJN, SPL
- **No-op**: NOP

## AI Strategy

The AI agents use genetic algorithms to evolve warriors:
1. Generate initial population of random warriors
2. Battle warriors against each other
3. Select best performers
4. Mutate and crossover to create new generation
5. Repeat until convergence or max generations

## Visualization

The battle visualizer shows:
- Core memory state (color-coded by owner)
- Execution pointers for each warrior
- Battle statistics (cycles, writes, executions)
- Winner determination