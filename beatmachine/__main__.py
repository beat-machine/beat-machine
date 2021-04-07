import os
import pickle

import click
import beatmachine as bm


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", nargs=1, type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--output", type=click.Path(writable=True, dir_okay=False))
@click.option("--min-bpm", type=int, default=60)
@click.option("--max-bpm", type=int, default=300)
def apply(input, output, min_bpm, max_bpm):
    """
    Apply an effect chain to an input file.

    See all valid effects using the `effects` subcommand. Preprocessed files
    generated with `preprocess` can be used to skip the processing step.

    Note that preprocessed files carry the same security risks as any pickled
    Python objects. Use .beat files from trusted sources!
    """
    if not output:
        stem, ext = os.path.splitext(input)

        if ext == ".beat":
            ext = ".mp3"

        output = stem + "-out" + ext

    if input.endswith(".beat"):
        click.echo("Using preprocessed .beat file")

        with open(input, "rb") as fp:
            beats = pickle.load(fp)
    else:
        click.echo(f"Processing {input}")
        click.echo("Hint: use the `preprocess` command to do this in advance")

        beats = bm.Beats.from_song(
            input, loader_args={"min_bpm": min_bpm, "max_bpm": max_bpm}
        )

    click.echo("Applying effects")
    raise NotImplementedError("Load effects")

    click.echo(f"Writing audio file to {output}")
    beats.save(output)


@cli.command()
@click.argument("input", nargs=1, type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--output", type=click.Path(writable=True, dir_okay=False))
@click.option("--min-bpm", type=int, default=60)
@click.option("--max-bpm", type=int, default=300)
def preprocess(input, output, min_bpm, max_bpm):
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
    beats = bm.Beats.from_song(
        input, loader_args={"min_bpm": min_bpm, "max_bpm": max_bpm}
    )

    if os.path.isfile(output):
        click.confirm(f"Overwrite existing file at {output}", abort=True)

    click.echo(f"Writing beats to {output}")
    with open(output, "wb") as fp:
        fp.write(pickle.dumps(beats))


@cli.command()
@click.argument("input", nargs=1, type=click.Path(exists=True, dir_okay=False))
@click.option("--min-bpm", type=int, default=60)
@click.option("--max-bpm", type=int, default=300)
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
