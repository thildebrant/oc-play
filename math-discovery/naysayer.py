"""
Naysayer Agent - Attempts to disprove conjectures or find prior art
"""

import sympy as sp
from sympy import symbols, simplify, expand, factor, solve, Eq
from sympy import sin, cos, tan, log, exp, sqrt, pi, E, I
import random
from typing import Optional, List, Tuple, Dict
from knowledge_base import MathTheorem, KnowledgeBase, MathField
import time

class RefutationMethod:
    """Base class for refutation methods."""
    
    def attempt_refutation(self, theorem: MathTheorem, kb: KnowledgeBase) -> Tuple[bool, Optional[str]]:
        """
        Attempt to refute a theorem.
        Returns (is_refuted, explanation)
        """
        raise NotImplementedError

class CounterexampleSearch(RefutationMethod):
    """Search for numerical counterexamples."""
    
    def attempt_refutation(self, theorem: MathTheorem, kb: KnowledgeBase) -> Tuple[bool, Optional[str]]:
        if not theorem.symbolic_form:
            return False, None
        
        try:
            # Parse the symbolic form
            expr = sp.sympify(theorem.symbolic_form)
            variables = expr.free_symbols
            
            # Generate test values
            test_cases = self._generate_test_cases(len(variables))
            
            for test_values in test_cases:
                # Create substitution dictionary
                subs_dict = {}
                for i, var in enumerate(variables):
                    subs_dict[var] = test_values[i]
                
                # Evaluate the expression
                try:
                    result = expr.subs(subs_dict)
                    result_float = complex(result)
                    
                    # Check if the identity holds (should be close to 0)
                    if abs(result_float) > 1e-8:
                        counterexample = ", ".join([f"{var}={val}" for var, val in subs_dict.items()])
                        return True, f"Counterexample found: {counterexample} gives {result_float}"
                except:
                    # Skip if evaluation fails (e.g., division by zero)
                    continue
            
            return False, None
            
        except Exception as e:
            return False, None
    
    def _generate_test_cases(self, num_vars: int) -> List[Tuple]:
        """Generate test cases for counterexample search."""
        test_values = [
            0, 1, -1, 2, -2, 0.5, -0.5, 
            sp.pi, -sp.pi, sp.E, 
            complex(1, 1), complex(0, 1)
        ]
        
        # Random sampling approach
        test_cases = []
        for _ in range(100):  # Try 100 random combinations
            case = []
            for _ in range(num_vars):
                case.append(random.choice(test_values))
            test_cases.append(tuple(case))
        
        # Also include edge cases
        edge_cases = [
            tuple([0] * num_vars),
            tuple([1] * num_vars),
            tuple([-1] * num_vars),
            tuple([sp.pi] * num_vars),
        ]
        test_cases.extend(edge_cases)
        
        return test_cases

