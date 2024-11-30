# !pip install ctransformers
import requests
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
import json

# Initialize the CTransformers LLaMA 2.7 model
MODEL_PATH = "llama-2-7b-chat.ggmlv3.q8_0.bin"
llm = CTransformers(model=MODEL_PATH, model_type="llama", config={"max_new_tokens": 256, "temperature": 0.7})

# Weather API
API_KEY_WEATHER = "your_openweathermap_api_key"

def get_weather(city_name):
    """Fetch weather data for a specific city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY_WEATHER}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] != "404":
        main_data = data["main"]
        weather_data = data["weather"][0]
        weather_info = f"Weather in {city_name}:\n{weather_data['description'].capitalize()}\nTemperature: {main_data['temp']}°C"
    else:
        weather_info = f"Sorry, I couldn't fetch the weather for {city_name} at the moment."
    return weather_info

# Traffic API (Google Maps example)
API_KEY_TRAFFIC = "your_google_maps_api_key"

def get_traffic_info():
    """Fetch traffic data from Google Maps API."""
    # Replace the below coordinates with relevant ones based on your location
    origin = "37.7749,-122.4194"  # Example: San Francisco latitude and longitude
    destination = "34.0522,-118.2437"  # Example: Los Angeles latitude and longitude
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={API_KEY_TRAFFIC}"
    
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "OK":
        route = data["routes"][0]
        traffic_info = route["legs"][0]["duration_in_traffic"]["text"]
    else:
        traffic_info = "Sorry, I couldn't fetch the traffic information at the moment."
    return traffic_info

# Define a function for generating responses with context
def generate_response(context_prompt, user_input):
    """
    Generates a response from the LLM based on the context and user input.
    """
    prompt = f"{context_prompt}\nUser: {user_input}\nAssistant:"
    response = llm(prompt)
    return response.strip()

# Streamlit UI
st.title("Tourism Itinerary Chatbot")
st.markdown("Plan your perfect trip with our AI chatbot!")

# Initialize session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define the context prompt
context_prompt = """
You are a helpful travel assistant AI for a tourism company.  You make sure to ask them first about their budget, interest and travel Duration. Make sure to also ask them if they want to have meals in between their travel according to their budget and meal preferences and also nearest to the location of visit. 
You assist customers in drafting personalized itineraries based on their preferences, including budget, travel duration, and interests like adventure, relaxation, or cultural experiences.
Always respond politely and comprehensively.
"""

# User input
user_input = st.text_input("Enter your query or preference:", "")

# Chat handling
if st.button("Send") and user_input.strip():
    # Check for weather or traffic queries
    if "weather" in user_input.lower():
        # Extract city name from user input (for simplicity, assume the city is mentioned after 'weather in')
        city_name = user_input.split("in")[-1].strip() if "in" in user_input.lower() else "London"  # Default to "London" if no city is specified
        response = get_weather(city_name)
    elif "traffic" in user_input.lower():
        response = get_traffic_info()
    else:
        # Generate response using LLaMA 2.7 model with the context prompt
        response = generate_response(context_prompt, user_input)
    
    # Save to chat history
    st.session_state.chat_history.append({"User": user_input, "Assistant": response})
    
    # Clear the input box
    st.experimental_rerun()

# Display chat history
if st.session_state.chat_history:
    st.subheader("Chat History")
    for i, chat in enumerate(st.session_state.chat_history):
        st.markdown(f"**User**: {chat['User']}")
        st.markdown(f"**Assistant**: {chat['Assistant']}")
        st.markdown("---")

# Save chat history to a file
if st.button("Download Chat History"):
    chat_history_file = "chat_history.json"
    with open(chat_history_file, "w") as f:
        json.dump(st.session_state.chat_history, f, indent=4)
    st.success(f"Chat history saved to {chat_history_file}")
    st.markdown(f"[Download {chat_history_file}](./{chat_history_file})")

# Footer
st.markdown("---")
st.caption("Powered by LLaMA 2 via CTransformers")
