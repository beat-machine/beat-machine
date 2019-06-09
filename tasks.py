from invoke import task
from setuptools import sandbox

# noinspection PyUnresolvedReferences
from beatmachine.effects import *
# noinspection PyProtectedMember
from beatmachine.effect_loader import _registry as registry


@task
def clean(ctx):
    """
    Runs `setup.py clean` and removes any extraneous MP3 files used for testing.
    """
    ctx.run('rm -rf *.mp3')
    sandbox.run_setup('setup.py', ['clean'])


@task
def dump_registered_effects(ctx):
    with open('EFFECTS.md', 'w') as effects:
        effects.write("""
# Effects
            
This auto-generated document contains a list of effects defined in the `beatmachine` module available for loading from
JSON.
        """.strip())
        effects.write("\n\n")
        for effect_name, required_parameters, optional_parameters, factory in sorted(registry.known_effects.values(),
                                                                              key=lambda l: l.effect_name):
            effects.write(f"## {effect_name}\n")
            effects.write(f"{factory.__doc__.strip()}\n\n")

            if required_parameters:
                effects.write(f"### Required Parameters\n")
                for parameter_name, parameter_type in required_parameters.items():
                    effects.write(f"`{parameter_name}`: **{parameter_type.__name__}**\n\n")

            if optional_parameters:
                effects.write(f"### Optional Parameters\n")
                for parameter_name, parameter_type in optional_parameters.items():
                    effects.write(f"`{parameter_name}`: **{parameter_type.__name__}**\n\n")
