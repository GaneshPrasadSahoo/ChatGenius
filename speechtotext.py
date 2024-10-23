import speech_recognition as sr
import pyttsx3
import time

r = sr.Recognizer()
engine = pyttsx3.init()  # Initialize the text-to-speech engine

def record_text():
    start_time = time.time()  # Record the start time
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                print("Listening...")
                audio = r.listen(source, timeout=10)  # Listen for a maximum of 5 seconds
                
                # If audio is captured, process it
                if audio:
                    MyText = r.recognize_google(audio)
                    return MyText
                
                # Check if 20 seconds have passed
                if time.time() - start_time > 20:
                    print("Stopped listening after 20 seconds.")
                    break

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except KeyboardInterrupt:
            print("Listening interrupted.")
            break  # Exit the loop on manual interruption

def output_text(text):
    print(f"You said: {text}")  # Print the recognized text
    engine.say(text)  # Convert text to speech
    engine.runAndWait()  # Wait until the speech is finished

while True:
    text = record_text()
    if text:
        output_text(text)
