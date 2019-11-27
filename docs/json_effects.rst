Effects as Data
===============

To make ``beatmachine`` useful in non-Python contexts, it provides a flexible
serialization system for representing and loading data-driven effects.

For example, in Python we might define an effect chain like so::

    fx_chain = [RemoveEveryNth(period=5), RemapBeats(mapping=[0, 1, 0, 3])]

This is nice but requires us to write code. In some situations, this might not
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

In these examples we use JSON, but any data format that can be parsed into a
``dict``-ish object should suffice. See
``EffectRegistry.load_effect_from_dict`` for more info.
