# oc-play

OpenClaw agent playground — a collection of experiments exploring AI agents in competitive and discovery settings.

## ⚠️ Security Warning

**USE AT YOUR OWN RISK.** This is experimental research code that has **NOT** been professionally security audited. The code contains known vulnerabilities including:

- **Code injection vulnerabilities** via SymPy expression parsing
- **Path traversal risks** in file operations
- **Resource exhaustion potential** without proper limits
- **Unvalidated input processing** from JSON files

**DO NOT:**
- Use this code in production environments
- Process untrusted or user-supplied data
- Expose this code to the internet
- Load JSON files from untrusted sources

**This software is provided "AS IS" without warranty of any kind.** It is intended for educational and research purposes only in controlled, offline environments. See [SECURITY.md](SECURITY.md) for details.

## Projects

### Core Wars AI Battle Arena (`corewars/`)

A Python implementation of the classic [Core Wars](https://www.corewars.org/) programming game, extended with AI agents that generate, evolve, and analyze Redcode warriors using genetic algorithms. Includes a MARS (Memory Array Redcode Simulator), tactical analysis, and a browser-based visualization dashboard.

**Run it:**
```bash
cd corewars
./watch.sh
```

### Mathematical Discovery Simulation (`math-discovery/`)

A multi-agent simulation where "explorer" agents generate mathematical conjectures and a "naysayer" agent attempts to refute them via counterexample search and symbolic verification (powered by SymPy). Tracks discoveries in a knowledge base and provides a browser dashboard for visualization.

**Setup and run:**
```bash
cd math-discovery
pip install -r requirements.txt
python3 quick_demo.py
```

## License

[MIT](LICENSE)
