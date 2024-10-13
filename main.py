import os
import sys
from pydub import AudioSegment
from pydub.silence import split_on_silence

DEFAULT_SILENCE_THRESHOLD=-40
DEFAULT_SILENCE_DURATION=50

def split_mp3_by_silence(input_file, output_folder, silence_threshold=-40, silence_duration=500):
    # Load the input MP3 file
    audio = AudioSegment.from_mp3(input_file)

    # Split the audio based on silence
    segments = split_on_silence(
        audio, 
        silence_thresh=silence_threshold, min_silence_len=silence_duration,
        keep_silence=500)

    try:
        os.mkdir(f"{output_folder}")
    except FileExistsError:
        print("Output directory exists. No change needed.")

    # Save each segment to separate files
    for i, segment in enumerate(segments):
        seg_str = str(i+1)
        # for 1-9 add a leading zero
        if int(seg_str) < 10:
            seg_str = f"0{seg_str}"

        output_file = f"{output_folder}/segment_{seg_str}.mp3"
        segment.export(output_file, format="mp3")
        print(f"Segment {i+1} saved as {output_file}")

if __name__ == "__main__":

    # Replace 'input.mp3' with the path to your input MP3 file
    #input_file_path = 'troop-audio-output-3.mp3'
    input_file_path = ""
    try:
        input_file_path = sys.argv[1]
    except:
        raise FileNotFoundError("There was no file path argument specified.")

    try:
        input_silence_threshold = int(sys.argv[2])
    except:
        print(f"No silence threshold set, using default {DEFAULT_SILENCE_THRESHOLD}")
        input_silence_threshold=DEFAULT_SILENCE_THRESHOLD

    try:
        input_silence_duration = int(sys.argv[3])
    except:
        print(f"No silence threshold set, using default {DEFAULT_SILENCE_DURATION}")
        input_silence_duration=DEFAULT_SILENCE_DURATION

    # Replace 'output_folder' with the path to the folder where you want to save the segments
    output_folder_path = 'output_folder'

    # You can adjust the silence threshold and duration based on your audio characteristics
    # >> silencedetect=noise=-30db:d=0.5 used in ffmpeg with success.
    # >> Adjusted duration to default 1 sec. 
    split_mp3_by_silence(
        input_file_path, 
        output_folder_path, silence_threshold=input_silence_threshold, silence_duration=input_silence_duration)
