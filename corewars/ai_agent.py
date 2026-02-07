"""
AI Agents that generate and evolve Core Wars warriors using genetic algorithms.
"""

import random
from typing import List, Tuple
from mars import Instruction, Opcode, AddressMode, Warrior, MARS

class WarriorGenerator:
    """Generate random Redcode warriors."""
    
    # Common warrior patterns/strategies
    STRATEGIES = {
        'bomber': {
            'opcodes': [Opcode.MOV, Opcode.ADD, Opcode.JMP],
            'description': 'Drops DAT bombs across core'
        },
        'scanner': {
            'opcodes': [Opcode.CMP, Opcode.JMN, Opcode.ADD, Opcode.MOV],
            'description': 'Scans for enemies then attacks'
        },
        'replicator': {
            'opcodes': [Opcode.SPL, Opcode.MOV, Opcode.DJN],
            'description': 'Creates copies of itself'
        },
        'dwarf': {
            'opcodes': [Opcode.ADD, Opcode.MOV, Opcode.JMP],
            'description': 'Small bomber that drops DAT bombs at intervals'
        },
        'imp': {
            'opcodes': [Opcode.MOV, Opcode.JMP],
            'description': 'Simple self-copying program'
        },
        'paper': {
            'opcodes': [Opcode.SPL, Opcode.MOV, Opcode.DJN, Opcode.JMP],
            'description': 'Replicates and spreads quickly'
        }
    }
    
    @staticmethod
    def random_instruction(strategy: str = None) -> Instruction:
        """Generate a random instruction, optionally following a strategy."""
        if strategy and strategy in WarriorGenerator.STRATEGIES:
            opcodes = WarriorGenerator.STRATEGIES[strategy]['opcodes']
            opcode = random.choice(opcodes)
        else:
            # Weighted random selection
            opcode_weights = {
                Opcode.MOV: 25,
                Opcode.ADD: 15,
                Opcode.SUB: 10,
                Opcode.JMP: 15,
                Opcode.JMZ: 8,
                Opcode.JMN: 8,
                Opcode.DJN: 10,
                Opcode.CMP: 5,
                Opcode.SPL: 8,
                Opcode.DAT: 5,
                Opcode.NOP: 1
            }
            opcodes = list(opcode_weights.keys())
            weights = list(opcode_weights.values())
            opcode = random.choices(opcodes, weights=weights)[0]
        
        # Generate addressing modes and values
        modes = [AddressMode.IMMEDIATE, AddressMode.DIRECT, AddressMode.INDIRECT,
                AddressMode.PREDECREMENT, AddressMode.POSTINCREMENT]
        
        a_mode = random.choice(modes)
        b_mode = random.choice(modes)
        
        # Generate values based on opcode type
        if opcode in [Opcode.JMP, Opcode.JMZ, Opcode.JMN, Opcode.DJN, Opcode.SPL]:
            # Jump instructions need reasonable offsets
            a_value = random.randint(-20, 20)
            b_value = random.randint(-20, 20)
        elif opcode == Opcode.DAT:
            # DAT is just data
            a_value = random.randint(-100, 100)
            b_value = random.randint(-100, 100)
        else:
            # Most instructions work with small values
            a_value = random.randint(-10, 10)
            b_value = random.randint(-10, 10)
        
        return Instruction(opcode, a_mode, a_value, b_mode, b_value)
    
    @staticmethod
    def generate_warrior(name: str, length: int = None, strategy: str = None) -> Warrior:
        """Generate a random warrior with given strategy."""
        if length is None:
            length = random.randint(5, 30)
        
        program = []
        
        # Special case for known patterns
        if strategy == 'imp':
            # Classic imp: MOV 0, 1
            program = [Instruction(Opcode.MOV, AddressMode.DIRECT, 0, AddressMode.DIRECT, 1)]
        elif strategy == 'dwarf':
            # Classic dwarf bomber
            program = [
                Instruction(Opcode.ADD, AddressMode.IMMEDIATE, 4, AddressMode.DIRECT, 3),
                Instruction(Opcode.MOV, AddressMode.DIRECT, 2, AddressMode.INDIRECT, 2),
                Instruction(Opcode.JMP, AddressMode.DIRECT, -2, AddressMode.DIRECT, 0),
                Instruction(Opcode.DAT, AddressMode.IMMEDIATE, 0, AddressMode.IMMEDIATE, 0)
            ]
        else:
            # Generate random program following strategy
            for _ in range(length):
                program.append(WarriorGenerator.random_instruction(strategy))
        
        return Warrior(name, program, author=f"AI-{strategy or 'random'}")

