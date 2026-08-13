# Kapture Finance Collections Voicebot — Vapi Submission

## What is included
- `Kapture_Finance_Collections_Voicebot_HLD.pdf` — engineer-facing HLD.
- `architecture_diagram.png` — architecture diagram.
- `system_prompt.txt` — final assistant system prompt.
- `tool_schemas.json` — Vapi function tool schemas.
- `mock_server.py` — FastAPI mock endpoint for Vapi tool calls.
- `vapi_assistant_config.json` — proposed assistant configuration.

## Setup
1. Create a Vapi account and assistant.
2. Add a phone number and assign the assistant.
3. Add the five custom function tools. Vapi custom tools support function parameters and a server URL; tool calls are posted to the configured server and the server returns results by `toolCallId`.
4. Run the mock server:
   `pip install fastapi uvicorn`
   `uvicorn mock_server:app --port 3000`
5. Expose it publicly for Vapi testing (for example, a tunnel), then put the public URL into the tools' Server URL. Vapi's local-development flow uses a tunnel plus its CLI forwarder.
6. Paste `system_prompt.txt` into the assistant's system prompt and attach the tools.
7. Use a test customer reference `rahul_demo`; the mock verification value is `1998`. Replace all demo data before production.
8. Test two scripts:
   - PTP: verified customer → says they can pay ₹8,499 on a specific date → log PTP → optional payment link → disposition `ptp`.
   - Already paid: verified customer → says payment already made → do not pressure → disposition `already_paid`.
9. Record the calls or make a 2–4 minute Loom and submit its link.

## Design choices
- Low temperature reduces creative policy drift.
- Streaming phone-oriented STT and a natural professional voice minimize turn latency.
- The deterministic state machine is the security boundary. The LLM is not trusted to decide whether debt may be disclosed.
- Tool endpoints are mocked for the assignment; production should connect to authenticated collections APIs and a durable audit store.
- Use Vapi custom credentials/authentication for protected server URLs in production.

## What broke / debugging notes
The implementation intentionally uses mocked APIs because real Kapture Finance systems are unavailable in an assignment environment. Validate the exact Vapi dashboard fields against the current account UI. For tool debugging, inspect Vapi tool-call payloads, verify the returned `toolCallId`, and test each tool independently before full-call testing.

## Improvements with more time
- Add a real policy engine and DNC service.
- Add multilingual approved scripts and language detection.
- Add durable idempotency keys for tool calls.
- Add automated red-team tests for debt leakage, prompt injection, coercion, and off-topic requests.
- Add dashboards for PTP conversion, p95 latency, tool failures, and policy blocks.
