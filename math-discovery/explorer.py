"""
Explorer Agents - Generate mathematical conjectures and new theorems
"""

import random
import sympy as sp
from sympy import symbols, expand, simplify, factor, collect, apart, together
from sympy import sin, cos, tan, sec, csc, cot, log, exp, sqrt, pi, E
from typing import List, Optional, Tuple
from knowledge_base import MathTheorem, MathField, Difficulty, KnowledgeBase
import itertools
import time

class ExplorationStrategy:
    """Base class for exploration strategies."""
    
    def generate_conjecture(self, kb: KnowledgeBase) -> Optional[MathTheorem]:
        """Generate a new mathematical conjecture."""
        raise NotImplementedError

class GeneralizationStrategy(ExplorationStrategy):
    """Generalize existing theorems to higher dimensions or more variables."""
    
    def generate_conjecture(self, kb: KnowledgeBase) -> Optional[MathTheorem]:
        # Pick a random theorem to generalize
        base_theorems = [t for t in kb.theorems.values() 
                        if t.field == MathField.ALGEBRA and t.difficulty <= Difficulty.HIGH_SCHOOL]
        
        if not base_theorems:
            return None
        
        base = random.choice(base_theorems)
        
        # Try different generalization approaches
        approach = random.choice(['add_variable', 'higher_power', 'parametrize'])
        
        if approach == 'add_variable':
            # E.g., (a+b)^2 -> (a+b+c)^2
            if '(a+b)' in base.statement:
                new_statement = base.statement.replace('(a+b)', '(a+b+c)')
                # Generate symbolic form
                a, b, c = symbols('a b c')
                
                if '^2' in new_statement:
                    expr = (a + b + c)**2
                    expanded = expand(expr)
                    symbolic = f"(a + b + c)**2 - ({expanded})"
                    
                    return MathTheorem(
                        id=f"gen_{int(time.time()*1000000)}",
                        statement=f"{new_statement} = {expanded}",
                        symbolic_form=symbolic,
                        field=MathField.ALGEBRA,
                        difficulty=Difficulty.ADVANCED,
                        discovered_by="GeneralizationAgent",
                        timestamp=time.time(),
                        related_to=[base.id]
                    )
        
        elif approach == 'higher_power':
            # E.g., a^2 - b^2 -> a^4 - b^4
            if '^2' in base.statement:
                new_statement = base.statement.replace('^2', '^4')
                a, b = symbols('a b')
                
                if 'a^4 - b^4' in new_statement:
                    # Factor a^4 - b^4
                    expr = a**4 - b**4
                    factored = factor(expr)
                    
                    return MathTheorem(
                        id=f"gen_{int(time.time()*1000000)}",
                        statement=f"a^4 - b^4 = {factored}",
                        symbolic_form=f"a**4 - b**4 - ({factored})",
                        field=MathField.ALGEBRA,
                        difficulty=Difficulty.ADVANCED,
                        discovered_by="GeneralizationAgent",
                        timestamp=time.time(),
                        related_to=[base.id]
                    )
        
        return None

class CombinationStrategy(ExplorationStrategy):
    """Combine multiple known theorems to create new ones."""
    
    def generate_conjecture(self, kb: KnowledgeBase) -> Optional[MathTheorem]:
        # Pick two compatible theorems
        algebra_theorems = kb.get_by_field(MathField.ALGEBRA)
        
        if len(algebra_theorems) < 2:
            return None
        
        theorem1, theorem2 = random.sample(algebra_theorems, 2)
        
        # Try to combine them
        a, b, c, d = symbols('a b c d')
        
        # Example: Combine (a+b)^2 and (c-d)^2
        if '(a+b)^2' in theorem1.statement and '(a-b)^2' in theorem2.statement:
            # Create: ((a+b)^2 + (a-b)^2)/2 = a^2 + b^2
            expr1 = (a + b)**2
            expr2 = (a - b)**2
            combined = (expr1 + expr2) / 2
            simplified = simplify(combined)
            
            return MathTheorem(
                id=f"comb_{int(time.time()*1000000)}",
                statement=f"((a+b)^2 + (a-b)^2)/2 = {simplified}",
                symbolic_form=f"((a+b)**2 + (a-b)**2)/2 - ({simplified})",
                field=MathField.ALGEBRA,
                difficulty=Difficulty.ADVANCED,
                discovered_by="CombinationAgent",
                timestamp=time.time(),
                related_to=[theorem1.id, theorem2.id]
            )
        
        # Try multiplicative combination
        if random.random() < 0.5:
            # Example: (a^2 - b^2) * (c^2 - d^2)
            expr = (a**2 - b**2) * (c**2 - d**2)
            expanded = expand(expr)
            
            return MathTheorem(
                id=f"comb_{int(time.time()*1000000)}",
                statement=f"(a^2 - b^2)(c^2 - d^2) = {expanded}",
                symbolic_form=f"(a**2 - b**2)*(c**2 - d**2) - ({expanded})",
                field=MathField.ALGEBRA,
                difficulty=Difficulty.ADVANCED,
                discovered_by="CombinationAgent",
                timestamp=time.time(),
                related_to=[theorem1.id, theorem2.id]
            )
        
        return None

