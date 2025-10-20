# AWS Lambda Guide for Beginners
*Moving Your Deadline Reminder Bot to the Cloud*

## What is AWS Lambda?

Lambda is like hiring someone to run your code for you. Instead of your computer doing the work, Amazon's computers do it automatically.

### Local vs Lambda Comparison:

**Local (Current):**
```bash
# Your computer must be on 24/7
python bot.py  # Manual execution
```
*You have to remember to run it, and your computer must stay on.*

**Lambda (Target):**
```bash
# AWS runs automatically at 8 AM daily
# No computer needed
```
*Amazon runs it for you automatically. Your computer can be off.*

## Code Changes Required

Think of this like moving from a house to an apartment - some things change, but your furniture (core logic) stays the same.

### Universal Lambda Requirements (ALL Lambda functions need these):

#### 1. Handler Function (Required)
Lambda needs a specific "front door" to enter your code. This is like changing your address.
```python
# Current way:
if __name__ == "__main__":
    send_message()

# Lambda way:
def lambda_handler(event, context):
    try:
        asyncio.run(main())
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

**What are `event` and `context`?**
- **`event`**: Information about what triggered your function (like a delivery package with details)
- **`context`**: Runtime information about your function (like a receipt showing time limits and memory)

```python
# For your bot, you usually ignore both:
def lambda_handler(event, context):
    # event = {} (empty for EventBridge schedule)
    # context = runtime info you don't need
    return asyncio.run(main())

# But you can use them for debugging:
def lambda_handler(event, context):
    print(f"Triggered by: {event}")  # Shows what started your function
    print(f"Time remaining: {context.get_remaining_time_in_millis()}")  # Shows timeout
    return asyncio.run(main())
```

**Common `event` examples:**
```python
# EventBridge (scheduled trigger):
event = {}

# Manual test:
event = {"test": True}

# API Gateway (if you add web interface later):
event = {"body": "user data", "headers": {...}}
```

#### 2. Return Value (Required)
Lambda wants to know if your code worked or failed. Like texting "done" when you finish a task.
```python
# Lambda always expects a return value
return {"status": "success"}  # Success
return {"status": "error", "message": str(e)}  # Error
```

#### 3. Error Handling (Recommended)
Catch problems before they crash everything. Like having a backup plan.
```python
def lambda_handler(event, context):
    try:
        # Your main logic
        return {"status": "success"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}
```

### Project-Specific Requirements (Only for this bot):

#### 1. Credential Loading
Your secrets (tokens) need to move from a local file to AWS's secure vault.
```python
# Local way:
load_dotenv('.env')
token = os.environ["DISCORD_TOKEN"]

# Lambda way:
import boto3
ssm = boto3.client('ssm')  # SSM = Systems Manager (Parameter Store)
token = ssm.get_parameter(Name='/bot/discord-token', WithDecryption=True)['Parameter']['Value']

# Dual compatibility:
def load_credentials():
    if os.getenv('AWS_LAMBDA_FUNCTION_NAME'):
        # Running in Lambda
        ssm = boto3.client('ssm')
        return {
            'notion_token': ssm.get_parameter(Name='/deadline-bot/notion-token', WithDecryption=True)['Parameter']['Value'],
            'database_id': ssm.get_parameter(Name='/deadline-bot/database-id')['Parameter']['Value'],
            'discord_token': ssm.get_parameter(Name='/deadline-bot/discord-token', WithDecryption=True)['Parameter']['Value'],
            'channel_id': ssm.get_parameter(Name='/deadline-bot/channel-id')['Parameter']['Value']
        }
    else:
        # Running locally
        load_dotenv('.env')
        return {
            'notion_token': os.environ["NOTION_TOKEN"],
            'database_id': os.environ["NOTION_DATABASE_ID"],
            'discord_token': os.environ["DISCORD_TOKEN"],
            'channel_id': os.environ["DISCORD_CHANNEL_ID"]
        }
```

#### 2. Async Handling
Your bot uses async functions (for Discord/Notion). Lambda needs a wrapper to handle this properly.
```python
# Current structure:
def send_message():
    client.run(token)

# Lambda structure:
def lambda_handler(event, context):
    return asyncio.run(main())

async def main():
    # Move your existing async logic here
    pass
```

#### 3. Complete Bot Structure
Here's how your bot.py looks with minimal Lambda changes:
```python
# Minimal changes to your existing bot.py:

# Add at top
import boto3
import asyncio

# Add credential function
def load_credentials():
    # (code from above)

