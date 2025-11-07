import yaml
import os
import streamlit as st

# === Load Mappings ===
def load_mappings(file_path="ui/prefill_mappings.yaml"):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)  # Top-level list of agents

# === Group Agents by Team ===
def group_agents_by_team(mappings):
    teams = {}
    for agent in mappings:
        team_key = agent.get("team", "Unassigned")
        teams.setdefault(team_key, []).append(agent)
    return teams

# === UI: Project Type + Prompt ===
def project_selector():
    st.sidebar.title("🧠 Project Intelligence")
    project_type = st.sidebar.selectbox("Select Project Type", ["Python", "JavaScript", "Node.js", "React", "Other"])
    project_prompt = st.sidebar.text_area("Describe Your Project", placeholder="What are you building?")
    return project_type, project_prompt

# === UI: Team Activation ===
def team_activation_ui(teams):
    st.sidebar.title("🧩 Activate Teams")
    active_teams = []
    for team, agents in teams.items():
        if st.sidebar.checkbox(f"Activate {team} Team ({len(agents)} agents)"):
            active_teams.extend(agents)
    return active_teams

# === Main UI ===
def main():
    st.set_page_config(page_title="Master Forge Launcher", layout="wide")
    st.title("🚀 Master Forge Agent Launcher")

    try:
        mappings = load_mappings()
    except Exception as e:
        st.error(f"Failed to load mappings: {e}")
        return

    teams = group_agents_by_team(mappings)
    project_type, project_prompt = project_selector()
    active_agents = team_activation_ui(teams)

    st.subheader("🧠 Active Agents")
    if not active_agents:
        st.info("No teams activated yet. Use the sidebar to activate one or more teams.")
    else:
        for agent in active_agents:
            st.markdown(f"### {agent.get('name', 'Unnamed')} ({agent.get('employee_id', 'ID Missing')})")
            st.markdown(f"**Role:** {agent.get('role', 'Unknown')}")
            st.markdown(f"**Team:** {agent.get('team', 'Unassigned')}")
            st.markdown(f"**Persona:** {agent.get('persona', 'N/A')}")
            st.markdown(f"**Tools Assigned:** {', '.join(agent.get('tools_assigned', []))}")
            st.markdown(f"**Hourly Rate:** ${agent.get('hourly_rate', 'N/A')}/hr")
            st.markdown(f"**Form:** {agent.get('physical_form', 'N/A')}")
            st.markdown("**Tasks:**")
            for task in agent.get("tasks", []):
                st.code(task.get("default_filename", "filename missing"))

    if st.button("🔥 Launch Selected Agents"):
        st.success(f"Launching {len(active_agents)} agents for a {project_type} project...")
        st.markdown(f"**Project Prompt:** {project_prompt}")
        # TODO: Inject dispatch logic here

if __name__ == "__main__":
    main()