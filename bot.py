from notion_client import AsyncClient
import os, datetime, discord, asyncio
from dotenv import load_dotenv

'''
    command to run the bot.py file: source venv/bin/activate && python bot.py
'''

# Load environment variables
load_dotenv('.env')
notion = AsyncClient(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DATABASE_ID"]

async def db_setup() -> dict:
    database = await notion.databases.retrieve(database_id)
    return database["properties"]

def get_three_days_out() -> datetime:
    today = datetime.date.today()
    three_days_out = today + datetime.timedelta(days=3)
    return three_days_out

async def get_assignments_due_date() -> None:
    '''
        This function retrieves all assignments that are not done and returns the assignments' due date
    '''
    three_days_out = get_three_days_out().isoformat()
    
    assignments = await notion.databases.query(
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
    results = assignments["results"]
    for assignment in results:
        assignment_name = assignment['properties']['Assignment']['title'][0]['plain_text']
        assignment_class = assignment['properties']['Class']['select']['name']
        assignment_type = assignment['properties']['Type']['select']['name']
        assignment_due_date = assignment['properties']['Due Date']['date']['start']
        
        print(f"Assignment: {assignment_name}")
        print(f"Class: {assignment_class}")
        print(f"Type: {assignment_type}")
        print(f"Due Date: {assignment_due_date}")
        print("-" * 30)

async def test_get_db_info() -> None:
    properties = await db_setup()
    print(properties)

if __name__ == "__main__":
    asyncio.run(get_assignments_due_date())