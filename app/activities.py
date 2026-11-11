import hashlib
import hmac
import os

from temporalio import activity

# Optional: a model writes the greeting when ANTHROPIC_API_KEY is set (any Anthropic-compatible
# endpoint via ANTHROPIC_BASE_URL); otherwise the fixed greeting.
MODEL = os.environ.get("GREETINGS_MODEL", "claude-haiku-4-5")


def _sign(text: str) -> str:
    # GREETINGS_SIGNING_SECRET is a secret shared with the partner system that verifies greetings.
    secret = os.environ.get("GREETINGS_SIGNING_SECRET", "")
    if not secret:
        return ""
    return hmac.new(secret.encode(), text.encode(), hashlib.sha256).hexdigest()[:16]


@activity.defn
async def compose_greeting(name: str) -> str:
    text = f"Hello, {name}! Greetings from a Temporal workflow."
    if os.environ.get("ANTHROPIC_API_KEY"):
        from anthropic import AsyncAnthropic

        reply = await AsyncAnthropic().messages.create(
            model=MODEL,
            max_tokens=60,
            messages=[{"role": "user", "content": f"Write a one-sentence warm greeting for {name}."}],
        )
        text = reply.content[0].text.strip()
    signature = _sign(text)
    return f"{text} [sig {signature}]" if signature else text
