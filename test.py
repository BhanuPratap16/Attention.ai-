import streamlit as st
from together import Together
import together
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title='ChatBot login window',page_icon=":bar_chart:",layout='wide')

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
# with file_path.open("wb") as file:
#     pickle.dump(hashed_passwords, file)
st.title("Tourism Itinerary Chatbot Authentication")
authenticator.login(key="login",location="main")

if st.session_state['authentication_status']:
    # Initialize Together API client
    # Extract user-specific Together API key
    st.title("Tourism Itinerary Chatbot")
    st.markdown("Plan your trip with our AI chatbot!")
    
    username = st.session_state['username']
    name= st.session_state['name']
    together_api_key = config['credentials']['usernames'][username]['together_api_key']
    st.success(f"Welcome, {name}!")
    authenticator.logout("Logout", "sidebar")
    client = Together(api_key= together_api_key)
    # authenticator.logout("Logout", "sidebar")

    # Prompt input from user
    prompt = st.chat_input("Enter your prompt here:")

    # Generate response using Together API
    context_prompt = """
You are a helpful and energetic travel assistant for a tourism company. Your goal is to assist customers in creating personalized travel itineraries based on their preferences. Follow these guidelines:

Start with Greetings: If the customer greets you first, respond politely with an energetic greeting. If they have not provided any travel-related information yet, ask them, "Are you planning to travel this time or sooner?" If they say yes, show your interest and let them know you would love to help them out.

Ask for Destination: Once they express interest in traveling, ask, "Where are you planning to travel?" Upon receiving the city name, complement the user’s choice by highlighting something famous about that destination. For example, mention a well-known landmark, a popular movie filmed there, or a signature dish from the city. For instance, "Oh, you're going to Paris! You'll get to see the magnificent Eiffel Tower, a true symbol of romance and beauty."

Ask for Interests: If the customer is unsure about their interests, provide them with a list of options like 'Adventure,' 'Relaxation,' 'Cultural Experiences,' and 'Nature' to choose from. If they already have interests in mind, proceed to the next step.

Ask for Budget: Once the customer’s interests are clear, inquire about their travel budget. For example, "What’s your estimated budget for this trip?"

Ask for Travel Duration: Ask the customer how long they plan to travel for, considering their budget and interests. For example, "How long are you planning to travel? A week, two weeks, or more?"

Meal Preferences: Ask if they would like to have meals during their trip and inquire about their meal preferences. Offer options within their budget and based on proximity to their chosen destinations. For example, "Would you like meals included during your trip? If so, do you have any specific preferences like local cuisine or specific types of meals?"

Traveling Alone or with a Group: Once the customer provides their destination, ask if they are traveling alone or with a group. If they are traveling with a group, inquire about the group’s interests and preferences to tailor the itinerary accordingly.

Provide Recommendations: Based on their responses, draft a personalized itinerary that includes suggestions for destinations, activities, and meals, all aligned with their budget, interests, and travel duration. Be polite, clear, and concise in your responses.

Full Overview of Locations: Once the itinerary is ready, provide a full overview of the travel locations. Show the estimated travel times between destinations and the time the customer will likely stay at each location. Use arrows to connect locations for easier understanding.

Politeness and Clarity: Always respond politely and comprehensively. Provide information in a way that feels helpful and customer-friendly, focusing on their needs.

"""
    def generate_response(prompt):
        
        result = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
           messages = [
        {'role': 'system', 'content': context_prompt},
        *st.session_state.messages, # You can use the 'system' role for instructions or context
        {'role': 'user', 'content': prompt}  # The user's input
    ],
            # stream=True
        )
        
        return result.choices[0].message.content

        #     response = ''
        #     for chunk in result:
        #         # Debugging the structure of chunk
        #         print(f"Chunk type: {type(chunk)}, Chunk value: {chunk}")
                
        #         # If chunk is a tuple, extract the second element
        #         if isinstance(chunk, tuple):
        #             chunk = chunk[1]  # Adjust based on observed structure

        #         # Process only if chunk is a dictionary
        #         if isinstance(chunk, dict) and 'choices' in chunk and len(chunk['choices']) > 0:
        #             response += chunk['choices'][0].get('text', '')

        #     return response if response else 'No response generated.'

        # except Exception as e:
        #     return f"Error generating response: {e}"


    # Session state for messages
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display old messages
    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    # Process new prompt
    if prompt:
        st.chat_message('user').markdown(prompt)
    #     result = client.chat.completions.create(
    #     model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    #     messages=[{"role": "user", "content": "What are some fun things to do in New York?"}],
    # )
        
        # response = ''
        # for chunk in result:
        #     if 'choices' in chunk and len(chunk['choices']) > 0:
        #         response += chunk['choices'][0].get('text', '')

        # return response
        # st.chat_message()
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        response = generate_response(prompt)
        st.chat_message('assistant').markdown(response)

        # Save assistant's response in session state
        st.session_state.messages.append({'role': 'assistant', 'content': response})
    # st.title('Some content')
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')

    # Initialize Together API client
    # client = Together(api_key='bcc6be4ce91ed88dd457a97efa719a8eec231b55832d7462d36da213f8496c45')
    # authenticator.logout("Logout", "sidebar")

    # # Prompt input from user
    # prompt = st.chat_input("Enter your prompt here:")

    # # Generate response using Together API
    # def generate_response(prompt):
        
    #     result = client.chat.completions.create(
    #         model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    #         messages=[{'role': 'user', 'content': prompt}],
    #         # stream=True
    #     )
        
    #     return result.choices[0].message.content

    #     #     response = ''
    #     #     for chunk in result:
    #     #         # Debugging the structure of chunk
    #     #         print(f"Chunk type: {type(chunk)}, Chunk value: {chunk}")
                
    #     #         # If chunk is a tuple, extract the second element
    #     #         if isinstance(chunk, tuple):
    #     #             chunk = chunk[1]  # Adjust based on observed structure

    #     #         # Process only if chunk is a dictionary
    #     #         if isinstance(chunk, dict) and 'choices' in chunk and len(chunk['choices']) > 0:
    #     #             response += chunk['choices'][0].get('text', '')

    #     #     return response if response else 'No response generated.'

    #     # except Exception as e:
    #     #     return f"Error generating response: {e}"


    # # Session state for messages
    # if 'messages' not in st.session_state:
    #     st.session_state.messages = []

    # # Display old messages
    # for message in st.session_state.messages:
    #     st.chat_message(message['role']).markdown(message['content'])

    # # Process new prompt
    # if prompt:
    #     st.chat_message('user').markdown(prompt)
    # #     result = client.chat.completions.create(
    # #     model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    # #     messages=[{"role": "user", "content": "What are some fun things to do in New York?"}],
    # # )
        
    #     # response = ''
    #     # for chunk in result:
    #     #     if 'choices' in chunk and len(chunk['choices']) > 0:
    #     #         response += chunk['choices'][0].get('text', '')

    #     # return response
    #     # st.chat_message()
    #     st.session_state.messages.append({'role': 'user', 'content': prompt})

    #     response = generate_response(prompt)
    #     st.chat_message('assistant').markdown(response)

    #     # Save assistant's response in session state
    #     st.session_state.messages.append({'role': 'assistant', 'content': response})
