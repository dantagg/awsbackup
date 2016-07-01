from __future__ import absolute_import, division, print_function
import os
import click
import boto3

@click.group()
@click.version_option()
def main():
    pass

@main.command()
@click.option('--bucket', '-b', prompt=True, default=lambda: os.environ.get('BUCKET', ''))
def create(bucket):
    client = boto3. client('s3')
    bucket_rc = client.create_bucket(Bucket=bucket)
    print("Hello World! %s" % (bucket_rc['Location'],))


