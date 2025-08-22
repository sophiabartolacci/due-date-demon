from notion_client import AsyncClient
import os, datetime, discord, dotenv

notion = AsyncClient(auth=os.environ[""])
