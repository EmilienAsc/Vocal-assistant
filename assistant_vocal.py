from elevenlabs import generate, play
import speech_recognition as sr
import openai

API_KEY = "API-KEY ChatGPT"
openai.api_key = API_KEY

# useful functions

def play_audio(content):
    audio = generate(
    text=content,
    voice="Elli",
    model="eleven_multilingual_v1"
    )
    play(audio)


def chat_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        stream=True,
    )

    for chunk in response:
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
            print(content, end="")


def transcribe_realtime():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        play_audio("Hi! I'm Elli, your voice assistant, so don't hesitate to ask me questions and I'll answer them!")
        try:
            chat_gpt("Keep your answers concise, and don't hesitate to keep the conversation going by asking relevant questions in return.")
        except:
            play_audio("An error has occurred, please try again later.")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="fr-FR") # Adapt to your language
            print("You said: ", text)
            response = chat_gpt(text)
            play_audio(response)
            print(response)
        except sr.WaitTimeoutError:
            print("No audio detected for 5 seconds.")
            play_audio("I'm sorry, I didn't understand.")
        except:
            print("Problem with ChatGPT API")
            

# start 

if __name__ == "__main__":
    transcribe_realtime()
