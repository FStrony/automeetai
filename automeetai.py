# We import the streamlit module with the alias 'st'.
# This allows us to use 'st' to access Streamlit features,
# which is a web application framework for Python.
import streamlit as st

# We import the annotated_text function to highlight text in the app.
from annotated_text import annotated_text

# We import specific libraries for AI service integration and media handling.
import assemblyai as aai
from openai import OpenAI

import uuid

# We import custom functions to convert files and handle data.
from mp4_to_mp3 import mp4_to_mp3
from mp3_to_text import mp3_to_text
from misc import deletar_arquivo_se_existir
from chat_with_openai import generate_response

# We import a dictionary with language codes for audio processing.
from assemblyai_language_codes import *

# We use Streamlit’s title() function to add a title to our web application.
st.title('🤖 AutomeetAI')

# We use the write() function to display plain text on the page.
# This function is very versatile and can also show data and display charts.
st.write('Automated meeting minutes using AI technology with Python.')

# Checks if API keys for AssemblyAI and OpenAI are available in secrets (st.secrets).
if 'assemblyai' in st.secrets and 'api_key' in st.secrets['assemblyai'] and \
   'openai'     in st.secrets and 'api_key' in st.secrets['openai'] :

	# Retrieves the API key for AssemblyAI from stored secrets and assigns it to `aai_api_key`.
	aai_api_key = st.secrets['assemblyai']['api_key']

	# Retrieves the API key for OpenAI from stored secrets and assigns it to `openai_api_key`.
	openai_api_key = st.secrets['openai']['api_key']

else:
	# If the keys are not available, creates a user interface for manual entry.

	# Adds a horizontal divider to separate sections in the app layout.
	st.divider()

	# Splits the page into two columns for API key input.
	col11, col12 = st.columns(2)

	with col11:
		# The `text_input` method creates a text box for the user to enter the API key.
		aai_api_key = st.text_input("AssemblyAI   •   API key")

	with col12:
		# Another `text_input` method, this time for the OpenAI API key.
		openai_api_key = st.text_input("OpenAI   •   API key")

# Another divider for visual organization.
st.divider()

# Text area for the system prompt: the assistant's behavior and role.
prompt_system = st.text_area("Provide general instructions or set the tone for the AI \"assistant\":", "You are an excellent project manager with great meeting-minute writing skills.")

# Text area for the user prompt: what the user wants the assistant to do.
prompt_text = st.text_area("What does the user want the assistant to do?", """In an expert-level essay, summarize the meeting notes into a single paragraph.
Then, write a list of each key point discussed in the meeting.
Finally, list any next steps or action items suggested by the speakers, if any.""")

# Another divider for visual clarity.
st.divider()

# Splits the page into two columns for additional settings.
col21, col22 = st.columns(2)

# Numeric input for the estimated number of speakers in the audio.
with col21:
	speakers_expected = st.number_input("Total number of speakers:", 1, 15)

# Spoken language selection, using the list of imported language codes.
with col22:
	language = st.selectbox("Select the spoken language:", tuple(language_codes.keys()))

# File uploader component so the user can upload an MP4 file.
uploaded_file = st.file_uploader("Select your file", accept_multiple_files=False, type=['mp4'])

# Divider below the upload component.
st.divider()

# If a file was uploaded, starts the processing.
if uploaded_file:

	with st.spinner('Converting from mp4 to mp3...'):

		# Gets the name of the uploaded file.
		mp4_filename = uploaded_file.name

		# Generates a unique name for the MP3 file using uuid (universally unique identifier).
		mp3_filename = '{nome_arquivo}.mp3'.format(nome_arquivo=uuid.uuid4().hex)

		# Temporarily opens the file for binary read and write.
		tempfile = open(mp4_filename, 'wb')
		tempfile.write(uploaded_file.read())

		# Converts the MP4 file to MP3.
		mp4_to_mp3(mp4_filename, mp3_filename)

	# Indicates successful conversion from MP4 to MP3.
	st.success("MP4 to MP3 conversion completed!")

	with st.spinner('Converting from mp3 to text...'):

		# Sets the API key for AssemblyAI.
		aai.settings.api_key = aai_api_key

		# Converts the MP3 audio to text.
		transcript = mp3_to_text(
			aai, 
			filename=mp3_filename,
			s_labels=True,  # Enables speaker labeling.
			s_expected=speakers_expected,
			l_code=language_codes[language]
		)

		# Indicates that the audio was successfully transcribed.
		st.success("Audio-to-text transcription completed!")

		# Initializes variables to store the transcribed and annotated text.
		texto_transcrito = ''
		texto_anotado = []

		# If the transcription was successful, displays the speaker segments.
		if transcript:
			# Iterates over transcribed utterances and prints each speaker’s line.
			for utterance in transcript.utterances:
				# Displays the speaker number and the corresponding text.
				texto_transcrito += f"Speaker {utterance.speaker}: {utterance.text}"
				texto_transcrito += '\n'

				# Adds the speech text along with the speaker label.
				texto_anotado.append((utterance.text, f"Speaker {utterance.speaker}"))

	with st.spinner('Generating meeting minutes...'):

		# Initializes the OpenAI client with your API key.
		client = OpenAI(api_key=openai_api_key)

		# Includes the audio transcription in the user prompt.
		prompt_text += '\n===========\n'
		prompt_text += texto_transcrito

		# Generates a response based on the prompts and transcription.
		texto_retorno = generate_response(client, prompt_system, prompt_text)

		# Indicates successful generation of the meeting minutes.
		st.success("Meeting minutes generated successfully!")

	# Displays the original transcription section.
	st.subheader('Original Transcription')

	# Shows the annotated text with speaker differentiation.
	annotated_text(texto_anotado)

	# Displays the generated meeting minutes in the app.
	st.subheader('Generated Minutes')
	st.markdown(texto_retorno)

	# Deletes the temporary MP3 file created.
	deletar_arquivo_se_existir(mp3_filename)
