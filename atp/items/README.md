# ATP item banks — `atp/items/*.json`

One JSON file per certification, named exactly after the cert id in
`atp/seed.py` (e.g. `atp-l4-math.json` for cert `atp-l4-math`). These are the
concrete exam questions behind each cert's blueprint. They are **generated +
human-editable**: SMEs edit these files directly; no build step.

**Blueprints-before-commissioning invariant** (docs/ATP.md §7): an exam can
only run for a cert whose item bank exists — `atp/exams.py` raises
`MissingItemBankError` otherwise. Adding a cert to the seed without adding its
bank here means it cannot be examined, by design.

## File format

```json
{
  "certId":  "atp-l4-math",          // must equal the filename + seed cert id
  "label":   "ATP-L4.math@2026.1",   // cosmetic, copied from the cert
  "version": "2026.1",               // bump when the bank changes materially
  "notes":   "free-text for SMEs",
  "items":   [ ... ]                 // the bank — see below
}
```

Each item:

| key        | type   | meaning |
|------------|--------|---------|
| `id`       | str    | stable unique id, `<cert-shorthand>-<sec>-NN` (e.g. `l4m-sym-01`). Never reuse or renumber a shipped id — evidence rows reference it forever. |
| `section`  | str    | MUST match one of the cert blueprint's `sections[].name` in `atp/seed.py` **verbatim** (copy-paste it). Unknown sections fail exam load. |
| `type`     | str    | one of `recall` \| `apply` \| `synthesize` \| `adversarial`, and it should be one of that section's `itemTypes` in the blueprint. |
| `prompt`   | str    | the question exactly as shown to the candidate model. Self-contained: include any passage/data inline. |
| `expected` | str    | reference answer **and/or grading criteria** for the judge model. State what full credit requires and name known-wrong answers where useful. Never shown to the candidate. |
| `points`   | int    | weight of the item *within its section* (section scores are points-weighted; sections are then combined by the blueprint's section weights). |

## Validation at exam load (`atp/exams.py`)

* file exists and has a non-empty `items` list;
* every item carries all six keys;
* every item's `section` is a blueprint section of the cert;
* every blueprint section has at least one item (otherwise the
  `passCriteria.perSection` bar would be unverifiable).

## How SMEs edit

1. Edit the cert's JSON in place (any editor; keep it valid JSON — trailing
   commas are not).
2. **Add** items freely (new ids, correct `section`/`type`); **retire** items
   by deleting them — but never recycle a deleted id.
3. Keep `expected` judge-ready: it is pasted into the judge prompt as the
   reference. Write criteria ("full credit requires…"), not just an answer,
   for synthesize/adversarial items.
4. Adversarial items should contain a trap (flawed premise, tempting wrong
   method) and `expected` must say what falling into the trap looks like.
5. Bump `version`, then sanity-check with a dry run (no model calls, no cost):

   ```bash
   BU_AUTH_DISABLED=1 python3 -m atp.exams atp-l4-math --dry-run --verify-chain
   ```

L5 (company-knowledge) banks additionally require SME sign-off on the cert
itself (`smeSignoff` in `atp/seed.py`) before awards are meaningful — the
bank alone is not enough (docs/ATP.md §1, L5 row).
