from beatmachine.beat_effects import *
from beatmachine.song_effects import *

SIMPLE_BEAT_EFFECTS = {
    'reverse': reverse,
    'cut_in_half': cut_in_half,
    'replace_with_silence': replace_with_silence,
    'remove': remove
}

SIMPLE_SONG_EFFECTS = {
    'randomize_all': randomize_all,
    'sort_by_loudness': sort_by_loudness,
    'sort_by_average_frequency': sort_by_average_frequency
}


def load_effect(obj):
    """
    Loads an effect from a given object. This will most likely be JSON data, but could be anything that can be indexed.

    :param obj: Object to load a single song effect from.
    :return: Song effect loaded.
    """
    if 'type' not in obj:
        raise ValueError('Tried to load an effect, but no type was specified!')

    effect_type = obj['type']

    if effect_type in SIMPLE_BEAT_EFFECTS:
        beat_effect = SIMPLE_BEAT_EFFECTS[effect_type]
        if 'every' not in obj:
            return every_beat(beat_effect)
        try:
            return every_nth_beat(int(obj['every']), beat_effect)
        except ValueError:
            return every_beat(beat_effect)

    if effect_type in SIMPLE_SONG_EFFECTS:
        return SIMPLE_SONG_EFFECTS[effect_type]

    if effect_type == 'swap':
        if 'x' not in obj or 'y' not in obj:
            raise ValueError('Specified swap effect without `x` and `y` beats!')
        return swap_beats(int(obj['x']), int(obj['y']))

    raise ValueError('Unknown effect: ' + effect_type)


def load_all_effects(obj):
    """
    Loads a list of song effects from an 'effects' list within the given JSON data.

    :param obj: Object to load song effects from.
    :return: Song effects loaded.
    """
    if 'effects' not in obj:
        raise ValueError('No effects to load were present!')

    return [load_effect(e) for e in obj['effects']]
