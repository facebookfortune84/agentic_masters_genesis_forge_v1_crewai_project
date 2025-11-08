def scan_secrets(path=".env"):
    import os

    if not os.path.exists(path):
        print(f"❌ Secrets file not found: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print("🔐 Agent Capabilities from Secrets:")
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            if "OPENAI" in key:
                print(f"🧠 LLM Access: {key}")
            elif "GROQ" in key:
                print(f"⚡ Groq Dispatch: {key}")
            elif "SHOPIFY" in key:
                print(f"🛍 Shopify Integration: {key}")
            elif "LINKEDIN" in key:
                print(f"🔗 LinkedIn Automation: {key}")
            elif "STRIPE" in key:
                print(f"💸 Stripe Monetization: {key}")
            elif "WORDPRESS" in key:
                print(f"📝 Blog Publishing: {key}")
            elif "FACEBOOK" in key:
                print(f"📣 Facebook Dispatch: {key}")
            elif "ELEVENLABS" in key:
                print(f"🔊 Voice Synthesis: {key}")
            else:
                print(f"🔧 Misc Capability: {key}")

if __name__ == "__main__":
    scan_secrets(".env")  # or "streamlit/secrets.toml"