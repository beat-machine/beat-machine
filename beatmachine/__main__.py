import os
import pickle
import json

import click
import beatmachine as bm


def _hint(msg):
    click.secho("Hint: " + msg, fg="bright_black")


class BeatsFromDisk(click.Path):
    def __init__(self):
        super().__init__(exists=True, dir_okay=False)

    def convert(self, value, param, ctx):
        if not value:
            return None

        value = super().convert(value, param, ctx)

        if value.endswith(".beat"):
            with open(value, "rb") as fp:
                beats = pickle.load(fp)
        else:
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
        raise NotImplementedError("Resolve effects")


@click.group()
@click.option(
    "-b", "--min-bpm", type=int, default=60, help="Minimum BPM for processing."
)
@click.option(
    "-B", "--max-bpm", type=int, default=300, help="Maximum BPM for processing."
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

    if not output:
        stem, ext = os.path.splitext(filename)

        if ext == ".beat":
            ext = ".mp3"

        output = stem + "-out" + ext

    click.echo("Applying effects")
    beats = beats.apply_all(*effects)

    click.echo(f"Writing audio file to {output}")
    beats.save(output)


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
        click.echo(f"Input file {input} has already been preprocessed", err=True)
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
def list_effects():
    """
    List all available effects.
    """
    pass


if __name__ == "__main__":
    cli()
