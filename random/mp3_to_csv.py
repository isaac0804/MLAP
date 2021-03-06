#!/usr/bin/env python3
from piano_transcription_inference import PianoTranscription, sample_rate, load_audio
from utils import read_path
import py_midicsv as pm
import os
import sys
import csv

'''
Recently when I read through repos on the github, I found out that most of the researchers tend to use Pretty Midi 
instead of this py_midicsv. Now, to play safe, I decided to switch to Pretty Midi and keep this option as an 
experimentation option.
'''


def transcribe(audio_path, output_midi_path):
    # Load audio
    audio, _ = load_audio(audio_path, sr=sample_rate, mono=True)

    # Transcriptor
    transcriptor = PianoTranscription(device='cuda', checkpoint_path=None)

    # Transcribe and write out to MIDI file
    transcriptor.transcribe(audio, output_midi_path)


def input_pipeline(input_mp3, output_mid, output_csv):
    print(f"Reading from {input_mp3}....")
    targets = read_path(input_mp3)
    index = 0
    temp = 0

    for target in targets:
        try:
            # Transcribe the MP3 file
            if index < 10:
                temp = "000" + str(index)
            elif index < 100:
                temp = "00" + str(index)
            elif index < 1000:
                temp = "0" + str(index)
            else:
                temp = index

            print(f"Transcribing into MIDI: {target}....")
            transcribe(os.path.join(input_mp3, target + '.mp3'), os.path.join(output_mid, str(temp) + '.mid'))
            ret = []
            # Load the MIDI file and parse it into CSV format

            print(f"Translating into CSV: {target}....")
            data = pm.midi_to_csv(os.path.join(output_mid, str(temp) + '.mid'))
            for row in data:
                row = row.replace("\n", "")
                row = list(row.split(","))
                ret.append(row)

            with open(os.path.join(output_csv, str(temp) + '.csv'), "w") as f:
                writer = csv.writer(f)
                writer.writerows(ret)
            index += 1
        except Exception:
            print(f"Some problem occurs while trying to process {target}.")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Not enough argument")
        print("./mp3_to_csv.py <input_mp3_path> <output_midi_path> <output_csv_path>")
        exit(-1)
    mp3_path = str(sys.argv[1])
    midi_path = str(sys.argv[2])
    csv_path = str(sys.argv[3])
    input_pipeline(mp3_path, midi_path, csv_path)
