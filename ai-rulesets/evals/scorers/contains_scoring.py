#!/usr/bin/env python3
import json, sys, pathlib

def score_line(obj, model_output: str) -> dict:
    expected = obj.get("expected_contains", [])
    results = {k: (k.lower() in model_output.lower()) for k in expected}
    score = sum(results.values()) / max(1, len(expected))
    return {"id": obj.get("id"), "score": score, "details": results}

def main():
    if len(sys.argv) < 3:
        print("Usage: contains_scoring.py <cases.jsonl> <output.txt>")
        return 2
    cases = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
    output = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
    for line in cases:
        obj = json.loads(line)
        res = score_line(obj, output)
        print(json.dumps(res))

if __name__ == "__main__":
    main()