# Add Lambda handler
def lambda_handler(event, context):
    try:
        asyncio.run(main())
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Wrap existing logic
async def main():
    creds = load_credentials()
    # Use creds['notion_token'] instead of os.environ["NOTION_TOKEN"]
    # Rest of your existing code stays the same

# Keep for local testing
if __name__ == "__main__":
    asyncio.run(main())
```

## Dependencies Packaging

This is the trickiest part. Lambda is like a fresh computer with nothing installed - you must pack everything yourself.

### Local vs Lambda Dependencies:

**Local:**
```bash
pip install notion-client discord.py  # Installs to system
python bot.py                         # Finds packages automatically
```
*Your computer remembers what you installed.*

**Lambda:**
```bash
# Lambda has NO packages installed
# Must include everything in ZIP file
```
*Lambda starts fresh every time - like amnesia.*

### Packaging Process:
Think of this like packing a suitcase with everything you need for a trip.
```bash
# Step 1: Create deployment folder
mkdir lambda-deployment
cd lambda-deployment

# Step 2: Install packages TO this folder
pip install notion-client discord.py boto3 -t .

# Step 3: Copy your code
cp ../bot.py .

# Step 4: Create ZIP (from INSIDE the folder)
zip -r ../bot-deployment.zip .
```

### What Gets Packaged:
Your ZIP file becomes a complete, self-contained package:
```
bot-deployment.zip
├── bot.py                    # Your code
├── notion_client/            # Full package
├── discord/                  # Full package  
├── aiohttp/                  # Discord dependency
├── boto3/                    # AWS SDK
└── ... (all dependencies)
```

## AWS Services Setup

These are the AWS tools you'll use. Think of them as different departments in a company.

### 1. Parameter Store (Secrets)
A secure vault for your API tokens. Like a password manager in the cloud.

**What is SSM?** SSM = **Systems Manager**. Parameter Store is part of Systems Manager.

**Store secrets:**
```bash
aws ssm put-parameter --name "/deadline-bot/notion-token" --value "your_token" --type "SecureString"
aws ssm put-parameter --name "/deadline-bot/database-id" --value "your_db_id" --type "String"
aws ssm put-parameter --name "/deadline-bot/discord-token" --value "your_discord_token" --type "SecureString"
aws ssm put-parameter --name "/deadline-bot/channel-id" --value "your_channel_id" --type "String"
```

**Test retrieval:**
```bash
aws ssm get-parameter --name "/deadline-bot/notion-token" --with-decryption
```

### 2. Lambda Function
The actual computer that runs your code. Like renting a worker who follows your instructions.

**Create function:**
```bash
aws lambda create-function \
  --function-name deadline-reminder-bot \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR-ACCOUNT:role/lambda-execution-role \
  --handler bot.lambda_handler \
  --zip-file fileb://bot-deployment.zip
```

**Update code:**
```bash
aws lambda update-function-code \
  --function-name deadline-reminder-bot \
  --zip-file fileb://bot-deployment.zip
```

**Test function:**
```bash
aws lambda invoke --function-name deadline-reminder-bot output.txt
cat output.txt
```

### 3. EventBridge (Scheduling)
A clock that triggers your Lambda. Like setting an alarm that starts your code.

**Create daily schedule:**
```bash
# Create rule for 8 AM UTC daily
aws events put-rule \
  --name daily-deadline-reminder \
  --schedule-expression "cron(0 8 * * ? *)"

# Connect to Lambda
aws events put-targets \
  --rule daily-deadline-reminder \
  --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:YOUR-ACCOUNT:function:deadline-reminder-bot"

# Give permission
aws lambda add-permission \
  --function-name deadline-reminder-bot \
  --statement-id allow-eventbridge \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com
```

**Common schedules:**
```bash
cron(0 8 * * ? *)      # 8 AM UTC daily
cron(0 13 * * ? *)     # 8 AM EST daily  
cron(0 8 ? * MON-FRI *) # 8 AM weekdays only
```

### 4. CloudWatch (Monitoring)
A security camera for your code. Shows you what happened and alerts you to problems.

**View logs:**
```bash
aws logs describe-log-streams --log-group-name /aws/lambda/deadline-reminder-bot
aws logs get-log-events --log-group-name /aws/lambda/deadline-reminder-bot --log-stream-name "STREAM_NAME"
```

**Create error alert:**
```bash
# Create SNS topic
aws sns create-topic --name lambda-alerts

# Subscribe email
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:YOUR-ACCOUNT:lambda-alerts \
  --protocol email \
  --notification-endpoint your-email@example.com

# Create alarm
aws cloudwatch put-metric-alarm \
  --alarm-name deadline-bot-errors \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --dimensions Name=FunctionName,Value=deadline-reminder-bot
