# Import the required modules
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Create a speech recognizer object
listener = sr.Recognizer()

# Create a text to speech engine object
engine = pyttsx3.init()

# Define a function to make the assistant speak
def talk(text):
    # Set the voice to female
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    # Say the text
    engine.say(text)
    # Run and wait until the speech is finished
    engine.runAndWait()

# Define a function to take voice commands from the user
def take_command():
    try:
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            # Listen for the user's voice and adjust for ambient noise
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            # Recognize the speech using Google Speech Recognition API
            command = listener.recognize_google(voice)
            # Convert the command to lowercase and check if it contains the assistant's name
            command = command.lower()
            if "VoiceVibe" in command:
                # Remove the assistant's name from the command
                command = command.replace("VoiceVibe", "")
                print(command)
    except:
        # Handle any exceptions and return an empty string
        print("Sorry, I could not hear you")
        command = ""
    return command

# Define a function to run the assistant
def run_VoiceVibe():
    # Get the voice command from the user
    command = take_command()
    # Check if the command contains certain keywords and perform the corresponding actions
    if "play" in command:
        # Play a song on YouTube using pywhatkit
        song = command.replace("play", "")
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)
        talk(f"Did you enjoy the song?")
        answer = take_command()
        if "yes" in answer:
            talk(f"I'm glad you liked it")
        elif "no" in answer:
            talk(f"I'm sorry you didn't like it")
        else:
            talk(f"Sorry, I didn't catch that")
    elif "time" in command:
        # Tell the current time using datetime
        time = datetime.datetime.now().strftime("%I:%M %p")
        talk(f"The current time is {time}")
        talk(f"Do you have any plans for today?")
        answer = take_command()
        if "yes" in answer:
            talk(f"That sounds nice. What are you going to do?")
            answer = take_command()
            talk(f"Wow, that sounds fun. I hope you have a great time")
        elif "no" in answer:
            talk(f"That's okay. Sometimes it's good to relax and do nothing")
        else:
            talk(f"Sorry, I didn't catch that")
    elif "who is" in command:
        # Give information about a person using wikipedia
        person = command.replace("who is", "")
        info = wikipedia.summary(person, 1)
        talk(info)
        talk(f"Do you want to know more about {person}?")
        answer = take_command()
        if "yes" in answer:
            info = wikipedia.summary(person, 3)
            talk(info)
        elif "no" in answer:
            talk(f"Okay, no problem. Let me know if you have any other questions")
        else:
            talk(f"Sorry, I didn't catch that")
    elif "joke" in command:
        # Tell a joke using pyjokes
        joke = pyjokes.get_joke()
        talk(joke)
        talk(f"Did you find that funny?")
        answer = take_command()
        if "yes" in answer:
            talk(f"I'm happy to make you laugh")
        elif "no" in answer:
            talk(f"I'm sorry to disappoint you. Maybe I should work on my sense of humor")
        else:
            talk(f"Sorry, I didn't catch that")
    elif "stop" in command:
        # Stop the assistant and exit the program
        talk("Goodbye")
        return False
    else:
        # Handle any unknown commands and ask for another command
        talk("Sorry, I did not understand that. Please say it again.")
    return True
# Greet the user and introduce the assistant
talk("Hello, I'm VoiceVibe, your voice assistant. How can I help you today?")

# Create a loop to run the assistant until the user says stop
running = True
while running:
    running = run_VoiceVibe()
