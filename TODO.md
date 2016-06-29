# List of steps to take for project

Between each item in the list. The IAM policy needs to be set up so it is the minimum required to deliver that
functionality

1. Create the backup bucket
awsbackup create --bucket mybucket
1. Add authentication details
2. Create the user with the policy to back up to the backup bucket
3. Create the backup script that the user uses to back up to the backup bucket
4. Change backup bucket creation to be a versioning bucket
5. Create versioning policy and apply it ot bucket
6. Create weekly backup with versioning, policy and script
7. Create monthly backup with versioning, policy and script
8. Test whether server identity can
    i. list buckets
    ii. delete files
    iii. delete buckets
