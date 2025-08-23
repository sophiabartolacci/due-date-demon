from notion_client import AsyncClient
import os, datetime, discord, asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

notion = AsyncClient(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DATABASE_ID"]

# Date

def is_date_in_range(date: datetime.date) -> bool:
    today = datetime.date.today()
    three_days_out = today + datetime.timedelta(days=3)
    return today <= date <= three_days_out

async def get_assignments_due_within_three_days(): 


async def test_get_db_info():
    
    database = await notion.databases.retrieve(database_id)
    properties = database["properties"]
    print(properties)



if __name__ == "__main__":
    asyncio.run(test_get_db_info())