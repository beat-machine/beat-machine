import os
import pickle
import json
import inspect
import textwrap
import pprint
from jsonschema.exceptions import ValidationError

import click
import beatmachine as bm


def _hint(msg):
    click.secho("Hint: " + msg, fg="blue")


class BeatsFromDisk(click.Path):
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
                if os.path.isfile(stem + '.beat'):
                    _hint(
                        f'A preprocessed version of this song seems to exist at {stem}.beat')
                    _hint(
                        f'Replacing "{value}" with "{stem}.beat" will skip this processing step')

            click.echo(f"Locating beats in {value}")
            beats = bm.Beats.from_song(value, loader_args=ctx.obj)

        return (beats, value)


class EffectChain(click.ParamType):
    name = "effects"

    def convert(self, value, param, ctx):
        if not value:
            return None

        # Check in the following order:
        #  1. Inline JSON
        #  2. Local path (absolute or relative to current directory)
        #  3. User preset folder (something like ~/.beatmachine/presets or env)

        try:
            effects_obj = json.loads(value)
        except ValueError:
            try:
                with open(value, 'r') as effects_file:
                    effects_obj = json.load(effects_file)
            except:
                self.fail(
                    "Effect argument should be an inline JSON string or a JSON file")

        if not isinstance(effects_obj, list):
            self.fail("Effect root JSON object must be an array")

        try:
            return bm.effects.load_effect_chain(effects_obj)
        except ValidationError as e:
            self.fail(f"Effect {e.instance} is invalid: {e.message}")


@click.group()
@click.option(
    "-b", "--min-bpm", type=int, default=60, help="Minimum BPM of input audio, if applicable."
)
@click.option(
    "-B", "--max-bpm", type=int, default=300, help="Maximum BPM of input audio, if applicable."
)
@click.pass_context
def cli(ctx, min_bpm, max_bpm):
    ctx.obj = {"min_bpm": min_bpm, "max_bpm": max_bpm}


@cli.command()
@click.option("-e", "--effects", required=True, type=EffectChain())
@click.option("-o", "--output", type=click.Path(writable=True, dir_okay=False))
@click.argument("input", nargs=1, type=BeatsFromDisk())
def apply(input, output, effects):
    """
    Apply an effect chain to an input file.

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

    click.echo("Applying effects")
    beats = beats.apply_all(*effects)

    click.echo(f"Writing audio file to {output}")
    beats.save(output)

    print('Done!')


@cli.command()
@click.argument("input", nargs=1, type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--output", type=click.Path(writable=True, dir_okay=False))
@click.pass_context
def preprocess(ctx, input, output):
    """
    Convert a given audio file into a pickled .beat file. The resulting file
    can be used as an input to any other command to skip the processing step.
    """

    if input.endswith(".beat"):
        click.echo(
            f"Input file {input} has already been preprocessed", err=True)
        return 1

    if not output:
        output = os.path.splitext(input)[0] + ".beat"

    click.echo(f"Processing {input}")
    beats = bm.Beats.from_song(input, loader_args=ctx.obj)

    if os.path.isfile(output):
        click.confirm(f"Overwrite existing file at {output}", abort=True)

    click.echo(f"Writing beats to {output}")
    with open(output, "wb") as fp:
        fp.write(pickle.dumps(beats))

    print('Done!')


@cli.command()
@click.argument("input", nargs=1, type=click.Path(exists=True, dir_okay=False))
def analyze():
    """
    Report song BPM and beat times using madmom.
    """
    pass


@cli.command("validate")
@click.argument("input", nargs=1, type=click.Path(exists=True, dir_okay=False))
def validate_effects():
    """
    Validate a JSON effect chain.
    """
    pass


@cli.command("effects")
@click.option("-j", "--json-schema", is_flag=True, help="If set, outputs a JSON schema for effect chains.")
@click.option("-n", "--names-only", is_flag=True, help="If set, prints a list of effect names.")
def list_effects(json_schema, names_only):
    """
    List all available effects in various formats.
    """

    if json_schema:
        print(bm.effects.base.EffectRegistry.dump_list_schema(root=True))
        return

    effects = bm.effects.base.EffectRegistry.effects

    if names_only:
        for name in effects.keys():
            print(name)
        return

    print(f'{len(effects)} effects are available.')

    # TODO: Clean up
    for name, effect_cls in effects.items():
        print()
        print()
        print(name)

        print()
        print('  Description')
        description = inspect.cleandoc(
            effect_cls.__doc__) or 'No description.'
        print(textwrap.fill(description,
              initial_indent='    ', subsequent_indent='    '))

        print()
        print('  Parameters')

        schema = effect_cls.__effect_schema__
        if schema:
            for param, param_schema in schema.items():
                print(
                    f'    {param} ({param_schema["type"]}) - {param_schema["title"]}')
                if 'description' in param_schema:
                    print(textwrap.fill(
                        param_schema['description'], initial_indent='      ', subsequent_indent='      '))
        else:
            print('    No parameters.')


if __name__ == "__main__":
    cli()
