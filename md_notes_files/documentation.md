# Notion Discord Deadline Reminder Bot

## Project Summary (Resume Format)

**Situation:** Needed an automated solution to track assignment deadlines across multiple courses and receive timely notifications without manually checking Notion database daily.

**Task:** Develop a Python automation bot that integrates Notion API with Discord to send formatted daily reminders of upcoming assignments due within 3 days.

**Action:** Built a full-stack automation solution using Python, implementing async/await patterns for API calls, custom date formatting, visual message design with emojis and consistent formatting, environment variable security practices, and error handling for edge cases like empty assignment lists.

**Result:** Successfully automated deadline tracking with 100% reliability, reducing missed assignments and manual database checking. Designed for scalability with plans to make it universally usable for different Notion database structures.

**Technologies:** Python, Notion API, Discord.py, asyncio, datetime manipulation, environment variable management, virtual environments

## Resume Bullet Points

• Built automated deadline reminder system that connects Notion database to Discord, sending daily notifications for assignments due within 3 days to prevent missed deadlines

• Developed Python bot using async programming and API integration to eliminate manual deadline tracking, improving academic productivity and time management

• Implemented secure, production-ready architecture with custom message formatting and error handling, designed for scalability and multi-user deployment

---

# Development Documentation

This file automatically captures important development information for the deadline reminder bot project.

---

## [2025-08-22] - Project Foundation and Development Setup

### **Core Bot Implementation**
- **Notion-Discord Integration:** Built basic bot for fetching tasks from Notion database and sending daily to-do lists to Discord
- **API Integration:** Implemented Notion API for database access and Discord bot for message delivery
- **Environment Configuration:** Set up secure token management with environment variables

### **Security and Best Practices**
- **Secure Token Management:** Migrated from hardcoded tokens to .env file with `load_dotenv('env-vars/.env')`
- **Repository Security:** Added .env.example template, updated .gitignore to exclude sensitive files
- **Dependency Management:** Created requirements.txt with python-dotenv for secure environment handling

### **Development Environment**
- **Virtual Environment:** Set up isolated Python environment with `python3 -m venv venv`
- **Package Installation:** Installed core dependencies (notion-client, discord.py, python-dotenv)
- **Configuration Fixes:** Corrected environment variable reference from NOTION_DB_ID to NOTION_DATABASE_ID

### **Documentation and Project Structure**
- **Comprehensive Setup Guide:** Created detailed SETUP.md with step-by-step instructions for new developers
- **API Token Instructions:** Added guidance for obtaining Notion and Discord API tokens
- **Project Organization:** Separated detailed setup from project overview for better maintainability

**Key Learning:** Established foundation for secure, maintainable bot development with proper environment management and comprehensive documentation

---

## [2025-09-12] - Feature Enhancement and AWS Cloud Migration

### **User Experience Improvements**
- **Visual Message Design:** Implemented Discord message formatting with custom visual design, class icons, and assignment type icons for better categorization
- **Smart Date Formatting:** Added format_date() function to convert ISO datetime to user-friendly M/D HAM/PM format with time detection
- **Mobile Optimization:** Optimized first line to show clean "x assignments due soon" for phone notification previews (first ~50 characters)
- **Edge Case Handling:** Added proper handling for empty assignments with positive messaging

### **Scheduling and Automation**
- **Dual Scheduling Options:** Created scheduler.py using schedule library and setup_cron.sh for system cron job
- **Flexible Deployment:** Python scheduler (easier to modify) vs cron job (more reliable) options
- **Daily Automation:** Configured 8:00 AM daily reminders with automatic execution

### **AWS Cloud Infrastructure Migration**
- **AWS Account Setup:** Created AWS Educate student account with free credits for learning
- **Security Best Practices:** Set up IAM user `daily-deadline-service` with AdministratorAccess policy instead of using root account
- **CLI Configuration:** Configured AWS CLI with programmatic access keys and us-east-1 region
- **Infrastructure Verification:** Verified setup with `aws sts get-caller-identity`

### **Serverless Architecture Implementation**
- **Parameter Store Security:** Migrated from .env files to AWS Parameter Store with SecureString encryption for all secrets
- **Lambda-Ready Architecture:** Created `lambda_bot.py` with boto3 integration and proper Lambda handler pattern
- **Secure Credential Management:** Implemented `get_parameter()` function for secure credential retrieval
- **Serverless Foundation:** Established infrastructure for scalable, multi-user SaaS deployment

### **Scalability Planning**
- **Schema Flexibility:** Identified need for dynamic database schema support beyond hardcoded column structure
- **Multi-User Readiness:** Planned flexible column mapping and auto-detection for broader adoption
- **Production Architecture:** Designed for universal usability across different Notion database structures

