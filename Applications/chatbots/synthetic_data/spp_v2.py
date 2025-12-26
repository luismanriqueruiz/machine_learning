import streamlit as st
import json

st.set_page_config(layout="wide")
st.title("Simulation Rules GUI Builder")

# --------------------------------------------------
# Initialize state
# --------------------------------------------------
if "rules" not in st.session_state:
    st.session_state.rules = {
        "personas": {},
        "intents": [],
        "actions": [],
        "transitions": {},
        "rewards": {
            "conversion": 10.0,
            "intent_alignment": 1.0,
            "neutral": 0.0,
            "bad_move": -1.0
        }
    }

rules = st.session_state.rules

# --------------------------------------------------
# Intents
# --------------------------------------------------
st.header("Intents")

intents_text = st.text_input(
    "Intents (comma-separated)",
    value=", ".join(rules["intents"]),
    key="intents_input"
)

rules["intents"] = [i.strip() for i in intents_text.split(",") if i.strip()]

# --------------------------------------------------
# Actions
# --------------------------------------------------
st.header("Actions")

actions_text = st.text_input(
    "Actions (comma-separated)",
    value=", ".join(rules["actions"]),
    key="actions_input"
)

rules["actions"] = [a.strip() for a in actions_text.split(",") if a.strip()]

# --------------------------------------------------
# Personas
# --------------------------------------------------
st.header("Personas")

new_persona = st.text_input("New persona name", key="new_persona_name")

if st.button("Add persona", key="add_persona_btn") and new_persona:
    if new_persona not in rules["personas"]:
        rules["personas"][new_persona] = {
            "intent_probs": {},
            "conversion_probability": 0.0
        }

persona_name = st.selectbox(
    "Select persona",
    ["— select —"] + list(rules["personas"].keys()),
    key="persona_selector"
)

if persona_name != "— select —":

    persona = rules["personas"][persona_name]

    # Conversion probability
    persona["conversion_probability"] = st.slider(
        "Conversion probability",
        0.0, 1.0,
        persona.get("conversion_probability", 0.0),
        step=0.01,
        key=f"{persona_name}::conversion"
    )

    # Intent probabilities via sliders
    st.subheader("Intent probabilities")

    if not rules["intents"]:
        st.info("Define intents first.")
    else:
        total = 0.0
        new_probs = {}

        for intent in rules["intents"]:
            value = persona["intent_probs"].get(intent, 0.0)

            new_value = st.slider(
                intent,
                0.0, 1.0,
                value,
                step=0.05,
                key=f"{persona_name}::{intent}"
            )

            new_probs[intent] = new_value
            total += new_value

        persona["intent_probs"] = new_probs

        st.write(f"Total probability: **{total:.2f}**")

        if abs(total - 1.0) > 0.01:
            st.warning("Intent probabilities should sum to 1.0")
        else:
            st.success("Probabilities look good ✔")

        if st.button("Normalize intent probabilities", key=f"norm_{persona_name}"):
            if total > 0:
                persona["intent_probs"] = {
                    k: v / total for k, v in new_probs.items()
                }
                st.rerun()

# --------------------------------------------------
# Transitions
# --------------------------------------------------
st.header("Transitions")

if not rules["actions"] or not rules["intents"]:
    st.info("Define actions and intents first.")
else:
    action = st.selectbox(
        "Select action",
        ["— select —"] + rules["actions"],
        key="transition_action"
    )

    if action != "— select —":
        st.subheader(f"Transitions for action: {action}")

        transitions = rules["transitions"].get(action, {})
        total = 0.0
        new_transitions = {}

        for intent in rules["intents"]:
            value = transitions.get(intent, 0.0)

            new_value = st.slider(
                intent,
                0.0, 1.0,
                value,
                step=0.05,
                key=f"transition::{action}::{intent}"
            )

            new_transitions[intent] = new_value
            total += new_value

        rules["transitions"][action] = new_transitions

        st.write(f"Total probability: **{total:.2f}**")

        if abs(total - 1.0) > 0.01:
            st.warning("Transition probabilities should sum to 1.0")
        else:
            st.success("Probabilities look good ✔")

        if st.button("Normalize transitions", key=f"norm_transition_{action}"):
            if total > 0:
                rules["transitions"][action] = {
                    k: v / total for k, v in new_transitions.items()
                }
                st.rerun()

# --------------------------------------------------
# Rewards
# --------------------------------------------------
st.header("Rewards")

for key in rules["rewards"]:
    rules["rewards"][key] = st.number_input(
        key,
        value=float(rules["rewards"][key]),
        key=f"reward::{key}"
    )

# --------------------------------------------------
# JSON Output
# --------------------------------------------------
st.header("Generated JSON")

json_output = json.dumps(rules, indent=2)
st.code(json_output, language="json")

st.download_button(
    "Download simulation_rules.json",
    data=json_output,
    file_name="simulation_rules.json",
    mime="application/json"
)
