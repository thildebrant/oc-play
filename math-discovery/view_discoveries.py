#!/usr/bin/env python3
"""
View accumulated mathematical discoveries across all sessions
"""

import json
import os
from datetime import datetime

def view_discoveries():
    """Display accumulated discoveries and session history."""
    
    print("="*70)
    print("MATHEMATICAL DISCOVERY ARCHIVE".center(70))
    print("="*70)
    
    # Load knowledge base
    kb_file = 'output/knowledge_base.json'
    if os.path.exists(kb_file):
        with open(kb_file, 'r') as f:
            kb = json.load(f)
        
        print(f"\n📚 KNOWLEDGE BASE")
        print(f"   Total Theorems: {len(kb['theorems'])}")
        
        # Count novel discoveries
        novel_count = sum(1 for t in kb['theorems'] if t.get('is_novel', False))
        classical_count = len(kb['theorems']) - novel_count
        
        print(f"   Classical (Initial): {classical_count}")
        print(f"   Novel Discoveries: {novel_count}")
        
        # Show statistics by field
        if 'statistics' in kb:
            print(f"\n   By Field:")
            for field, count in kb['statistics']['by_field'].items():
                if count > 0:
                    print(f"      {field}: {count}")
        
        # Show recent novel discoveries
        novel_theorems = [t for t in kb['theorems'] if t.get('is_novel', False)]
        if novel_theorems:
            # Sort by timestamp
            novel_theorems.sort(key=lambda t: t.get('timestamp', 0), reverse=True)
            
            print(f"\n💡 RECENT NOVEL DISCOVERIES:")
            for theorem in novel_theorems[:10]:  # Show up to 10
                timestamp = theorem.get('timestamp', 0)
                date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M') if timestamp > 0 else 'Unknown'
                print(f"\n   📝 {theorem['statement']}")
                print(f"      Discovered by: {theorem.get('discovered_by', 'Unknown')}")
                print(f"      Field: {theorem.get('field', 'Unknown')}")
                print(f"      Time: {date_str}")
                if theorem.get('proof_sketch'):
                    print(f"      Proof: {theorem['proof_sketch']}")
    else:
        print("\n❌ No knowledge base found. Run the simulation first!")
    
    # Load session history
    history_file = 'output/discovery_history.jsonl'
    if os.path.exists(history_file):
        print(f"\n📊 SESSION HISTORY")
        print("-" * 70)
        
        sessions = []
        with open(history_file, 'r') as f:
            for line in f:
                if line.strip():
                    sessions.append(json.loads(line))
        
        if sessions:
            # Show summary statistics
            total_discoveries = sum(s.get('discoveries', 0) for s in sessions)
            total_novel = sum(s.get('novel', 0) for s in sessions)
            total_refuted = sum(s.get('refuted', 0) for s in sessions)
            total_cycles = sum(s.get('cycles', 0) for s in sessions)
            total_duration = sum(s.get('duration', 0) for s in sessions)
            
            print(f"   Total Sessions: {len(sessions)}")
            print(f"   Total Runtime: {total_duration:.1f} seconds")
            print(f"   Total Cycles: {total_cycles}")
            print(f"   Total Discoveries: {total_discoveries}")
            print(f"   Total Novel: {total_novel}")
            print(f"   Total Refuted: {total_refuted}")
            
            # Show recent sessions
            print(f"\n   Recent Sessions:")
            for session in sessions[-5:]:  # Last 5 sessions
                timestamp = session.get('timestamp', 0)
                date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                duration = session.get('duration', 0)
                discoveries = session.get('discoveries', 0)
                novel = session.get('novel', 0)
                kb_size = session.get('total_kb_size', 0)
                
                print(f"\n   🕒 {date_str}")
                print(f"      Duration: {duration:.1f}s, Discoveries: {discoveries}, Novel: {novel}")
                print(f"      KB Size After: {kb_size} theorems")
        else:
            print("   No sessions recorded yet")
    
    # Check for specific interesting patterns
    if os.path.exists(kb_file):
        with open(kb_file, 'r') as f:
            kb = json.load(f)
        
        # Look for theorems with high difficulty
        advanced_theorems = [t for t in kb['theorems'] 
                            if t.get('difficulty', 0) >= 3 and t.get('is_novel', False)]
        
        if advanced_theorems:
            print(f"\n🎓 ADVANCED DISCOVERIES (Difficulty ≥ 3):")
            for theorem in advanced_theorems[:5]:
                print(f"   • {theorem['statement'][:80]}...")
        
        # Look for theorems that relate to multiple others
        connected_theorems = [t for t in kb['theorems'] 
                             if t.get('related_to') and len(t['related_to']) > 1]
        
        if connected_theorems:
            print(f"\n🔗 HIGHLY CONNECTED THEOREMS:")
            for theorem in connected_theorems[:5]:
                related_count = len(theorem.get('related_to', []))
                print(f"   • {theorem['statement'][:60]}...")
                print(f"     (Connected to {related_count} other theorems)")

    print("\n" + "="*70)
    print("\nTip: Run 'python3 discovery_sim.py' to continue discovering!")
    print("     Add '--fresh-start' to begin with a clean knowledge base.")
    print("     Use 'python3 -m http.server 8080 --bind 127.0.0.1' then open http://localhost:8080/dashboard.html (localhost only).")

if __name__ == "__main__":
    view_discoveries()