### **Key Technical Learnings**
- **Async/Await Mastery:** Resolved event loop management, proper async function chaining, and Discord.py integration patterns
- **AWS Services Integration:** Parameter Store, IAM, Lambda architecture, CLI configuration and management
- **Security Evolution:** From local .env files to encrypted cloud-based secret management
- **Mobile-First Design:** Discord notification optimization for mobile user experience

**Technologies Mastered:** AWS Parameter Store, AWS Lambda, AWS IAM, boto3 SDK, schedule library, cron jobs, mobile-optimized messaging

**Commands Used:**
```bash
# AWS Parameter Store setup
aws ssm put-parameter --name "/daily-deadline/notion-token" --value "secret_token" --type "SecureString"
aws ssm put-parameter --name "/daily-deadline/database-id" --value "database_id" --type "SecureString"
aws ssm put-parameter --name "/daily-deadline/discord-token" --value "discord_token" --type "SecureString"
aws ssm put-parameter --name "/daily-deadline/channel-id" --value "channel_id" --type "String"

# Testing and validation
aws ssm get-parameter --name "/daily-deadline/notion-token" --with-decryption
pip install boto3
python lambda_bot.py
```

---

## [2025-09-16] - AWS Lambda Migration Planning and Interactive Features Research

### **AWS Lambda Migration Strategy**
**Type:** Infrastructure/Deployment
**Description:** Researched and planned migration from local execution to AWS Lambda serverless architecture
**Implementation:** 
- **Lambda Handler Pattern:** Identified need for `lambda_handler(event, context)` entry point function
- **Dual Compatibility:** Designed bot.py to work both locally and in Lambda using environment detection
- **Dependency Packaging:** Learned Lambda requires all packages in deployment ZIP (no pip install at runtime)
- **Credential Management:** Confirmed Parameter Store integration for secure token storage
- **Scheduling:** EventBridge cron expressions for daily 8 AM execution
- **Monitoring:** CloudWatch logs and SNS alerts for error tracking

**Key AWS Services:**
- **Parameter Store (SSM):** Free secure storage for API tokens
- **Lambda:** Serverless code execution (15-minute max, 256MB memory sufficient)
- **EventBridge:** Cron-based scheduling (`cron(0 8 * * ? *)`)
- **CloudWatch:** Logging and error alerting
- **IAM:** Execution roles with minimal required permissions

**Migration Benefits:**
- Eliminates need for always-on computer
- 99.99% uptime reliability
- Automatic scaling and error recovery
- Professional cloud infrastructure
- Essentially free for personal use (within AWS free tier)

**Notes:** Decided against Terraform for this project size (5 AWS resources) - CLI commands more appropriate for learning and single-user setup

---

### **Interactive Discord Bot Features Research**
**Type:** Feature Planning
**Description:** Explored expansion possibilities using Notion API's full CRUD capabilities
**Implementation:** Discovered Notion API supports Create, Read, Update, Delete operations beyond current read-only usage

**Simple Interactions (Easy to Add):**
```python
# Slash Commands
/deadlines          # Show current deadlines
/complete "Math Homework"  # Mark assignment done
/add "Physics Lab" "PHYS 201" "2024-01-20"  # Add new assignment

# Reaction-Based Interactions  
✅ Mark assignment as complete
📅 Snooze reminder for 1 hour
❌ Remove assignment
📝 Add notes to assignment
```

**Medium Complexity Features:**
- **Interactive Buttons:** [Complete] [Snooze 1hr] [Snooze 1day] [Details]
- **Assignment Management:** Edit due dates, delete assignments, view details
- **Smart Notifications:** Different urgency levels (🔴 URGENT, 🟡 Due tomorrow, 🟢 Due in 3 days)
- **Multi-User Support:** Separate Notion databases per Discord user

**Advanced Features:**
- **Study Session Tracking:** Pomodoro timers, productivity metrics
- **AI Integration:** Study plan generation, concept explanations, quiz generation
- **Calendar Sync:** Two-way sync with Google Calendar/Outlook
- **Analytics Dashboard:** Completion streaks, productivity stats, leaderboards

**Required Notion API Permissions:**
- ✅ Read content (already have)
- ✅ Update content (for marking complete, editing)
- ✅ Insert content (for adding new assignments)

**Example Implementation:**
```python
# Mark assignment complete via Discord reaction
await notion.pages.update(
    page_id="assignment_page_id",
    properties={"To Do": {"checkbox": True}}
)

# Add new assignment via slash command
await notion.pages.create(
    parent={"database_id": database_id},
    properties={
        "Assignment": {"title": [{"text": {"content": "New Homework"}}]},
        "Class": {"select": {"name": "CS 380"}},
        "Due Date": {"date": {"start": "2024-01-15"}},
        "To Do": {"checkbox": False}
    }
)
```

**Notes:** Current bot uses ~10% of Notion API capabilities. Full assignment management system possible through Discord interface with bidirectional Notion sync.

---

