import itertools
from typing import Generator, Iterable, List, T


def chunks(iterable: Iterable[T], size: int) -> Generator[List[T], None, None]:
    iterator = iter(iterable)
    for first in iterator:
        yield list(itertools.chain([first], itertools.islice(iterator, size - 1)))
