from invoke import task
from setuptools import sandbox


@task
def clean(ctx):
    """
    Runs `setup.py clean` and removes any extraneous MP3 files used for testing.
    """
    ctx.run('rm -rf *.mp3')
    sandbox.run_setup('setup.py', ['clean'])
