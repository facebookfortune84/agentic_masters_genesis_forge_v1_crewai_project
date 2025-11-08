# env_to_toml.py — Convert .env to secrets.toml

def parse_env_to_toml(env_path=".env", toml_path="streamlit/secrets.toml"):
    import os

    if not os.path.exists(env_path):
        print(f"❌ .env file not found at: {env_path}")
        return

    os.makedirs(os.path.dirname(toml_path), exist_ok=True)

    with open(env_path, "r", encoding="utf-8") as env_file:
        lines = env_file.readlines()

    with open(toml_path, "w", encoding="utf-8") as toml_file:
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                # Escape quotes and special characters
                value = value.replace('"', '\\"')
                toml_file.write(f'{key} = "{value}"\n')

    print(f"✅ Converted {env_path} → {toml_path}")

# Run it
if __name__ == "__main__":
    parse_env_to_toml()