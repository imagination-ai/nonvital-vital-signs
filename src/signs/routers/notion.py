from fastapi import APIRouter
from requests import Session

from signs.config import app_settings

router = APIRouter(
    prefix="/notion",
    tags=["Notion API"],
)

s = Session()

DEFAULT_HEADERS = {
    "Authorization": f"Bearer {app_settings.NOTION_SECRET_OB}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}
NOTION_API_BASE_URL = "https://api.notion.com/v1"


def parse_events_items(results):
    items = results[0]["properties"].items()
    print(items)
    return items


def get_knowledge_pool_highlights(limit):
    url = f"{NOTION_API_BASE_URL}/databases/44f8dcff8df647e8af66847e104e073b/query"
    response = s.post(url, headers=DEFAULT_HEADERS).json()
    if "results" in response:
        results = response["results"]
        return [
            result["properties"]["Name"]["title"][0]["text"]["content"]
            for result in results[:limit]
        ]


@router.get(
    "/last_highlights",
    tags=["Knowledge Pool Parsing"],
    # TODO: Return Type - responses={}
)
async def parse_knowledge_pool(limit: int = 5):
    highlights = get_knowledge_pool_highlights(limit)
    return {"status": 200, "data": {"highlights": highlights}, "success": True}


@router.get(
    "/last_events",
    tags=["Get Last Events from Notion"],
)
async def parse_events(limit: int = 5):
    url = f"{NOTION_API_BASE_URL}/databases/5d34842a3d1d4ff9962c8559bdf9bd12/query"
    response = s.post(url, headers=DEFAULT_HEADERS).json()
    return parse_events_items(response["results"])
