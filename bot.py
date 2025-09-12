from notion_client import AsyncClient
from datetime import datetime, date, timedelta 
import os, discord, asyncio
from dotenv import load_dotenv

'''
    command to run the bot.py file: source venv/bin/activate && python bot.py
'''

# Setup
load_dotenv('.env')
notion = AsyncClient(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DATABASE_ID"]

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

async def db_setup() -> dict:
    '''
    Retrieves the database schema properties from Notion
    Returns: dict - Database properties structure
    '''
    database = await notion.databases.retrieve(database_id)
    return database["properties"]

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
        assignment_class = entry['properties']['Class']['select']['name']
        assignment_type = entry['properties']['Type']['select']['name']
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
    print(all_assignments)
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
    Uses environment variables for Discord token and channel ID
    '''
    token = os.environ["DISCORD_TOKEN"]
    channel_id = int(os.environ["DISCORD_CHANNEL_ID"])
    
    client = discord.Client(intents=discord.Intents.default())
    
    @client.event
    async def on_ready():
        channel = client.get_channel(channel_id)
        await channel.send(await format_message())
        await client.close()
    
    client.run(token)

if __name__ == "__main__":
    send_message()
    