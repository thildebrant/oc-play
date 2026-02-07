#!/usr/bin/env python3
"""
Mathematical Discovery Simulation
Agents attempt to discover new theorems while a naysayer validates them
"""

import time
import json
import random
from typing import List, Dict, Optional
from knowledge_base import KnowledgeBase, MathTheorem
from explorer import ExplorerAgent
from naysayer import NaysayerAgent
import argparse
from datetime import datetime

class DiscoverySimulation:
    """Main simulation engine for mathematical discovery."""
    
    def __init__(self, num_explorers: int = 3, verbose: bool = True):
        self.kb = KnowledgeBase()
        self.explorers: List[ExplorerAgent] = []
        self.naysayer = NaysayerAgent("The Grand Skeptic")
        self.verbose = verbose
        self.discovery_history = []
        self.start_time = time.time()
        self.cycle_count = 0
        
        # Create explorer agents with different personalities
        explorer_names = [
            "Euler", "Gauss", "Ramanujan", "Fermat", "Newton",
            "Leibniz", "Hilbert", "Cantor", "Riemann", "Poincaré"
        ]
        
        for i in range(num_explorers):
            name = explorer_names[i % len(explorer_names)]
            self.explorers.append(ExplorerAgent(f"{name}_{i+1}"))
        
        if self.verbose:
            print("="*70)
            print("MATHEMATICAL DISCOVERY SIMULATION".center(70))
            print("="*70)
            print(f"Initialized with {num_explorers} explorer agents")
            print(f"Knowledge base contains {len(self.kb.theorems)} initial theorems")
            print(f"Naysayer: {self.naysayer.name}")
            print("="*70)
    
    def run_discovery_cycle(self) -> Dict:
        """Run one cycle of discovery attempts."""
        self.cycle_count += 1
        cycle_results = {
            'cycle': self.cycle_count,
            'timestamp': time.time(),
            'attempts': [],
            'discoveries': [],
            'rejections': []
        }
        
        # Shuffle order of explorers
        random.shuffle(self.explorers)
        
        for explorer in self.explorers:
            # Explorer attempts to make a discovery
            conjecture = explorer.explore(self.kb)
            
            if conjecture:
                attempt = {
                    'explorer': explorer.name,
                    'conjecture_id': conjecture.id,
                    'statement': conjecture.statement[:100] + "..." if len(conjecture.statement) > 100 else conjecture.statement
                }
                cycle_results['attempts'].append(attempt)
                
                # Naysayer evaluates the conjecture
                evaluation = self.naysayer.evaluate(conjecture, self.kb)
                
                if self.verbose:
                    print(f"\n🔬 {explorer.name} proposes:")
                    print(f"   {conjecture.statement[:80]}...")
                    print(f"   Field: {conjecture.field.value}, Difficulty: {conjecture.difficulty.value}")
                    print(f"   🤔 Naysayer: {evaluation}")
                
                if evaluation.verdict == 'accepted':
                    # Add to knowledge base
                    conjecture.is_novel = True
                    self.kb.add_theorem(conjecture)
                    explorer.record_success(conjecture)
                    
                    cycle_results['discoveries'].append({
                        'theorem_id': conjecture.id,
                        'explorer': explorer.name,
                        'field': conjecture.field.value
                    })
                    
                    self.discovery_history.append({
                        'cycle': self.cycle_count,
                        'time': time.time() - self.start_time,
                        'explorer': explorer.name,
                        'theorem': conjecture.statement,
                        'field': conjecture.field.value
                    })
                    
                    if self.verbose:
                        print(f"   ✅ DISCOVERY ACCEPTED! Added to knowledge base as {conjecture.id}")
                
                elif evaluation.verdict == 'rejected':
                    cycle_results['rejections'].append({
                        'explorer': explorer.name,
                        'reason': evaluation.reason,
                        'evidence': evaluation.evidence
                    })
                    
                    if self.verbose:
                        print(f"   ❌ REJECTED: {evaluation.reason}")
                
                elif evaluation.verdict == 'trivial':
                    if self.verbose:
                        print(f"   🤷 TRIVIAL: Not worth recording")
        
        return cycle_results
    
    def run_simulation(self, cycles: int = 100, save_interval: int = 10):
        """Run the complete simulation for specified cycles."""
        
        print(f"\n🚀 Starting simulation for {cycles} cycles...")
        print("-"*70)
        
        for i in range(cycles):
            # Run discovery cycle
            cycle_results = self.run_discovery_cycle()
            
            # Periodic status update
            if (i + 1) % 10 == 0:
                self.print_status()
            
            # Save progress periodically
            if (i + 1) % save_interval == 0:
                self.save_state(f"simulation_state_cycle_{i+1}.json")
            
            # Small delay to make monitoring easier
            time.sleep(0.1)
        
        # Final report
        self.print_final_report()
        
        # Save final state
        self.save_state("simulation_final.json")
    
    def print_status(self):
        """Print current simulation status."""
        stats = self.kb.get_statistics()
        
        print("\n" + "="*70)
        print(f"STATUS at cycle {self.cycle_count}".center(70))
        print("="*70)
        print(f"Knowledge Base: {stats['total_theorems']} theorems ({stats['novel_discoveries']} novel)")
        print(f"By Field: ", end="")
        for field, count in stats['by_field'].items():
            print(f"{field}: {count} ", end="")
        print()
        
        # Explorer stats
        print("\nExplorer Performance:")
        for explorer in self.explorers:
            e_stats = explorer.get_stats()
            print(f"  {explorer.name}: {e_stats['successes']}/{e_stats['attempts']} "
                  f"(success rate: {e_stats['success_rate']:.1%})")
        
        # Naysayer stats
        n_stats = self.naysayer.get_stats()
        print(f"\nNaysayer Stats:")
        print(f"  Evaluated: {n_stats['total_evaluated']}")
        print(f"  Rejected: {n_stats['rejections']} ({n_stats['rejection_rate']:.1%})")
        print(f"  Accepted: {n_stats['acceptances']} ({n_stats['acceptance_rate']:.1%})")
        print(f"  Trivial: {n_stats['trivial']}")
        print("="*70)
    
    def print_final_report(self):
        """Print comprehensive final report."""
        print("\n" + "="*70)
        print("FINAL REPORT".center(70))
        print("="*70)
        
        runtime = time.time() - self.start_time
        print(f"Simulation Runtime: {runtime:.2f} seconds")
        print(f"Total Cycles: {self.cycle_count}")
        
        stats = self.kb.get_statistics()
        print(f"\nKnowledge Base Growth:")
        print(f"  Started with: {len([t for t in self.kb.theorems.values() if not t.is_novel])} theorems")
        print(f"  Discovered: {stats['novel_discoveries']} new theorems")
        print(f"  Total: {stats['total_theorems']} theorems")
        
        # Field distribution
        print(f"\nDiscoveries by Field:")
        novel_by_field = {}
        for theorem in self.kb.get_novel_discoveries():
            field = theorem.field.value
            novel_by_field[field] = novel_by_field.get(field, 0) + 1
        
        for field, count in novel_by_field.items():
            print(f"  {field}: {count}")
        
        # Top explorers
        print(f"\nTop Explorers:")
        explorer_ranking = sorted(self.explorers, 
                                 key=lambda e: e.get_stats()['successes'], 
                                 reverse=True)
        for i, explorer in enumerate(explorer_ranking[:3], 1):
            stats = explorer.get_stats()
            print(f"  {i}. {explorer.name}: {stats['successes']} discoveries")
        
        # Sample discoveries
        print(f"\nSample Novel Discoveries:")
        novel = self.kb.get_novel_discoveries()
        for theorem in random.sample(novel, min(3, len(novel))):
            print(f"  • {theorem.statement[:80]}...")
            print(f"    (by {theorem.discovered_by}, field: {theorem.field.value})")
        
        print("="*70)
    
    def save_state(self, filename: str):
        """Save simulation state to file."""
        state = {
            'timestamp': datetime.now().isoformat(),
            'cycle': self.cycle_count,
            'runtime': time.time() - self.start_time,
            'statistics': self.kb.get_statistics(),
            'discovery_history': self.discovery_history[-50:],  # Last 50 discoveries
            'explorer_stats': [e.get_stats() for e in self.explorers],
            'naysayer_stats': self.naysayer.get_stats()
        }
        
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
        
        # Also save knowledge base
        self.kb.save_to_file(filename.replace('.json', '_kb.json'))
        
        if self.verbose:
            print(f"💾 State saved to {filename}")
    
    def load_state(self, filename: str):
        """Load simulation state from file."""
        with open(filename, 'r') as f:
            state = json.load(f)
        
        self.cycle_count = state['cycle']
        self.discovery_history = state['discovery_history']
        
        # Load knowledge base
        kb_file = filename.replace('.json', '_kb.json')
        self.kb.load_from_file(kb_file)
        
        print(f"📂 State loaded from {filename}")

def main():
    parser = argparse.ArgumentParser(description='Mathematical Discovery Simulation')
    parser.add_argument('--explorers', type=int, default=3, 
                       help='Number of explorer agents')
    parser.add_argument('--cycles', type=int, default=50,
                       help='Number of discovery cycles')
    parser.add_argument('--quiet', action='store_true',
                       help='Run in quiet mode')
    parser.add_argument('--load', type=str,
                       help='Load previous simulation state')
    
    args = parser.parse_args()
    
    # Create and run simulation
    sim = DiscoverySimulation(
        num_explorers=args.explorers,
        verbose=not args.quiet
    )
    
    if args.load:
        sim.load_state(args.load)
    
    try:
        sim.run_simulation(cycles=args.cycles)
    except KeyboardInterrupt:
        print("\n\n⚠️ Simulation interrupted by user")
        sim.print_final_report()
        sim.save_state("simulation_interrupted.json")

if __name__ == "__main__":
    main()