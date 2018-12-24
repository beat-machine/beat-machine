from beatmachine.effects import *

SIMPLE_BEAT_EFFECTS = {
    'reverse': periodic.reverse,
    'cut_in_half': periodic.cut_in_half,
    'replace_with_silence': periodic.replace_with_silence,
    'remove': periodic.remove
}

SIMPLE_SONG_EFFECTS = {
    'randomize_all': song.randomize_all,
    'sort_by_loudness': song.sort_by_loudness,
    'sort_by_average_frequency': song.sort_by_average_frequency
}


def load_effect(obj):
    """
    Loads an effect from a given object. This will most likely be JSON data, but could be anything that can be indexed.

    :param obj: Object to load a single song effect from.
    :return: Song effect loaded.
    """
    raise NotImplementedError


def load_all_effects(obj):
    """
    Loads a list of song effects from an 'effects' list within the given JSON data.

    :param obj: Object to load song effects from.
    :return: Song effects loaded.
    """
    raise NotImplementedError
