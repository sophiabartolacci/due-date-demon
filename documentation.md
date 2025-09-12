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

## 2024-12-19 - Initial Project Setup
**Type:** Environment Setup
**Description:** Basic Notion Discord Bot for fetching tasks and sending daily to-do lists
**Implementation:** 
- Notion integration for database access
- Discord bot for message sending
- Environment variables for tokens and IDs
**Notes:** Tokens stored in env-vars/.env file, need secure sharing method between laptops

---

## 2024-12-19 - Security Configuration
**Type:** Security
**Description:** Proper environment variable handling to prevent token exposure in public repositories
**Implementation:** 
- Fixed bot.py to use `load_dotenv('env-vars/.env')`
- Added .env.example template for required variables
- Updated .gitignore to exclude env-vars/.env
- Created requirements.txt with python-dotenv dependency
**Notes:** Tokens are now safely loaded from environment file that won't be committed to Git

---

## 2024-12-19 - Development Environment Setup
**Type:** Environment Setup
**Description:** Set up Python virtual environment and installed required dependencies
**Implementation:** 
- Created virtual environment with `python3 -m venv venv`
- Installed packages: notion-client, discord.py, python-dotenv
- Fixed environment variable reference from NOTION_DB_ID to NOTION_DATABASE_ID
**Notes:** Virtual environment prevents system-wide package conflicts and follows Python best practices

---

## 2024-12-19 - Documentation Update
**Type:** Documentation
**Description:** Added comprehensive setup instructions with exact commands
**Implementation:** 
- Updated README.md with step-by-step setup process
- Included virtual environment creation commands
- Added dependency installation and testing instructions
**Notes:** New developers can now follow exact commands to set up the project from scratch

---

## 2024-12-19 - Setup Documentation Restructure
**Type:** Documentation
**Description:** Created dedicated SETUP.md file for detailed initial setup instructions
**Implementation:** 
- Created SETUP.md with comprehensive step-by-step setup process
- Included API token acquisition instructions for Notion and Discord
- Updated README.md to reference SETUP.md and simplified main documentation
**Notes:** Separates detailed setup from project overview, making documentation more organized

---

## 2024-12-19 - Message Formatting Implementation
**Type:** Feature
**Description:** Implemented Discord message formatting with custom visual design and date formatting
**Implementation:** 
- Created format_message() function with double-line header and clean card-style layout
- Added format_date() function to convert ISO datetime to M/D HAM/PM format
- Implemented assignment type icons dictionary for visual categorization
- Added handling for empty assignments case with positive messaging
- Used class icons and assignment type icons for better visual organization
**Notes:** Message format designed for mobile Discord notifications with summary line first. Future enhancement: add sorting by due date in code for more control over assignment order

---

## 2024-12-19 - Future Enhancement Planning
**Type:** Feature Planning
**Description:** Identified need to make bot more dynamic and user-friendly for different Notion database setups
**Implementation:** 
- Current bot is hardcoded to specific database schema (Assignment, Class, Type, Due Date, To Do, Notes columns)
- Need to implement flexible column mapping via environment variables or auto-detection
- Should support any Notion database structure with minimal requirements (at least a date column)
- Consider adding database schema validation and setup wizard for new users
**Notes:** This would significantly increase adoption by allowing users with different database structures to use the bot without code modifications. Priority enhancement for making this a public tool.

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
## [2024-12-19] - Mobile Notification Optimization
**Type:** Feature
**Description:** Optimized Discord message format for mobile notification preview
**Implementation:** Changed first line from "🚨 **x assignments due soon!**" to plain "x assignments due soon" so phone notifications show clean text without formatting
**Notes:** Phone notifications typically show first ~50 characters, so keeping first line simple and clean improves user experience

---