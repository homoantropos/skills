# 🔴 KILLED — must not ship

- False premise that leads to wrong results or crashes (age as year difference, money in float, "this field always exists", one time zone, unlimited storage). Fixing a line doesn't help; it repeats. Minor consequence → rank by consequence.
- Tests pass, results guaranteed wrong. Silent lies outrank crashes.
- Guaranteed crash: unhandled errors.
- Freeze or blocked scrolling.
- Storage overflow, writes fail.
- Security hole: secret in code, config or history; injection (SQL, shell, HTML, path); missing or bypassable auth or access check; personal data exposed in logs, URLs or responses.
- Irreversible data loss: destructive migration without rollback, delete or overwrite without backup.
