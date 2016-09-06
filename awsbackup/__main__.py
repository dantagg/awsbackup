from __future__ import absolute_import, division, print_function
import os
from jinja2 import Environment, PackageLoader

import click
import boto3
from botocore.client import ClientError

DEFAULT_AWS_PROFILE = 'default'
DEFAULT_BACKUP_CREDENTIAL_FILE = 'credentials'

env = Environment(loader=PackageLoader('awsbackup', 'templates'))

class AwsBackup(object):
    def __init__(self, home=None, profile=''):
        self.home = os.path.abspath(home or '.')
        self.profile = profile

class BucketExistsError(Exception):
    pass


#pass_awsbackup = click.make_pass_decorator(AwsBackup)


@click.group()
@click.version_option()
@click.option('--profile', '-p', default=lambda: os.environ.get('AWS_PROFILE', DEFAULT_AWS_PROFILE),
    help="tell awsbackup which aws profile to use from your aws credential file, by default it will use '%s'"
         % (DEFAULT_AWS_PROFILE,))
@click.pass_context
def main(ctx, profile):
    ctx.obj = AwsBackup(profile=profile)


@main.command()
@click.option('--bucket', '-b', prompt=True, default=lambda: os.environ.get('AWS_S3_BUCKET', ''),
              help='tell awsbackup what to call the bucket to send backups to')
@click.option('--user', '-u', prompt=True,
              help='tell awsbackup what user to create for the server to use to backup with')
@click.option('--file', '-f', type=click.File('w'), prompt=True,
              default=lambda: os.environ.get('AWS_BACKUP_CREDENTIAL_FILE', DEFAULT_BACKUP_CREDENTIAL_FILE),
              help="Location of file to SAVE user's credentials to")
@click.pass_context
def create(ctx, bucket, user, file):

    policy_template = env.get_template('backup_user_policy.json')
    backup_policy = policy_template.render(bucket=bucket)
    backup_policy_name = user+'_access_policy'

    profile = ctx.obj.profile   # get the profile from the parent command's options
    session = boto3.Session(profile_name=profile)

    s3_client = session.client('s3')
    try:
        bl = s3_client.get_bucket_location(Bucket=bucket)
        raise BucketExistsError("Bucket %s already exists!" % (bucket,))  # this bucket has been created already
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'NoSuchBucket':
            pass    # the bucket doesn't exist, phew
        elif ce.response['Error']['Code'] == 'AllAccessDisabled':
            raise BucketExistsError("Bucket %s already exists with a different owner!" % (bucket,))  # someone else has a bucket with this name
        else:
            raise ce

    bucket_rc = s3_client.create_bucket(Bucket=bucket)

    iam_client = session.client('iam')
    usr = iam_client.create_user(UserName=user)
    usr_policy = iam_client.put_user_policy(UserName=user, PolicyName=backup_policy_name, PolicyDocument=backup_policy)
    usr_keys = iam_client.create_access_key(UserName=user)
    access_key = usr_keys['AccessKey']['AccessKeyId']
    access_secret = usr_keys['AccessKey']['SecretAccessKey']
    credentials = "[%s]\naws_access_key_id = %s\naws_secret_access_key = %s" % (user, access_key, access_secret)
    file.write(credentials)

    import pdb; pdb.set_trace()

    cleanup(session, bucket, user, backup_policy_name, usr_keys['AccessKey']['AccessKeyId'])


@main.command()
@click.option('--bucket', '-b', prompt=True, default=lambda: os.environ.get('AWS_S3_BUCKET', ''),
              help='tell awsbackup what bucket to send backups to')
@click.option('--name', '-n', type=click.File('w'), prompt=True,
              default=lambda: os.environ.get('AWS_BACKUP_SCRIPT_FILE', DEFAULT_BACKUP_SCRIPT_FILE),
              help="Location of file to SAVE script to")
@click.option('--from', '-f', prompt=True,
              default=lambda: os.environ.get('AWS_BACKUP_DIRECTORY', DEFAULT_BACKUP_DIRECTORY),
              help="Location of directory to BACKUP")
@click.pass_context
def syncscript(ctx, bucket, name):
    pass

def cleanup(session, bucket, user, backup_policy_name, key_id):
    client = session.client('s3')
    client.delete_bucket(Bucket=bucket)
    client = session.client('iam')
    client.delete_user_policy(UserName=user, PolicyName=backup_policy_name)
    client.delete_access_key(UserName=user,AccessKeyId=key_id)
    client.delete_user(UserName=user)