class PriorArtDetection(RefutationMethod):
    """Check if the theorem already exists or is trivially derived."""
    
    def attempt_refutation(self, theorem: MathTheorem, kb: KnowledgeBase) -> Tuple[bool, Optional[str]]:
        # Search for similar theorems
        similar = kb.search_similar(theorem.statement, theorem.symbolic_form)
        
        if similar:
            # Check for exact matches
            for existing in similar:
                if theorem.symbolic_form and existing.symbolic_form:
                    try:
                        new_expr = sp.sympify(theorem.symbolic_form)
                        exist_expr = sp.sympify(existing.symbolic_form)
                        
                        # Check if they're equivalent
                        if simplify(new_expr - exist_expr) == 0:
                            return True, f"This is equivalent to existing theorem {existing.id}: {existing.statement}"
                    except:
                        pass
            
            # Check if it's a trivial variation
            if len(similar) > 0:
                similarity_score = self._calculate_similarity(theorem, similar[0])
                if similarity_score > 0.8:
                    return True, f"This appears to be a trivial variation of {similar[0].id}"
        
        return False, None
    
    def _calculate_similarity(self, theorem1: MathTheorem, theorem2: MathTheorem) -> float:
        """Calculate similarity between two theorems."""
        # Simple word overlap similarity
        words1 = set(theorem1.statement.lower().split())
        words2 = set(theorem2.statement.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0

class TrivialityDetection(RefutationMethod):
    """Detect if a theorem is trivial or tautological."""
    
    def attempt_refutation(self, theorem: MathTheorem, kb: KnowledgeBase) -> Tuple[bool, Optional[str]]:
        if not theorem.symbolic_form:
            return False, None
        
        try:
            expr = sp.sympify(theorem.symbolic_form)
            
            # Check if it simplifies to 0 (tautology)
            simplified = simplify(expr)
            if simplified == 0:
                return True, "This is a tautology (always true by definition)"
            
            # Check if both sides are identical
            if '=' in theorem.statement:
                parts = theorem.statement.split('=')
                if len(parts) == 2:
                    left = parts[0].strip()
                    right = parts[1].strip()
                    if left == right:
                        return True, "Both sides of the equation are identical"
            
            # Check if it's just a restatement with different notation
            expanded = expand(expr)
            if expanded == 0:
                return True, "This reduces to 0 = 0 when expanded"
            
            return False, None
            
        except:
            return False, None

class AlgebraicVerification(RefutationMethod):
    """Verify if the theorem is actually correct using symbolic manipulation."""
    
    def attempt_refutation(self, theorem: MathTheorem, kb: KnowledgeBase) -> Tuple[bool, Optional[str]]:
        if not theorem.symbolic_form:
            return False, None
        
        try:
            expr = sp.sympify(theorem.symbolic_form)
            
            # Try different simplification approaches
            methods = [
                ('simplify', simplify),
                ('expand', expand),
                ('factor', factor),
                ('trigsimp', sp.trigsimp),
            ]
            
            for method_name, method in methods:
                try:
                    result = method(expr)
                    
                    # If it doesn't simplify to 0, the identity is false
                    if result != 0 and result != False:
                        # Double-check with numerical evaluation
                        variables = expr.free_symbols
                        if variables:
                            # Test with specific values
                            test_dict = {var: 1.5 for var in variables}
                            numerical_result = float(expr.subs(test_dict))
                            
                            if abs(numerical_result) > 1e-8:
                                return True, f"Algebraic verification failed: {method_name} gives {result}"
                except:
                    continue
            
            return False, None
            
        except Exception as e:
            return False, None

class SpecialCaseAnalysis(RefutationMethod):
    """Check special cases that might invalidate the theorem."""
    
    def attempt_refutation(self, theorem: MathTheorem, kb: KnowledgeBase) -> Tuple[bool, Optional[str]]:
        if not theorem.symbolic_form:
            return False, None
        
        try:
            expr = sp.sympify(theorem.symbolic_form)
            variables = list(expr.free_symbols)
            
            # Check division by zero cases
            if '/' in theorem.statement or 'tan' in theorem.statement or 'sec' in theorem.statement:
                # Check if there are values that make denominators zero
                for var in variables:
                    # Set variable to 0 and check
                    test_expr = expr.subs(var, 0)
                    if sp.zoo in sp.preorder_traversal(test_expr):  # zoo is complex infinity
                        return True, f"Division by zero when {var} = 0"
            
            # Check domain restrictions for logs and square roots
            if 'log' in theorem.statement or 'sqrt' in theorem.statement:
                # Test with negative values
                for var in variables:
                    test_expr = expr.subs(var, -1)
                    if test_expr.has(sp.zoo) or test_expr.has(sp.nan):
                        return True, f"Domain error: invalid for {var} < 0"
            
            # Check trigonometric singularities
            if any(func in theorem.statement for func in ['tan', 'cot', 'sec', 'csc']):
                critical_values = [0, sp.pi/2, sp.pi, 3*sp.pi/2]
                for var in variables:
                    for val in critical_values:
                        test_expr = expr.subs(var, val)
                        if test_expr.has(sp.zoo):
                            return True, f"Singularity at {var} = {val}"
            
            return False, None
            
        except:
            return False, None

class NaysayerAgent:
    """The skeptical agent that tries to disprove new conjectures."""
    
    def __init__(self, name: str = "Naysayer"):
        self.name = name
        self.methods = [
            CounterexampleSearch(),
            PriorArtDetection(),
            TrivialityDetection(),
            AlgebraicVerification(),
            SpecialCaseAnalysis()
        ]
        self.refutations = []
        self.attempts = 0
        self.successful_refutations = 0
        
    def evaluate_conjecture(self, theorem: MathTheorem, kb: KnowledgeBase) -> Dict:
        """
        Evaluate a conjecture and attempt to refute it.
        Returns evaluation results.
        """
        self.attempts += 1
        evaluation = {
            'theorem_id': theorem.id,
            'timestamp': time.time(),
            'is_valid': True,
            'refutation_reason': None,
            'refutation_method': None,
            'confidence': 0.0
        }
        
        # Try each refutation method
        for method in self.methods:
            method_name = method.__class__.__name__
            
            try:
                is_refuted, explanation = method.attempt_refutation(theorem, kb)
                
                if is_refuted:
                    evaluation['is_valid'] = False
                    evaluation['refutation_reason'] = explanation
                    evaluation['refutation_method'] = method_name
                    evaluation['confidence'] = 0.9  # High confidence in refutation
                    
                    self.successful_refutations += 1
                    self.refutations.append(theorem.id)
                    
                    # Mark theorem as refuted
                    theorem.is_novel = False
                    theorem.counterexample = explanation
                    
                    return evaluation
            except Exception as e:
                # Continue with other methods if one fails
                continue
        
        # If no refutation found, check how confident we are in validity
        evaluation['confidence'] = self._calculate_validity_confidence(theorem, kb)
        
        return evaluation
    
    def _calculate_validity_confidence(self, theorem: MathTheorem, kb: KnowledgeBase) -> float:
        """Calculate confidence that the theorem is valid."""
        confidence = 0.5  # Base confidence
        
        # Higher confidence if it's related to known theorems
        if theorem.related_to:
            confidence += 0.1 * len(theorem.related_to)
        
        # Higher confidence for simpler theorems
        if theorem.statement.count('+') + theorem.statement.count('*') < 5:
            confidence += 0.1
        
        # Lower confidence for very complex expressions
        if len(theorem.statement) > 100:
            confidence -= 0.2
        
        # Higher confidence if similar theorems exist and are valid
        similar = kb.search_similar(theorem.statement, theorem.symbolic_form)
        if similar:
            valid_similar = [t for t in similar if t.is_novel or t.discovered_by == "Classical"]
            if valid_similar:
                confidence += 0.15
        
        return min(1.0, max(0.0, confidence))
    
    def get_stats(self) -> Dict:
        """Get naysayer statistics."""
        return {
            'name': self.name,
            'attempts': self.attempts,
            'successful_refutations': self.successful_refutations,
            'refutation_rate': self.successful_refutations / max(1, self.attempts),
            'refuted_theorems': self.refutations
        }