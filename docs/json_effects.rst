JSON Effects
============

To make ``beatmachine`` useful in non-Python contexts, it provides a flexible
serialization system for representing and loading data-driven effects.

For example, in Python we might define an effect chain like so::

    fx_chain = [RemoveEveryNth(period=5), RemapBeats(mapping=[0, 1, 0, 3])]

This is nice, but requires us to write code. In some situations, this might not
be desirable. To address this, every valid effect can be deserialized
from data. Here's what our above effect chain would look like in JSON::

    [
        {
            "type": "remove",
            "period": 5
        },
        {
            "type": "remap",
            "mapping": [0, 1, 0, 3]
        }
    ]

The most common use case is JSON, but in reality, any data format that can be
read into a ``dict``-like object also works. See
``EffectRegistry.load_effect_from_dict`` for more info.

Look in the ``effects`` module for a list of all effects. To write an effect
as JSON, create an object with ``"type"`` corresponding to its
``__effect_name__`` and a field for each parameter in ``__init__``.