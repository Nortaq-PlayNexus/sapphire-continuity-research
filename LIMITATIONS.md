# LIMITATIONS

## Scope Limitations
- **No OpenAI API access tested** - Credentials not configured/available. OpenAI mechanism tests are blocked or would need approval.
- **Local models only** - All testing uses Ollama models on local hardware (GTX 1080 8GB). Results may not generalize.
- **KV cache recovery uncertain** - Most local inference engines don't expose portable KV cache serialization. Ollama's capabilities need investigation.
- **Windows environment** - Process restart testing has platform-specific challenges.

## Methodological Limitations
- **H8 uses prompt injection, not real store** - The episodic-memory ChromaDB store exists but wasn't used as substrate in H8. We need to test with real store.
- **H3 untested** - Interruption/resumption across process restart is the key gap but technically complex.
- **Mechanism confounding** - Some mechanisms are hard to isolate cleanly in practice.
- **No_memory not memory-free** - As documented in CE-1, distractor episodes remain in no_memory condition.

## Known Blockers
- KV cache save/restore support in available engines needs verification
- Process restart automation on Windows needs care
- Some tests may require specific model availability

## What This Cannot Establish
- Consciousness, subjective experience, or "continuous existence" as metaphysical claims
- Parametric persistence without direct evidence
- Cross-environment portability without engine support
- Hidden OpenAI runtime state (correctly identified as not exposed via documented APIs)
