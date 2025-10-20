# Deadline Reminder Bot Makefile

# Variables
PYTHON = python3
VENV_DIR = venv39


# First-time setup
.PHONY: setup
setup:
	@echo "Creating Python 3.9 virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	source $(VENV_DIR)/bin/activate && pip install --upgrade pip
	source $(VENV_DIR)/bin/activate && pip install discord.py notion-client python-dotenv boto3
	@echo "Setup complete!"

# Install or update dependencies
.PHONY: install
install:
	source $(VENV_DIR)/bin/activate && pip install --upgrade discord.py notion-client python-dotenv boto3

# Run the bot once
.PHONY: run
run:
	source $(VENV_DIR)/bin/activate && python bot.py

# Test environment setup
.PHONY: test
test:
	@echo "Testing environment..."
	source $(VENV_DIR)/bin/activate && python -c "import notion_client, discord, dotenv; print('All dependencies installed successfully!')"

# AWS Parameter Store operations
.PHONY: aws-check
aws-check:
	@echo "Checking AWS Parameter Store..."
	aws ssm get-parameters-by-path --path "/daily-deadline" --with-decryption

.PHONY: aws-test
aws-test:
	@echo "Testing Parameter Store integration..."
	source $(VENV_DIR)/bin/activate && pip install boto3
	source $(VENV_DIR)/bin/activate && python -c "import boto3; ssm = boto3.client('ssm'); print('AWS connection successful!')"

# Lambda operations (ongoing)
.PHONY: package
package:
	@echo "Creating Lambda deployment package..."
	rm -rf lambda-deployment
	mkdir -p lambda-deployment
	source $(VENV_DIR)/bin/activate && pip install discord.py notion-client boto3 async-timeout aiohttp python-dotenv -t lambda-deployment/
	cp bot.py lambda-deployment/
	cd lambda-deployment && zip -r ../bot-deployment.zip .
	@echo "Deployment package created: bot-deployment.zip"

.PHONY: deploy
deploy: package
	@echo "Updating Lambda function code..."
	aws lambda update-function-code --function-name deadline-reminder-bot --zip-file fileb://bot-deployment.zip
	@echo "Lambda function updated successfully"


# EventBridge scheduling
.PHONY: schedule-create
schedule-create:
	@echo "Creating EventBridge rule for daily scheduling..."
	aws events put-rule --cli-input-json file://eventbridge-rule.json
	aws lambda add-permission --function-name deadline-reminder-bot --statement-id allow-eventbridge --action lambda:InvokeFunction --principal events.amazonaws.com --source-arn arn:aws:events:us-east-1:507881106119:rule/daily-deadline-reminder
	aws events put-targets --rule daily-deadline-reminder --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:507881106119:function:deadline-reminder-bot"
	@echo "Daily scheduling enabled at 8 AM EST"

.PHONY: schedule-disable
schedule-disable:
	@echo "Disabling daily schedule..."
	aws events disable-rule --name daily-deadline-reminder

.PHONY: schedule-enable
schedule-enable:
	@echo "Enabling daily schedule..."
	aws events enable-rule --name daily-deadline-reminder

.PHONY: schedule-status
schedule-status:
	@echo "Checking schedule status..."
	aws events describe-rule --name daily-deadline-reminder

# Clean up
.PHONY: clean
clean:
	rm -rf $(VENV_DIR) lambda-deployment bot-deployment.zip
	@echo "Cleaned up virtual environment and deployment files."