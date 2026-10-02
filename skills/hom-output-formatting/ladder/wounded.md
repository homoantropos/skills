# 🟠 WOUNDED — fix before commit

- Breaks the documented code style.
- No input guards.
- Obvious edge cases: offline, crash or reload mid-operation.
- Layout shift (CLS): the user taps the wrong button.
- Slowdown, or unjustified heavy data in memory.
- Async races, esp. storage read/write.
- Memory leak (freezes the app → 🔴).
- Security weakness with no shown exploit: unsafe defaults (debug on, CORS `*`), weak hashing or crypto, no rate limit on login.
