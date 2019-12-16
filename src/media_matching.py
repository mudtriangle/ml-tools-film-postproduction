from SMPTE import SMPTEInterval


def find_audio_match(timecode_string, audio_file_dictionary):
    interval = SMPTEInterval(timecode_string)

    matches = []
    for audio_file in audio_file_dictionary.keys():
        if interval.overlaps(SMPTEInterval(audio_file_dictionary[audio_file]['timecode'])):
            matches.append(audio_file)

    return matches