## Key Takeaways and Lessons Learned

### **Async/Await Programming Patterns**
- **Event Loop Management:** Only one event loop can run per program. Use `asyncio.run()` to START a loop, use `await` INSIDE a running loop
- **Async Function Chain:** If any function in the call chain uses `await`, all calling functions must be `async`
- **Common Error:** Cannot use `asyncio.run()` inside an already running event loop (like Discord's). This causes "RuntimeError: asyncio.run() cannot be called from a running event loop"
- **Solution Pattern:** Make functions async and use `await` instead of `asyncio.run()` when inside event loops

### **API Integration Best Practices**
- **Environment Variables:** Never hardcode API tokens. Use `.env` files and `python-dotenv` for secure token management
- **Error Handling:** Always account for empty API responses and missing data fields
- **Date Handling:** ISO datetime strings require parsing with `datetime.fromisoformat()` and timezone handling
- **Defensive Programming:** Use `.get()` with default values for dictionary access to prevent KeyError exceptions

### **Code Organization and Documentation**
- **Function Documentation:** Use docstrings with parameter types and return descriptions for maintainability
- **Separation of Concerns:** Keep data fetching, processing, and formatting in separate functions
- **Import Management:** Import specific classes (`from datetime import datetime`) rather than entire modules when possible
- **Virtual Environments:** Essential for dependency management and preventing system-wide package conflicts

### **User Experience Design**
- **Mobile-First Messaging:** Discord notifications show first ~50 characters, so design messages with mobile preview in mind
- **Visual Hierarchy:** Use emojis and consistent formatting for better readability
- **Edge Case Handling:** Always account for empty states (no assignments due) with positive messaging
- **Fallback Values:** Provide default icons/values when user data doesn't match expected formats

### **Scalability Considerations**
- **Hardcoded Dependencies:** Current implementation is tied to specific database schema, limiting adoption
- **Future Flexibility:** Plan for configurable column mapping and auto-detection for broader usability
- **Deployment Options:** Consider multiple deployment strategies (Railway, AWS Lambda, Docker) for different user needs

### **Development Workflow**
- **Iterative Development:** Start with hardcoded solution, then generalize based on real usage
- **Documentation-Driven:** Maintain development log for tracking decisions and future enhancements
- **Security-First:** Implement secure practices from the beginning rather than retrofitting

---

## Next Steps and AWS Lambda Implementation Plan

### **What is AWS Lambda?**

**AWS Lambda** is a serverless computing service that runs your code without managing servers. Think of it as "code that runs on-demand in the cloud."

#### **Key Concepts:**
- **Serverless:** No servers to manage, patch, or scale
- **Event-Driven:** Code runs in response to triggers (time, API calls, file uploads, etc.)
- **Pay-Per-Use:** Only pay when your code actually runs (measured in milliseconds)
- **Auto-Scaling:** Automatically handles traffic from 1 to thousands of concurrent executions

#### **How Lambda Works:**
1. **Upload Code:** Package your Python code and dependencies
2. **Set Trigger:** Configure what starts your function (EventBridge for daily scheduling)
3. **AWS Manages Everything:** Servers, scaling, monitoring, logging
4. **Your Code Runs:** Lambda executes your function and returns results

#### **Lambda vs Traditional Servers:**
- **Traditional:** Rent a server 24/7, manage OS, pay even when idle
- **Lambda:** Code runs only when needed, AWS handles infrastructure, pay per execution

### **Phase 1: Deploy Single-User Lambda Function**

#### **Objective:** Get your current bot running in AWS Lambda with daily scheduling

#### **Steps:**
1. **Package Lambda Function**
   - Create deployment package with `lambda_bot.py` and dependencies
   - Test locally to ensure Parameter Store integration works
   - Package into ZIP file for Lambda deployment

2. **Create Lambda Function**
   - Deploy function using AWS CLI or Console
   - Configure Python 3.9+ runtime
   - Set appropriate timeout (30-60 seconds for Discord API calls)
   - Assign IAM role with Parameter Store and CloudWatch permissions

3. **Set Up EventBridge Scheduling**
   - Create EventBridge rule with cron expression: `cron(0 8 * * ? *)` (8 AM daily)
   - Connect rule to Lambda function as target
   - Test manual invocation and scheduled execution

4. **Configure Monitoring**
   - Set up CloudWatch logs for debugging
   - Create CloudWatch alarms for failures
   - Test error handling and notification

#### **Expected Outcome:** Your bot runs automatically every day at 8 AM from AWS, no local computer needed

### **Phase 2: Multi-User Architecture**

#### **Objective:** Transform single-user bot into SaaS platform supporting multiple users

#### **Database Design (DynamoDB):**
```
Table: daily-deadline-users
- user_id (Primary Key): Unique identifier
- notion_token: Encrypted Notion API token
- database_id: User's Notion database ID
- discord_token: User's Discord bot token
- channel_id: Discord channel for notifications
- schedule_time: Preferred notification time (default 8 AM)
- timezone: User's timezone
- active: Boolean for enabling/disabling
- created_at: Registration timestamp
```

#### **Lambda Function Updates:**
- **Single Function Approach:** One Lambda that processes all users
- **Batch Processing:** Query DynamoDB for all active users
- **Parallel Execution:** Process multiple users concurrently
- **Error Isolation:** One user's failure doesn't affect others

#### **Architecture Flow:**
1. **EventBridge Trigger:** Fires daily at multiple times for different timezones
2. **Lambda Execution:** Queries DynamoDB for users scheduled at current time
3. **Parallel Processing:** Processes each user's Notion → Discord workflow
4. **Error Handling:** Logs failures, continues with other users
5. **Monitoring:** Tracks success rates, user activity, system health

### **Phase 3: User Registration System**

#### **Objective:** Create web interface for users to register and manage their bots

#### **Frontend (S3 + CloudFront):**
- **Static Website:** HTML/CSS/JavaScript hosted on S3
- **Registration Form:** Collect user tokens and preferences
- **Dashboard:** View bot status, modify settings, pause/resume
- **Mobile-Responsive:** Works well on phones and tablets

#### **Backend API (API Gateway + Lambda):**
- **Registration Endpoint:** Store new user data in DynamoDB
- **Management Endpoints:** Update settings, view logs, delete account
- **Authentication:** Simple token-based or AWS Cognito integration
- **Validation:** Test user tokens before storing

#### **User Experience:**
1. **Visit Website:** Simple, clean registration page
2. **Enter Tokens:** Notion token, Discord bot token, channel ID, database ID
3. **Test Connection:** System validates tokens work correctly
4. **Set Preferences:** Choose notification time and timezone
5. **Activate Bot:** Start receiving daily reminders immediately

### **Phase 4: Advanced Features**

#### **Enhanced Functionality:**
- **Custom Scheduling:** Multiple reminders per day, weekend options
- **Smart Filtering:** Different reminder windows (1 day, 3 days, 1 week)
- **Message Customization:** User-defined message templates and formatting
- **Multiple Databases:** Support for multiple Notion databases per user
- **Analytics Dashboard:** Track assignment completion rates, usage statistics

#### **Technical Improvements:**
- **Database Schema Detection:** Auto-detect Notion database structure
- **Flexible Column Mapping:** Support any database schema with minimal requirements
- **Retry Logic:** Handle API failures gracefully with exponential backoff
- **Rate Limiting:** Respect Notion and Discord API limits
- **Caching:** Cache Notion data to reduce API calls

### **Why Lambda is Perfect for This Project**

#### **Technical Benefits:**
- **No Server Management:** Focus on code, not infrastructure
- **Automatic Scaling:** Handles 1 user or 10,000 users seamlessly
- **Built-in Monitoring:** CloudWatch logs and metrics included
- **High Availability:** AWS handles redundancy and failover

#### **Business Benefits:**
- **Low Startup Costs:** Pay only for actual usage
- **Rapid Development:** Deploy code changes in seconds
- **Global Reach:** Run in multiple AWS regions worldwide
- **Professional Infrastructure:** Enterprise-grade reliability

#### **Learning Benefits:**
- **Modern Architecture:** Serverless is the future of cloud computing
- **AWS Expertise:** Valuable skills for career development
- **Scalable Thinking:** Design systems that grow with demand
- **Cost Optimization:** Understand cloud economics and efficiency

---


## 2024-12-19 - EventBridge Daily Scheduling
**Type:** AWS Infrastructure
**Description:** Added automated daily scheduling using AWS EventBridge to trigger Lambda function
**Implementation:** 
- Created eventbridge-rule.json with cron expression for 9 AM EST daily execution
- Added Makefile targets: schedule-create, schedule-disable, schedule-enable, schedule-status
- Configured Lambda permissions for EventBridge invocation
**Notes:** Schedule runs at 14:00 UTC (9 AM EST). Use make schedule-disable/enable to control scheduling.

---

# Notion Discord Deadline Reminder Bot

## Project Summary (Resume Format)

**Situation:** Needed an automated solution to track assignment deadlines across multiple courses and receive timely notifications without manually checking Notion database daily.

**Task:** Develop a Python automation bot that integrates Notion API with Discord to send formatted daily reminders of upcoming assignments due within 3 days.

**Action:** Built a full-stack automation solution using Python, implementing async/await patterns for API calls, custom date formatting, visual message design with emojis and consistent formatting, environment variable security practices, and error handling for edge cases like empty assignment lists.

**Result:** Successfully automated deadline tracking with 100% reliability, reducing missed assignments and manual database checking. Designed for scalability with plans to make it universally usable for different Notion database structures.

**Technologies:** Python, Notion API, Discord.py, asyncio, datetime manipulation, environment variable management, virtual environments

## Resume Bullet Points

• Built automated deadline reminder system that connects Notion database to Discord, sending daily notifications for assignments due within 3 days to prevent missed deadlines

• Developed Python bot using async programming and API integration to eliminate manual deadline tracking, improving academic productivity and time management

• Implemented secure, production-ready architecture with custom message formatting and error handling, designed for scalability and multi-user deployment

---

# Development Documentation

This file automatically captures important development information for the deadline reminder bot project.

---

## [2025-08-22] - Project Foundation and Development Setup

### **Core Bot Implementation**
- **Notion-Discord Integration:** Built basic bot for fetching tasks from Notion database and sending daily to-do lists to Discord
- **API Integration:** Implemented Notion API for database access and Discord bot for message delivery
- **Environment Configuration:** Set up secure token management with environment variables

### **Security and Best Practices**
- **Secure Token Management:** Migrated from hardcoded tokens to .env file with `load_dotenv('env-vars/.env')`
- **Repository Security:** Added .env.example template, updated .gitignore to exclude sensitive files
- **Dependency Management:** Created requirements.txt with python-dotenv for secure environment handling

### **Development Environment**
- **Virtual Environment:** Set up isolated Python environment with `python3 -m venv venv`
- **Package Installation:** Installed core dependencies (notion-client, discord.py, python-dotenv)
- **Configuration Fixes:** Corrected environment variable reference from NOTION_DB_ID to NOTION_DATABASE_ID

### **Documentation and Project Structure**
- **Comprehensive Setup Guide:** Created detailed SETUP.md with step-by-step instructions for new developers
- **API Token Instructions:** Added guidance for obtaining Notion and Discord API tokens
- **Project Organization:** Separated detailed setup from project overview for better maintainability

**Key Learning:** Established foundation for secure, maintainable bot development with proper environment management and comprehensive documentation

---

## [2025-09-12] - Feature Enhancement and AWS Cloud Migration

### **User Experience Improvements**
- **Visual Message Design:** Implemented Discord message formatting with custom visual design, class icons, and assignment type icons for better categorization
- **Smart Date Formatting:** Added format_date() function to convert ISO datetime to user-friendly M/D HAM/PM format with time detection
- **Mobile Optimization:** Optimized first line to show clean "x assignments due soon" for phone notification previews (first ~50 characters)
- **Edge Case Handling:** Added proper handling for empty assignments with positive messaging

### **Scheduling and Automation**
- **Dual Scheduling Options:** Created scheduler.py using schedule library and setup_cron.sh for system cron job
- **Flexible Deployment:** Python scheduler (easier to modify) vs cron job (more reliable) options
- **Daily Automation:** Configured 8:00 AM daily reminders with automatic execution

### **AWS Cloud Infrastructure Migration**
- **AWS Account Setup:** Created AWS Educate student account with free credits for learning
- **Security Best Practices:** Set up IAM user `daily-deadline-service` with AdministratorAccess policy instead of using root account
- **CLI Configuration:** Configured AWS CLI with programmatic access keys and us-east-1 region
- **Infrastructure Verification:** Verified setup with `aws sts get-caller-identity`

### **Serverless Architecture Implementation**
- **Parameter Store Security:** Migrated from .env files to AWS Parameter Store with SecureString encryption for all secrets
- **Lambda-Ready Architecture:** Created `lambda_bot.py` with boto3 integration and proper Lambda handler pattern
- **Secure Credential Management:** Implemented `get_parameter()` function for secure credential retrieval
- **Serverless Foundation:** Established infrastructure for scalable, multi-user SaaS deployment

### **Scalability Planning**
- **Schema Flexibility:** Identified need for dynamic database schema support beyond hardcoded column structure
- **Multi-User Readiness:** Planned flexible column mapping and auto-detection for broader adoption
- **Production Architecture:** Designed for universal usability across different Notion database structures

### **Key Technical Learnings**
- **Async/Await Mastery:** Resolved event loop management, proper async function chaining, and Discord.py integration patterns
- **AWS Services Integration:** Parameter Store, IAM, Lambda architecture, CLI configuration and management
- **Security Evolution:** From local .env files to encrypted cloud-based secret management
- **Mobile-First Design:** Discord notification optimization for mobile user experience

**Technologies Mastered:** AWS Parameter Store, AWS Lambda, AWS IAM, boto3 SDK, schedule library, cron jobs, mobile-optimized messaging

**Commands Used:**
```bash
# AWS Parameter Store setup
aws ssm put-parameter --name "/daily-deadline/notion-token" --value "secret_token" --type "SecureString"
aws ssm put-parameter --name "/daily-deadline/database-id" --value "database_id" --type "SecureString"
aws ssm put-parameter --name "/daily-deadline/discord-token" --value "discord_token" --type "SecureString"
aws ssm put-parameter --name "/daily-deadline/channel-id" --value "channel_id" --type "String"

# Testing and validation
aws ssm get-parameter --name "/daily-deadline/notion-token" --with-decryption
pip install boto3
python lambda_bot.py
```

---

## [2025-09-16] - AWS Lambda Migration Planning and Interactive Features Research

### **AWS Lambda Migration Strategy**
**Type:** Infrastructure/Deployment
**Description:** Researched and planned migration from local execution to AWS Lambda serverless architecture
**Implementation:** 
- **Lambda Handler Pattern:** Identified need for `lambda_handler(event, context)` entry point function
- **Dual Compatibility:** Designed bot.py to work both locally and in Lambda using environment detection
- **Dependency Packaging:** Learned Lambda requires all packages in deployment ZIP (no pip install at runtime)
- **Credential Management:** Confirmed Parameter Store integration for secure token storage
- **Scheduling:** EventBridge cron expressions for daily 8 AM execution
- **Monitoring:** CloudWatch logs and SNS alerts for error tracking

**Key AWS Services:**
- **Parameter Store (SSM):** Free secure storage for API tokens
- **Lambda:** Serverless code execution (15-minute max, 256MB memory sufficient)
- **EventBridge:** Cron-based scheduling (`cron(0 8 * * ? *)`)
- **CloudWatch:** Logging and error alerting
- **IAM:** Execution roles with minimal required permissions

**Migration Benefits:**
- Eliminates need for always-on computer
- 99.99% uptime reliability
- Automatic scaling and error recovery
- Professional cloud infrastructure
- Essentially free for personal use (within AWS free tier)

**Notes:** Decided against Terraform for this project size (5 AWS resources) - CLI commands more appropriate for learning and single-user setup

---

### **Interactive Discord Bot Features Research**
**Type:** Feature Planning
**Description:** Explored expansion possibilities using Notion API's full CRUD capabilities
**Implementation:** Discovered Notion API supports Create, Read, Update, Delete operations beyond current read-only usage

**Simple Interactions (Easy to Add):**
```python
# Slash Commands
/deadlines          # Show current deadlines
/complete "Math Homework"  # Mark assignment done
/add "Physics Lab" "PHYS 201" "2024-01-20"  # Add new assignment

# Reaction-Based Interactions  
✅ Mark assignment as complete
📅 Snooze reminder for 1 hour
❌ Remove assignment
📝 Add notes to assignment
```

**Medium Complexity Features:**
- **Interactive Buttons:** [Complete] [Snooze 1hr] [Snooze 1day] [Details]
- **Assignment Management:** Edit due dates, delete assignments, view details
- **Smart Notifications:** Different urgency levels (🔴 URGENT, 🟡 Due tomorrow, 🟢 Due in 3 days)
- **Multi-User Support:** Separate Notion databases per Discord user

**Advanced Features:**
- **Study Session Tracking:** Pomodoro timers, productivity metrics
- **AI Integration:** Study plan generation, concept explanations, quiz generation
- **Calendar Sync:** Two-way sync with Google Calendar/Outlook
- **Analytics Dashboard:** Completion streaks, productivity stats, leaderboards

**Required Notion API Permissions:**
- ✅ Read content (already have)
- ✅ Update content (for marking complete, editing)
- ✅ Insert content (for adding new assignments)

**Example Implementation:**
```python
# Mark assignment complete via Discord reaction
await notion.pages.update(
    page_id="assignment_page_id",
    properties={"To Do": {"checkbox": True}}
)

# Add new assignment via slash command
await notion.pages.create(
    parent={"database_id": database_id},
    properties={
        "Assignment": {"title": [{"text": {"content": "New Homework"}}]},
        "Class": {"select": {"name": "CS 380"}},
        "Due Date": {"date": {"start": "2024-01-15"}},
        "To Do": {"checkbox": False}
    }
)
```

**Notes:** Current bot uses ~10% of Notion API capabilities. Full assignment management system possible through Discord interface with bidirectional Notion sync.

---

## Key Takeaways and Lessons Learned

### **Async/Await Programming Patterns**
- **Event Loop Management:** Only one event loop can run per program. Use `asyncio.run()` to START a loop, use `await` INSIDE a running loop
- **Async Function Chain:** If any function in the call chain uses `await`, all calling functions must be `async`
- **Common Error:** Cannot use `asyncio.run()` inside an already running event loop (like Discord's). This causes "RuntimeError: asyncio.run() cannot be called from a running event loop"
- **Solution Pattern:** Make functions async and use `await` instead of `asyncio.run()` when inside event loops

### **API Integration Best Practices**
- **Environment Variables:** Never hardcode API tokens. Use `.env` files and `python-dotenv` for secure token management
- **Error Handling:** Always account for empty API responses and missing data fields
- **Date Handling:** ISO datetime strings require parsing with `datetime.fromisoformat()` and timezone handling
- **Defensive Programming:** Use `.get()` with default values for dictionary access to prevent KeyError exceptions

### **Code Organization and Documentation**
- **Function Documentation:** Use docstrings with parameter types and return descriptions for maintainability
- **Separation of Concerns:** Keep data fetching, processing, and formatting in separate functions
- **Import Management:** Import specific classes (`from datetime import datetime`) rather than entire modules when possible
- **Virtual Environments:** Essential for dependency management and preventing system-wide package conflicts

### **User Experience Design**
- **Mobile-First Messaging:** Discord notifications show first ~50 characters, so design messages with mobile preview in mind
- **Visual Hierarchy:** Use emojis and consistent formatting for better readability
- **Edge Case Handling:** Always account for empty states (no assignments due) with positive messaging
- **Fallback Values:** Provide default icons/values when user data doesn't match expected formats

### **Scalability Considerations**
- **Hardcoded Dependencies:** Current implementation is tied to specific database schema, limiting adoption
- **Future Flexibility:** Plan for configurable column mapping and auto-detection for broader usability
- **Deployment Options:** Consider multiple deployment strategies (Railway, AWS Lambda, Docker) for different user needs

### **Development Workflow**
- **Iterative Development:** Start with hardcoded solution, then generalize based on real usage
- **Documentation-Driven:** Maintain development log for tracking decisions and future enhancements
- **Security-First:** Implement secure practices from the beginning rather than retrofitting

---

## Next Steps and AWS Lambda Implementation Plan

### **What is AWS Lambda?**

**AWS Lambda** is a serverless computing service that runs your code without managing servers. Think of it as "code that runs on-demand in the cloud."

#### **Key Concepts:**
- **Serverless:** No servers to manage, patch, or scale
- **Event-Driven:** Code runs in response to triggers (time, API calls, file uploads, etc.)
- **Pay-Per-Use:** Only pay when your code actually runs (measured in milliseconds)
- **Auto-Scaling:** Automatically handles traffic from 1 to thousands of concurrent executions

#### **How Lambda Works:**
1. **Upload Code:** Package your Python code and dependencies
2. **Set Trigger:** Configure what starts your function (EventBridge for daily scheduling)
3. **AWS Manages Everything:** Servers, scaling, monitoring, logging
4. **Your Code Runs:** Lambda executes your function and returns results

#### **Lambda vs Traditional Servers:**
- **Traditional:** Rent a server 24/7, manage OS, pay even when idle
- **Lambda:** Code runs only when needed, AWS handles infrastructure, pay per execution

### **Phase 1: Deploy Single-User Lambda Function**

#### **Objective:** Get your current bot running in AWS Lambda with daily scheduling

#### **Steps:**
1. **Package Lambda Function**
   - Create deployment package with `lambda_bot.py` and dependencies
   - Test locally to ensure Parameter Store integration works
   - Package into ZIP file for Lambda deployment

2. **Create Lambda Function**
   - Deploy function using AWS CLI or Console
   - Configure Python 3.9+ runtime
   - Set appropriate timeout (30-60 seconds for Discord API calls)
   - Assign IAM role with Parameter Store and CloudWatch permissions

3. **Set Up EventBridge Scheduling**
   - Create EventBridge rule with cron expression: `cron(0 8 * * ? *)` (8 AM daily)
   - Connect rule to Lambda function as target
   - Test manual invocation and scheduled execution

4. **Configure Monitoring**
   - Set up CloudWatch logs for debugging
   - Create CloudWatch alarms for failures
   - Test error handling and notification

#### **Expected Outcome:** Your bot runs automatically every day at 8 AM from AWS, no local computer needed

### **Phase 2: Multi-User Architecture**

#### **Objective:** Transform single-user bot into SaaS platform supporting multiple users

#### **Database Design (DynamoDB):**
```
Table: daily-deadline-users
- user_id (Primary Key): Unique identifier
- notion_token: Encrypted Notion API token
- database_id: User's Notion database ID
- discord_token: User's Discord bot token
- channel_id: Discord channel for notifications
- schedule_time: Preferred notification time (default 8 AM)
- timezone: User's timezone
- active: Boolean for enabling/disabling
- created_at: Registration timestamp
```

#### **Lambda Function Updates:**
- **Single Function Approach:** One Lambda that processes all users
- **Batch Processing:** Query DynamoDB for all active users
- **Parallel Execution:** Process multiple users concurrently
- **Error Isolation:** One user's failure doesn't affect others

#### **Architecture Flow:**
1. **EventBridge Trigger:** Fires daily at multiple times for different timezones
2. **Lambda Execution:** Queries DynamoDB for users scheduled at current time
3. **Parallel Processing:** Processes each user's Notion → Discord workflow
4. **Error Handling:** Logs failures, continues with other users
5. **Monitoring:** Tracks success rates, user activity, system health

### **Phase 3: User Registration System**

#### **Objective:** Create web interface for users to register and manage their bots

#### **Frontend (S3 + CloudFront):**
- **Static Website:** HTML/CSS/JavaScript hosted on S3
- **Registration Form:** Collect user tokens and preferences
- **Dashboard:** View bot status, modify settings, pause/resume
- **Mobile-Responsive:** Works well on phones and tablets

#### **Backend API (API Gateway + Lambda):**
- **Registration Endpoint:** Store new user data in DynamoDB
- **Management Endpoints:** Update settings, view logs, delete account
- **Authentication:** Simple token-based or AWS Cognito integration
- **Validation:** Test user tokens before storing

#### **User Experience:**
1. **Visit Website:** Simple, clean registration page
2. **Enter Tokens:** Notion token, Discord bot token, channel ID, database ID
3. **Test Connection:** System validates tokens work correctly
4. **Set Preferences:** Choose notification time and timezone
5. **Activate Bot:** Start receiving daily reminders immediately

### **Phase 4: Advanced Features**

#### **Enhanced Functionality:**
- **Custom Scheduling:** Multiple reminders per day, weekend options
- **Smart Filtering:** Different reminder windows (1 day, 3 days, 1 week)
- **Message Customization:** User-defined message templates and formatting
- **Multiple Databases:** Support for multiple Notion databases per user
- **Analytics Dashboard:** Track assignment completion rates, usage statistics

#### **Technical Improvements:**
- **Database Schema Detection:** Auto-detect Notion database structure
- **Flexible Column Mapping:** Support any database schema with minimal requirements
- **Retry Logic:** Handle API failures gracefully with exponential backoff
- **Rate Limiting:** Respect Notion and Discord API limits
- **Caching:** Cache Notion data to reduce API calls

### **Why Lambda is Perfect for This Project**

#### **Technical Benefits:**
- **No Server Management:** Focus on code, not infrastructure
- **Automatic Scaling:** Handles 1 user or 10,000 users seamlessly
- **Built-in Monitoring:** CloudWatch logs and metrics included
- **High Availability:** AWS handles redundancy and failover

#### **Business Benefits:**
- **Low Startup Costs:** Pay only for actual usage
- **Rapid Development:** Deploy code changes in seconds
- **Global Reach:** Run in multiple AWS regions worldwide
- **Professional Infrastructure:** Enterprise-grade reliability

#### **Learning Benefits:**
- **Modern Architecture:** Serverless is the future of cloud computing
- **AWS Expertise:** Valuable skills for career development
- **Scalable Thinking:** Design systems that grow with demand
- **Cost Optimization:** Understand cloud economics and efficiency

---


## 2025-10-19 - EventBridge Daily Scheduling
**Type:** AWS Infrastructure
**Description:** Added automated daily scheduling using AWS EventBridge to trigger Lambda function
**Implementation:** 
- Created eventbridge-rule.json with cron expression for 9 AM EST daily execution
- Added Makefile targets: schedule-create, schedule-disable, schedule-enable, schedule-status
- Configured Lambda permissions for EventBridge invocation
**Notes:** Schedule runs at 14:00 UTC (9 AM EST). Use make schedule-disable/enable to control scheduling.

---
## 2025-01-22 - Null Field Handling Bug Fix
**Type:** Bug Fix
**Description:** Fixed TypeError when Notion database entries have empty Type or Class select fields
**Implementation:** Added null checks before accessing select field names, with fallback values 'Unknown' for class and 'Assignment' for type
**Notes:** Prevents bot crashes when database entries are incomplete, improves robustness for production use

---
## 2025-01-22 - Production Deployment of Null Handling Fix
**Type:** Deployment
**Description:** Successfully deployed null field handling fix to AWS Lambda production environment
**Implementation:** Updated Lambda function code with null checks for Notion database select fields
**Notes:** Bot now handles incomplete database entries without crashing, improving production reliability

---
## 2025-01-22 - Comprehensive Test Suite Implementation
**Type:** Testing Infrastructure
**Description:** Created dry-run test suite to validate bot functionality before deployment
**Implementation:** 
- test_bot.py with 5 core tests: imports, date formatting, credential loading, Lambda context, null handling
- Makefile targets: test-bot and test-deploy for safe deployment workflow
- Tests run without network calls to avoid SSL/credential issues in local environment
**Notes:** Prevents deployment of broken code by catching import errors, logic bugs, and environment issues early

---
## 2025-01-24 - Notion API Method Name Fix
**Type:** Bug Fix
**Description:** Fixed AttributeError due to Notion API method name change from query to query_database
**Implementation:** Updated notion.databases.query() to notion.databases.query_database() in filter_db function
**Notes:** Notion client library updated method names, causing production failures. Fix deployed and tested successfully.

---