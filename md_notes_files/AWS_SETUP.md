# AWS Setup Guide - Due Date Demon

## Prerequisites
- AWS account created
- AWS CLI installed (`brew install awscli`)
- `lambda-trust-policy.json` file exists

## 1. IAM User Setup

### Create IAM User
- Name: `daily-deadline-service`
- Access type: Programmatic access only
- Permissions: AdministratorAccess (for development)

### Create Access Keys
- Use case: Command Line Interface (CLI)
- Save Access Key ID and Secret Access Key securely

## 2. AWS CLI Configuration

```bash
aws configure
```

- **Access Key ID**: [your-access-key-id]
- **Secret Access Key**: [your-secret-access-key]
- **Region**: us-east-1
- **Output**: json

### Verification
```bash
aws sts get-caller-identity
```
Should return ARN ending with `user/daily-deadline-service`

## 3. One-Time AWS Setup Commands

### Create IAM Role
```bash
aws iam create-role --role-name lambda-execution-role --assume-role-policy-document file://lambda-trust-policy.json
aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess
```

### Create Lambda Function
```bash
# Replace ACCOUNT_ID with your AWS account ID
aws lambda create-function \
  --function-name deadline-reminder-bot \
  --runtime python3.9 \
  --role arn:aws:iam::ACCOUNT_ID:role/lambda-execution-role \
  --handler bot.lambda_handler \
  --zip-file fileb://bot-deployment.zip \
  --timeout 60 \
  --memory-size 256
```

### Set Up EventBridge Scheduling
```bash
# Create daily 8 AM EST schedule (13:00 UTC)
aws events put-rule \
  --name daily-deadline-reminder \
  --schedule-expression "cron(0 13 * * ? *)"

# Connect to Lambda (replace ACCOUNT_ID with your AWS account ID)
aws events put-targets \
  --rule daily-deadline-reminder \
  --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:ACCOUNT_ID:function:deadline-reminder-bot"

# Give EventBridge permission to invoke Lambda
aws lambda add-permission \
  --function-name deadline-reminder-bot \
  --statement-id allow-eventbridge \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com
```

## 4. Ongoing Operations

Use the Makefile for regular operations:
- `make setup` - Set up local development environment
- `make run` - Run bot locally for testing
- `make package` - Create Lambda deployment package
- `make deploy` - Update Lambda function code
- `make schedule-create` - Set up EventBridge scheduling
- `make schedule-disable` - Disable daily schedule
- `make schedule-enable` - Re-enable daily schedule

## 5. Parameter Store Setup (Required)

The bot requires these parameters to be set in AWS Parameter Store:

```bash
# Set up your credentials in Parameter Store
aws ssm put-parameter --name "/daily-deadline/notion-token" --value "YOUR_NOTION_TOKEN" --type "SecureString"
aws ssm put-parameter --name "/daily-deadline/notion-database-id" --value "YOUR_DATABASE_ID" --type "SecureString"
aws ssm put-parameter --name "/daily-deadline/discord-token" --value "YOUR_DISCORD_TOKEN" --type "SecureString"
aws ssm put-parameter --name "/daily-deadline/discord-channel-id" --value "YOUR_CHANNEL_ID" --type "SecureString"
```

## 6. Future Enhancements
- [ ] Configure DynamoDB for multi-user support
- [ ] Implement Infrastructure as Code (Terraform/CDK)
- [ ] Add CloudWatch alarms for monitoring

## Security Notes
- Never commit AWS credentials to Git
- Store backup credentials in password manager
- Rotate access keys every 90 days
- Use least privilege permissions in production