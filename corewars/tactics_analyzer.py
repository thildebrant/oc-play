#!/usr/bin/env python3
"""
Tactics Analyzer - Examines different Core Wars strategies and tactics
"""

import json
import time
from typing import Dict, List, Tuple
from collections import defaultdict
from mars import MARS, Warrior, Instruction, Opcode, AddressMode
from ai_agent import WarriorGenerator, AIAgent
from battle import BattleRunner

class TacticsAnalyzer:
    """Analyze warrior tactics and strategies."""
    
    def __init__(self):
        self.battles_data = []
        self.strategy_stats = defaultdict(lambda: {
            'wins': 0, 'losses': 0, 'draws': 0, 
            'total_cycles': 0, 'battles': 0,
            'kills': 0, 'deaths': 0
        })
        
    def analyze_warrior_code(self, warrior: Warrior) -> Dict:
        """Analyze warrior code to determine tactics."""
        analysis = {
            'name': warrior.name,
            'author': warrior.author,
            'length': len(warrior.program),
            'instructions': {},
            'patterns': [],
            'strategy': 'unknown'
        }
        
        # Count instruction types
        for inst in warrior.program:
            opcode = inst.opcode.value
            analysis['instructions'][opcode] = analysis['instructions'].get(opcode, 0) + 1
        
        # Detect patterns
        inst_types = set(inst.opcode for inst in warrior.program)
        
        # Imp detection (single MOV 0,1)
        if len(warrior.program) == 1:
            inst = warrior.program[0]
            if inst.opcode == Opcode.MOV and inst.a_value == 0 and inst.b_value == 1:
                analysis['patterns'].append('imp')
                analysis['strategy'] = 'imp'
        
        # Bomber detection (MOV + ADD/SUB + JMP pattern)
        if Opcode.MOV in inst_types and (Opcode.ADD in inst_types or Opcode.SUB in inst_types) and Opcode.JMP in inst_types:
            analysis['patterns'].append('bomber')
            if analysis['strategy'] == 'unknown':
                analysis['strategy'] = 'bomber'
        
        # Scanner detection (CMP/SEQ/SNE + JMP pattern)
        if (Opcode.CMP in inst_types or Opcode.SEQ in inst_types or Opcode.SNE in inst_types):
            analysis['patterns'].append('scanner')
            if analysis['strategy'] == 'unknown':
                analysis['strategy'] = 'scanner'
        
        # Replicator detection (SPL instruction)
        if Opcode.SPL in inst_types:
            analysis['patterns'].append('replicator')
            if analysis['strategy'] == 'unknown':
                analysis['strategy'] = 'replicator'
        
        # Clear detection (lots of DAT)
        dat_ratio = analysis['instructions'].get('DAT', 0) / len(warrior.program)
        if dat_ratio > 0.3:
            analysis['patterns'].append('clear')
            if analysis['strategy'] == 'unknown':
                analysis['strategy'] = 'clear'
        
        # Quick scanner (short with CMP)
        if len(warrior.program) < 10 and (Opcode.CMP in inst_types or Opcode.SEQ in inst_types):
            analysis['patterns'].append('quick-scan')
        
        # Stone (optimized bomber)
        if len(warrior.program) == 4 and Opcode.MOV in inst_types and Opcode.ADD in inst_types:
            analysis['patterns'].append('stone')
            analysis['strategy'] = 'stone'
        
        # Paper (replicator that spreads)
        if Opcode.SPL in inst_types and Opcode.MOV in inst_types and len(warrior.program) > 5:
            analysis['patterns'].append('paper')
            analysis['strategy'] = 'paper'
        
        return analysis
    
    def run_strategy_tournament(self) -> Dict:
        """Run tournament between different strategies."""
        print("\n" + "="*70)
        print("CORE WARS STRATEGY TOURNAMENT".center(70))
        print("="*70)
        
        strategies = ['imp', 'dwarf', 'bomber', 'scanner', 'replicator', 'paper']
        warriors = {}
        
        # Create warriors for each strategy
        print("\n📋 Creating Warriors:")
        for strategy in strategies:
            warrior = WarriorGenerator.generate_warrior(f"{strategy.title()}", strategy=strategy)
            warriors[strategy] = warrior
            analysis = self.analyze_warrior_code(warrior)
            print(f"  • {strategy.title()}: {analysis['length']} instructions, patterns: {', '.join(analysis['patterns'])}")
        
        # Add some classic warriors
        warriors['classic_dwarf'] = Warrior("Classic Dwarf", [
            Instruction(Opcode.ADD, AddressMode.IMMEDIATE, 4, AddressMode.DIRECT, 3),
            Instruction(Opcode.MOV, AddressMode.DIRECT, 2, AddressMode.INDIRECT, 2),
            Instruction(Opcode.JMP, AddressMode.DIRECT, -2, AddressMode.DIRECT, 0),
            Instruction(Opcode.DAT, AddressMode.IMMEDIATE, 0, AddressMode.IMMEDIATE, 0)
        ], author="Classic")
        
        warriors['stone'] = Warrior("Stone", [
            Instruction(Opcode.MOV, AddressMode.INDIRECT, 0, AddressMode.INDIRECT, 2),
            Instruction(Opcode.ADD, AddressMode.IMMEDIATE, 2, AddressMode.DIRECT, -1),
            Instruction(Opcode.JMP, AddressMode.DIRECT, -2, AddressMode.DIRECT, 0),
            Instruction(Opcode.DAT, AddressMode.IMMEDIATE, 0, AddressMode.IMMEDIATE, 2)
        ], author="Optimized")
        
        # Round-robin tournament
        print("\n⚔️ Running Round-Robin Tournament:")
        print("-" * 70)
        
        results = defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0})
        detailed_results = []
        
        warrior_list = list(warriors.items())
        for i, (name1, warrior1) in enumerate(warrior_list):
            for j, (name2, warrior2) in enumerate(warrior_list[i+1:], i+1):
                print(f"\n  Battle: {name1} vs {name2}")
                
                # Run 3 battles to reduce randomness
                battle_results = {'w1': 0, 'w2': 0, 'draw': 0}
                
                for round_num in range(3):
                    mars = MARS(core_size=8000, max_cycles=80000)
                    
                    # Clone warriors to avoid mutation
                    w1 = Warrior(warrior1.name, warrior1.program[:], warrior1.author)
                    w2 = Warrior(warrior2.name, warrior2.program[:], warrior2.author)
                    
                    mars.load_warrior(w1)
                    mars.load_warrior(w2)
                    
                    winner = mars.run_battle()
                    
                    if winner:
                        if winner.name == w1.name:
                            battle_results['w1'] += 1
                        else:
                            battle_results['w2'] += 1
                    else:
                        battle_results['draw'] += 1
                    
                    # Record detailed data
                    self.battles_data.append({
                        'warrior1': name1,
                        'warrior2': name2,
                        'winner': winner.name if winner else 'DRAW',
                        'cycles': mars.cycle,
                        'round': round_num + 1
                    })
                
                # Determine overall winner
                print(f"    Results: {name1}: {battle_results['w1']}, {name2}: {battle_results['w2']}, Draws: {battle_results['draw']}")
                
                if battle_results['w1'] > battle_results['w2']:
                    results[name1]['wins'] += 1
                    results[name2]['losses'] += 1
                    print(f"    ✓ {name1} wins overall")
                elif battle_results['w2'] > battle_results['w1']:
                    results[name2]['wins'] += 1
                    results[name1]['losses'] += 1
                    print(f"    ✓ {name2} wins overall")
                else:
                    results[name1]['draws'] += 1
                    results[name2]['draws'] += 1
                    print(f"    = Draw overall")
                
                # Update strategy stats
                self.update_strategy_stats(name1, warrior1, battle_results['w1'], 
                                          battle_results['draw'], battle_results['w2'])
                self.update_strategy_stats(name2, warrior2, battle_results['w2'], 
                                          battle_results['draw'], battle_results['w1'])
        
        # Calculate rankings
        print("\n" + "="*70)
        print("TOURNAMENT RANKINGS".center(70))
        print("="*70)
        
        rankings = []
        for name, stats in results.items():
            points = stats['wins'] * 3 + stats['draws']
            win_rate = stats['wins'] / (stats['wins'] + stats['losses'] + stats['draws'])
            rankings.append({
                'name': name,
                'points': points,
                'wins': stats['wins'],
                'draws': stats['draws'],
                'losses': stats['losses'],
                'win_rate': win_rate
            })
        
        rankings.sort(key=lambda x: x['points'], reverse=True)
        
        print(f"\n{'Rank':<6} {'Strategy':<15} {'Points':<8} {'W-D-L':<12} {'Win Rate':<10}")
        print("-" * 70)
        for i, rank in enumerate(rankings, 1):
            wdl = f"{rank['wins']}-{rank['draws']}-{rank['losses']}"
            print(f"{i:<6} {rank['name']:<15} {rank['points']:<8} {wdl:<12} {rank['win_rate']:.1%}")
        
        return {
            'rankings': rankings,
            'detailed_battles': self.battles_data,
            'strategy_stats': dict(self.strategy_stats)
        }
    
    def update_strategy_stats(self, name: str, warrior: Warrior, wins: int, draws: int, losses: int):
        """Update strategy statistics."""
        analysis = self.analyze_warrior_code(warrior)
        strategy = analysis['strategy']
        
        self.strategy_stats[strategy]['battles'] += wins + draws + losses
        self.strategy_stats[strategy]['wins'] += wins
        self.strategy_stats[strategy]['draws'] += draws
        self.strategy_stats[strategy]['losses'] += losses
    
    def analyze_tactics_effectiveness(self) -> Dict:
        """Analyze which tactics are most effective."""
        print("\n" + "="*70)
        print("TACTICS EFFECTIVENESS ANALYSIS".center(70))
        print("="*70)
        
        effectiveness = {}
        for strategy, stats in self.strategy_stats.items():
            if stats['battles'] > 0:
                win_rate = stats['wins'] / stats['battles']
                effectiveness[strategy] = {
                    'win_rate': win_rate,
                    'total_battles': stats['battles'],
                    'wins': stats['wins'],
                    'draws': stats['draws'],
                    'losses': stats['losses']
                }
        
        # Sort by effectiveness
        sorted_tactics = sorted(effectiveness.items(), key=lambda x: x[1]['win_rate'], reverse=True)
        
        print(f"\n{'Tactic':<15} {'Win Rate':<12} {'Battles':<10} {'Performance':<20}")
        print("-" * 70)
        
        for tactic, data in sorted_tactics:
            perf = f"W:{data['wins']} D:{data['draws']} L:{data['losses']}"
            print(f"{tactic:<15} {data['win_rate']:.1%}{'':5} {data['total_battles']:<10} {perf:<20}")
        
        return effectiveness

def main():
    analyzer = TacticsAnalyzer()
    
    # Run strategy tournament
    tournament_results = analyzer.run_strategy_tournament()
    
    # Analyze effectiveness
    effectiveness = analyzer.analyze_tactics_effectiveness()
    
    # Save results to JSON for webpage
    results = {
        'tournament': tournament_results,
        'effectiveness': effectiveness,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('tournament_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Tournament complete! Results saved to tournament_results.json")
    print("   Run 'python3 -m http.server 8000' and open index.html to view the webpage.")

if __name__ == "__main__":
    main()