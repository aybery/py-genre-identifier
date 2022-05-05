
# Location of where audio files will be saved
UPLOAD_FOLDER = "Audio"

#  How large a file can be (this is 16 MB)
MAX_CONTENT_LENGTH = 16 * 1000 * 1000

#  All the file extensions that you can use in this program
ALLOWED_EXTENSIONS = 'wav'

#  This is used by flask as a key, stored as plain text for development purposes
SECRET_KEY = 'Secret!_dont-tell-NE1'

#  This is the sample rate of the audio file
SAMPLE_RATE = 22050

#  An array of all 10 different genres available
GENRES = [
    'blues',
    'classical',
    'country',
    'disco',
    'hiphop',
    'jazz',
    'metal',
    'pop',
    'reggae',
    'rock'
]

TEST_DATA = "features_30_sec.csv"