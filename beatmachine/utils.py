import itertools
import typing as t


def chunks(iterable: t.Iterable[t.T], size: int) -> t.Generator[t.List[t.T], None, None]:
    iterator = iter(iterable)
    for first in iterator:
        yield list(itertools.chain([first], itertools.islice(iterator, size - 1)))
