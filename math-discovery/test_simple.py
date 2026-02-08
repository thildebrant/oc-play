#!/usr/bin/env python3
"""Simple test of the discovery system without full simulation"""

import sys
import os

# Test basic imports
try:
    print("Testing imports...")
    from knowledge_base import KnowledgeBase, MathTheorem, MathField, Difficulty
    print("✓ Knowledge base imported")
    
    # Test knowledge base creation
    kb = KnowledgeBase()
    print(f"✓ Knowledge base created with {len(kb.theorems)} initial theorems")
    
    # Test loading previous knowledge
    if os.path.exists('output/knowledge_base.json'):
        kb.load_from_file('output/knowledge_base.json')
        print(f"✓ Loaded knowledge base: {len(kb.theorems)} total theorems")
        novel = kb.get_novel_discoveries()
        print(f"  - Novel discoveries: {len(novel)}")
        for theorem in novel[:3]:
            print(f"    • {theorem.statement}")
    
    # Test creating a new theorem
    new_theorem = MathTheorem(
        id="test_001",
        statement="Test theorem: (a+b+c)^2 = a^2 + b^2 + c^2 + 2(ab + bc + ca)",
        symbolic_form=None,
        field=MathField.ALGEBRA,
        difficulty=Difficulty.ADVANCED,
        discovered_by="TestAgent",
        timestamp=0,
        is_novel=True
    )
    print(f"✓ Created new theorem: {new_theorem.statement[:50]}...")
    
    print("\n✅ All basic tests passed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nInstall missing dependencies with:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
