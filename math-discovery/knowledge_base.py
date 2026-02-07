"""
Mathematical Knowledge Base - Starting with high school identities
"""

import json
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sympy as sp
from sympy import symbols, simplify, expand, factor, trigsimp, solve, Eq
import numpy as np

class MathField(Enum):
    ALGEBRA = "algebra"
    TRIGONOMETRY = "trigonometry"
    GEOMETRY = "geometry"
    CALCULUS = "calculus"
    NUMBER_THEORY = "number_theory"
    COMBINATORICS = "combinatorics"

class Difficulty(Enum):
    ELEMENTARY = 1
    HIGH_SCHOOL = 2
    ADVANCED = 3
    RESEARCH = 4

@dataclass
class MathTheorem:
    """Represents a mathematical theorem or identity."""
    id: str
    statement: str
    symbolic_form: Optional[str]  # SymPy expression as string
    field: MathField
    difficulty: Difficulty
    discovered_by: str
    timestamp: float
    proof_sketch: Optional[str] = None
    counterexample: Optional[str] = None
    is_novel: bool = True
    related_to: List[str] = None
    
    def __post_init__(self):
        if self.related_to is None:
            self.related_to = []

class KnowledgeBase:
    """Repository of mathematical knowledge."""
    
    def __init__(self):
        self.theorems: Dict[str, MathTheorem] = {}
        self.discovery_log = []
        self._initialize_base_knowledge()
        
    def _initialize_base_knowledge(self):
        """Initialize with fundamental high school identities."""
        
        # Algebraic Identities
        algebraic_identities = [
            # Basic expansions
            ("alg_001", "(a+b)^2 = a^2 + 2*a*b + b^2", 
             "(a + b)**2 - (a**2 + 2*a*b + b**2)"),
            ("alg_002", "(a-b)^2 = a^2 - 2*a*b + b^2",
             "(a - b)**2 - (a**2 - 2*a*b + b**2)"),
            ("alg_003", "a^2 - b^2 = (a+b)(a-b)",
             "a**2 - b**2 - (a + b)*(a - b)"),
            ("alg_004", "(a+b)^3 = a^3 + 3*a^2*b + 3*a*b^2 + b^3",
             "(a + b)**3 - (a**3 + 3*a**2*b + 3*a*b**2 + b**3)"),
            ("alg_005", "(a-b)^3 = a^3 - 3*a^2*b + 3*a*b^2 - b^3",
             "(a - b)**3 - (a**3 - 3*a**2*b + 3*a*b**2 - b**3)"),
            ("alg_006", "a^3 + b^3 = (a+b)(a^2 - a*b + b^2)",
             "a**3 + b**3 - (a + b)*(a**2 - a*b + b**2)"),
            ("alg_007", "a^3 - b^3 = (a-b)(a^2 + a*b + b^2)",
             "a**3 - b**3 - (a - b)*(a**2 + a*b + b**2)"),
            # More complex
            ("alg_008", "(a+b+c)^2 = a^2 + b^2 + c^2 + 2(ab + bc + ca)",
             "(a + b + c)**2 - (a**2 + b**2 + c**2 + 2*(a*b + b*c + c*a))"),
            ("alg_009", "a^3 + b^3 + c^3 - 3abc = (a+b+c)(a^2+b^2+c^2-ab-bc-ca)",
             "a**3 + b**3 + c**3 - 3*a*b*c - (a+b+c)*(a**2+b**2+c**2-a*b-b*c-c*a)"),
        ]
        
        for id, statement, symbolic in algebraic_identities:
            self.add_theorem(MathTheorem(
                id=id,
                statement=statement,
                symbolic_form=symbolic,
                field=MathField.ALGEBRA,
                difficulty=Difficulty.HIGH_SCHOOL,
                discovered_by="Classical",
                timestamp=0,
                is_novel=False
            ))
        
        # Trigonometric Identities
        trig_identities = [
            ("trig_001", "sin^2(x) + cos^2(x) = 1",
             "sin(x)**2 + cos(x)**2 - 1"),
            ("trig_002", "1 + tan^2(x) = sec^2(x)",
             "1 + tan(x)**2 - sec(x)**2"),
            ("trig_003", "1 + cot^2(x) = csc^2(x)",
             "1 + cot(x)**2 - csc(x)**2"),
            ("trig_004", "sin(2x) = 2*sin(x)*cos(x)",
             "sin(2*x) - 2*sin(x)*cos(x)"),
            ("trig_005", "cos(2x) = cos^2(x) - sin^2(x)",
             "cos(2*x) - (cos(x)**2 - sin(x)**2)"),
            ("trig_006", "cos(2x) = 2*cos^2(x) - 1",
             "cos(2*x) - (2*cos(x)**2 - 1)"),
            ("trig_007", "cos(2x) = 1 - 2*sin^2(x)",
             "cos(2*x) - (1 - 2*sin(x)**2)"),
            ("trig_008", "tan(2x) = 2*tan(x)/(1 - tan^2(x))",
             "tan(2*x) - 2*tan(x)/(1 - tan(x)**2)"),
            ("trig_009", "sin(a+b) = sin(a)*cos(b) + cos(a)*sin(b)",
             "sin(a + b) - (sin(a)*cos(b) + cos(a)*sin(b))"),
            ("trig_010", "cos(a+b) = cos(a)*cos(b) - sin(a)*sin(b)",
             "cos(a + b) - (cos(a)*cos(b) - sin(a)*sin(b))"),
        ]
        
        for id, statement, symbolic in trig_identities:
            self.add_theorem(MathTheorem(
                id=id,
                statement=statement,
                symbolic_form=symbolic,
                field=MathField.TRIGONOMETRY,
                difficulty=Difficulty.HIGH_SCHOOL,
                discovered_by="Classical",
                timestamp=0,
                is_novel=False
            ))
        
        # Logarithmic and Exponential
        log_identities = [
            ("log_001", "log(ab) = log(a) + log(b)",
             "log(a*b) - (log(a) + log(b))"),
            ("log_002", "log(a/b) = log(a) - log(b)",
             "log(a/b) - (log(a) - log(b))"),
            ("log_003", "log(a^n) = n*log(a)",
             "log(a**n) - n*log(a)"),
            ("log_004", "a^(log_a(x)) = x",
             "a**(log(x)/log(a)) - x"),
        ]
        
        for id, statement, symbolic in log_identities:
            self.add_theorem(MathTheorem(
                id=id,
                statement=statement,
                symbolic_form=symbolic,
                field=MathField.ALGEBRA,
                difficulty=Difficulty.HIGH_SCHOOL,
                discovered_by="Classical",
                timestamp=0,
                is_novel=False
            ))
    
    def add_theorem(self, theorem: MathTheorem) -> bool:
        """Add a new theorem to the knowledge base."""
        if theorem.id in self.theorems:
            return False
        
        self.theorems[theorem.id] = theorem
        self.discovery_log.append({
            'id': theorem.id,
            'timestamp': theorem.timestamp,
            'discovered_by': theorem.discovered_by,
            'is_novel': theorem.is_novel,
            'field': theorem.field.value
        })
        return True
    
    def search_similar(self, statement: str, symbolic_form: str = None) -> List[MathTheorem]:
        """Search for similar theorems in the knowledge base."""
        similar = []
        
        if symbolic_form:
            try:
                # Parse the new expression
                expr = sp.sympify(symbolic_form)
                
                for theorem in self.theorems.values():
                    if theorem.symbolic_form:
                        try:
                            known_expr = sp.sympify(theorem.symbolic_form)
                            # Check if expressions are equivalent
                            if simplify(expr - known_expr) == 0:
                                similar.append(theorem)
                            # Check if one is a special case of the other
                            elif self._is_special_case(expr, known_expr):
                                similar.append(theorem)
                        except:
                            pass
            except:
                pass
        
        # Text-based similarity (simple keyword matching)
        keywords = set(statement.lower().split())
        for theorem in self.theorems.values():
            theorem_keywords = set(theorem.statement.lower().split())
            overlap = len(keywords & theorem_keywords)
            if overlap > min(3, len(keywords) // 2):
                if theorem not in similar:
                    similar.append(theorem)
        
        return similar
    
    def _is_special_case(self, expr1, expr2) -> bool:
        """Check if one expression is a special case of another."""
        # This is a simplified check - could be made more sophisticated
        try:
            # Check if substituting specific values makes them equal
            test_values = [
                {symbols('a'): 1, symbols('b'): 1},
                {symbols('a'): 0, symbols('b'): 1},
                {symbols('a'): 1, symbols('b'): 0},
            ]
            
            for vals in test_values:
                if expr1.subs(vals) == expr2.subs(vals):
                    return True
        except:
            pass
        
        return False
    
    def get_by_field(self, field: MathField) -> List[MathTheorem]:
        """Get all theorems in a specific field."""
        return [t for t in self.theorems.values() if t.field == field]
    
    def get_novel_discoveries(self) -> List[MathTheorem]:
        """Get all novel discoveries."""
        return [t for t in self.theorems.values() if t.is_novel]
    
    def get_statistics(self) -> Dict:
        """Get statistics about the knowledge base."""
        stats = {
            'total_theorems': len(self.theorems),
            'novel_discoveries': len(self.get_novel_discoveries()),
            'by_field': {},
            'by_difficulty': {},
            'discovery_rate': []
        }
        
        for field in MathField:
            stats['by_field'][field.value] = len(self.get_by_field(field))
        
        for difficulty in Difficulty:
            stats['by_difficulty'][difficulty.value] = len([
                t for t in self.theorems.values() if t.difficulty == difficulty
            ])
        
        # Calculate discovery rate over time windows
        if self.discovery_log:
            current_time = time.time()
            time_windows = [3600, 86400, 604800]  # 1 hour, 1 day, 1 week
            
            for window in time_windows:
                recent = [
                    d for d in self.discovery_log
                    if current_time - d['timestamp'] < window and d['is_novel']
                ]
                stats['discovery_rate'].append({
                    'window_seconds': window,
                    'discoveries': len(recent)
                })
        
        return stats
    
    def save_to_file(self, filename: str):
        """Save knowledge base to JSON file."""
        data = {
            'theorems': [asdict(t) for t in self.theorems.values()],
            'discovery_log': self.discovery_log,
            'statistics': self.get_statistics()
        }
        
        # Convert enums to strings
        for theorem in data['theorems']:
            theorem['field'] = theorem['field'].value
            theorem['difficulty'] = theorem['difficulty'].value
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filename: str):
        """Load knowledge base from JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.theorems.clear()
        self.discovery_log = data.get('discovery_log', [])
        
        for theorem_data in data['theorems']:
            # Convert strings back to enums
            theorem_data['field'] = MathField(theorem_data['field'])
            theorem_data['difficulty'] = Difficulty(theorem_data['difficulty'])
            
            theorem = MathTheorem(**theorem_data)
            self.theorems[theorem.id] = theorem