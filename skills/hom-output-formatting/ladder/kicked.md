# 🟡 KICKED IN THE PANTS — should fix

- Missing error handling where failure is possible.
- Invasive code that worsens merge conflicts.
- Unagreed changes outside the task.
- Commit history vs documented style or task.
- UI doesn't match the task.
- No backup of stored data.
- A "run again" request that arrives during the last allowed run of a loop capped at N runs is dropped → the work waits until something unrelated restarts the loop. Delay only, needs that timing.
- A click-suppression window after long-press that starts when the timer fires, not on release → a hold longer than the window also fires the click: one gesture, two actions. Needs a long hold.
- Streamed text deltas still applied after the final result is shown → the final message flickers or is overwritten by stray text; ignore deltas once final, reset per send. Visible glitch, no data harm.
