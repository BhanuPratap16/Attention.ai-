import requests
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
from datetime import datetime

# Initialize the model (LLaMA 2.7)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-2-7B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-2-7B")

# Weather API
API_KEY_WEATHER = "0fd1f698329a71e6cd4b521998280d50"

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

# Define a chatbot function to handle different types of queries
def chatbot_response(user_input):
    """Generate a response based on user input."""
    if "weather" in user_input.lower():
        # Extract city name from user input (for simplicity, assume the city is mentioned after 'weather in')
        city_name = user_input.split("in")[-1].strip() if "in" in user_input.lower() else "London"  # Default to "London" if no city is specified
        return get_weather(city_name)
    elif "traffic" in user_input.lower():
        return get_traffic_info()
    else:
        # Use LLaMA 2 model to respond to other questions
        inputs = tokenizer(user_input, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=256)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Streamlit UI
st.title("Tourism Chatbot")
st.write("Ask me about weather, traffic, or anything else!")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You: ")

if user_input:
    # Get chatbot response
    response = chatbot_response(user_input)
    # Save chat history
    st.session_state.history.append(f"You: {user_input}")
    st.session_state.history.append(f"Bot: {response}")
    
    # Display chat history
    for chat in st.session_state.history:
        st.write(chat)
