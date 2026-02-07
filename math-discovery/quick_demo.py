#!/usr/bin/env python3
"""Quick demo of the mathematical discovery system"""

from knowledge_base import KnowledgeBase, MathTheorem, MathField, Difficulty
from explorer import ExplorerAgent, GeneralizationStrategy
from naysayer import NaysayerAgent
import time

def demo():
    print("="*60)
    print("MATHEMATICAL DISCOVERY DEMO".center(60))
    print("="*60)
    
    # Initialize
    kb = KnowledgeBase()
    print(f"\n📚 Starting with {len(kb.theorems)} classical theorems")
    
    # Create agents
    explorer = ExplorerAgent("Ramanujan", [GeneralizationStrategy()])
    naysayer = NaysayerAgent("The Skeptic")
    
    print("\n🔬 Running discovery attempts...\n")
    
    successes = 0
    refutations = 0
    
    for i in range(10):
        print(f"Attempt {i+1}:")
        
        # Explorer attempts discovery
        conjecture = explorer.explore(kb)
        
        if conjecture:
            print(f"  💡 Conjecture: {conjecture.statement[:60]}...")
            
            # Naysayer evaluates
            evaluation = naysayer.evaluate_conjecture(conjecture, kb)
            
            if evaluation['is_valid']:
                successes += 1
                kb.add_theorem(conjecture)
                print(f"  ✅ ACCEPTED! (Confidence: {evaluation['confidence']:.1%})")
            else:
                refutations += 1
                print(f"  ❌ REFUTED: {evaluation['refutation_reason'][:50]}...")
        else:
            print(f"  ⚪ No conjecture generated")
        
        print()
        time.sleep(0.5)
    
    print("="*60)
    print("RESULTS".center(60))
    print("="*60)
    print(f"Successful discoveries: {successes}")
    print(f"Refuted conjectures: {refutations}")
    print(f"Total theorems in KB: {len(kb.theorems)}")
    
    # Show some discoveries
    novel = kb.get_novel_discoveries()
    if novel:
        print(f"\n✨ Novel theorems discovered:")
        for theorem in novel[:3]:
            print(f"  • {theorem.statement}")

if __name__ == "__main__":
    demo()