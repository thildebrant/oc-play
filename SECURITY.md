# Security Policy

## ⚠️ Disclaimer

**This code has NOT been professionally security reviewed and contains known vulnerabilities.**

This is experimental research software intended for **educational and research purposes only** in controlled, offline environments. By using this software, you acknowledge and accept all risks.

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY ARISING FROM THE USE OF THIS SOFTWARE.**

## Known Security Issues

### HIGH SEVERITY

**Code Injection via SymPy `sympify()`**
- **Affected Files**: `math-discovery/knowledge_base.py`, `math-discovery/naysayer.py`
- **Risk**: Arbitrary Python code execution when processing malicious JSON files
- **Impact**: Remote code execution, system compromise
- **Mitigation**: Do not load JSON files from untrusted sources

### MEDIUM SEVERITY

**Path Traversal in File Operations**
- **Affected Files**: `math-discovery/discovery_sim.py`, `math-discovery/knowledge_base.py`
- **Risk**: Command-line arguments can specify arbitrary file paths
- **Impact**: Reading/writing files outside intended directories
- **Mitigation**: Only use with trusted command-line arguments

**JSON Deserialization Without Validation**
- **Affected Files**: All JSON-loading code
- **Risk**: Malformed or malicious JSON can cause crashes or resource exhaustion
- **Impact**: Denial of service, unexpected behavior
- **Mitigation**: Only load JSON files you created yourself

**Resource Exhaustion**
- **Affected Files**: `math-discovery/naysayer.py`, `corewars/mars.py`
- **Risk**: No limits on memory-intensive operations
- **Impact**: System slowdown, crashes, memory exhaustion
- **Mitigation**: Monitor resource usage, use reasonable input values

## Safe Usage Guidelines

To minimize risk when using this software:

1. **Run in isolated environments** (virtual machines, containers)
2. **Never load untrusted JSON files** or external data
3. **Do not expose to network access** (localhost only)
4. **Monitor system resources** when running simulations
5. **Use default command-line arguments** unless you understand the risks
6. **Keep dependencies updated** (`pip install -U -r requirements.txt`)
7. **Do not run as root/administrator**

## Reporting a Vulnerability

If you discover additional security issues in this project:

1. **Open a GitHub issue** with details (if not actively exploited in the wild)
2. **Contact the repository owner directly** for critical vulnerabilities
3. Include proof of concept if possible

This is an experimental project and does not handle sensitive production data, but security reports are appreciated for educational purposes.

## Scope

This repository contains two self-contained, offline Python projects:

1. **Core Wars AI Battle Arena** - Genetic algorithm-driven code warriors
2. **Mathematical Discovery Simulation** - Multi-agent theorem exploration

**Neither project is intended for production use.** The HTML dashboards are for local viewing only and should never be exposed to public networks.

## Out of Scope

The following are considered out of scope for security concerns:

- Denial of service via intentionally malicious command-line arguments
- Resource exhaustion from intentionally extreme parameter values
- Any use case involving untrusted data or network exposure
- Production deployments (explicitly not supported)
