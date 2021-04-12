# MLAP
Machine Learning Anime Piano (MLAP)

## Data representation

Input(one-hot 308-dimensional vector):

- 88 NOTE_ON events
    - normally it should be 128, but we use an 88 keys piano performance as dataset
- 88 NOTE_OFF events
- 100 TIME_SHIFT events
    - minimum 10 ms time step, maximum 1 second, can be stacked 
- 32 VELOCITY events
    - 32 levels of velocity magnitude is sufficient 

## Plan / Road map ?
1. Convert mp3 to tensors
3. Build Music Transformer
4. Train
5. Test

## Dev Log

**12 April 2021**
- Use pretty midi convert all the data into (index of) one-hot vectors and stored as .pickle file
## Noticeboard
Dataset last update: 5 April 2021

Note that the file and scripts in the "random" directory is not maintained.
