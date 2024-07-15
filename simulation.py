import streamlit as st
import json
import time

# Loading recipe instructions from actions.json
def load_actions():
    with open('actions.json', 'r') as f:
        return json.load(f)

# Initializing session state variables 
if 'current_step_index' not in st.session_state:
    st.session_state.current_step_index = 0

if 'steps' not in st.session_state:
    st.session_state.steps = load_actions()['steps']


def display_current_step():
    step_len = st.session_state.steps[st.session_state.current_step_index]
    st.markdown(f"### Step {step_len['step']}")
    st.markdown(f"**Action:** {step_len['action']}")
    
    st.markdown("**Ingredients:**")
    for ing in step_len['ingredients']:
        names = ing.get('name', 'Unknown ingredient')
        quantity = ing.get('quantity')
        unit = ing.get('unit')
        
        # Creating the ingredient based on the given instruction
        ingredient_str = names
        if quantity is not None:
            ingredient_str = f"{quantity} {unit} of {names}" if unit is not None else f"{quantity} of {names}"
        
        st.markdown(f"- {ingredient_str}")
    
    if 'parameters' in step_len:
        st.markdown(f"**Parameters:** {step_len['parameters']}")
    
    if 'time' in step_len and step_len['time'] is not None:
        st.markdown(f"**Time:** {step_len['time']} minutes")
    else:
        st.markdown("**Time:** Not specified")

    if st.button('Execute Step'):
        execute_step()


def execute_step():
    step_len_2 = st.session_state.steps[st.session_state.current_step_index]
    st.write(f"Executing: {step_len_2['action']}")
    if 'time' in step_len_2 and step_len_2['time'] is not None:
        time.sleep(step_len_2['time'] * 60)  # Simulate the cooking time (convert minutes to seconds)
    st.write(f"Completed: {step_len_2['action']}")
    next_step()


def next_step():
    st.session_state.current_step_index += 1
    if st.session_state.current_step_index < len(st.session_state.steps):
        st.experimental_rerun()
    else:
        st.write("Recipe completed!")

# interface
st.title("Cooking Machine Simulation")

if st.session_state.current_step_index == 0:
    if st.button('Start Simulation'):
        st.session_state.current_step_index = 1
        st.experimental_rerun()
else:
    display_current_step()
