# Software Quality Assurance Final Group Project Report

## Overview

This project aimed to integrate software quality assurance (SQA) activities into an existing Python project. The primary tasks were focused on security automation, dynamic testing (fuzzing), and forensic tracking, following three main requirements:

## 4.a Git Hook for Security Reporting

### Activity:
- Developed a Git Hook that triggers static code analysis on every `git commit` involving Python files.
- The hook automatically scans the codebase for security weaknesses using a scanner and outputs findings into a CSV file (`fuzz.csv`).
- Integrated Bandit security analysis tool within GitHub Actions workflows (`.github/workflows/ci.yml` and `python.build.yml`) to ensure continuous security checks.
- Implemented a simple Python-based custom scanner (`scanner.py`) tailored for YAML files to find misconfigurations and secrets leakage.

### Files Created/Modified:

- `.github/workflows/ci.yml`
- `.github/workflows/python.build.yml`
- `scanner.py`
- Git Hook script for pre-commit (configured locally during development).

### Results:
- Security vulnerabilities are detected early during development.
- The CSV report (`fuzz.csv`) provides a clear, structured record of vulnerabilities found.
- Automation reduced the risk of manual errors and enforced security compliance at each commit.


## 4.b Fuzz Testing (fuzz.py)

### Activity:
- Developed `fuzz.py` to dynamically fuzz 5 selected Python methods.
- Chose methods from different modules to ensure broad code coverage:
  - Functions from `parser.py`, `scanner.py`, and `graph_analysis.py`.
- Random alphanumeric strings and edge case inputs were used as fuzz inputs.
- Recorded any crashes or unexpected behavior into the fuzz report CSV.

### Files Created/Modified:
- `fuzz.py`
- `fuzz_targets.txt`
- `fuzz.csv`
- GitHub Actions configured to automatically run fuzz.py during CI/CD.

### Results:
- Fuzzing helped identify edge cases not considered in normal unit tests.
- Minor issues and unexpected input-handling failures were discovered, which were fixed based on fuzz outputs.
- Fuzzing automation in CI ensures that regression bugs will be caught early in future changes.


## 4.c Forensics Integration

### Activity:
- Added forensic logging to 5 selected Python methods.
- Forensic logging tracks the inputs and execution paths during runtime for later investigation and auditing.
- Integrated `forensics.py` with simple logging functions.
- Each key method was modified to call the forensic logger at the beginning and end of execution.
- All forensic logs were captured into a single `forensics.log` file for post-mortem analysis.

### Files Created/Modified:
- `forensics.py`
- Modified methods in:
  - `parser.py`
  - `scanner.py`
  - `graph_analysis.py`
  - `main.py`
  - `constants.py`
- Created `forensics.log` to store the runtime logs.

### Results:
- Ensured traceability and accountability for code execution during runtime.
- The forensic logs provide valuable information for debugging, security auditing, and understanding runtime behavior.
- Helped reinforce secure software development practices by maintaining an execution audit trail.


## Lessons Learned

- **Automation in SQA**:  
  Automating security scans, fuzz tests, and forensic tracking dramatically increases software reliability and reduces manual errors.

- **Fuzz Testing Value**:  
  Randomized dynamic testing exposed hidden bugs that static analysis and unit tests missed.

- **Security Best Practices**:  
  Hard-coded secrets and YAML misconfigurations are common risks. Continuous scanning keeps these vulnerabilities in check.

- **Importance of Logging**:  
  Proper forensic logging not only helps in debugging but also provides legal evidence in case of security incidents.

- **Working with GitHub Actions**:  
  Learned how to automate complex workflows in GitHub, including CI/CD pipelines for static analysis, testing, and dynamic fuzzing.

- **Challenges**:  
  - Integrating forensic logs without modifying original business logic was tricky.
  - Handling different types of fuzz input generation for various functions was challenging.
  - Setting up correct permissions and paths for GitHub Actions required attention to detail.


# Final Deliverables

- Static security analysis via Git Hook and CI pipelines.
- Dynamic fuzz testing with fuzz.py automated in GitHub Actions.
- Forensic logging integrated into major project modules.
- Clear documentation and structured outputs (`fuzz.csv`, `forensics.log`).
