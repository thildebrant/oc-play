#!/usr/bin/env python3
"""Test the discovery system with manual theorem creation"""

from knowledge_base import KnowledgeBase, MathTheorem, MathField, Difficulty
from naysayer import NaysayerAgent
import time

def test_discoveries():
    print("="*60)
    print("TESTING MATHEMATICAL DISCOVERY SYSTEM".center(60))
    print("="*60)
    
    kb = KnowledgeBase()
    naysayer = NaysayerAgent("The Skeptic")
    
    # Manually create some test conjectures
    test_theorems = [
        # Valid new theorem
        MathTheorem(
            id="test_001",
            statement="(a+b+c)^2 = a^2 + b^2 + c^2 + 2(ab + ac + bc)",
            symbolic_form="(a+b+c)**2 - (a**2 + b**2 + c**2 + 2*(a*b + a*c + b*c))",
            field=MathField.ALGEBRA,
            difficulty=Difficulty.ADVANCED,
            discovered_by="TestAgent",
            timestamp=time.time()
        ),
        
        # Invalid theorem (wrong)
        MathTheorem(
            id="test_002",
            statement="(a+b)^2 = a^2 + b^2",  # Missing 2ab
            symbolic_form="(a+b)**2 - (a**2 + b**2)",
            field=MathField.ALGEBRA,
            difficulty=Difficulty.HIGH_SCHOOL,
            discovered_by="TestAgent",
            timestamp=time.time()
        ),
        
        # Tautology
        MathTheorem(
            id="test_003",
            statement="a + b = a + b",
            symbolic_form="(a + b) - (a + b)",
            field=MathField.ALGEBRA,
            difficulty=Difficulty.ELEMENTARY,
            discovered_by="TestAgent",
            timestamp=time.time()
        ),
        
        # Already known (similar to existing)
        MathTheorem(
            id="test_004",
            statement="(x+y)^2 = x^2 + 2*x*y + y^2",  # Just renamed variables
            symbolic_form="(x+y)**2 - (x**2 + 2*x*y + y**2)",
            field=MathField.ALGEBRA,
            difficulty=Difficulty.HIGH_SCHOOL,
            discovered_by="TestAgent",
            timestamp=time.time()
        ),
        
        # Valid trigonometric identity
        MathTheorem(
            id="test_005",
            statement="sin(3x) = 3*sin(x) - 4*sin^3(x)",
            symbolic_form="sin(3*x) - (3*sin(x) - 4*sin(x)**3)",
            field=MathField.TRIGONOMETRY,
            difficulty=Difficulty.ADVANCED,
            discovered_by="TestAgent",
            timestamp=time.time()
        ),
    ]
    
    print(f"\n📚 Testing {len(test_theorems)} conjectures...\n")
    
    for theorem in test_theorems:
        print(f"Testing: {theorem.statement}")
        evaluation = naysayer.evaluate_conjecture(theorem, kb)
        
        if evaluation['is_valid']:
            print(f"  ✅ VALID (Confidence: {evaluation['confidence']:.1%})")
            
            # Check if truly novel
            similar = kb.search_similar(theorem.statement, theorem.symbolic_form)
            if similar:
                print(f"  ⚠️  Similar to: {similar[0].statement}")
            else:
                print(f"  ✨ Novel discovery!")
                kb.add_theorem(theorem)
        else:
            print(f"  ❌ INVALID")
            print(f"     Reason: {evaluation['refutation_reason']}")
            print(f"     Method: {evaluation['refutation_method']}")
        
        print()
    
    # Summary
    print("="*60)
    print(f"Knowledge base now has {len(kb.theorems)} theorems")
    novel = kb.get_novel_discoveries()
    print(f"Novel discoveries: {len(novel)}")
    
    if novel:
        print("\nNovel theorems:")
        for t in novel:
            print(f"  • {t.statement}")

if __name__ == "__main__":
    test_discoveries()