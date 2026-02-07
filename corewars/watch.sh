#!/bin/bash
# Quick script to watch Core Wars battles

echo "🎮 Core Wars Battle Arena 🎮"
echo ""
echo "Choose an option:"
echo "1) Quick visual battle"
echo "2) Tournament (5 rounds)"
echo "3) Evolution demo"
echo "4) Long tournament (20 rounds with evolution)"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        python3 battle.py --quick --visualize
        ;;
    2)
        python3 battle.py --rounds 5
        ;;
    3)
        python3 examples.py
        ;;
    4)
        python3 battle.py --rounds 20 --visualize
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac