import sys
import asyncio
import json

from src.phase_c_guard import run_adversarial_suite

def main():
    with open("adversarial_set_20.json", encoding="utf-8") as f:
        adv_set = json.load(f)
    results = run_adversarial_suite(adv_set)
    passed = 0
    for i, r in enumerate(results):
        if r["passed"]:
            passed += 1
        else:
            print(f"FAILED TO BLOCK [{r['category']}]: {adv_set[i]['input']}")
            print(f"ACTUAL: {r['actual']}")
    print(f"PASS RATE: {passed}/{len(results)}")

if __name__ == "__main__":
    main()
