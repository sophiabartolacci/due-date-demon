# Automated Deadline Reminder Bot

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)
[![Discord](https://img.shields.io/badge/Discord-API-7289da.svg)](https://discord.com/developers/docs)
[![Notion](https://img.shields.io/badge/Notion-API-000000.svg)](https://developers.notion.com/)
[![Amazon Q](https://img.shields.io/badge/Amazon_Q-Developer-FF9900.svg)](https://aws.amazon.com/q/)

## 🌟 Overview

A serverless bot that automatically checks my Notion database for upcoming deadlines and sends Discord reminders every day at 8 AM. It uses AWS Lambda for serverless execution, Parameter Store for secure credential management, and Amazon Q Developer helped catch security vulnerabilities and document the development process. The system runs for less than $1/month and could easily be expanded to support multiple users with a web interface.

## 🤔 Why I Built This

I wanted to keep track of upcoming deadlines while learning more about AWS after working with it during my co-op. I was inspired by how Slack gives daily meeting schedules, which I found really useful and gave me a lookahead of what my day would look like. What started as a simple automation project turned into a production-ready system with proper security, monitoring, and CI/CD.

## ✨ Features

**Automated Scheduling:** Runs daily at 8 AM using AWS EventBridge triggers with zero manual intervention.
**Smart Filtering:** Only shows assignments due within 3 days, filtering out completed tasks automatically.
**Rich Notifications:** Sends formatted Discord messages with class icons, assignment types, due dates, and notes.
**Dual Environment Support:** Works seamlessly in both local development and AWS cloud environments.
**Secure Credential Management:** Uses AWS Parameter Store for secure token storage with automatic environment detection.
**Structured Logging:** JSON-formatted CloudWatch logs with clear status indicators for monitoring and alerting.
**AI-Assisted Development:** Integrated Amazon Q Developer for code review, security analysis, and documentation.
**Production Ready:** Configured for serverless deployment with proper error handling and fault tolerance.
**Performance Optimized:** Async/await implementation for non-blocking API operations and efficient resource usage.
**CWE-532 Compliant:** No sensitive data exposure in logs with least-privilege IAM permissions.



## 🛠️ Technology Stack

```python
# Core Technologies
Python 3.9+          # Primary language with async/await
AWS Lambda           # Serverless compute platform
Notion API           # Database integration
Discord.py           # Bot framework
Boto3               # AWS SDK

# Development Tools
Amazon Q Developer   # AI code assistant
Makefile            # Build automation
CloudWatch          # Monitoring & logging
Parameter Store     # Secret management
EventBridge         # Scheduling service
```

## 📊 Sample Output

```
🚨 **2 ASSIGNMENTS DUE SOON!**

─────────────────────────
📚 **Upcoming Assignments**
─────────────────────────

💻 **CS 380: Database Project**
      📐 Project
      📅 12/22 11:59PM
      📋 Final implementation due

📊 **INFO 103: Research Paper**
      📝 Homework
      📅 12/20
```

## 🔧 Quick Start

### Local Development
```bash
# Setup environment
make setup

# Run locally
make run
```

### AWS Deployment
```bash
# Deploy to Lambda
make deploy

# Enable daily scheduling
make schedule-create
```

## 📚 Documentation

- [AWS Setup Guide](md_notes_files/AWS_SETUP.md) - Complete deployment instructions
- [Development Log](md_notes_files/documentation.md) - AI-assisted project evolution tracking

---

## 🎯 What I Learned

**Building this taught me:**
- **☁️ Serverless Architecture**: How to design and deploy AWS Lambda functions with proper monitoring
- **🔒 Security Best Practices**: Finding and fixing vulnerabilities, managing secrets securely
- **🤖 AI-Assisted Development**: Using Amazon Q Developer for code review and security analysis
- **📊 Production Systems**: Structured logging, error handling, and observability patterns
- **🚀 Automation**: CI/CD pipelines, infrastructure as code, and deployment automation
- **📚 Technical Communication**: Writing clear documentation and maintaining development logs

**Technologies explored:** AWS Lambda, EventBridge, Parameter Store, CloudWatch, Notion API, Discord API, Python async/await

---

## 🚀 Next Steps: Making It Scalable

- **Multi-User Support**: Expand to handle multiple users so that anyone can use it
- **Web Interface**: Build a simple React/Next.js frontend for user registration and management
- **OAuth Integration**: Let users connect Notion/Discord without copying tokens
- **Auto-Detection**: Smart database schema detection to work with any Notion setup
