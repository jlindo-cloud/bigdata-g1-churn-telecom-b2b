from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from database import logs_collection
from security import get_current_user
from services.audit_service import save_log

router = APIRouter(
    prefix="/logs",
    tags=["Logs"]
)


@router.get("")
@router.get("/")
def get_logs(
    request: Request,
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = Query(default=None, min_length=1),
    current_user=Depends(get_current_user)
):
    if page < 1:
        page = 1

    if page_size < 1:
        page_size = 20

    if page_size > 100:
        page_size = 100

    query = {}
    if search:
        query["$or"] = [
            {"username": {"$regex": search, "$options": "i"}},
            {"action": {"$regex": search, "$options": "i"}},
            {"endpoint": {"$regex": search, "$options": "i"}}
        ]

    try:
        cursor = logs_collection.find(query, {"_id": 0})
        items = list(cursor)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="No se pudieron consultar los logs") from exc

    items.sort(
        key=lambda item: item.get("timestamp") or item.get("date") or item.get("created_at"),
        reverse=True
    )

    skip = (page - 1) * page_size
    paged_items = items[skip:skip + page_size]

    save_log(
        username=current_user["username"],
        endpoint="/logs",
        method="GET",
        action="Consulta logs",
        ip=request.client.host if request.client else None,
        role=current_user.get("role")
    )

    return paged_items
