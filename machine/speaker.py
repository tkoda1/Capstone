# https://www.geeksforgeeks.org/working-with-wav-files-in-python-using-pydub/
# pip install pydub
# you need to set the speaker as the defualt audio output!

from pydub import AudioSegment
from pydub.playback import play

from constants import (
    REFILL_PILL_PATH, 
    RELEASE_PILL_PATH,
    FINISH_DISPENSING_PATH,
    INVALID_DISPENSING_PATH)

release_pill = AudioSegment.from_file(file = RELEASE_PILL_PATH, 
                                      format = "wav") + 30
refill_reminder = AudioSegment.from_file(file = REFILL_PILL_PATH,
                                         format = "wav") + 30
finish_dispensing = AudioSegment.from_file(file = FINISH_DISPENSING_PATH,
                                           format = "wav") + 30
invalid_dispensing = AudioSegment.from_file(file = INVALID_DISPENSING_PATH,
                                            format = "wav") + 30


# indicating which pill is being dispensed
def play_release_pill():
    play(release_pill)

# indicating pill refill reminder
def play_refill_reminder():
    play(refill_reminder)

# indicating when finished dispensing all scheduled pills
def play_finish_dispensing():
    play(finish_dispensing)

# indicating if the wrong pill amount was dispensed
def play_invalid_dispensing():
    play(invalid_dispensing)