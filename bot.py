
import boto3, discord, json, logging, os, traceback
from datetime import datetime, date, timedelta, timezone
from dotenv import load_dotenv
from notion_client import AsyncClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
discord_client = discord.Client(intents=intents)

class_icons = {
    "CS 380": "💻",
    "STAT 201": "💼",
    "INFO 103": "📊",
    "INFO 310": "➕",
    "INFO 212": "🎨",
    "MUSC 191": "🎸"
}

assignment_type_icons = {
    "Homework": "📝",
    "Reflection": "🪞",
    "Lab": "🔬",
    "Reading": "📖",
    "Quiz": "❓",
    "Exam": "💯",
    "Extra Credit": "💯",
    "Project": "📐"
}

def load_credentials():
    try:
        if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
            # Running in AWS Lambda
            ssm = boto3.client('ssm')
            
            return {
                "notion_token": ssm.get_parameter(Name='/daily-deadline/notion-token', WithDecryption=True)['Parameter']['Value'],
                "database_id": ssm.get_parameter(Name='/daily-deadline/notion-database-id', WithDecryption=True)['Parameter']['Value'],
                "discord_token": ssm.get_parameter(Name='/daily-deadline/discord-token', WithDecryption=True)['Parameter']['Value'],
                "discord_channel_id": ssm.get_parameter(Name='/daily-deadline/discord-channel-id', WithDecryption=True)['Parameter']['Value']
            }
        else:
            load_dotenv('.env')  
            return {
                "notion_token": os.environ["NOTION_TOKEN"],
                "database_id": os.environ["NOTION_DATABASE_ID"], 
                "discord_token": os.environ["DISCORD_TOKEN"],
                "discord_channel_id": os.environ["DISCORD_CHANNEL_ID"]
            }
    except Exception as e:
        logger.error("Failed to load credentials")
        raise RuntimeError("Configuration error: Unable to load required credentials") from e

# Global setup
creds = load_credentials()
notion = AsyncClient(auth=creds['notion_token'])
database_id = creds['database_id']

# for future use?
# async def db_setup() -> dict:
#     '''
#     Retrieves the database schema properties from Notion
#     Returns: dict - Database properties structure
#     '''
#     database = await notion.databases.retrieve(database_id)
#     return database["properties"]

def format_date(date_str: str) -> str:
    '''
    Converts ISO datetime string to M/D format, with time if specified
    Parameters: date_str (str) - ISO format datetime string
    Returns: str - Formatted date like "9/13" or "9/13 11:59PM"
    '''
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute

    # If time is 00:00, it's likely a date-only entry
    if hour == 0 and minute == 0:
        return f"{month}/{day}"
    
    # Format time if it's not midnight
    if hour == 0:
        formatted_time = f"12:{minute:02d}AM"
    elif hour < 12:
        formatted_time = f"{hour}:{minute:02d}AM"
    elif hour == 12:
        formatted_time = f"12:{minute:02d}PM"
    else:
        formatted_time = f"{hour - 12}:{minute:02d}PM"
    
    return f"{month}/{day} {formatted_time}"

def get_three_days_out() -> date:
    '''
    Calculates the date 3 days from today
    Returns: date - Date object 3 days in the future
    '''
    today = date.today()
    three_days_out = today + timedelta(days=3)
    return three_days_out

async def filter_db() -> dict:
    '''
    Queries Notion database for uncompleted assignments due within 3 days
    Returns: dict - Notion API response with filtered assignments
    '''
    three_days_out = get_three_days_out().isoformat()
    
    assignment_info = await notion.databases.query(
        database_id=database_id,
        filter={
            "and": [
                {
                    "property": "To Do",
                    "checkbox": {
                        "equals": False
                    }
                },
                {
                    "property": "Due Date",
                    "date": {
                        "is_not_empty": True
                    }
                },
                {
                    "property": "Due Date",
                    "date": {
                        "on_or_before": three_days_out
                    }
                }
            ]
        }
    )
    return assignment_info

