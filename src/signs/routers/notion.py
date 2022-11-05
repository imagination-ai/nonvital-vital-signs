from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
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


class KnowledgePoolResultModel(BaseModel):
    content: str
    url: str
    title: str

    @classmethod
    def from_result(cls, result):
        url = _get_url_from_knowledge_pool_result(result)
        content = _get_content_from_knowledge_pool_result(result)
        title = _get_title_from_knowledge_pool_result(result)
        return cls(content=content, title=title, url=url)


def _get_url_from_knowledge_pool_result(result):
    url = ""
    urls = result["properties"]["url"]["rollup"]["array"]
    if len(urls) > 0:
        url = urls[0]["url"]

    return url


def _get_content_from_knowledge_pool_result(result):
    return result["properties"]["Name"]["title"][0]["text"]["content"]


def _get_title_from_knowledge_pool_result(result):
    return result["properties"]["interest-title"]["formula"]["string"]


def get_knowledge_pool_highlights(limit):
    url = f"{NOTION_API_BASE_URL}/databases/44f8dcff8df647e8af66847e104e073b/query"
    response = s.post(url, headers=DEFAULT_HEADERS).json()

    if "results" in response:
        results = response["results"]
        return [
            KnowledgePoolResultModel.from_result(result)
            for result in results[:limit]
        ]


class NotionResponse(BaseModel):
    status: int
    success: bool


class KnowledgePoolResponseModel(NotionResponse):
    data: dict


@router.get("/last_highlights", response_model=KnowledgePoolResponseModel)
async def parse_knowledge_pool(limit: int = 5):
    highlights = get_knowledge_pool_highlights(limit)
    data = {"highlights": highlights}
    return KnowledgePoolResponseModel(status=200, success=True, data=data)


@router.get(
    "/last_events",
)
async def parse_events(limit: int = 5):
    url = f"{NOTION_API_BASE_URL}/databases/5d34842a3d1d4ff9962c8559bdf9bd12/query"
    response = s.post(url, headers=DEFAULT_HEADERS).json()
    return parse_events_items(response["results"])
