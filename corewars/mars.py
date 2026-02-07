"""
MARS (Memory Array Redcode Simulator) - Core Wars Virtual Machine
"""

import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple

class AddressMode(Enum):
    IMMEDIATE = '#'  # Immediate value
    DIRECT = '$'     # Direct addressing
    INDIRECT = '@'   # Indirect addressing
    PREDECREMENT = '<'  # Pre-decrement indirect
    POSTINCREMENT = '>'  # Post-increment indirect

class Opcode(Enum):
    DAT = 'DAT'  # Data (kills process)
    MOV = 'MOV'  # Move
    ADD = 'ADD'  # Add
    SUB = 'SUB'  # Subtract
    MUL = 'MUL'  # Multiply
    DIV = 'DIV'  # Divide
    MOD = 'MOD'  # Modulo
    JMP = 'JMP'  # Jump
    JMZ = 'JMZ'  # Jump if zero
    JMN = 'JMN'  # Jump if not zero
    DJN = 'DJN'  # Decrement and jump if not zero
    CMP = 'CMP'  # Compare (skip if equal)
    SEQ = 'SEQ'  # Skip if equal (same as CMP)
    SNE = 'SNE'  # Skip if not equal
    SLT = 'SLT'  # Skip if less than
    SPL = 'SPL'  # Split (fork process)
    NOP = 'NOP'  # No operation

@dataclass
class Instruction:
    opcode: Opcode
    a_mode: AddressMode
    a_value: int
    b_mode: AddressMode
    b_value: int
    
    def __str__(self):
        return f"{self.opcode.value} {self.a_mode.value}{self.a_value}, {self.b_mode.value}{self.b_value}"

class Warrior:
    def __init__(self, name: str, program: List[Instruction], author: str = "AI"):
        self.name = name
        self.author = author
        self.program = program
        self.processes: List[int] = []
        self.start_address: int = 0
        
    def __str__(self):
        return f"Warrior({self.name} by {self.author}, {len(self.program)} instructions)"

