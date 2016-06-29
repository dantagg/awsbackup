from __future__ import absolute_import, division, print_function
import os
import click

@click.command()
@click.option('--bucket', prompt=True, default=lambda: os.environ.get('BUCKET', ''))
def main(bucket):
    print("Hello World! %s" % (bucket,))