```

## What Stays the Same

The good news: your hard work stays intact! Lambda is just a new way to run the same code.

**Your core business logic doesn't change:**
```python
# These functions work identically in Lambda:
async def extract_assignment_info()
async def format_message()
def format_date()
def get_three_days_out()

# Same imports:
from notion_client import AsyncClient
import discord
from datetime import datetime
```

## Migration Steps

Follow these steps in order. Each step builds on the previous one.

1. **Modify bot.py** - Add Lambda handler and credential loading
2. **Test locally** - Ensure dual compatibility works
3. **Package dependencies** - Create deployment ZIP
4. **Store secrets** - Put tokens in Parameter Store
5. **Create Lambda** - Upload and configure function
6. **Set schedule** - Create EventBridge rule
7. **Monitor** - Set up CloudWatch alerts
8. **Test end-to-end** - Verify daily execution

## Key Differences Summary

Quick reference for local vs Lambda differences:

| Aspect | Local | Lambda |
|--------|-------|--------|
| **Entry Point** | `if __name__ == "__main__"` | `def lambda_handler(event, context)` |
| **Secrets** | `.env` file | Parameter Store |
| **Dependencies** | `pip install` | ZIP package |
| **Scheduling** | Manual/cron | EventBridge |
| **Monitoring** | Terminal output | CloudWatch |


---

# TODO Checklist: Lambda Migration

## Phase 1: Code Preparation (Local Development)

### ☐ 1. Modify bot.py for Lambda compatibility
**Code Changes Required:**
```python
# Add imports
import boto3
import asyncio

# Add credential loading function
def load_credentials():
    # (dual compatibility code from guide)

# Add Lambda handler
def lambda_handler(event, context):
    try:
        asyncio.run(main())
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Wrap existing logic in main()
async def main():
    creds = load_credentials()
    # Use creds['notion_token'] instead of os.environ["NOTION_TOKEN"]
    # Rest of existing code stays the same
```

### ☐ 2. Test locally with dual compatibility
**Code/CLI:**
```bash
# Should still work locally
python bot.py
```

### ☐ 3. Create deployment package
**Code/CLI:**
```bash
mkdir lambda-deployment
cd lambda-deployment
pip install notion-client discord.py boto3 -t .
cp ../bot.py .
zip -r ../bot-deployment.zip .
```

## Phase 2: AWS Infrastructure Setup

### ☐ 4. Store secrets in Parameter Store

**Option A - CLI:**
```bash
aws ssm put-parameter --name "/deadline-bot/notion-token" --value "YOUR_TOKEN" --type "SecureString"
aws ssm put-parameter --name "/deadline-bot/database-id" --value "YOUR_DB_ID" --type "String"
aws ssm put-parameter --name "/deadline-bot/discord-token" --value "YOUR_DISCORD_TOKEN" --type "SecureString"
aws ssm put-parameter --name "/deadline-bot/channel-id" --value "YOUR_CHANNEL_ID" --type "String"
```

**Option B - AWS Console UI:**
1. Go to AWS Systems Manager → Parameter Store
2. Click "Create parameter"
3. For each secret:
   - Name: `/deadline-bot/notion-token`
   - Type: SecureString (for tokens) or String (for IDs)
   - Value: [paste your token]
4. Click "Create parameter"
5. Repeat for all 4 secrets

### ☐ 5. Test parameter retrieval
**Code/CLI:**
```bash
aws ssm get-parameter --name "/deadline-bot/notion-token" --with-decryption
```

### ☐ 6. Create IAM execution role (if not exists)

**Option A - CLI:**
```bash
# Create role
aws iam create-role --role-name lambda-execution-role --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}'

# Attach policies
aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess
```

**Option B - AWS Console UI:**
1. Go to IAM → Roles
2. Click "Create role"
3. Select "AWS service" → "Lambda"
4. Attach policies:
   - `AWSLambdaBasicExecutionRole`
   - `AmazonSSMReadOnlyAccess`
5. Name: `lambda-execution-role`
6. Click "Create role"

### ☐ 7. Create Lambda function

**Option A - CLI:**
```bash
aws lambda create-function \
  --function-name deadline-reminder-bot \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR-ACCOUNT-ID:role/lambda-execution-role \
  --handler bot.lambda_handler \
  --zip-file fileb://bot-deployment.zip \
  --timeout 60 \
  --memory-size 256
