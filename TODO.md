# List of steps to take for project

Between each item in the list. The IAM policy needs to be set up so it is the minimum required to deliver that
functionality

1. ~~Create the backup bucket~~<br>
 `awsbackup create --bucket mybucket`
2. ~~Add authentication details~~ <br>
  `awsbackup --profile myprofile --bucket backupmybucket`
3. ~~Create the User with the permissions to backup to the bucket and the credentials to sign in~~ <br>
  `awsbackup --profile myprofile --bucket backupmybucket --user backupmyuser`

3. Create the backup script that the user uses to back up to the backup bucket
4. Change backup bucket creation to be a versioning bucket
5. Create versioning policy and apply it ot bucket
6. Create weekly backup with versioning, policy and script
7. Create monthly backup with versioning, policy and script
8. Test whether server identity can
    i. list buckets
    ii. delete files
    iii. delete buckets


