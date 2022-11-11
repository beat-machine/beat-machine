import inspect
import json
import os
import pickle
import textwrap
from types import SimpleNamespace

import click
from jsonschema.exceptions import ValidationError

import beatmachine as bm
from beatmachine.backends.madmom import MadmomDbnBackend
from beatmachine.effect_registry import EffectRegistry


def _hint(msg):
    click.secho("Hint: " + msg, fg="blue")


def _load_beats_from_song(ctx, input):
    backend = MadmomDbnBackend(min_bpm=ctx.obj.min_bpm, max_bpm=ctx.obj.max_bpm, model_count=4)
    return bm.Beats.from_song(input, backend)


class BeatsParam(click.Path):
    def __init__(self, preprocess_hint=True):
        super().__init__(exists=True, dir_okay=False)
        self.preprocess_hint = preprocess_hint

    def convert(self, value, param, ctx):
        if not value:
            return None

        value = super().convert(value, param, ctx)

        if value.endswith(".beat"):
            with open(value, "rb") as fp:
                beats = pickle.load(fp)
        else:
            if self.preprocess_hint:
                stem, _ = os.path.splitext(value)
                if os.path.isfile(stem + ".beat"):
                    _hint(f"A preprocessed version of this song seems to exist at {stem}.beat")
                    _hint(f'Replacing "{value}" with "{stem}.beat" will skip this processing step')

            click.echo(f"Locating beats in {value}")
            beats = _load_beats_from_song(ctx, value)

        return (beats, value)


class EffectsParam(click.ParamType):
    name = "effects"

    def convert(self, value, param, ctx):
        if not value:
            return None

        try:
            effects_obj = json.loads(value)
        except ValueError:
            try:
                with open(value, "r") as effects_file:
                    effects_obj = json.load(effects_file)
            except:
                self.fail("Effect argument should be an inline JSON string or a path to a file")

        if not isinstance(effects_obj, list):
            effects_obj = [effects_obj]

        try:
            return EffectRegistry.load_effect_chain(effects_obj)
        except ValidationError as e:
            self.fail(f"Effect {e.instance} is invalid: {e.message}")


@click.group()
@click.option("-b", "--min-bpm", type=int, default=60, help="Minimum BPM")
@click.option("-B", "--max-bpm", type=int, default=300, help="Maximum BPM")
@click.option("-y", "--skip-confirm", is_flag=True, help="If set, skip confirmation prompts")
@click.pass_context
def cli(ctx, min_bpm, max_bpm, skip_confirm):
    """
    Remix songs by rearranging and modifying beats.

    Beat detection features are provided by madmom: https://github.com/CPJKU/madmom.

    View the repository at https://github.com/beat-machine/beat-machine.
    """
    ctx.obj = SimpleNamespace(min_bpm=min_bpm, max_bpm=max_bpm, skip_confirm=skip_confirm)


@cli.command()
@click.option("-e", "--effects", required=True, type=EffectsParam())
@click.option("-o", "--output", type=click.Path(writable=True, dir_okay=False))
@click.argument("input", nargs=1, type=BeatsParam())
@click.pass_context
def apply(ctx, input, output, effects):
    """
    Apply effects to a song.

    See all valid effects using the `effects` subcommand. Preprocessed files
    generated with `preprocess` can be used to skip the processing step.

    Note that preprocessed files carry the same security risks as any pickled
    Python objects. Only use .beat files from trusted sources!
    """
    beats, filename = input
    stem, ext = os.path.splitext(filename)

    if not output:
        if ext == ".beat":
            ext = ".mp3"

        output = stem + "-out" + ext

    if os.path.isfile(output) and not ctx.obj.skip_confirm:
        click.confirm(f"Overwrite existing file at {output}", abort=True)

    click.echo("Applying effects")
    beats = beats.apply_all(*effects)

    click.echo(f"Writing audio file to {output}")
    beats.save(output)

    print("Done!")


@cli.command()
@click.argument("input", nargs=1, type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--output", type=click.Path(writable=True, dir_okay=False))
@click.pass_context
def preprocess(ctx, input, output):
    """
    Locate beats in an audio file and save them for later use.
    """

    if input.endswith(".beat"):
        click.echo(f"Input file {input} has already been preprocessed", err=True)
        return 1

    if not output:
        output = os.path.splitext(input)[0] + ".beat"

    click.echo(f"Processing {input}")

    beats = _load_beats_from_song(ctx, input)

    if os.path.isfile(output) and not ctx.obj['skip_confirm']:
        click.confirm(f"Overwrite existing file at {output}", abort=True)

    click.echo(f"Writing beats to {output}")
    with open(output, "wb") as fp:
        fp.write(pickle.dumps(beats))

    print("Done!")


def _print_effect_human_readable(effect_cls):
    effect_name = effect_cls.__effect_name__
    print(effect_name)

    print()
    print("Description")
    description = inspect.cleandoc(effect_cls.__doc__) or "No description."
    print(textwrap.fill(description, initial_indent=2 * " ", subsequent_indent=2 * " "))

    print()
    print("Parameters")

    example_obj = {'type': effect_name}
    schema = effect_cls.__effect_schema__
    if schema:
        for param, param_schema in schema.items():
            example_obj[param] = param_schema['default']
            print(f'  {param} ({param_schema["type"]}) - {param_schema["title"]}')
            if "description" in param_schema:
                print(textwrap.fill(param_schema["description"], initial_indent=4 * " ", subsequent_indent=4 * " "))
    else:
        print("  No parameters.")

    print()
    print("Example JSON")
    print('  ', json.dumps(example_obj), sep='')


@cli.command("effects")
@click.option("-j", "--json-schema", is_flag=True, help="If set, formats output as a JSON schema.")
@click.argument("effect", type=str, required=False)
def effect_info(json_schema, effect):
    """
    List all available effects.
    """

    effects = EffectRegistry.effects

    # if no effect name is given, list all effects.
    if not effect:
        if json_schema:
            print(json.dumps(EffectRegistry.dump_list_schema(root=True)))
            return

        for name in effects.keys():
            print(name)
        return

    try:
        effect_cls = effects[effect.lower()]
    except KeyError:
        click.echo(f"Couldn't find an effect named `{effect}`. Use `beatmachine effects` to get a list of effects.", err=True)
        return

    if json_schema:
        print(json.dumps(EffectRegistry.dump_single_effect_schema(effect.lower(), root=True)))
        return

    _print_effect_human_readable(effect_cls)


if __name__ == "__main__":
    cli()
