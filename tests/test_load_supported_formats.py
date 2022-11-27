# These tests are kind of naive, but are better than nothing for now.

from beatmachine import Beats


def test_can_load_mp3(drums_mp3_path):
    data = Beats.from_song(drums_mp3_path).to_ndarray()
    assert (data != 0).any()


def test_can_load_wav(drums_wav_path):
    data = Beats.from_song(drums_wav_path).to_ndarray()
    assert (data != 0).any()
