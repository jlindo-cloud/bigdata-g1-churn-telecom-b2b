from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from database import predictions_collection
from security import get_current_user
from services.audit_service import save_log


router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


# ====================================  =================
# Estadísticas generales
# GET /companies/stats
# =====================================================
@router.get("/stats")
def company_stats():

    total = predictions_collection.count_documents({})

    active = predictions_collection.count_documents(
        {"prediction": 0}
    )

    churn = predictions_collection.count_documents(
        {"prediction": 1}
    )

    high = predictions_collection.count_documents(
        {"risk_score": {"$gte": 0.80}}
    )

    medium = predictions_collection.count_documents(
        {
            "risk_score": {
                "$gte": 0.30,
                "$lt": 0.80
            }
        }
    )

    low = predictions_collection.count_documents(
        {"risk_score": {"$lt": 0.30}}
    )

    return {
        "total_companies": total,
        "active_companies": active,
        "predicted_churn": churn,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low
    }


def _risk_level(risk_score: Optional[float]) -> str:
    if risk_score is None:
        return "Bajo"
    if risk_score >= 0.80:
        return "Crítico"
    if risk_score >= 0.60:
        return "Alto"
    if risk_score >= 0.30:
        return "Medio"
    return "Bajo"


def _serialize_company(document: dict) -> dict:
    document = dict(document)
    if "_id" in document:
        document["_id"] = str(document["_id"])
    document["risk_level"] = _risk_level(document.get("risk_score"))
    return document


# =====================================================
# Top 20 empresas con mayor riesgo
# GET /companies/top-risk
# =====================================================
@router.get("/top-risk")
def top_risk():

    companies = []

    cursor = (
        predictions_collection.find({}, {"_id": 0})
        .sort("risk_score", -1)
        .limit(20)
    )

    for company in cursor:
        companies.append(company)

    return companies


# =====================================================
# Empresas de alto riesgo
# GET /companies/high-risk
# =====================================================
@router.get("/high-risk")
def high_risk():

    companies = []

    cursor = predictions_collection.find(
        {
            "risk_score": {
                "$gte": 0.80
            }
        },
        {"_id": 0}
    )

    for company in cursor:
        companies.append(company)

    return companies


# =====================================================
# Empresas de bajo riesgo
# GET /companies/low-risk
# =====================================================
@router.get("/low-risk")
def low_risk():

    companies = []

    cursor = predictions_collection.find(
        {
            "risk_score": {
                "$lt": 0.30
            }
        },
        {"_id": 0}
    )

    for company in cursor:
        companies.append(company)

    return companies


# =====================================================
# Buscar por nombre
# GET /companies/search?name=express
# =====================================================
@router.get("/search")
def search_company(
    name: str = Query(..., min_length=2)
):

    companies = []

    cursor = predictions_collection.find(
        {
            "razon_social": {
                "$regex": name,
                "$options": "i"
            }
        },
        {"_id": 0}
    )

    for company in cursor:
        companies.append(company)

    return companies


# =====================================================
# Empresas por sector
# GET /companies/sector/Transporte
# =====================================================
@router.get("/sector/{sector}")
def companies_by_sector(sector: str):

    companies = []

    cursor = predictions_collection.find(
        {
            "sector": sector
        },
        {"_id": 0}
    )

    for company in cursor:
        companies.append(company)

    return companies


# =====================================================
# Empresas por región
# GET /companies/region/Lima
# =====================================================
@router.get("/region/{region}")
def companies_by_region(region: str):

    companies = []

    cursor = predictions_collection.find(
        {
            "region": region
        },
        {"_id": 0}
    )

    for company in cursor:
        companies.append(company)

    return companies


# =====================================================
# Empresas por segmento
# GET /companies/segment/Enterprise
# =====================================================
@router.get("/segment/{segment}")
def companies_by_segment(segment: str):

    companies = []

    cursor = predictions_collection.find(
        {
            "segmento": segment
        },
        {"_id": 0}
    )

    for company in cursor:
        companies.append(company)

    return companies


# =====================================================
# Empresas por ejecutivo
# GET /companies/executive/Ejecutivo_4
# =====================================================
@router.get("/executive/{executive}")
def companies_by_executive(executive: str):

    companies = []

    cursor = predictions_collection.find(
        {
            "ejecutivo_comercial": executive
        },
        {"_id": 0}
    )

    for company in cursor:
        companies.append(_serialize_company(company))

    return companies


# =====================================================
# Listado paginado
# GET /companies?page=1&page_size=20
# =====================================================
@router.get("")
@router.get("/")
def get_companies(

    request: Request = None,

    page: int = 1,

    page_size: int = 20,
    search: Optional[str] = Query(default=None, min_length=1),
    sector: Optional[str] = None,
    region: Optional[str] = None,
    segmento: Optional[str] = None,
    ejecutivo_comercial: Optional[str] = None,
    prediction: Optional[int] = None,
    risk_min: Optional[float] = None,
    risk_max: Optional[float] = None,
    current_user=Depends(get_current_user)

):

    if page < 1:
        page = 1

    if page_size < 1:
        page_size = 20

    if page_size > 100:
        page_size = 100

    skip = (page - 1) * page_size

    if isinstance(search, Query):
        search = None
    if isinstance(sector, Query):
        sector = None
    if isinstance(region, Query):
        region = None
    if isinstance(segmento, Query):
        segmento = None
    if isinstance(ejecutivo_comercial, Query):
        ejecutivo_comercial = None
    if isinstance(prediction, Query):
        prediction = None
    if isinstance(risk_min, Query):
        risk_min = None
    if isinstance(risk_max, Query):
        risk_max = None

    query = {}

    if search:
        query["razon_social"] = {"$regex": search, "$options": "i"}

    if sector:
        query["sector"] = sector

    if region:
        query["region"] = region

    if segmento:
        query["segmento"] = segmento

    if ejecutivo_comercial:
        query["ejecutivo_comercial"] = ejecutivo_comercial

    if prediction is not None:
        query["prediction"] = prediction

    if risk_min is not None or risk_max is not None:
        risk_query = {}
        if risk_min is not None:
            risk_query["$gte"] = risk_min
        if risk_max is not None:
            risk_query["$lte"] = risk_max
        query["risk_score"] = risk_query

    companies = []

    cursor = predictions_collection.find(
        query,
        {"_id": 0}
    ).sort("company_id", 1).skip(skip).limit(page_size)

    for company in cursor:
        companies.append(_serialize_company(company))

    # Registrar auditoría
    if request is not None and hasattr(request, "client") and request.client is not None:
        save_log(

            username=current_user["username"],

            endpoint="/companies",

            method="GET",

            action="Consulta listado de empresas",

            ip=request.client.host

        )

    return companies


# =====================================================
# Empresa por ID
# GET /companies/15
# =====================================================
@router.get("/{company_id}")
def get_company(company_id: int):

    company = predictions_collection.find_one(
        {
            "company_id": company_id
        },
        {"_id": 0}
    )

    if company is None:

        raise HTTPException(
            status_code=404,
            detail="Empresa no encontrada"
        )

    return _serialize_company(company)