def apply_effects_to_beats(beats, song_effects):
    """
    Applies a list of effects to a list of PyDub AudioSegments representing the beats of a song.

    :param beats: List of beats.
    :param song_effects: Effects to apply.
    :return: An AudioSegment comprised of the given beats with the effects applied.
    """
    for song_effect in song_effects:
        beats = song_effect(beats)

    return sum(beats)
