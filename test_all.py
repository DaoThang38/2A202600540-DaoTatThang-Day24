import subprocess
import sys

def run_and_print(cmd):
    print(f"\n=============================\nRunning: {' '.join(cmd)}\n=============================\n")
    # Using encoding='utf-8' explicitly
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    return result.returncode

if __name__ == "__main__":
    run_and_print(["pytest", "tests/", "-v"])
    run_and_print([sys.executable, "src/phase_a_ragas.py"])
    run_and_print([sys.executable, "src/phase_b_judge.py"])
    run_and_print([sys.executable, "src/phase_c_guard.py"])
    run_and_print([sys.executable, "check_lab.py"])