class SymmetryStrategy(ExplorationStrategy):
    """Explore symmetric properties and transformations."""
    
    def generate_conjecture(self, kb: KnowledgeBase) -> Optional[MathTheorem]:
        a, b, c = symbols('a b c')
        
        # Generate symmetric expressions
        patterns = [
            # Cyclic symmetry
            (a*b + b*c + c*a, "Cyclic sum: ab + bc + ca"),
            (a**2*b + b**2*c + c**2*a, "Cyclic: a^2*b + b^2*c + c^2*a"),
            # Symmetric polynomials
            ((a + b)*(b + c)*(c + a), "Product of pairwise sums"),
            (a**3 + b**3 + c**3 - 3*a*b*c, "Sum of cubes minus triple product"),
        ]
        
        expr, description = random.choice(patterns)
        
        # Try to find interesting properties
        expanded = expand(expr)
        factored = factor(expr)
        
        # Check if we found something non-trivial
        if factored != expr and factored != expanded:
            return MathTheorem(
                id=f"sym_{int(time.time()*1000000)}",
                statement=f"{description}: {expr} = {factored}",
                symbolic_form=f"{expr} - ({factored})",
                field=MathField.ALGEBRA,
                difficulty=Difficulty.ADVANCED,
                discovered_by="SymmetryAgent",
                timestamp=time.time()
            )
        
        # Try symmetric inequalities
        if random.random() < 0.3:
            # Arithmetic-Geometric mean style
            arithmetic = (a + b + c) / 3
            geometric = (a * b * c)**(1/3)
            
            return MathTheorem(
                id=f"sym_{int(time.time()*1000000)}",
                statement=f"For positive a,b,c: (a+b+c)/3 >= (abc)^(1/3)",
                symbolic_form=None,  # Inequalities need different handling
                field=MathField.ALGEBRA,
                difficulty=Difficulty.ADVANCED,
                discovered_by="SymmetryAgent",
                timestamp=time.time(),
                proof_sketch="AM-GM inequality for three variables"
            )
        
        return None

class TrigonometricExplorer(ExplorationStrategy):
    """Explore new trigonometric identities."""
    
    def generate_conjecture(self, kb: KnowledgeBase) -> Optional[MathTheorem]:
        x, y = symbols('x y')
        
        # Generate combinations of trig functions
        patterns = [
            # Sum-to-product identities
            (sin(x) + sin(y), "sin(x) + sin(y)"),
            (cos(x) + cos(y), "cos(x) + cos(y)"),
            (sin(x)*cos(y) + cos(x)*sin(y), "sin(x)cos(y) + cos(x)sin(y)"),
            # Triple angle formulas
            (sin(3*x), "sin(3x)"),
            (cos(3*x), "cos(3x)"),
            # Half-angle formulas
            (sin(x/2), "sin(x/2)"),
            (cos(x/2), "cos(x/2)"),
            # Power reduction
            (sin(x)**3, "sin^3(x)"),
            (cos(x)**3, "cos^3(x)"),
        ]
        
        expr, description = random.choice(patterns)
        
        # Try to simplify or expand
        try:
            simplified = sp.trigsimp(expr)
            expanded = sp.expand_trig(expr)
            
            # Check if we found something interesting
            if simplified != expr:
                return MathTheorem(
                    id=f"trig_{int(time.time()*1000000)}",
                    statement=f"{description} = {simplified}",
                    symbolic_form=f"{expr} - ({simplified})",
                    field=MathField.TRIGONOMETRY,
                    difficulty=Difficulty.ADVANCED,
                    discovered_by="TrigonometricExplorer",
                    timestamp=time.time()
                )
            elif expanded != expr:
                return MathTheorem(
                    id=f"trig_{int(time.time()*1000000)}",
                    statement=f"{description} = {expanded}",
                    symbolic_form=f"{expr} - ({expanded})",
                    field=MathField.TRIGONOMETRY,
                    difficulty=Difficulty.ADVANCED,
                    discovered_by="TrigonometricExplorer",
                    timestamp=time.time()
                )
        except:
            pass
        
        # Try specific identities
        if random.random() < 0.3:
            # Generate product-to-sum identity
            expr = sin(x) * sin(y)
            simplified = (cos(x - y) - cos(x + y)) / 2
            
            return MathTheorem(
                id=f"trig_{int(time.time()*1000000)}",
                statement=f"sin(x)sin(y) = (cos(x-y) - cos(x+y))/2",
                symbolic_form=f"sin(x)*sin(y) - (cos(x-y) - cos(x+y))/2",
                field=MathField.TRIGONOMETRY,
                difficulty=Difficulty.ADVANCED,
                discovered_by="TrigonometricExplorer",
                timestamp=time.time()
            )
        
        return None