class MARS:
    def __init__(self, core_size: int = 8000, max_cycles: int = 80000, 
                 max_processes: int = 8000, max_length: int = 100):
        self.core_size = core_size
        self.max_cycles = max_cycles
        self.max_processes = max_processes
        self.max_length = max_length
        
        # Initialize core with DAT 0, 0 instructions
        self.core: List[Instruction] = [
            Instruction(Opcode.DAT, AddressMode.IMMEDIATE, 0, AddressMode.IMMEDIATE, 0)
            for _ in range(core_size)
        ]
        
        # Tracking data
        self.warriors: List[Warrior] = []
        self.current_warrior = 0
        self.cycle = 0
        self.winner: Optional[Warrior] = None
        
    def load_warrior(self, warrior: Warrior, address: Optional[int] = None):
        """Load a warrior into the core at the specified address."""
        if address is None:
            # Random placement with minimum separation
            min_separation = self.core_size // (len(self.warriors) + 1)
            address = random.randint(0, self.core_size - len(warrior.program) - 1)
            
            # Ensure minimum separation from other warriors
            for other_warrior in self.warriors:
                while abs(address - other_warrior.start_address) < min_separation:
                    address = random.randint(0, self.core_size - len(warrior.program) - 1)
        
        warrior.start_address = address
        warrior.processes = [address]
        
        # Copy program into core
        for i, instruction in enumerate(warrior.program):
            self.core[(address + i) % self.core_size] = instruction
            
        self.warriors.append(warrior)
        
    def normalize(self, address: int) -> int:
        """Normalize address to core bounds."""
        return address % self.core_size
    
    def resolve_address(self, base: int, mode: AddressMode, value: int, is_write: bool = False) -> int:
        """Resolve an address based on addressing mode."""
        if mode == AddressMode.IMMEDIATE:
            return base
        elif mode == AddressMode.DIRECT:
            return self.normalize(base + value)
        elif mode == AddressMode.INDIRECT:
            pointer_addr = self.normalize(base + value)
            pointer = self.core[pointer_addr]
            return self.normalize(pointer_addr + pointer.b_value)
        elif mode == AddressMode.PREDECREMENT:
            pointer_addr = self.normalize(base + value)
            self.core[pointer_addr].b_value -= 1
            return self.normalize(pointer_addr + self.core[pointer_addr].b_value)
        elif mode == AddressMode.POSTINCREMENT:
            pointer_addr = self.normalize(base + value)
            result = self.normalize(pointer_addr + self.core[pointer_addr].b_value)
            self.core[pointer_addr].b_value += 1
            return result
        return base
    
    def execute_instruction(self, warrior: Warrior, pc: int) -> List[int]:
        """Execute a single instruction and return new program counter(s)."""
        inst = self.core[pc]
        
        # Resolve addresses
        a_addr = self.resolve_address(pc, inst.a_mode, inst.a_value)
        b_addr = self.resolve_address(pc, inst.b_mode, inst.b_value, is_write=True)
        
        # Get values (immediate mode uses the value directly)
        if inst.a_mode == AddressMode.IMMEDIATE:
            a_val = inst.a_value
        else:
            a_val = self.core[a_addr].b_value
            
        if inst.b_mode == AddressMode.IMMEDIATE:
            b_val = inst.b_value
        else:
            b_val = self.core[b_addr].b_value
        
        # Execute opcode
        if inst.opcode == Opcode.DAT:
            return []  # Process dies
            
        elif inst.opcode == Opcode.MOV:
            if inst.a_mode == AddressMode.IMMEDIATE:
                self.core[b_addr].b_value = inst.a_value
            else:
                self.core[b_addr] = self.core[a_addr]
            return [self.normalize(pc + 1)]
            
        elif inst.opcode == Opcode.ADD:
            self.core[b_addr].b_value += a_val
            return [self.normalize(pc + 1)]
            
        elif inst.opcode == Opcode.SUB:
            self.core[b_addr].b_value -= a_val
            return [self.normalize(pc + 1)]
            
        elif inst.opcode == Opcode.MUL:
            self.core[b_addr].b_value *= a_val
            return [self.normalize(pc + 1)]
            
        elif inst.opcode == Opcode.DIV:
            if a_val != 0:
                self.core[b_addr].b_value //= a_val
            return [self.normalize(pc + 1)]
            
        elif inst.opcode == Opcode.MOD:
            if a_val != 0:
                self.core[b_addr].b_value %= a_val
            return [self.normalize(pc + 1)]
            
        elif inst.opcode == Opcode.JMP:
            return [a_addr]
            
        elif inst.opcode == Opcode.JMZ:
            if b_val == 0:
                return [a_addr]
            return [self.normalize(pc + 1)]
            
        elif inst.opcode == Opcode.JMN:
            if b_val != 0:
                return [a_addr]
            return [self.normalize(pc + 1)]
            
        elif inst.opcode == Opcode.DJN:
            self.core[b_addr].b_value -= 1
            if self.core[b_addr].b_value != 0:
                return [a_addr]
            return [self.normalize(pc + 1)]
            
        elif inst.opcode in [Opcode.CMP, Opcode.SEQ]:
            if a_val == b_val:
                return [self.normalize(pc + 2)]  # Skip next instruction
            return [self.normalize(pc + 1)]
            
        elif inst.opcode == Opcode.SNE:
            if a_val != b_val:
                return [self.normalize(pc + 2)]  # Skip next instruction
            return [self.normalize(pc + 1)]
            
        elif inst.opcode == Opcode.SLT:
            if a_val < b_val:
                return [self.normalize(pc + 2)]  # Skip next instruction
            return [self.normalize(pc + 1)]
            
        elif inst.opcode == Opcode.SPL:
            # Split creates new process
            new_pcs = [self.normalize(pc + 1)]
            if len(warrior.processes) < self.max_processes:
                new_pcs.append(a_addr)
            return new_pcs
            
        elif inst.opcode == Opcode.NOP:
            return [self.normalize(pc + 1)]
            
        return [self.normalize(pc + 1)]
    
    def run_cycle(self) -> bool:
        """Run one cycle of execution. Returns True if battle continues."""
        if self.cycle >= self.max_cycles:
            return False
            
        # Track alive warriors
        alive_warriors = [w for w in self.warriors if w.processes]
        
        if len(alive_warriors) <= 1:
            if alive_warriors:
                self.winner = alive_warriors[0]
            return False
        
        # Execute one instruction per warrior
        for warrior in self.warriors:
            if not warrior.processes:
                continue
                
            # Get current process
            pc = warrior.processes.pop(0)
            
            # Execute instruction
            new_pcs = self.execute_instruction(warrior, pc)
            
            # Add new program counters to process queue
            warrior.processes.extend(new_pcs)
        
        self.cycle += 1
        return True
    
    def run_battle(self) -> Optional[Warrior]:
        """Run a complete battle until one warrior wins or max cycles reached."""
        while self.run_cycle():
            pass
        return self.winner
    
    def get_memory_state(self) -> List[int]:
        """Get current memory ownership state (0=empty, 1=warrior1, 2=warrior2, etc)."""
        state = [0] * self.core_size
        
        for i, warrior in enumerate(self.warriors, 1):
            # Mark initial program area
            for j in range(len(warrior.program)):
                addr = self.normalize(warrior.start_address + j)
                if self.core[addr].opcode != Opcode.DAT or \
                   self.core[addr].a_value != 0 or self.core[addr].b_value != 0:
                    state[addr] = i
                    
            # Mark process locations
            for pc in warrior.processes:
                state[pc] = i + 10  # Different color for execution pointers
                
        return state