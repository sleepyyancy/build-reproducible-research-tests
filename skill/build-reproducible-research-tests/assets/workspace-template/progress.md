# Progress Log: {{TEST_TITLE}}

## Session: {{DATE}}

### Current phase
- **Status:** in progress
- Current objective: {{OBJECTIVE}}

### Actions
- {{ACTION}}

### Files created or changed
- {{RELATIVE_PATH_AND_REASON}}

## Run records
| Run ID | Entry point | Configuration | Start/end | Exit status | Log | Artifact status |
|---|---|---|---|---|---|---|
| {{RUN_ID}} | {{SCRIPT_OR_PROCESS}} | {{CONFIG_ID}} | {{TIME}} | {{STATUS}} | {{RELATIVE_PATH}} | {{COMPLETE_OR_PARTIAL}} |

## Verification results
| Check | Expected | Actual | Status | Evidence |
|---|---|---|---|---|
| {{CHECK}} | {{EXPECTED}} | {{ACTUAL}} | {{PASS|FAIL|WARN}} | {{RELATIVE_PATH_OR_NOTE}} |

## Error log
| Time | Stage | Error | Attempt | Resolution | Prior outputs valid? |
|---|---|---|---:|---|---|
| — | — | None | 0 | — | — |

## Recovery checkpoint
| Question | Answer |
|---|---|
| Current phase | {{PHASE}} |
| Next verified action | {{NEXT_ACTION}} |
| Goal | {{GOAL}} |
| Key findings | See `findings.md` |
| Last completed verification | {{CHECK_OR_NONE}} |
