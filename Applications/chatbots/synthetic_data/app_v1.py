import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide")
st.title("Simulation Rules GUI Builder")

if "simulation_rules" not in st.session_state:
    st.session_state.simulation_rules = {
        "personas": {},
        "intents": [],
        "actions": [],
        "transitions": {},
        "rewards": {}
    }

rules = st.session_state.simulation_rules

# INTENTS
st.header("Intents")

intents_text = st.text_area(
    "Enter intents (comma-separated)",
    value=", ".join(rules["intents"])
)

rules["intents"] = [i.strip() for i in intents_text.split(",") if i.strip()]

st.header("Actions")

actions_text = st.text_area(
    "Enter actions (comma-separated)",
    value=", ".join(rules["actions"])
)

rules["actions"] = [a.strip() for a in actions_text.split(",") if a.strip()]


# PERSONAS
st.header("Personas")

new_persona = st.text_input("Add persona")

if st.button("Add Persona") and new_persona:
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

    intent_probs_df = pd.DataFrame(
        {
            "intent": rules["intents"],
            "probability": [
                persona["intent_probs"].get(i, 0.0)
                for i in rules["intents"]
            ]
        }
    )

    edited_df = st.data_editor(
        intent_probs_df,
        num_rows="fixed",
        key=f"personas::{persona_name}::intent_probs",
        column_config={
            "probability": st.column_config.NumberColumn(
                min_value=0.0,
                max_value=1.0
            )
        }
    )

    persona["intent_probs"] = dict(
        zip(edited_df["intent"], edited_df["probability"])
    )



# TRANSITIONS
st.header("Transitions")

if not rules["actions"]:
    st.info("Define actions first to edit transitions.")
    st.stop()

action = st.selectbox(
    "Select action",
    ["— select —"] + rules["actions"],
    key="action_selector"
)


if action != "— select —":
    transition_df = pd.DataFrame(
        {
            "intent": rules["intents"],
            "probability": [
                rules["transitions"]
                .get(action, {})
                .get(i, 0.0)
                for i in rules["intents"]
            ]
        }
    )

    edited_transition_df = st.data_editor(
        transition_df,
        num_rows="fixed",
        key=f"transitions::{action}",   # ← deterministic & unique
        column_config={
            "probability": st.column_config.NumberColumn(
                min_value=0.0,
                max_value=1.0
            )
        }
    )

    rules["transitions"][action] = dict(
        zip(
            edited_transition_df["intent"],
            edited_transition_df["probability"]
        )
    )


# REWARDS
st.header("Rewards")

reward_keys = ["conversion", "intent_alignment", "neutral", "bad_move"]

for key in reward_keys:
    rules["rewards"][key] = st.number_input(
        key,
        value=float(rules["rewards"].get(key, 0.0))
    )

st.header("Generated JSON")

json_output = json.dumps(rules, indent=2)
st.code(json_output, language="json")

st.download_button(
    "Download simulation_rules.json",
    data=json_output,
    file_name="simulation_rules.json",
    mime="application/json"
)
