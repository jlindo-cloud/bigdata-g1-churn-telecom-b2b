from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from database import predictions_collection
from security import get_current_user

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)


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


def _serialize_prediction(prediction: dict) -> dict:
    prediction = dict(prediction)
    prediction["_id"] = str(prediction.get("_id"))
    prediction["risk_level"] = _risk_level(prediction.get("risk_score"))
    return prediction


# =====================================================
# Obtener todas las predicciones
# GET /predictions
# =====================================================

@router.get("")
@router.get("/")
def get_predictions(
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

    results = []

    cursor = predictions_collection.find(query).sort("company_id", 1).skip(skip).limit(page_size)

    for prediction_doc in cursor:
        results.append(_serialize_prediction(prediction_doc))

    return results


# =====================================================
# Obtener una empresa por company_id
# GET /predictions/100
# =====================================================

@router.get("/{company_id}")
def get_prediction(company_id: int):

    prediction = predictions_collection.find_one(
        {"company_id": company_id}
    )

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Empresa no encontrada"
        )

    return _serialize_prediction(prediction)


# =====================================================
# Empresas de alto riesgo
# GET /predictions/risk/high
# =====================================================

@router.get("/risk/high")
def high_risk():

    results = []

    cursor = predictions_collection.find(
        {
            "risk_score": {
                "$gte": 0.80
            }
        }
    )

    for prediction in cursor:

        prediction["_id"] = str(prediction["_id"])

        results.append(prediction)

    return results


# =====================================================
# Riesgo medio
# GET /predictions/risk/medium
# =====================================================

@router.get("/risk/medium")
def medium_risk():

    results = []

    cursor = predictions_collection.find(

        {
            "risk_score": {
                "$gte": 0.30,
                "$lt": 0.80
            }
        }

    )

    for prediction in cursor:
        results.append(_serialize_prediction(prediction))

    return results


# =====================================================
# Riesgo bajo
# GET /predictions/risk/low
# =====================================================

@router.get("/risk/low")
def low_risk():

    results = []

    cursor = predictions_collection.find(

        {
            "risk_score": {
                "$lt": 0.30
            }
        }

    )

    for prediction in cursor:
        results.append(_serialize_prediction(prediction))

    return results


# =====================================================
# Buscar por sector
# GET /predictions/sector/Finanzas
# =====================================================

@router.get("/sector/{sector}")
def by_sector(sector: str):

    results = []

    cursor = predictions_collection.find(
        {
            "sector": sector
        }
    )

    for prediction in cursor:
        results.append(_serialize_prediction(prediction))

    return results


# =====================================================
# Buscar por región
# GET /predictions/region/Lima
# =====================================================

@router.get("/region/{region}")
def by_region(region: str):

    results = []

    cursor = predictions_collection.find(
        {
            "region": region
        }
    )

    for prediction in cursor:
        results.append(_serialize_prediction(prediction))

    return results


# =====================================================
# Buscar por segmento
# GET /predictions/segmento/Gold
# =====================================================

@router.get("/segmento/{segmento}")
def by_segment(segmento: str):

    results = []

    cursor = predictions_collection.find(
        {
            "segmento": segmento
        }
    )

    for prediction in cursor:
        results.append(_serialize_prediction(prediction))

    return results


# =====================================================
# Empresas con churn predicho
# GET /predictions/churn
# =====================================================

@router.get("/churn")
def churn_predictions():

    results = []

    cursor = predictions_collection.find(
        {
            "prediction": 1
        }
    )

    for prediction in cursor:
        results.append(_serialize_prediction(prediction))

    return results


# =====================================================
# Empresas sin churn
# GET /predictions/no-churn
# =====================================================

@router.get("/no-churn")
def active_predictions():

    results = []

    cursor = predictions_collection.find(
        {
            "prediction": 0
        }
    )

    for prediction in cursor:

        prediction["_id"] = str(prediction["_id"])

        results.append(prediction)

    return results


# =====================================================
# Top 20 empresas con mayor riesgo
# GET /predictions/top-risk
# =====================================================

@router.get("/top-risk")
def top_risk():

    results = []

    cursor = predictions_collection.find().sort(
        "risk_score",
        -1
    ).limit(20)

    for prediction in cursor:
        results.append(_serialize_prediction(prediction))

    return results


# =====================================================
# Estadísticas rápidas
# GET /predictions/stats
# =====================================================

@router.get("/stats")
def stats():

    total = predictions_collection.count_documents({})

    high = predictions_collection.count_documents(
        {
            "risk_score": {
                "$gte": 0.80
            }
        }
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
        {
            "risk_score": {
                "$lt": 0.30
            }
        }
    )

    churn = predictions_collection.count_documents(
        {
            "prediction": 1
        }
    )

    active = predictions_collection.count_documents(
        {
            "prediction": 0
        }
    )

    return {

        "total_companies": total,

        "high_risk": high,

        "medium_risk": medium,

        "low_risk": low,

        "predicted_churn": churn,

        "predicted_active": active

    }