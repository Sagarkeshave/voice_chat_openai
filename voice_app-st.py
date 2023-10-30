import streamlit as st
import speech_recognition as sr
import openai
from gtts import gTTS
import os


# Streamlit app title and description
st.title("Voice Chat with AI")
st.write("Speak and let the AI respond!")


# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    os.system('output.mp3')


# Function to process voice input using OpenAI GPT-3.5
def process_voice_input(input_text):
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3.5 turbo engine
        prompt=input_text,
        max_tokens=50  # Limit the response length if needed
    )
    return response.choices[0].text.strip()


# User input for OpenAI API key and topic
api_key = st.text_input("Enter your OpenAI API key (without quotes) :", key="API")

if api_key:
    openai.api_key = api_key
    x = 3
    st.write(f"Limited for {x} responses")
    # Streamlit app logic
    for i in range(x):  # Limited for n responses

        # Record voice input using SpeechRecognition
        with sr.Microphone() as source:
            st.write("Listening...")
            audio = sr.Recognizer().listen(source)

            try:
                # Google Web Speech API to recognize the voice input
                user_input = sr.Recognizer().recognize_google(audio)
                st.write("You said: " + user_input)

                # Get response from model
                model_response = process_voice_input(user_input)

                # Convert the model's text response to speech
                text_to_speech(model_response)

                st.write("AI Response: " + model_response)

            except sr.UnknownValueError:
                st.write("Sorry, I could not understand your audio.")
            except sr.RequestError as e:
                st.write(f"Could not request results from Google Web Speech API; {e}")

