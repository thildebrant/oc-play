#!/usr/bin/env python3
"""
Core Wars Battle Runner with visualization
"""

import os
import sys
import time
import random
import argparse
from typing import List, Optional
from mars import MARS, Warrior
from ai_agent import AIAgent, WarriorGenerator

class BattleVisualizer:
    """Terminal-based battle visualizer."""
    
    COLORS = {
        'reset': '\033[0m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
    }
    
    def __init__(self, mars: MARS, display_width: int = 80):
        self.mars = mars
        self.display_width = display_width
        self.cells_per_char = mars.core_size // (display_width * 20)  # 20 lines of display
        
    def clear_screen(self):
        """Clear terminal screen."""
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def get_color_for_warrior(self, warrior_id: int) -> str:
        """Get color code for a warrior."""
        colors = ['red', 'blue', 'green', 'yellow', 'magenta', 'cyan']
        if warrior_id == 0:
            return self.COLORS['black']
        elif warrior_id > 10:  # Execution pointer
            return self.COLORS[f'bright_{colors[(warrior_id - 11) % len(colors)]}']
        else:  # Regular warrior code
            return self.COLORS[colors[(warrior_id - 1) % len(colors)]]
    
    def render_core(self) -> str:
        """Render the core memory as a colored grid."""
        state = self.mars.get_memory_state()
        output = []
        
        # Title
        output.append("=" * self.display_width)
        output.append("CORE WARS BATTLE ARENA".center(self.display_width))
        output.append("=" * self.display_width)
        
        # Warriors info
        for i, warrior in enumerate(self.mars.warriors, 1):
            color = self.get_color_for_warrior(i)
            status = "ALIVE" if warrior.processes else "DEAD"
            proc_count = len(warrior.processes)
            output.append(f"{color}■{self.COLORS['reset']} {warrior.name} by {warrior.author}: {status} ({proc_count} processes)")
        
        output.append("-" * self.display_width)
        
        # Core visualization
        chars = []
        for i in range(0, len(state), self.cells_per_char):
            # Find dominant warrior in this block
            block = state[i:i+self.cells_per_char]
            if not block:
                continue
                
            # Count occurrences
            counts = {}
            for val in block:
                counts[val] = counts.get(val, 0) + 1
            
            # Get most common
            dominant = max(counts, key=counts.get)
            
            # Choose character based on density
            if counts[dominant] == len(block):
                char = '█'  # Full block
            elif counts[dominant] > len(block) * 0.7:
                char = '▓'  # Dense
            elif counts[dominant] > len(block) * 0.4:
                char = '▒'  # Medium
            elif counts[dominant] > 0:
                char = '░'  # Sparse
            else:
                char = ' '  # Empty
            
            color = self.get_color_for_warrior(dominant)
            chars.append(f"{color}{char}{self.COLORS['reset']}")
        
        # Format as grid
        for i in range(0, len(chars), self.display_width):
            output.append(''.join(chars[i:i+self.display_width]))
        
        # Stats
        output.append("-" * self.display_width)
        output.append(f"Cycle: {self.mars.cycle}/{self.mars.max_cycles}")
        
        return '\n'.join(output)
    
    def animate_battle(self, delay: float = 0.01, skip_frames: int = 10):
        """Animate the battle in the terminal."""
        frame = 0
        
        while self.mars.run_cycle():
            frame += 1
            if frame % skip_frames == 0:
                self.clear_screen()
                print(self.render_core())
                time.sleep(delay)
        
        # Show final state
        self.clear_screen()
        print(self.render_core())
        print("\n" + "=" * self.display_width)
        
        if self.mars.winner:
            print(f"🏆 WINNER: {self.mars.winner.name} by {self.mars.winner.author}!")
        else:
            print("⏱️  DRAW - Maximum cycles reached!")
        print("=" * self.display_width)

