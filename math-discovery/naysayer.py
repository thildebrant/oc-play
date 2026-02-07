"""
Naysayer Agent - Attempts to disprove conjectures or find prior art
"""

import sympy as sp
from sympy import symbols, simplify, expand, factor, solve, Eq
from sympy import sin, cos, tan, log, exp, sqrt, pi, E, I
import random
import numpy as np
from typing import Optional, List, Tuple
from knowledge_base import MathTheorem, KnowledgeBase

class NaysayerResponse:
    """Response from the naysayer agent."""
    
    def __init__(self, verdict: str, reason: str, evidence: Optional[str] = None):
        self.verdict = verdict  # 'rejected', 'accepted', 'trivial'
        self.reason = reason
        self.evidence = evidence
        
    def __str__(self):
        return f"{self.verdict}: {self.reason}" + (f" [{self.evidence}]" if self.evidence else "")

class NaysayerAgent:
    """Skeptical agent that tries to disprove or invalidate conjectures."""
    
    def __init__(self, name: str = "Naysayer"):
        self.name = name
        self.rejections = 0
        self.acceptances = 0
        self.trivial_count = 0
        self.evaluation_log = []
        
    def evaluate(self, conjecture: MathTheorem, kb: KnowledgeBase) -> NaysayerResponse:
        """Evaluate a conjecture for validity and novelty."""
        
        # Check 1: Is it already known?
        similar = kb.search_similar(conjecture.statement, conjecture.symbolic_form)
        if similar:
            self.rejections += 1
            self.evaluation_log.append({
                'conjecture': conjecture.id,
                'verdict': 'rejected',
                'reason': 'already_known'
            })
            return NaysayerResponse(
                'rejected',
                f"Already known or trivial variation",
                f"Similar to {similar[0].id}: {similar[0].statement}"
            )
        
        # Check 2: Is it mathematically valid?
        if conjecture.symbolic_form:
            validity = self._check_validity(conjecture.symbolic_form)
            if not validity[0]:
                self.rejections += 1
                self.evaluation_log.append({
                    'conjecture': conjecture.id,
                    'verdict': 'rejected',
                    'reason': 'invalid'
                })
                return NaysayerResponse(
                    'rejected',
                    f"Mathematically invalid",
                    validity[1]
                )
        
        # Check 3: Can we find a counterexample?
        counterexample = self._find_counterexample(conjecture)
        if counterexample:
            self.rejections += 1
            self.evaluation_log.append({
                'conjecture': conjecture.id,
                'verdict': 'rejected',
                'reason': 'counterexample'
            })
            return NaysayerResponse(
                'rejected',
                f"Counterexample found",
                counterexample
            )
        
        # Check 4: Is it trivial?
        if self._is_trivial(conjecture):
            self.trivial_count += 1
            self.evaluation_log.append({
                'conjecture': conjecture.id,
                'verdict': 'trivial',
                'reason': 'too_simple'
            })
            return NaysayerResponse(
                'trivial',
                f"Too trivial or obvious",
                "Statement reduces to known simple form"
            )
        
        # Check 5: Does it contradict known theorems?
        contradiction = self._check_contradiction(conjecture, kb)
        if contradiction:
            self.rejections += 1
            self.evaluation_log.append({
                'conjecture': conjecture.id,
                'verdict': 'rejected',
                'reason': 'contradiction'
            })
            return NaysayerResponse(
                'rejected',
                f"Contradicts known theorem",
                contradiction
            )
        
        # If we couldn't disprove it, grudgingly accept it
        self.acceptances += 1
        self.evaluation_log.append({
            'conjecture': conjecture.id,
            'verdict': 'accepted',
            'reason': 'no_issues_found'
        })
        
        return NaysayerResponse(
            'accepted',
            f"Could not disprove (yet)",
            "Passed all validation checks"
        )
    
    def _check_validity(self, symbolic_form: str) -> Tuple[bool, str]:
        """Check if the symbolic form is mathematically valid."""
        try:
            expr = sp.sympify(symbolic_form)
            
            # Check if it's supposed to be an identity (equals zero)
            if isinstance(expr, sp.Basic):
                # Try to simplify
                simplified = simplify(expr)
                
                # For identities, simplified should be 0
                if simplified == 0:
                    return (True, "Identity verified")
                
                # Try harder with trigsimp for trig identities
                if any(isinstance(arg, (sp.sin, sp.cos, sp.tan)) for arg in expr.atoms(sp.Function)):
                    trig_simplified = sp.trigsimp(expr)
                    if trig_simplified == 0:
                        return (True, "Trigonometric identity verified")
                
                # Check with random values
                vars = list(expr.free_symbols)
                if vars:
                    for _ in range(10):
                        values = {v: random.uniform(-10, 10) for v in vars}
                        result = expr.subs(values)
                        if abs(complex(result)) > 0.0001:
                            return (False, f"Not an identity: evaluates to {result} with {values}")
                    
                    return (True, "Numerically verified")
                
                return (False, f"Expression simplifies to {simplified}, not 0")
            
        except Exception as e:
            return (False, f"Could not parse expression: {str(e)}")
        
        return (True, "Could not falsify")
    
    def _find_counterexample(self, conjecture: MathTheorem) -> Optional[str]:
        """Try to find a counterexample to the conjecture."""
        
        if not conjecture.symbolic_form:
            return None
        
        try:
            expr = sp.sympify(conjecture.symbolic_form)
            vars = list(expr.free_symbols)
            
            if not vars:
                return None
            
            # Try specific edge cases
            test_cases = [
                {v: 0 for v in vars},
                {v: 1 for v in vars},
                {v: -1 for v in vars},
                {v: 2 for v in vars},
            ]
            
            # Add random cases
            for _ in range(20):
                test_cases.append({v: random.uniform(-100, 100) for v in vars})
            
            for values in test_cases:
                try:
                    result = expr.subs(values)
                    
                    # Handle complex results
                    if result.is_complex:
                        result_value = complex(result)
                    else:
                        result_value = float(result)
                    
                    # Check if it's supposed to be zero (identity)
                    if abs(result_value) > 0.001:
                        vals_str = ", ".join(f"{k}={v:.3f}" for k, v in values.items())
                        return f"With {vals_str}: expression = {result_value:.6f} ≠ 0"
                        
                except:
                    pass
            
            # Try to find values that make denominators zero (invalid domains)
            for atom in expr.atoms():
                if atom.is_Pow and atom.exp < 0:
                    # Found a denominator
                    base = atom.base
                    try:
                        # Solve for when denominator is zero
                        solutions = solve(base, vars[0] if vars else None)
                        if solutions:
                            return f"Undefined when {vars[0]} = {solutions[0]}"
                    except:
                        pass
                        
        except Exception as e:
            pass
        
        return None
    
    def _is_trivial(self, conjecture: MathTheorem) -> bool:
        """Check if the conjecture is too trivial."""
        
        # Check statement length and complexity
        if len(conjecture.statement) < 10:
            return True
        
        # Check if it's just a rearrangement
        if conjecture.symbolic_form:
            try:
                expr = sp.sympify(conjecture.symbolic_form)
                
                # If it's just a=a or similar
                if expr == 0 and len(str(expr)) < 5:
                    return True
                
                # Check complexity
                complexity = len(expr.atoms())
                if complexity < 3:
                    return True
                    
            except:
                pass
        
        # Check for obvious statements
        trivial_patterns = [
            'a = a',
            'a + 0 = a',
            'a * 1 = a',
            'a - a = 0',
        ]
        
        for pattern in trivial_patterns:
            if pattern in conjecture.statement.lower():
                return True
        
        return False
    
    def _check_contradiction(self, conjecture: MathTheorem, kb: KnowledgeBase) -> Optional[str]:
        """Check if the conjecture contradicts known theorems."""
        
        # This is a simplified check
        # In a real system, this would use theorem provers
        
        if not conjecture.symbolic_form:
            return None
        
        try:
            expr = sp.sympify(conjecture.symbolic_form)
            
            # Check against fundamental laws
            vars = list(expr.free_symbols)
            
            # Check commutativity if applicable
            if len(vars) >= 2:
                a, b = vars[:2]
                # If the expression claims a*b != b*a for commutative operations
                if 'a*b' in str(expr) and 'b*a' in str(expr):
                    expr_swapped = expr.subs([(a, b), (b, a)])
                    if simplify(expr_swapped + expr) != 0:
                        return "Violates commutativity of multiplication"
            
            # Check for division by zero claims
            if '1/0' in conjecture.statement or 'divide by zero' in conjecture.statement.lower():
                return "Division by zero is undefined"
            
            # Check for sqrt of negative numbers (in real domain)
            if 'sqrt' in str(expr) and not any(isinstance(s, sp.I) for s in expr.atoms()):
                # Test with negative values
                for v in vars:
                    test_expr = expr.subs(v, -1)
                    if test_expr.has(sp.sqrt):
                        return "Square root of negative number in real domain"
            
        except:
            pass
        
        return None
    
    def get_stats(self) -> dict:
        """Get naysayer statistics."""
        total = self.rejections + self.acceptances + self.trivial_count
        
        return {
            'name': self.name,
            'total_evaluated': total,
            'rejections': self.rejections,
            'acceptances': self.acceptances,
            'trivial': self.trivial_count,
            'rejection_rate': self.rejections / max(1, total),
            'acceptance_rate': self.acceptances / max(1, total),
            'recent_evaluations': self.evaluation_log[-10:]  # Last 10 evaluations
        }
    
    def generate_critique(self, conjecture: MathTheorem) -> str:
        """Generate a detailed critique of the conjecture."""
        
        critiques = []
        
        # Analyze structure
        if len(conjecture.statement) < 20:
            critiques.append("Statement is too short and likely trivial")
        
        # Check for common patterns
        if '=' in conjecture.statement:
            parts = conjecture.statement.split('=')
            if len(parts) == 2 and parts[0].strip() == parts[1].strip():
                critiques.append("This is a tautology (a=a)")
        
        # Analyze mathematical depth
        if conjecture.symbolic_form:
            try:
                expr = sp.sympify(conjecture.symbolic_form)
                depth = self._calculate_depth(expr)
                
                if depth < 2:
                    critiques.append("Mathematical expression lacks depth")
                elif depth > 10:
                    critiques.append("Expression might be unnecessarily complex")
                    
            except:
                critiques.append("Could not parse symbolic form for analysis")
        
        # Check field appropriateness
        if 'sin' in conjecture.statement or 'cos' in conjecture.statement:
            if conjecture.field != "trigonometry":
                critiques.append(f"Should be categorized as trigonometry, not {conjecture.field}")
        
        if not critiques:
            critiques.append("The conjecture appears structurally sound")
        
        return " | ".join(critiques)
    
    def _calculate_depth(self, expr) -> int:
        """Calculate the depth of a mathematical expression."""
        if isinstance(expr, (int, float, sp.Symbol)):
            return 0
        elif isinstance(expr, sp.Basic):
            if expr.args:
                return 1 + max(self._calculate_depth(arg) for arg in expr.args)
            return 1
        return 0