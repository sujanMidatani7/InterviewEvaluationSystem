import speech_recognition as sr

def takeCommand(audio):
    """
    Transcribes audio data into text using speech recognition.

    Args:
        audio (str): The path to the audio file.

    Returns:
        str: The transcribed text from the audio.
    """
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = r.record(source)

    try:
        query = r.recognize_google(audio_data, language="en-in")
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Unable to recognize speech")
    except sr.RequestError as e:
        print(f"Error occurred: {e}")

    return "Some error occurred."
