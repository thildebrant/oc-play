#!/usr/bin/env python3
"""
View discoveries from the Mathematical Discovery Simulator
"""

import json
import sys
from knowledge_base import MathField, Difficulty

def view_discoveries(filename="simulation_final.json"):
    """Display discovered theorems from simulation."""
    
    # Load simulation state
    with open(filename, 'r') as f:
        state = json.load(f)
    
    # Load knowledge base
    kb_file = filename.replace('.json', '_kb.json')
    with open(kb_file, 'r') as f:
        kb_data = json.load(f)
    
    print("="*80)
    print("MATHEMATICAL DISCOVERIES".center(80))
    print("="*80)
    
    # Summary statistics
    print(f"\n📊 Summary Statistics:")
    print(f"  Total theorems: {state['statistics']['total_theorems']}")
    print(f"  Novel discoveries: {state['statistics']['novel_discoveries']}")
    print(f"  Simulation runtime: {state['runtime']:.2f} seconds")
    print(f"  Total cycles: {state['cycle']}")
    
    # Field distribution
    print(f"\n🎯 Discoveries by Field:")
    for field, count in state['statistics']['by_field'].items():
        print(f"  {field}: {count}")
    
    # Explorer performance
    print(f"\n🏆 Explorer Performance:")
    explorers = sorted(state['explorer_stats'], 
                      key=lambda x: x['successes'], reverse=True)
    for i, explorer in enumerate(explorers, 1):
        success_rate = explorer['success_rate'] * 100
        print(f"  {i}. {explorer['name']}: {explorer['successes']} discoveries "
              f"({success_rate:.1f}% success rate)")
    
    # Naysayer statistics
    naysayer = state['naysayer_stats']
    print(f"\n🤔 Naysayer Statistics:")
    print(f"  Total evaluated: {naysayer['total_evaluated']}")
    print(f"  Rejected: {naysayer['rejections']} ({naysayer['rejection_rate']*100:.1f}%)")
    print(f"  Accepted: {naysayer['acceptances']} ({naysayer['acceptance_rate']*100:.1f}%)")
    print(f"  Trivial: {naysayer['trivial']}")
    
    # Novel theorems
    print(f"\n✨ Novel Discoveries:")
    print("-"*80)
    
    novel_theorems = [t for t in kb_data['theorems'] if t['is_novel']]
    
    if not novel_theorems:
        print("  No novel theorems discovered in this simulation.")
    else:
        for theorem in novel_theorems:
            print(f"\n📌 {theorem['id']}")
            print(f"  Statement: {theorem['statement']}")
            print(f"  Field: {theorem['field']}")
            print(f"  Discovered by: {theorem['discovered_by']}")
            if theorem.get('proof_sketch'):
                print(f"  Proof: {theorem['proof_sketch']}")
            if theorem.get('related_to'):
                print(f"  Related to: {', '.join(theorem['related_to'])}")
    
    # Discovery timeline
    if state['discovery_history']:
        print(f"\n📅 Discovery Timeline:")
        print("-"*80)
        for discovery in state['discovery_history']:
            time_min = discovery['time'] / 60
            print(f"  Cycle {discovery['cycle']} ({time_min:.1f} min): "
                  f"{discovery['explorer']} discovered:")
            print(f"    {discovery['theorem'][:100]}...")
    
    print("\n" + "="*80)
    print("End of Report")
    print("="*80)

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "simulation_final.json"
    view_discoveries(filename)