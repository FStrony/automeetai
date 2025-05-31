# Import the necessary module from moviepy for handling audio and video
from moviepy import AudioFileClip

# Import the uuid module to generate unique identifiers
import uuid

# Define a function called 'mp4_to_mp3' that converts an MP4 file to MP3 format
def mp4_to_mp3(mp4, mp3):
    try:
        # Create an audio object from the MP4 file using the AudioFileClip class
        filetoconvert = AudioFileClip(mp4)

        # Save the extracted audio from the MP4 file in MP3 format
        filetoconvert.write_audiofile(mp3)

        # Close the audio object to free up system resources
        filetoconvert.close()

    except FileNotFoundError:
        # This exception is caught if the MP4 file is not found
        print(f"Error: The MP4 file '{mp4}' was not found.")

    except Exception as e:
        # Catch any other exception and print the error message
        print(f"An error occurred during the conversion: {e}")



# Check if the script is being run as the main program
if __name__ == "__main__":
    # Define the path to the local MP4 file that will be converted
    mp4_local_filename = "audio_video/entrevista de Boechat com Jô Soares curto.mp4"

    # Generate a unique filename for the MP3 file using uuid to avoid name collisions
    mp3_local_filename = f"audio_video/{uuid.uuid4().hex}.mp3"

    # Call the function to convert the MP4 file to MP3
    mp4_to_mp3(mp4_local_filename, mp3_local_filename)