async def extract_assignment_info() -> list:
    '''
    Extracts and structures assignment data from Notion API response
    Returns: list - List of dictionaries containing assignment details
    '''
    assignment_info = await filter_db()
    all_assignments = []
    results = assignment_info["results"]
    for entry in results:
        assignment_name = entry['properties']['Assignment']['title'][0]['plain_text']
        
        class_select = entry['properties']['Class']['select']
        if not class_select:
            logger.warning(f"Entry '{assignment_name}' has empty Class field")
        assignment_class = class_select['name'] if class_select else 'Unknown'
        
        type_select = entry['properties']['Type']['select']
        if not type_select:
            logger.warning(f"Entry '{assignment_name}' has empty Type field")
        assignment_type = type_select['name'] if type_select else 'Assignment'
        
        assignment_due_date = entry['properties']['Due Date']['date']['start']
        notes_list = entry['properties']['Notes']['rich_text']
        
        # check if notes_list is empty
        if not notes_list:  
            assignment_notes = "No notes"
        else:
            assignment_notes = notes_list[0]['plain_text']

        # store all assignment information in a dictionary
        entry_info = {
            "name": assignment_name,
            "class": assignment_class,
            "type": assignment_type,
            "due_date": assignment_due_date,
            "notes": assignment_notes
        }

        # add each entry to a list of all assignments
        all_assignments.append(entry_info)
    logger.info(f"Successfully retrieved {len(all_assignments)} assignments from Notion")
    return all_assignments

async def format_message() -> str:
    '''
    Creates formatted Discord message with assignment details
    Returns: str - Formatted message ready for Discord
    '''
    assignments = await extract_assignment_info()

    # account for when there are no assignments due soon
    if len(assignments) == 0:
        return "**No assignments due soon! **🎉"
    else:
        message = f"🚨 **{len(assignments)} ASSIGNMENTS DUE SOON!**\n\n"
        message += "─────────────────────────\n"
        message += "📚 **Upcoming Assignments**\n"
        message += "─────────────────────────\n\n"

        for assignment in assignments:
            icon = class_icons.get(assignment['class'], "📚")
            class_name = assignment['class']
            assignment_name = assignment['name']
            assignment_type_icon = assignment_type_icons.get(assignment['type'], "📋")
            assignment_type_name = assignment['type']
            assignment_due_date = assignment['due_date']
            message += f"{icon} **{class_name}: {assignment_name}**\n"
            message += f"      {assignment_type_icon} {assignment_type_name}\n"
            message += f"      📅 {format_date(assignment_due_date)}\n"

            if assignment['notes'] != "No notes":
                message += f"      📋 {assignment['notes']}\n"
        
            message += "\n" 
        message += "\n\n"
        return message

def send_message():
    '''
    Sends the formatted assignment message to Discord channel
    Uses global credentials loaded from Parameter Store or .env file
    '''
    discord_token = creds['discord_token']
    channel_id = int(creds['discord_channel_id'])

    client = discord.Client(intents=discord.Intents.default())
    
    @client.event
    async def on_ready():
        try:
            logger.info(f"Discord client connected successfully")
            channel = client.get_channel(channel_id)
            
            if not channel:
                raise ValueError(f"Discord channel {channel_id} not found or bot lacks access")
            
            message = await format_message()
            await channel.send(message)
            
            logger.info(f"Message sent successfully to Discord channel {channel_id}")
            await client.close()
            
        except Exception as e:
            logger.error(f"Discord send failed: {str(e)}")
            await client.close()
            raise
    
    client.run(discord_token)

def lambda_handler(event, context):
    '''
    AWS Lambda entry point
    Parameters:
        event: EventBridge trigger data (empty dict for scheduled events)
        context: Lambda runtime information
    Returns:
        dict: Status response for Lambda
    '''
    # Structured logging for CloudWatch
    log_context = {
        "function_name": context.function_name,
        "request_id": context.aws_request_id,
        "remaining_time_ms": context.get_remaining_time_in_millis()
    }
    
    logger.info(json.dumps({
        "event": "lambda_start",
        "status": "INFO",
        "message": "Deadline reminder bot execution started",
        **log_context
    }))
    
    try:
        logger.info(json.dumps({
            "event": "bot_execution",
            "status": "INFO", 
            "message": "Starting Discord message send process",
            **log_context
        }))
        
        send_message()
        
        logger.info(json.dumps({
            "event": "lambda_success",
            "status": "SUCCESS",
            "message": "Deadline reminder sent successfully to Discord",
            **log_context
        }))
        
        return {
            "statusCode": 200,
            "status": "success",
            "message": "Deadline reminder sent successfully",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        error_details = {
            "event": "lambda_error",
            "status": "ERROR",
            "message": f"Lambda execution failed: {str(e)}",
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc(),
            **log_context
        }
        
        logger.error(json.dumps(error_details))
        
        return {
            "statusCode": 500,
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

if __name__ == "__main__":
    send_message()
    