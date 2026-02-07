#!/usr/bin/env python3
"""
Mathematical Discovery Simulation
Orchestrates explorer agents and naysayer to discover new theorems
"""

import time
import json
import random
from typing import List, Dict, Optional
from knowledge_base import KnowledgeBase, MathTheorem
from explorer import ExplorerAgent
from naysayer import NaysayerAgent
import argparse
import os

class DiscoverySimulation:
    """Main simulation engine for mathematical discovery."""
    
    def __init__(self, num_explorers: int = 3, save_interval: int = 10, 
                 load_previous: bool = True, knowledge_file: str = 'output/knowledge_base.json'):
        self.kb = KnowledgeBase()
        
        # Load previous discoveries if requested and file exists
        self.knowledge_file = knowledge_file
        if load_previous and os.path.exists(knowledge_file):
            try:
                self.kb.load_from_file(knowledge_file)
                print(f"📚 Loaded {len(self.kb.theorems)} theorems from previous runs")
                print(f"   Including {len(self.kb.get_novel_discoveries())} novel discoveries")
            except Exception as e:
                print(f"⚠️  Could not load previous knowledge: {e}")
                print("   Starting with fresh knowledge base")
        
        self.naysayer = NaysayerAgent("The Skeptic")
        
        # Create explorer agents with different personalities
        self.explorers = []
        explorer_names = [
            "Euler", "Gauss", "Ramanujan", "Erdos", "Noether",
            "Hilbert", "Riemann", "Cauchy", "Fermat", "Pascal"
        ]
        
        for i in range(num_explorers):
            name = explorer_names[i % len(explorer_names)]
            self.explorers.append(ExplorerAgent(f"{name}-{i+1}"))
        
        self.save_interval = save_interval
        self.discovery_count = 0
        self.cycle_count = 0
        self.start_time = time.time()
        
        # Statistics tracking
        self.stats = {
            'total_attempts': 0,
            'successful_discoveries': 0,
            'refuted_conjectures': 0,
            'novel_theorems': 0,
            'discovery_timeline': [],
            'agent_performance': {},
            'session_start': time.time(),
            'loaded_previous': load_previous
        }
        
        # Initialize agent performance tracking
        for explorer in self.explorers:
            self.stats['agent_performance'][explorer.name] = {
                'attempts': 0,
                'discoveries': 0,
                'refuted': 0
            }
        
        self.stats['agent_performance'][self.naysayer.name] = {
            'evaluations': 0,
            'refutations': 0
        }
    
    def run_discovery_cycle(self) -> Optional[Dict]:
        """Run one cycle of discovery attempt."""
        self.cycle_count += 1
        
        # Select a random explorer
        explorer = random.choice(self.explorers)
        
        # Attempt to generate a conjecture
        conjecture = explorer.explore(self.kb)
        
        if not conjecture:
            return None
        
        self.stats['total_attempts'] += 1
        self.stats['agent_performance'][explorer.name]['attempts'] += 1
        
        # Create discovery record
        discovery = {
            'cycle': self.cycle_count,
            'timestamp': time.time(),
            'explorer': explorer.name,
            'theorem_id': conjecture.id,
            'statement': conjecture.statement,
            'field': conjecture.field.value,
            'status': 'proposed'
        }
        
        # Naysayer evaluation
        evaluation = self.naysayer.evaluate_conjecture(conjecture, self.kb)
        self.stats['agent_performance'][self.naysayer.name]['evaluations'] += 1
        
        discovery['evaluation'] = evaluation
        
        if evaluation['is_valid']:
            # Check if it's truly novel (not too similar to existing)
            similar = self.kb.search_similar(conjecture.statement, conjecture.symbolic_form)
            
            if len(similar) == 0 or evaluation['confidence'] > 0.7:
                # Novel discovery!
                conjecture.is_novel = True
                self.kb.add_theorem(conjecture)
                explorer.record_success(conjecture)
                
                self.stats['successful_discoveries'] += 1
                self.stats['novel_theorems'] += 1
                self.stats['agent_performance'][explorer.name]['discoveries'] += 1
                
                discovery['status'] = 'accepted'
                discovery['novelty'] = True
                
                print(f"✨ DISCOVERY by {explorer.name}:")
                print(f"   {conjecture.statement}")
                print(f"   Field: {conjecture.field.value}, Confidence: {evaluation['confidence']:.1%}")
            else:
                # Valid but not novel
                discovery['status'] = 'redundant'
                discovery['novelty'] = False
                print(f"↔️  Redundant theorem by {explorer.name}: {conjecture.statement[:50]}...")
        else:
            # Refuted by naysayer
            self.stats['refuted_conjectures'] += 1
            self.stats['agent_performance'][explorer.name]['refuted'] += 1
            self.stats['agent_performance'][self.naysayer.name]['refutations'] += 1
            
            discovery['status'] = 'refuted'
            discovery['refutation'] = evaluation['refutation_reason']
            
            print(f"❌ REFUTED by {self.naysayer.name}:")
            print(f"   Conjecture: {conjecture.statement[:50]}...")
            print(f"   Reason: {evaluation['refutation_reason']}")
        
        # Add to timeline
        self.stats['discovery_timeline'].append(discovery)
        
        # Save periodically
        if self.cycle_count % self.save_interval == 0:
            self.save_state()
        
        return discovery
    
    def run_simulation(self, duration_seconds: int = 60, max_cycles: int = 1000):
        """Run the simulation for a specified duration or number of cycles."""
        print("="*70)
        print("MATHEMATICAL DISCOVERY SIMULATION".center(70))
        print("="*70)
        print(f"Explorers: {len(self.explorers)}")
        print(f"Knowledge Base: {len(self.kb.theorems)} theorems")
        print(f"  - Classical: {len([t for t in self.kb.theorems.values() if not t.is_novel])}")
        print(f"  - Novel Discoveries: {len(self.kb.get_novel_discoveries())}")
        print(f"Duration: {duration_seconds}s or {max_cycles} cycles")
        print("="*70 + "\n")
        
        end_time = time.time() + duration_seconds
        
        while time.time() < end_time and self.cycle_count < max_cycles:
            self.run_discovery_cycle()
            
            # Small delay to make output readable
            time.sleep(0.1)
            
            # Print periodic statistics
            if self.cycle_count % 50 == 0:
                self.print_statistics()
        
        # Final statistics
        print("\n" + "="*70)
        print("SIMULATION COMPLETE".center(70))
        print("="*70)
        self.print_detailed_statistics()
        self.save_state(final=True)
        
    def print_statistics(self):
        """Print current statistics."""
        runtime = time.time() - self.start_time
        print(f"\n📊 Cycle {self.cycle_count} | Runtime: {runtime:.1f}s")
        print(f"   Discoveries: {self.stats['successful_discoveries']} | "
              f"Refuted: {self.stats['refuted_conjectures']} | "
              f"Novel: {self.stats['novel_theorems']}")
    
    def print_detailed_statistics(self):
        """Print detailed final statistics."""
        runtime = time.time() - self.start_time
        
        print(f"\n📈 FINAL STATISTICS")
        print(f"   Total Runtime: {runtime:.1f} seconds")
        print(f"   Total Cycles: {self.cycle_count}")
        print(f"   Total Attempts: {self.stats['total_attempts']}")
        print(f"   Successful Discoveries: {self.stats['successful_discoveries']}")
        print(f"   Novel Theorems: {self.stats['novel_theorems']}")
        print(f"   Refuted Conjectures: {self.stats['refuted_conjectures']}")
        
        if self.stats['total_attempts'] > 0:
            success_rate = self.stats['successful_discoveries'] / self.stats['total_attempts']
            print(f"   Success Rate: {success_rate:.1%}")
        
        print(f"\n🏆 AGENT PERFORMANCE:")
        
        # Explorer performance
        explorer_stats = []
        for explorer in self.explorers:
            stats = self.stats['agent_performance'][explorer.name]
            if stats['attempts'] > 0:
                success_rate = stats['discoveries'] / stats['attempts']
                explorer_stats.append((explorer.name, stats['discoveries'], success_rate))
        
        # Sort by discoveries
        explorer_stats.sort(key=lambda x: x[1], reverse=True)
        
        for name, discoveries, rate in explorer_stats[:5]:  # Top 5
            print(f"   {name}: {discoveries} discoveries ({rate:.1%} success rate)")
        
        # Naysayer performance
        naysayer_stats = self.stats['agent_performance'][self.naysayer.name]
        if naysayer_stats['evaluations'] > 0:
            refutation_rate = naysayer_stats['refutations'] / naysayer_stats['evaluations']
            print(f"\n   {self.naysayer.name}: {naysayer_stats['refutations']} refutations "
                  f"({refutation_rate:.1%} refutation rate)")
        
        # Knowledge base growth
        kb_stats = self.kb.get_statistics()
        print(f"\n📚 KNOWLEDGE BASE:")
        print(f"   Total Theorems: {kb_stats['total_theorems']}")
        print(f"   Novel Discoveries: {kb_stats['novel_discoveries']}")
        
        print(f"\n   By Field:")
        for field, count in kb_stats['by_field'].items():
            if count > 0:
                print(f"      {field}: {count}")
                
        # Show sample novel discoveries
        novel_theorems = self.kb.get_novel_discoveries()
        if novel_theorems:
            print(f"\n💡 SAMPLE NOVEL DISCOVERIES:")
            for theorem in novel_theorems[:3]:  # Show up to 3
                print(f"   • {theorem.statement[:60]}...")
                print(f"     (by {theorem.discovered_by}, field: {theorem.field.value})")
    
    def save_state(self, final: bool = False):
        """Save simulation state to files."""
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Save knowledge base (accumulates across runs)
        self.kb.save_to_file(self.knowledge_file)
        
        # Save simulation statistics (session-specific)
        stats_file = 'output/simulation_stats.json' if not final else 'output/simulation_final.json'
        with open(stats_file, 'w') as f:
            # Prepare stats for JSON serialization
            stats_to_save = {
                'timestamp': time.time(),
                'runtime': time.time() - self.start_time,
                'cycles': self.cycle_count,
                'statistics': self.stats,
                'kb_stats': self.kb.get_statistics()
            }
            json.dump(stats_to_save, f, indent=2)
        
        # Save timeline for monitoring
        with open('output/discovery_timeline.json', 'w') as f:
            json.dump(self.stats['discovery_timeline'], f, indent=2)
        
        # Save a session history file (append mode)
        history_file = 'output/discovery_history.jsonl'
        with open(history_file, 'a') as f:
            session_summary = {
                'session_id': f"session_{int(self.start_time)}",
                'timestamp': time.time(),
                'duration': time.time() - self.start_time,
                'cycles': self.cycle_count,
                'discoveries': self.stats['successful_discoveries'],
                'novel': self.stats['novel_theorems'],
                'refuted': self.stats['refuted_conjectures'],
                'total_kb_size': len(self.kb.theorems)
            }
            f.write(json.dumps(session_summary) + '\n')
        
        if final:
            print(f"\n💾 State saved to {stats_file}")
        else:
            print(f"💾 State saved (cycle {self.cycle_count})")

def main():
    parser = argparse.ArgumentParser(description='Run mathematical discovery simulation')
    parser.add_argument('--explorers', type=int, default=5, 
                       help='Number of explorer agents')
    parser.add_argument('--duration', type=int, default=60,
                       help='Simulation duration in seconds')
    parser.add_argument('--cycles', type=int, default=1000,
                       help='Maximum number of cycles')
    parser.add_argument('--save-interval', type=int, default=20,
                       help='Save state every N cycles')
    parser.add_argument('--fresh-start', action='store_true',
                       help='Start with fresh knowledge base (ignore previous discoveries)')
    parser.add_argument('--knowledge-file', default='output/knowledge_base.json',
                       help='Path to knowledge base file')
    
    args = parser.parse_args()
    
    sim = DiscoverySimulation(
        num_explorers=args.explorers,
        save_interval=args.save_interval,
        load_previous=not args.fresh_start,
        knowledge_file=args.knowledge_file
    )
    
    sim.run_simulation(
        duration_seconds=args.duration,
        max_cycles=args.cycles
    )

if __name__ == "__main__":
    main()