class PatternRecognitionStrategy(ExplorationStrategy):
    """Look for patterns in sequences and series."""
    
    def generate_conjecture(self, kb: KnowledgeBase) -> Optional[MathTheorem]:
        n = symbols('n', integer=True, positive=True)
        
        # Generate interesting sequences
        patterns = [
            # Sum of powers
            (sum(k**2 for k in range(1, 6)), "1^2 + 2^2 + ... + n^2"),
            (sum(k**3 for k in range(1, 6)), "1^3 + 2^3 + ... + n^3"),
            # Fibonacci-like
            (1, 1, 2, 3, 5, 8, "Fibonacci sequence"),
            # Factorials
            (1, 1, 2, 6, 24, 120, "n!"),
            # Triangular numbers
            (1, 3, 6, 10, 15, "Triangular numbers"),
        ]
        
        # Try to find closed forms
        if random.random() < 0.5:
            # Sum of first n squares
            formula = n * (n + 1) * (2*n + 1) / 6
            
            return MathTheorem(
                id=f"pat_{int(time.time()*1000000)}",
                statement=f"Sum of first n squares: 1^2 + 2^2 + ... + n^2 = n(n+1)(2n+1)/6",
                symbolic_form=f"Sum(k**2, (k, 1, n)) - n*(n+1)*(2*n+1)/6",
                field=MathField.COMBINATORICS,
                difficulty=Difficulty.ADVANCED,
                discovered_by="PatternRecognizer",
                timestamp=time.time()
            )
        
        # Binomial patterns
        if random.random() < 0.3:
            k = symbols('k', integer=True)
            # Pascal's triangle property
            return MathTheorem(
                id=f"pat_{int(time.time()*1000000)}",
                statement=f"C(n,k) + C(n,k+1) = C(n+1,k+1)",
                symbolic_form=None,
                field=MathField.COMBINATORICS,
                difficulty=Difficulty.ADVANCED,
                discovered_by="PatternRecognizer",
                timestamp=time.time(),
                proof_sketch="Pascal's triangle recursive property"
            )
        
        return None

class ExplorerAgent:
    """Agent that uses multiple strategies to explore mathematical space."""
    
    def __init__(self, name: str, strategies: List[ExplorationStrategy] = None):
        self.name = name
        self.strategies = strategies or [
            GeneralizationStrategy(),
            CombinationStrategy(),
            SymmetryStrategy(),
            TrigonometricExplorer(),
            PatternRecognitionStrategy()
        ]
        self.discoveries = []
        self.attempts = 0
        self.successes = 0
        
    def explore(self, kb: KnowledgeBase) -> Optional[MathTheorem]:
        """Attempt to discover a new theorem."""
        self.attempts += 1
        
        # Choose a random strategy
        strategy = random.choice(self.strategies)
        
        try:
            conjecture = strategy.generate_conjecture(kb)
            
            if conjecture:
                conjecture.discovered_by = self.name
                return conjecture
        except Exception as e:
            # Exploration can fail due to symbolic computation issues
            pass
        
        return None
    
    def record_success(self, theorem: MathTheorem):
        """Record a successful discovery."""
        self.successes += 1
        self.discoveries.append(theorem.id)
    
    def get_stats(self) -> dict:
        """Get agent statistics."""
        return {
            'name': self.name,
            'attempts': self.attempts,
            'successes': self.successes,
            'success_rate': self.successes / max(1, self.attempts),
            'discoveries': self.discoveries
        }