class GeneticWarriorEvolver:
    """Evolve warriors using genetic algorithms."""
    
    def __init__(self, population_size: int = 20, mutation_rate: float = 0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generation = 0
        self.population: List[Tuple[Warrior, float]] = []
        
    def initialize_population(self):
        """Create initial population with various strategies."""
        strategies = list(WarriorGenerator.STRATEGIES.keys())
        self.population = []
        
        for i in range(self.population_size):
            strategy = random.choice(strategies + [None])  # Include some random warriors
            warrior = WarriorGenerator.generate_warrior(
                f"Gen{self.generation}-W{i}",
                strategy=strategy
            )
            self.population.append((warrior, 0.0))
    
    def evaluate_fitness(self, warrior: Warrior, test_opponents: List[Warrior] = None) -> float:
        """Evaluate warrior fitness by battling against opponents."""
        if test_opponents is None:
            # Battle against some standard opponents
            test_opponents = [
                WarriorGenerator.generate_warrior("Imp", strategy='imp'),
                WarriorGenerator.generate_warrior("Dwarf", strategy='dwarf'),
                WarriorGenerator.generate_warrior("Scanner", strategy='scanner'),
                WarriorGenerator.generate_warrior("Random", strategy=None)
            ]
        
        wins = 0
        total_battles = len(test_opponents)
        
        for opponent in test_opponents:
            # Run battle
            mars = MARS(core_size=8000, max_cycles=80000)
            mars.load_warrior(Warrior(warrior.name, warrior.program[:], warrior.author))
            mars.load_warrior(Warrior(opponent.name, opponent.program[:], opponent.author))
            
            winner = mars.run_battle()
            if winner and winner.name == warrior.name:
                wins += 1
            elif winner is None:  # Draw
                wins += 0.5
        
        return wins / total_battles
    
    def mutate_instruction(self, inst: Instruction) -> Instruction:
        """Mutate a single instruction."""
        if random.random() < 0.3:  # Change opcode
            new_opcode = random.choice(list(Opcode))
            return Instruction(new_opcode, inst.a_mode, inst.a_value, inst.b_mode, inst.b_value)
        elif random.random() < 0.5:  # Change values
            a_value = inst.a_value + random.randint(-2, 2)
            b_value = inst.b_value + random.randint(-2, 2)
            return Instruction(inst.opcode, inst.a_mode, a_value, inst.b_mode, b_value)
        else:  # Change addressing modes
            modes = [AddressMode.IMMEDIATE, AddressMode.DIRECT, AddressMode.INDIRECT,
                    AddressMode.PREDECREMENT, AddressMode.POSTINCREMENT]
            a_mode = random.choice(modes)
            b_mode = random.choice(modes)
            return Instruction(inst.opcode, a_mode, inst.a_value, b_mode, inst.b_value)
    
    def mutate_warrior(self, warrior: Warrior) -> Warrior:
        """Create mutated version of warrior."""
        new_program = []
        
        for inst in warrior.program:
            if random.random() < self.mutation_rate:
                new_program.append(self.mutate_instruction(inst))
            else:
                new_program.append(inst)
        
        # Sometimes add/remove instructions
        if random.random() < 0.1 and len(new_program) > 2:  # Remove
            new_program.pop(random.randint(0, len(new_program) - 1))
        elif random.random() < 0.1 and len(new_program) < 50:  # Add
            pos = random.randint(0, len(new_program))
            new_program.insert(pos, WarriorGenerator.random_instruction())
        
        return Warrior(f"{warrior.name}-mut", new_program, warrior.author)
    
    def crossover(self, parent1: Warrior, parent2: Warrior) -> Warrior:
        """Create offspring from two parent warriors."""
        # Choose crossover point
        min_length = min(len(parent1.program), len(parent2.program))
        if min_length < 2:
            return parent1  # Too short to crossover
        
        crossover_point = random.randint(1, min_length - 1)
        
        # Create offspring
        new_program = parent1.program[:crossover_point] + parent2.program[crossover_point:]
        
        return Warrior(f"Gen{self.generation}-cross", new_program, "AI-evolved")
    
    def evolve_generation(self):
        """Evolve population to next generation."""
        # Evaluate fitness for all warriors
        for i, (warrior, _) in enumerate(self.population):
            fitness = self.evaluate_fitness(warrior)
            self.population[i] = (warrior, fitness)
        
        # Sort by fitness
        self.population.sort(key=lambda x: x[1], reverse=True)
        
        # Select top performers
        elite_count = self.population_size // 4
        new_population = self.population[:elite_count]
        
        # Generate offspring
        while len(new_population) < self.population_size:
            # Tournament selection
            parent1 = self.tournament_select()
            parent2 = self.tournament_select()
            
            # Crossover
            if random.random() < 0.7:
                offspring = self.crossover(parent1[0], parent2[0])
            else:
                offspring = parent1[0]
            
            # Mutation
            if random.random() < 0.8:
                offspring = self.mutate_warrior(offspring)
            
            offspring.name = f"Gen{self.generation+1}-W{len(new_population)}"
            new_population.append((offspring, 0.0))
        
        self.population = new_population
        self.generation += 1
    
    def tournament_select(self, tournament_size: int = 3) -> Tuple[Warrior, float]:
        """Select warrior using tournament selection."""
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        return max(tournament, key=lambda x: x[1])
    
    def get_best_warrior(self) -> Warrior:
        """Get the current best warrior."""
        return max(self.population, key=lambda x: x[1])[0]

class AIAgent:
    """High-level AI agent that manages warrior creation and evolution."""
    
    def __init__(self, name: str, strategy_preference: List[str] = None):
        self.name = name
        self.strategy_preference = strategy_preference or list(WarriorGenerator.STRATEGIES.keys())
        self.evolver = GeneticWarriorEvolver()
        self.battle_history = []
        
    def create_warrior(self) -> Warrior:
        """Create a new warrior using current knowledge."""
        if self.evolver.generation == 0:
            # First generation: use preferred strategy
            strategy = random.choice(self.strategy_preference)
            warrior = WarriorGenerator.generate_warrior(
                f"{self.name}-W{self.evolver.generation}",
                strategy=strategy
            )
        else:
            # Use evolved warrior
            warrior = self.evolver.get_best_warrior()
            warrior.name = f"{self.name}-W{self.evolver.generation}"
            warrior.author = self.name
            
        return warrior
    
    def learn_from_battle(self, my_warrior: Warrior, opponent: Warrior, won: bool):
        """Learn from battle results."""
        self.battle_history.append({
            'generation': self.evolver.generation,
            'warrior': my_warrior.name,
            'opponent': opponent.name,
            'won': won
        })
        
        # Periodically evolve
        if len(self.battle_history) % 5 == 0:
            if self.evolver.generation == 0:
                self.evolver.initialize_population()
            self.evolver.evolve_generation()