# Import the required modules
import speech_recognition as sr
import pywhatkit
import datetime
import playsound
import wikipedia
import pyjokes

from TTS.api import TTS

# Init TTS
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC_ph")

# Create a speech recognizer object
listener = sr.Recognizer()


# Create a text to speech engine object

# Define a function to make the assistant speak
def talk(text):
    tts.tts_to_file(text=text, file_path="output.wav")
    playsound.playsound('output.wav')


# Define a function to take voice commands from the user
def take_command():
    # Use the default microphone as the audio source
    try:
        with sr.Microphone() as source:
            # Listen for the user's voice and adjust for ambient noise
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            # Recognize the speech using Google Speech Recognition API
            command = listener.recognize_google(voice)
            # Convert the command to lowercase and check if it contains the assistant's name
            print(command)
            command = command.lower()
    except Exception as e:
        print("excerption:", e)
        command = ''
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


if __name__ == '__main__':
    # Greet the user and introduce the assistant
    talk("Hello, I'm VoiceVibe, your voice assistant. How can I help you today?")

    # Create a loop to run the assistant until the user says stop
    running = True
    while running:
        running = run_VoiceVibe()
