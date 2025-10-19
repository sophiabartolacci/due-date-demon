# AWS CLI Commands Reference - Daily Deadline Bot

## AWS Configuration
```bash
aws configure
# Configure AWS CLI with access keys, region, and output format

aws sts get-caller-identity
# Verify AWS CLI setup and show current user/account info

aws --version
# Check installed AWS CLI version
```

## Parameter Store (Systems Manager)
```bash
aws ssm put-parameter --name "/daily-deadline/notion-token" --value "token" --type "SecureString"
# Store encrypted parameter in Parameter Store

aws ssm get-parameter --name "/daily-deadline/notion-token" --with-decryption
# Retrieve and decrypt parameter from Parameter Store

aws ssm get-parameters-by-path --path "/daily-deadline" --recursive --with-decryption
# Get all parameters under a specific path

aws ssm describe-parameters --filters "Key=Name,Values=/daily-deadline"
# List all parameters matching a filter (without values)

aws ssm delete-parameter --name "/daily-deadline/parameter-name"
# Delete a parameter from Parameter Store
```

## Lambda Functions
```bash
aws lambda list-functions
# List all Lambda functions in your account

aws lambda create-function --function-name daily-deadline --runtime python3.9 --role arn:aws:iam::account:role/lambda-role --handler lambda_function.lambda_handler --zip-file fileb://function.zip
# Create a new Lambda function

aws lambda invoke --function-name daily-deadline output.txt
# Test/invoke a Lambda function manually

aws lambda update-function-code --function-name daily-deadline --zip-file fileb://function.zip
# Update Lambda function code

aws lambda get-function --function-name daily-deadline
# Get Lambda function configuration and metadata
```

## IAM (Identity and Access Management)
```bash
aws iam list-users
# List all IAM users in your account

aws iam list-access-keys --user-name daily-deadline-service
# List access keys for a specific user

aws iam create-access-key --user-name daily-deadline-service
# Create new access key for a user

aws iam delete-access-key --user-name daily-deadline-service --access-key-id AKIAEXAMPLE
# Delete an access key
```

## EventBridge (CloudWatch Events)
```bash
aws events list-rules
# List all EventBridge rules

aws events put-rule --name daily-deadline-schedule --schedule-expression "cron(0 8 * * ? *)"
# Create a rule that triggers daily at 8 AM

aws events put-targets --rule daily-deadline-schedule --targets "Id"="1","Arn"="arn:aws:lambda:region:account:function:daily-deadline"
# Add Lambda function as target for EventBridge rule
```

## CloudWatch Logs
```bash
aws logs describe-log-groups
# List all CloudWatch log groups

aws logs describe-log-streams --log-group-name /aws/lambda/daily-deadline
# List log streams for a specific log group

aws logs get-log-events --log-group-name /aws/lambda/daily-deadline --log-stream-name "stream-name"
# Get log events from a specific log stream
```

## General AWS
```bash
aws help
# Show general AWS CLI help

aws <service> help
# Show help for a specific service (e.g., aws lambda help)

aws <service> <command> help
# Show help for a specific command (e.g., aws lambda create-function help)
```

## Python/Local Development
```bash
pip install boto3
# Install AWS SDK for Python

python lambda_bot.py
# Test Lambda function locally

source venv/bin/activate
# Activate Python virtual environment

pip freeze > requirements.txt
# Generate requirements file for dependencies
```