```

**Option B - AWS Console UI:**
1. Go to AWS Lambda → Functions
2. Click "Create function"
3. Choose "Author from scratch"
4. Function name: `deadline-reminder-bot`
5. Runtime: Python 3.9
6. Execution role: Use existing `lambda-execution-role`
7. Click "Create function"
8. Upload code:
   - Scroll to "Code source"
   - Click "Upload from" → ".zip file"
   - Select `bot-deployment.zip`
   - Click "Save"
9. Configure settings:
   - Go to "Configuration" → "General configuration"
   - Timeout: 1 minute
   - Memory: 256 MB

### ☐ 8. Test Lambda function

**Option A - CLI:**
```bash
aws lambda invoke --function-name deadline-reminder-bot output.txt
cat output.txt
```

**Option B - AWS Console UI:**
1. In Lambda function page, click "Test"
2. Create test event:
   - Event name: `test-event`
   - Template: Hello World
3. Click "Test"
4. Check execution results

## Phase 3: Scheduling Setup

### ☐ 9. Create EventBridge schedule

**Option A - CLI:**
```bash
# Create rule
aws events put-rule \
  --name daily-deadline-reminder \
  --schedule-expression "cron(0 8 * * ? *)"

# Add Lambda target
aws events put-targets \
  --rule daily-deadline-reminder \
  --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:YOUR-ACCOUNT:function:deadline-reminder-bot"

# Give EventBridge permission
aws lambda add-permission \
  --function-name deadline-reminder-bot \
  --statement-id allow-eventbridge \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:us-east-1:YOUR-ACCOUNT:rule/daily-deadline-reminder
```

**Option B - AWS Console UI:**
1. Go to Amazon EventBridge → Rules
2. Click "Create rule"
3. Name: `daily-deadline-reminder`
4. Rule type: Schedule
5. Schedule pattern: Cron expression
6. Cron: `cron(0 8 * * ? *)` (adjust for timezone)
7. Target: Lambda function
8. Function: `deadline-reminder-bot`
9. Click "Create rule"

## Phase 4: Monitoring Setup

### ☐ 10. Set up error alerts

**Option A - CLI:**
```bash
# Create SNS topic
aws sns create-topic --name lambda-alerts

# Subscribe email
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:YOUR-ACCOUNT:lambda-alerts \
  --protocol email \
  --notification-endpoint your-email@example.com

# Create CloudWatch alarm
aws cloudwatch put-metric-alarm \
  --alarm-name deadline-bot-errors \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --dimensions Name=FunctionName,Value=deadline-reminder-bot \
  --alarm-actions arn:aws:sns:us-east-1:YOUR-ACCOUNT:lambda-alerts
```

**Option B - AWS Console UI:**
1. Go to CloudWatch → Alarms
2. Click "Create alarm"
3. Select metric: AWS/Lambda → By Function Name → deadline-reminder-bot → Errors
4. Conditions: Greater than 0
5. Create SNS topic: `lambda-alerts`
6. Add your email
7. Alarm name: `deadline-bot-errors`
8. Click "Create alarm"

### ☐ 11. Verify monitoring

**Code/CLI:**
```bash
# Check logs
aws logs describe-log-streams --log-group-name /aws/lambda/deadline-reminder-bot
```

**AWS Console UI:**
1. Go to Lambda → Functions → deadline-reminder-bot
2. Click "Monitor" tab
3. Click "View logs in CloudWatch"

## Phase 5: Final Testing

### ☐ 12. Test end-to-end execution
- Manually trigger Lambda function
- Verify Discord message is sent
- Check CloudWatch logs for success
- Confirm no errors in monitoring

### ☐ 13. Wait for scheduled execution
- Wait for next 8 AM trigger
- Verify automatic execution works
- Monitor for several days

### ☐ 14. Decommission local version
- Stop any local cron jobs
- Archive local bot files
- Update documentation

---

---

## How to Reference the IAM Role Again

**Once created, you can reference the role in multiple ways:**

**By Name (CLI):**
```bash
# Use the role name in other commands
aws lambda create-function --role arn:aws:iam::YOUR-ACCOUNT:role/lambda-execution-role
```

**By ARN (CLI):**
```bash
# Get the full ARN
aws iam get-role --role-name lambda-execution-role --query 'Role.Arn' --output text
# Returns: arn:aws:iam::123456789012:role/lambda-execution-role
```

**In Console UI:**
- Go to IAM → Roles → Search for "lambda-execution-role"
- Copy the ARN from the role summary page
- Use in Lambda function creation dropdown

**Pro Tips:**
- Use CLI for automation and repeatability
- Use Console UI for learning and visual confirmation
- Test each phase before moving to the next
- Keep your local version working until Lambda is fully tested