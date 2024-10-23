from dotenv import load_dotenv
load_dotenv()  

import streamlit as st
import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import time
import threading

# Google Generative AI configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize our Streamlit app
st.set_page_config(page_title="ChatGenius🤖")

st.header("ChatGenius🤖")
st.write("ChatGenius🤖 is an AI chatbot that writes text. You can use it to write stories, messages, or programming code. You can use the ChatGenius as a virtual tutor in almost any subject.")

# Text input for user to chat with the bot
input_text = st.text_input("Chat With AI.. ", key="input")
submit = st.button("Send Text")

# Speech recognition engine initialization
r = sr.Recognizer()
engine = pyttsx3.init() 
def record_text():
    start_time = time.time()  
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                st.write("Listening...")
                audio = r.listen(source, timeout=10)  

                if audio:
                    MyText = r.recognize_google(audio)
                    return MyText
                
                if time.time() - start_time > 20:
                    st.write("Stopped listening after 20 seconds.")
                    break

        except sr.UnknownValueError:
            st.write("Could not understand audio")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
        except KeyboardInterrupt:
            st.write("Listening interrupted.")
            break

def output_text(text):
    engine.say(text)  
    engine.runAndWait() 

voice_input = st.button("Talk to AI")

if submit and input_text:
    response = get_gemini_response(input_text)
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)

if voice_input:
    text = record_text()  
    if text:
        st.write(f"You said: {text}")
        response = get_gemini_response(text)  
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            threading.Thread(target=output_text, args=(chunk.text,)).start() 