class BattleRunner:
    """Run battles between AI agents."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = []
        
    def run_single_battle(self, agent1: AIAgent, agent2: AIAgent, 
                         visualize: bool = False, core_size: int = 8000) -> Optional[Warrior]:
        """Run a single battle between two AI agents."""
        # Create warriors
        warrior1 = agent1.create_warrior()
        warrior2 = agent2.create_warrior()
        
        if self.verbose:
            print(f"\n🤺 Battle: {warrior1.name} vs {warrior2.name}")
            print(f"  {warrior1.name}: {len(warrior1.program)} instructions")
            print(f"  {warrior2.name}: {len(warrior2.program)} instructions")
        
        # Setup MARS
        mars = MARS(core_size=core_size, max_cycles=80000)
        mars.load_warrior(warrior1)
        mars.load_warrior(warrior2)
        
        # Run battle
        if visualize:
            visualizer = BattleVisualizer(mars)
            visualizer.animate_battle(delay=0.02, skip_frames=100)
            winner = mars.winner
        else:
            winner = mars.run_battle()
        
        # Record results
        self.results.append({
            'warrior1': warrior1.name,
            'warrior2': warrior2.name,
            'winner': winner.name if winner else 'DRAW',
            'cycles': mars.cycle
        })
        
        # Let agents learn
        agent1.learn_from_battle(warrior1, warrior2, winner == warrior1 if winner else False)
        agent2.learn_from_battle(warrior2, warrior1, winner == warrior2 if winner else False)
        
        if self.verbose and not visualize:
            if winner:
                print(f"  🏆 Winner: {winner.name} in {mars.cycle} cycles")
            else:
                print(f"  ⏱️ Draw after {mars.cycle} cycles")
        
        return winner
    
    def run_tournament(self, agent1: AIAgent, agent2: AIAgent, 
                      rounds: int = 10, visualize_final: bool = True):
        """Run a tournament between two agents."""
        print(f"\n{'='*60}")
        print(f"CORE WARS TOURNAMENT".center(60))
        print(f"{'='*60}")
        print(f"  {agent1.name} vs {agent2.name}")
        print(f"  {rounds} rounds")
        print(f"{'='*60}\n")
        
        wins = {agent1.name: 0, agent2.name: 0, 'DRAW': 0}
        
        for round_num in range(rounds):
            print(f"Round {round_num + 1}/{rounds}...", end='')
            
            # Visualize last round
            visualize = visualize_final and (round_num == rounds - 1)
            
            winner = self.run_single_battle(agent1, agent2, visualize=visualize)
            
            if winner:
                if winner.author == agent1.name:
                    wins[agent1.name] += 1
                    print(f" {agent1.name} wins!")
                else:
                    wins[agent2.name] += 1
                    print(f" {agent2.name} wins!")
            else:
                wins['DRAW'] += 1
                print(" Draw!")
            
            # Let agents evolve periodically
            if (round_num + 1) % 5 == 0:
                print("  📈 Agents evolving...")
                if agent1.evolver.generation == 0:
                    agent1.evolver.initialize_population()
                agent1.evolver.evolve_generation()
                
                if agent2.evolver.generation == 0:
                    agent2.evolver.initialize_population()
                agent2.evolver.evolve_generation()
        
        # Print results
        print(f"\n{'='*60}")
        print(f"TOURNAMENT RESULTS".center(60))
        print(f"{'='*60}")
        print(f"  {agent1.name}: {wins[agent1.name]} wins")
        print(f"  {agent2.name}: {wins[agent2.name]} wins")
        print(f"  Draws: {wins['DRAW']}")
        
        if wins[agent1.name] > wins[agent2.name]:
            print(f"\n🏆 TOURNAMENT WINNER: {agent1.name}!")
        elif wins[agent2.name] > wins[agent1.name]:
            print(f"\n🏆 TOURNAMENT WINNER: {agent2.name}!")
        else:
            print(f"\n🤝 TOURNAMENT DRAW!")
        print(f"{'='*60}\n")

def main():
    parser = argparse.ArgumentParser(description='Core Wars AI Battle Arena')
    parser.add_argument('--visualize', action='store_true', help='Visualize battles')
    parser.add_argument('--rounds', type=int, default=10, help='Number of rounds')
    parser.add_argument('--strategy1', choices=list(WarriorGenerator.STRATEGIES.keys()),
                       help='Strategy for Agent 1')
    parser.add_argument('--strategy2', choices=list(WarriorGenerator.STRATEGIES.keys()),
                       help='Strategy for Agent 2')
    parser.add_argument('--quick', action='store_true', help='Quick single battle')
    
    args = parser.parse_args()
    
    # Create AI agents with different strategy preferences
    strategies1 = [args.strategy1] if args.strategy1 else ['bomber', 'dwarf', 'scanner']
    strategies2 = [args.strategy2] if args.strategy2 else ['replicator', 'imp', 'paper']
    
    agent1 = AIAgent("AlphaWarrior", strategies1)
    agent2 = AIAgent("BetaFighter", strategies2)
    
    runner = BattleRunner(verbose=True)
    
    if args.quick:
        # Single battle
        print("\n🎮 Running single battle...")
        runner.run_single_battle(agent1, agent2, visualize=args.visualize)
    else:
        # Tournament
        runner.run_tournament(agent1, agent2, rounds=args.rounds, 
                            visualize_final=args.visualize)

if __name__ == '__main__':
    main()