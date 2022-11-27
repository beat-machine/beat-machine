from pathlib import Path

import numpy as np
import pytest

RESOURCES_DIR = Path(__file__).parent / "resources"


@pytest.fixture
def drums_mp3_path():
    return RESOURCES_DIR / "drums.mp3"


@pytest.fixture
def drums_wav_path():
    return RESOURCES_DIR / "drums.wav"


@pytest.fixture
def song_ascending():
    return [np.full(4, 1), np.full(4, 2), np.full(4, 3), np.full(4, 4)]
