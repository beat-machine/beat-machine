from collections import namedtuple

RegisteredEffect = namedtuple('RegisteredEffect',
                              ['effect_name', 'required_parameters', 'optional_parameters', 'factory'])


class EffectRegistry:
    """
    An EffectRegistry is used to keep track of effects that can be loaded from some external source.
    """
    def __init__(self):
        self.known_effects = {}

    def register(self, effect_name, required_parameters=None, optional_parameters=None):
        """
        Creates a decorator that registers a given function ("effect factory") into this EffectRegistry.

        :param effect_name: Name of the effect to register.
        :param required_parameters: A map from names to validating functions of required parameters.
        :param optional_parameters: A map from names to validating functions of optional parameters.
        :return: The original function, decorated so that it's registered in this EffectRegistry.
        """
        if not required_parameters:
            required_parameters = {}

        if not optional_parameters:
            optional_parameters = {}

        def decorator(func):
            self.known_effects[effect_name] = RegisteredEffect(effect_name, required_parameters, optional_parameters,
                                                               func)
            return func

        return decorator


_registry = EffectRegistry()
loadable = _registry.register


def load_effect(obj):
    """
    Loads a single effect from an indexable object. Most likely, this will be loaded from JSON.
    :param obj: Object to load an effect from.
    :raises ValueError: If loading the effect was unsuccessful.
    :return: The effect described by the given object.
    """
    if 'type' not in obj:
        raise ValueError('Attempted to load an effect, but no type was present')

    effect_type = obj['type']
    if effect_type not in _registry.known_effects:
        raise ValueError(f'Attempted to load an unknown effect `{effect_type}`')

    _, required_parameters, optional_parameters, factory = _registry.known_effects[effect_type]
    kwargs = {}

    kwargs.update(_load_effect_parameters(obj, effect_type, required_parameters, True))
    kwargs.update(_load_effect_parameters(obj, effect_type, optional_parameters, False))

    return factory(**kwargs)


def _load_effect_parameters(obj, effect_type, parameter_map, strict):
    loaded_parameters = {}
    for parameter_name, parameter_validator in parameter_map.items():
        if strict and parameter_name not in obj:
            raise ValueError(f'Attempted to load an effect of type `{effect_type}`, but it was missing required '
                             f'parameter `{parameter_name}`')

        if parameter_name in obj:
            try:
                loaded_parameters[parameter_name] = parameter_validator(obj[parameter_name])
            except ValueError or TypeError:
                raise ValueError(
                    f'Attempted to load an effect of type `{effect_type}`, but the given value for parameter '
                    f'`{parameter_name}` was invalid: `{obj[parameter_name]}`')

    return loaded_parameters


def load_all_effects(obj):
    """
    Loads all effects from an "effects" list within the given object.
    :param obj: Object to load effects from.
    :raises ValueError: If no effects were specified or an effect was not loaded successfully.
    :return: A list of effects described by the given object.
    """
    if 'effects' not in obj or not obj['effects']:
        raise ValueError('Attempted to load effects, but none were specified')

    return [load_effect(o) for o in obj['effects']]
