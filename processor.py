#!/usr/bin/env python3
import numpy as np
import pretty_midi
import math
import pickle
import sys
import os
from utils import read_path

START_IDX = {
    'NOTE_ON': 0,
    'NOTE_OFF': 88,
    'TIME_SHIFT': 88 + 88,
    'VELOCITY': 88 + 88 + 100
}


class Token:
    def __init__(self, event_type, value):
        self.type = event_type
        self.value = value

    def __repr__(self):
        return '<Event type: {}, value: {}>'.format(self.type, self.value)

    def to_int(self):
        if self.type == "TIME_SHIFT":
            return START_IDX[self.type] + self.value // 10
        else:
            return START_IDX[self.type] + self.value


def list_events(midi):
    events = []
    for inst in midi.instruments:
        notes = inst.notes
        print(f"Number of notes is {len(notes)}")
        for note in notes:
            events.append([note.start, 'on', note.pitch, note.velocity])
            events.append([note.end, 'off', note.pitch])
    events.sort()
    return events


def list_tokens(events):
    tokens = []
    current = 0.0
    previous_velocity = 0
    for event in events:
        if event[0] - current >= 1:
            for i in range(math.floor(event[0] - current)):
                tokens.append(Token("TIME_SHIFT", 1000))
            if math.ceil((event[0] - current - i - 1) * 100) * 10 != 0:
                tokens.append(Token("TIME_SHIFT", math.ceil((event[0] - current - i - 1) * 100) * 10))
        else:
            if math.ceil((event[0] - current) * 100) * 10 != 0:
                tokens.append(Token("TIME_SHIFT", math.ceil((event[0] - current) * 100) * 10))
        if event[2] == 'on':
            if event[4] // 4 != previous_velocity:
                tokens.append(Token("VELOCITY", event[4] // 4))
                previous_velocity = event[4] // 4
            tokens.append(Token("NOTE_ON", event[3]))
        if event[2] == 'off':
            tokens.append(Token("NOTE_OFF", event[3]))
        current = event[0]
    print(f"Number of tokens is {len(tokens)}")
    return tokens


def list_one_hot_idx(tokens):
    one_hot_idx = []
    for token in tokens:
        assert (token.to_int() < 308)
        one_hot_idx.append(token.to_int())
        print(token.to_int())
    return one_hot_idx


def process_all(input_midi, output_pickle):
    targets = read_path(input_midi)
    for target in targets:
        midi = pretty_midi.PrettyMIDI(os.path.join(input_midi, target))
        events = list_events(midi)
        tokens = list_tokens(events)
        one_hot_idx = list_one_hot_idx(tokens)
        with open('{}/{}.pickle'.format(output_pickle, target.replace("." + target.split(".")[-1], "")), 'wb') as f:
            pickle.dump(one_hot_idx, f)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Not enough argument")
        print("./processor.py <input_midi_path> <output_pickle_path>")
        exit(-1)
    midi_path = str(sys.argv[1])
    pickle_path = str(sys.argv[2])
    process_all(midi_path, pickle_path)