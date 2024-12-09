# Itinerary Chatbot

# How to run?
### STEPS:

### STEP 01- First, Clone the repository

Look for any suitable folder to save the files in your PC. Open up your Command Prompt in that Folder.

```bash
https://github.com/BhanuPratap16/Itinerary-Chatbot.git
```
Change the directory to Itinerary-Chatbot 
```bash
cd Itinerary-Chatbot
```

### STEP 02- Create a conda environment after opening the repository

```bash
conda create -n myenv python=3.11 -y
```

```bash
conda activate myenv
```


### STEP 03- install the requirements
```bash
pip install -r requirements.txt
```


### Step 04 - Generate API Keys from Together AI 

1. Login to together.ai 
2. Go to Manage Account on Dashboard Section and Copy your API Key
3. then, Go to the config.yaml file and replace the together_api_key with your api key in both spaces.

Now, Use one of the username and password from pass.txt on Login Page of Itinerary Chatbot

### Step 05- Run app.py file 

```bash
# Finally run the following command
streamlit run app.py
```
now, open up your local host and port
### Step 05- Enter your login credentials from pass.txt and Enter 

Draft your Itinerary with Chatbot . Thanks!!

