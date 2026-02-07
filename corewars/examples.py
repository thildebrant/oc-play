#!/usr/bin/env python3
"""
Example Core Wars warriors and battles
"""

from mars import Instruction, Opcode, AddressMode, Warrior, MARS
from ai_agent import AIAgent
from battle import BattleRunner, BattleVisualizer

def create_classic_warriors():
    """Create some classic Core Wars warriors."""
    
    # Imp - The simplest warrior
    imp = Warrior("Imp", [
        Instruction(Opcode.MOV, AddressMode.DIRECT, 0, AddressMode.DIRECT, 1)
    ], author="Classic")
    
    # Dwarf - A simple bomber
    dwarf = Warrior("Dwarf", [
        Instruction(Opcode.ADD, AddressMode.IMMEDIATE, 4, AddressMode.DIRECT, 3),
        Instruction(Opcode.MOV, AddressMode.DIRECT, 2, AddressMode.INDIRECT, 2),
        Instruction(Opcode.JMP, AddressMode.DIRECT, -2, AddressMode.DIRECT, 0),
        Instruction(Opcode.DAT, AddressMode.IMMEDIATE, 0, AddressMode.IMMEDIATE, 0)
    ], author="Classic")
    
    # Stone - An optimized bomber
    stone = Warrior("Stone", [
        Instruction(Opcode.MOV, AddressMode.INDIRECT, 0, AddressMode.INDIRECT, 2),
        Instruction(Opcode.ADD, AddressMode.IMMEDIATE, 2, AddressMode.DIRECT, -1),
        Instruction(Opcode.JMP, AddressMode.DIRECT, -2, AddressMode.DIRECT, 0),
        Instruction(Opcode.DAT, AddressMode.IMMEDIATE, 0, AddressMode.IMMEDIATE, 2)
    ], author="Classic")
    
    # Scanner - Searches for enemies
    scanner = Warrior("Scanner", [
        Instruction(Opcode.CMP, AddressMode.DIRECT, 100, AddressMode.DIRECT, 200),
        Instruction(Opcode.JMP, AddressMode.DIRECT, 4, AddressMode.DIRECT, 0),
        Instruction(Opcode.ADD, AddressMode.IMMEDIATE, 1, AddressMode.DIRECT, -2),
        Instruction(Opcode.ADD, AddressMode.IMMEDIATE, 1, AddressMode.DIRECT, -3),
        Instruction(Opcode.JMP, AddressMode.DIRECT, -4, AddressMode.DIRECT, 0),
        Instruction(Opcode.MOV, AddressMode.IMMEDIATE, 0, AddressMode.DIRECT, 100)
    ], author="Classic")
    
    return imp, dwarf, stone, scanner

def run_classic_battle():
    """Run a battle between classic warriors."""
    imp, dwarf, stone, scanner = create_classic_warriors()
    
    print("Classic Battle: Dwarf vs Imp")
    print("-" * 40)
    
    mars = MARS(core_size=8000, max_cycles=80000)
    mars.load_warrior(dwarf)
    mars.load_warrior(imp)
    
    winner = mars.run_battle()
    
    if winner:
        print(f"Winner: {winner.name} after {mars.cycle} cycles")
    else:
        print(f"Draw after {mars.cycle} cycles")
    
    print("\nClassic Battle: Stone vs Scanner")
    print("-" * 40)
    
    mars2 = MARS(core_size=8000, max_cycles=80000)
    mars2.load_warrior(stone)
    mars2.load_warrior(scanner)
    
    winner2 = mars2.run_battle()
    
    if winner2:
        print(f"Winner: {winner2.name} after {mars2.cycle} cycles")
    else:
        print(f"Draw after {mars2.cycle} cycles")

def demo_evolution():
    """Demonstrate AI warrior evolution."""
    print("\nAI Evolution Demo")
    print("=" * 60)
    print("Watch as AI agents evolve better warriors over time...")
    print()
    
    # Create two AI agents
    agent1 = AIAgent("Attacker", ["bomber", "dwarf"])
    agent2 = AIAgent("Defender", ["scanner", "replicator"])
    
    # Initialize their populations
    agent1.evolver.initialize_population()
    agent2.evolver.initialize_population()
    
    runner = BattleRunner(verbose=True)
    
    # Run multiple generations
    for generation in range(3):
        print(f"\n--- Generation {generation + 1} ---")
        
        # Battle current best warriors
        warrior1 = agent1.evolver.get_best_warrior()
        warrior2 = agent2.evolver.get_best_warrior()
        
        print(f"Battling: {warrior1.name} vs {warrior2.name}")
        
        mars = MARS(core_size=8000, max_cycles=10000)
        mars.load_warrior(warrior1)
        mars.load_warrior(warrior2)
        
        winner = mars.run_battle()
        
        if winner:
            print(f"  Winner: {winner.name} in {mars.cycle} cycles")
            # Update fitness
            if winner.name == warrior1.name:
                agent1.evolver.population[0] = (warrior1, 1.0)
                agent2.evolver.population[0] = (warrior2, 0.0)
            else:
                agent1.evolver.population[0] = (warrior1, 0.0)
                agent2.evolver.population[0] = (warrior2, 1.0)
        else:
            print(f"  Draw after {mars.cycle} cycles")
            agent1.evolver.population[0] = (warrior1, 0.5)
            agent2.evolver.population[0] = (warrior2, 0.5)
        
        # Evolve to next generation
        print("  Evolving...")
        agent1.evolver.evolve_generation()
        agent2.evolver.evolve_generation()
    
    print("\n" + "=" * 60)
    print("Evolution complete! Warriors have adapted over generations.")

if __name__ == "__main__":
    print("=" * 60)
    print("CORE WARS EXAMPLES".center(60))
    print("=" * 60)
    
    # Run classic battles
    run_classic_battle()
    
    # Demonstrate evolution
    demo_evolution()