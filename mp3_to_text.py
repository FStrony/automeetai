# Make sure the `assemblyai` package is installed.
# You can install it using: `pip install -U assemblyai`
#
# Note for macOS users: use `pip3` if `pip` points to another Python version.

import assemblyai as aai


# Function to convert an MP3 audio file into text using the AssemblyAI service.
def mp3_to_text(aai, filename, s_labels, s_expected, l_code):
    try:
        # Set up transcription configuration, including speaker labels,
        # expected number of speakers, and language code.
        config = aai.TranscriptionConfig(
            speaker_labels=s_labels,       # Enable or disable speaker labels.
            speakers_expected=s_expected,  # Expected number of speakers in the audio.
            language_code=l_code           # Language code, e.g., 'pt' for Portuguese.
        )

        # Create a Transcriber instance to handle the transcription process.
        transcriber = aai.Transcriber()

        # Transcribe the MP3 file using the specified configuration.
        transcript = transcriber.transcribe(
            filename,
            config=config
        )

        # Return the transcript object received from the API.
        return transcript

    except FileNotFoundError:
        # Catch this error if the specified MP3 file was not found.
        print("Error: The specified audio file was not found.")
    except Exception as e:
        # Catch any other exceptions and print the error message.
        print(f"An error occurred: {e}")


# Check if the script is being run directly (not imported as a module).
if __name__ == "__main__":

    # Set your AssemblyAI API key for authentication.
    aai.settings.api_key = ""

    # Specify the local MP3 file path you want to transcribe.
    mp3_local_filename = "audio_video/f7f9e2a4567343da94f7e24aa403ed1b.mp3"

    # Call the transcription function with desired settings.
    transcript = mp3_to_text(
        aai,
        filename=mp3_local_filename,
        s_labels=True,   # Enable speaker labels in the transcript.
        s_expected=2,    # Expect 2 speakers in the audio.
        l_code='pt'      # Set the language of the audio to Portuguese.
    )

    # If transcription was successful, display the spoken utterances.
    if transcript:
        # Iterate through each utterance and print speaker and their text.
        for utterance in transcript.utterances:
            print(f"Speaker {utterance.speaker}: {utterance.text}")
