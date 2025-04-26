#!/usr/bin/env python3
import os, random, string, hashlib, time, csv, importlib
from datetime import datetime

# ensure our temp‐dir exists
os.makedirs("temp_fuzz_files", exist_ok=True)

# load your top‐5
with open("fuzz_targets.txt") as f:
    targets = [line.strip() for line in f if line.strip()]

# dynamic import helper
def resolve(fn_name):
    module, _, func = fn_name.rpartition(".")
    mod = importlib.import_module(module)
    return getattr(mod, func)

# build a small pool of random inputs
GENERIC_INPUTS = [
    None,
    0, 1, -1, 3.14,
    "", "foo", "{}", "[]", "null",
    [], {}, [1,2,3], {"a":1},
    True, False
]

rows = []
for fn_name in targets:
    fn = resolve(fn_name)
    for _ in range(30):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if fn_name.endswith("loadMultiYAML"):
            content = "\n".join(
                "".join(random.choices(string.ascii_letters + string.digits, k=10))
                for _ in range(random.randint(1,5))
            )
            fname = f"temp_fuzz_files/fuzz_{hashlib.md5(content.encode()).hexdigest()[:6]}.yaml"
            with open(fname, "w") as yf:
                yf.write(content)
            inp = fname
            ih = hashlib.md5(content.encode()).hexdigest()
        else:
            inp = random.choice(GENERIC_INPUTS)
            ih = hashlib.md5(repr(inp).encode()).hexdigest()

        start = time.time()
        try:
            result = fn(inp)
            status, exc_type, exc_msg = "PASS", "", ""
        except Exception as e:
            status, exc_type, exc_msg = "FAIL", type(e).__name__, str(e)
            result = None
        elapsed = int((time.time() - start) * 1_000)

        rows.append({
            "timestamp":         ts,
            "function":          fn_name,
            "yaml_file":         inp if fn_name.endswith("loadMultiYAML") else "",
            "input_hash":        ih,
            "result_status":     status,
            "exception_type":    exc_type,
            "exception_message": exc_msg,
            "execution_time_ms": elapsed,
            # optional YAML fields:
            "security_finding":     getattr(result, "security_finding", ""),
            "severity":             getattr(result, "severity", ""),
            "vulnerability_type":   getattr(result, "vulnerability_type", ""),
            "has_privilege_issues": getattr(result, "has_privilege_issues", ""),
            "has_http_issues":      getattr(result, "has_http_issues", ""),
            "has_seccomp_issues":   getattr(result, "has_seccomp_issues", ""),
            "has_secret_issues":    getattr(result, "has_secret_issues", ""),
            "has_hpa_issues":       getattr(result, "has_hpa_issues", ""),
            "yaml_valid":           getattr(result, "yaml_valid", ""),
            "resource_kind":        getattr(result, "resource_kind", ""),
        })

# write out exactly as your screenshot
fieldnames = list(rows[0].keys())
with open("fuzz.csv", "w", newline="") as csvf:
    writer = csv.DictWriter(csvf, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# force an immediate, clean exit (skips all destructors & flushes)
os._exit(0)
