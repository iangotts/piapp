# PIapp — agent instructions

PIapp uses spec. Read `.spec/constitution.md` first.

- Authority: `docs/PIapp Biz Spec v5.0.md`. Tech Spec v3.0 and UI Spec v3.0 implement it.
- Decisions: `docs/decisions.md` (append only). Business decisions D-01..D-23 live in the Business Spec; technical ones are ADR-001..027 in the Tech Spec.
- Check: `python3 .spec/trace_check.py` must pass before approving specs or building.
- Stop and ask at the human gates in the constitution (section 4), plus the PIapp rules in section 8.
- Open technical gaps T-01..T-12 (Tech Spec section 19) are not decided. Do not build anything that depends on one without asking.
