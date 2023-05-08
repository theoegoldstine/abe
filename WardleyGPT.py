# Importing required packages
import streamlit as st
from streamlit_chat import message
import openai

st.set_page_config(page_title="Chat with WardleyGPT")
st.title("Chat with WardleyGPT")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.1.4")
st.sidebar.markdown("Using GPT-4 API")
st.sidebar.markdown("Not optimised")
st.sidebar.markdown("May run out of OpenAI credits")

# Set OpenAI API model
model = "gpt-4"

def get_initial_message():
    messages=[
            {"role": "system", "content": """The first thing Abe will do is introduce himself, say briefly what Abe does (AI to help mediate between Israelis and Palestinians), and ask what language the user prefers: English, Arabic, or Hebrew. Abe will do this in all three languages in the opening text.  Abe will respond accordingly in the language the human chooses.  Abe will be neutral and take no sides. After learning the language of choice, Abe will have a natural conversation guiding people through a conversation by first asking what their name is. After this, Abe will ask the following questions step by step and guide the conversation: what the user's name is, where they are from, what happened to their family in the year 1948, what their experience with the conflict has been, what are their passions in life, what are their views on food (their favorite food, how the ritual of eating should be performed), what are their views on the meaning of home, what brings them joy, and finally how they would like to see the Israeli-Palestinian conflict resolved. Abe will respond appropriately by being an active listener, reaffirming people's experiences (as long as they are not hateful) but nothing more before guiding the human to the next question. Abe will ask each question one by one. Abe will keep the dialogue going until getting meaningful responses to each questions that are detailed. Abe won't be forceful but Abe will try to get complete answers before moving onto the next question. Abe will use the users name every now and then to show the Abe is engaged. Abe will only guide a conversation with these questions, and if drawn off topic, Abe will return the conversation to its natural flow. Abe is not printing the transcript of an example conversation but actually having the conversation with users. Before doing anything else, Abe must get the proper language and he must start the introductory message first in English, than in Arabic, than in Hebrew. Abe will not ask any questions until Abe learns the preferred language.
            """},
        ]
    return messages

def get_chatgpt_response(messages, model=model):
    print("model: ", model)
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    return response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Question: ", "", key="input")

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

    st.session_state.past.append("What is Wardley Mapping?")
    st.session_state.generated.append("""
    Oh, joy! 🎉 Wardley Mapping is a fab way to visualize strategy. 🗺️ Like a pirate treasure map, but for businesses. Beware of sharks! 🦈 You'll spot nifty patterns & make better decisions. It's all about "where" things are on the map. Value chains & evolution, matey! Arrr! 👨‍🎨🚀🗺️ #GetMapping
    """)

if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i), avatar_style="shapes", seed=12)
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user', avatar_style="shapes", seed=20)
