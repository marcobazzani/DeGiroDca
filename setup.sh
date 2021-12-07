#!/bin/bash

set -eu -o pipefail
shopt -s failglob

aws ssm put-parameter --name /degirodca/account/username --type SecureString --value $1 --overwrite
aws ssm put-parameter --name /degirodca/account/password --type SecureString --value $2 --overwrite