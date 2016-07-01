from __future__ import absolute_import, division, print_function
import os
import click
import boto3
from botocore.client import ClientError

DEFAULT_AWS_PROFILE = 'default'

class AwsBackup(object):
    def __init__(self, home=None, profile=''):
        self.home = os.path.abspath(home or '.')
        self.profile = profile

class BucketExistsError(Exception):
    pass


#pass_awsbackup = click.make_pass_decorator(AwsBackup)


@click.group()
@click.version_option()
@click.option('--profile', '-p', default=lambda: os.environ.get('AWS_PROFILE', DEFAULT_AWS_PROFILE))
@click.pass_context
def main(ctx, profile):
    ctx.obj = AwsBackup(profile=profile)


@main.command()
@click.option('--bucket', '-b', prompt=True, default=lambda: os.environ.get('AWS_S3_BUCKET', ''))
@click.pass_context
def create(ctx, bucket):
    profile = ctx.obj.profile
    session = boto3.Session(profile_name=profile)
    client = session.client('s3')
    try:
        bl = client.get_bucket_location(Bucket=bucket)
        raise BucketExistsError("Bucket %s already exists!" % (bucket,))
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'NoSuchBucket':
            pass
        elif ce.response['Error']['Code'] == 'AllAccessDisabled':
            raise BucketExistsError("Bucket %s already exists!" % (bucket,))
        else:
            raise ce



    bucket_rc = client.create_bucket(Bucket=bucket)
    import pdb; pdb.set_trace()
    print("Hello World! %s" % (bucket_rc['Location'],))


