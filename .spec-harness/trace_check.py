#!/usr/bin/env python3
"""spec-harness traceability check.

Deterministic, stdlib-only. Fails (exit 1) when specs drift apart.

Checks
  1. COVERAGE  every ID defined in the authority spec appears in each dependent
               spec that is configured to cover that ID family (ranges such as
               "BR-30 to BR-34" or "BR-30..34" count as covering the span).
  2. ORPHANS   IDs of an authority family that appear in a dependent but not in
               the authority (typo, or a requirement that was deleted).
  3. LOCAL     IDs owned by a dependent (e.g. T-01 gaps) that are referenced but
               never defined in a table row "| T-01 |".
  4. TABLES    markdown tables whose rows have inconsistent column counts.

Usage
  python3 trace_check.py [--config .spec-harness/config.json] [--json] [--root DIR]

Config (JSON)
  {
    "authority": "docs/Business Spec.md",
    "families": {"BR": "BR-\\d+", "CAP": "CAP-\\d+", "D": "D-\\d+"},
    "dependents": [
      {"path": "docs/Tech Spec.md", "covers": ["BR", "CAP", "D"],
       "local_families": {"T": "T-\\d+"}}
    ],
    "retired": ["BR-31"],
    "ignore": ["E-03"]
  }
"""
import argparse, json, os, re, sys


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return f.read()


def ids_in(text, pattern):
    return set(re.findall(r"\b(?:%s)\b" % pattern, text))


def expand_ranges(text, prefix):
    """IDs covered by ranges like 'BR-30 to BR-34', 'BR-30..34', 'BR-30–34'."""
    out = set()
    rx = re.compile(
        r"\b%s-(\d+)\s*(?:to|\.\.|–|—|-|…)\s*(?:%s-)?(\d+)\b" % (prefix, prefix)
    )
    for a, b in rx.findall(text):
        lo, hi = int(a), int(b)
        if lo < hi and hi - lo < 200:
            width = len(a)
            out.update("%s-%0*d" % (prefix, width, n) for n in range(lo, hi + 1))
    return out


def check_tables(name, text):
    problems, lines, i = [], text.split("\n"), 0
    in_fence = False
    while i < len(lines):
        if lines[i].lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and lines[i].startswith("|"):
            j, n = i, None
            while j < len(lines) and lines[j].startswith("|"):
                c = len(re.findall(r"(?<!\\)\|", lines[j]))
                if n is None:
                    n = c
                elif c != n:
                    problems.append(
                        "%s:%d table row has %d pipes, header has %d: %s"
                        % (name, j + 1, c, n, lines[j][:60])
                    )
                j += 1
            i = j
        else:
            i += 1
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=".spec-harness/config.json")
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    cfg_path = os.path.join(a.root, a.config)
    if not os.path.exists(cfg_path):
        print("config not found: %s (run /spec-harness:spec-init)" % cfg_path, file=sys.stderr)
        return 2
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    ignore = set(cfg.get("ignore", []))
    retired = set(cfg.get("retired", []))  # IDs deliberately retired: may be mentioned, never required
    fam = cfg["families"]
    auth_text = read(a.root, cfg["authority"])
    auth_ids = {k: ids_in(auth_text, p) - ignore for k, p in fam.items()}

    findings = []  # (severity, rule, message)
    summary = {"authority": cfg["authority"], "ids": {k: len(v) for k, v in auth_ids.items()}}

    findings += [("error", "TABLES", m) for m in check_tables(cfg["authority"], auth_text)]

    for dep in cfg.get("dependents", []):
        path = dep["path"]
        if not os.path.exists(os.path.join(a.root, path)):
            findings.append(("error", "MISSING", "dependent not found: %s" % path))
            continue
        text = read(a.root, path)
        for k in dep.get("covers", []):
            prefix = fam[k].split("-")[0]
            present = ids_in(text, fam[k]) | expand_ranges(text, prefix)
            missing = sorted(auth_ids[k] - present - retired)
            orphan = sorted((ids_in(text, fam[k]) - auth_ids[k]) - ignore - retired)
            if missing:
                findings.append(("error", "COVERAGE", "%s: %d %s id(s) in authority not in dependent: %s"
                                 % (path, len(missing), k, ", ".join(missing))))
            if orphan:
                findings.append(("error", "ORPHAN", "%s: %s id(s) not in authority: %s"
                                 % (path, k, ", ".join(orphan))))
        for k, p in dep.get("local_families", {}).items():
            refs = ids_in(text, p) - ignore
            defs = set(re.findall(r"\|\s*\**(%s)\**\s*\|" % p, text))
            undefined = sorted(refs - defs)
            if undefined:
                findings.append(("error", "LOCAL", "%s: %s id(s) referenced but not defined in a table: %s"
                                 % (path, k, ", ".join(undefined))))
        findings += [("error", "TABLES", m) for m in check_tables(path, text)]

    errors = [f for f in findings if f[0] == "error"]
    if a.json:
        print(json.dumps({"summary": summary, "findings": findings, "ok": not errors}, indent=2))
    else:
        print("authority: %s  %s" % (cfg["authority"], summary["ids"]))
        for sev, rule, msg in findings:
            print("[%s] %-8s %s" % (sev.upper(), rule, msg))
        print("PASS" if not errors else "FAIL: %d finding(s)" % len(errors))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
