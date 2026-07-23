from typing import Optional

from fastapi import APIRouter, Depends

from database import metrics_collection, model_info_collection, predictions_collection
from security import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# =====================================================
# Dashboard principal compatible con V0
# GET /dashboard/
# =====================================================
@router.get("")
@router.get("/")
def dashboard(current_user=Depends(get_current_user)):

    # KPIs principales
    total = predictions_collection.count_documents({})
    active = predictions_collection.count_documents({"prediction": 0})
    churn = predictions_collection.count_documents({"prediction": 1})

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
        {
            "risk_score": {
                "$lt": 0.30
            }
        }
    )

    # Riesgo promedio
    avg_pipeline = [
        {
            "$group": {
                "_id": None,
                "avg": {"$avg": "$risk_score"},
                "max": {"$max": "$risk_score"},
                "min": {"$min": "$risk_score"}
            }
        }
    ]

    stats = list(predictions_collection.aggregate(avg_pipeline))
    avg_risk = round(stats[0]["avg"], 4) if stats else 0
    max_risk = round(stats[0]["max"], 4) if stats else 0
    min_risk = round(stats[0]["min"], 4) if stats else 0

    # Métricas del modelo
    metric = metrics_collection.find_one({}, {"_id": 0})

    if metric is None:
        metric = {
            "accuracy": 0,
            "precision": 0,
            "recall": 0,
            "f1_score": 0,
            "true_positive": 0,
            "true_negative": 0,
            "false_positive": 0,
            "false_negative": 0
        }

    model_info = model_info_collection.find_one({}, {"_id": 0})
    if model_info is None:
        model_info = {
            "algorithm": None,
            "version": None,
            "training_date": None
        }

    # Empresas por región
    region_pipeline = [
        {
            "$group": {
                "_id": "$region",
                "cantidad": {"$sum": 1}
            }
        },
        {
            "$sort": {"cantidad": -1}
        }
    ]

    customers_by_region = []

    for item in predictions_collection.aggregate(region_pipeline):
        customers_by_region.append(
            {
                "región": item["_id"] or "Sin región",
                "cantidad": item["cantidad"]
            }
        )

    # Empresas por sector
    sector_pipeline = [
        {
            "$group": {
                "_id": "$sector",
                "cantidad": {"$sum": 1}
            }
        },
        {
            "$sort": {"cantidad": -1}
        }
    ]

    customers_by_sector = []

    for item in predictions_collection.aggregate(sector_pipeline):
        customers_by_sector.append(
            {
                "sector": item["_id"] or "Sin sector",
                "cantidad": item["cantidad"]
            }
        )

    return {
        "total_companies": total,
        "predicted_churn": churn,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "average_risk": avg_risk,
        "accuracy": float(metric.get("accuracy", 0)),
        "precision": float(metric.get("precision", 0)),
        "recall": float(metric.get("recall", 0)),
        "f1_score": float(metric.get("f1_score", 0)),
        "training_date": model_info.get("training_date"),
        "algorithm": model_info.get("algorithm"),
        "version": model_info.get("version")
    }


# =====================================================
# Distribución por sector
# GET /dashboard/sectors
# =====================================================
@router.get("/sectors")
def sectors(current_user=Depends(get_current_user)):

    pipeline = [
        {
            "$group": {
                "_id": "$sector",
                "companies": {"$sum": 1}
            }
        },
        {
            "$sort": {"companies": -1}
        }
    ]

    return [
        {
            "sector": item["_id"],
            "companies": item["companies"]
        }
        for item in predictions_collection.aggregate(pipeline)
    ]


# =====================================================
# Distribución por región
# GET /dashboard/regions
# =====================================================
@router.get("/regions")
def regions(current_user=Depends(get_current_user)):

    pipeline = [
        {
            "$group": {
                "_id": "$region",
                "companies": {"$sum": 1}
            }
        },
        {
            "$sort": {"companies": -1}
        }
    ]

    return [
        {
            "region": item["_id"],
            "companies": item["companies"]
        }
        for item in predictions_collection.aggregate(pipeline)
    ]


# =====================================================
# Distribución por segmento
# GET /dashboard/segments
# =====================================================
@router.get("/segments")
def segments(current_user=Depends(get_current_user)):

    pipeline = [
        {
            "$group": {
                "_id": "$segmento",
                "companies": {"$sum": 1}
            }
        },
        {
            "$sort": {"companies": -1}
        }
    ]

    return [
        {
            "segment": item["_id"],
            "companies": item["companies"]
        }
        for item in predictions_collection.aggregate(pipeline)
    ]


# =====================================================
# Distribución por Ejecutivo Comercial
# GET /dashboard/executives
# =====================================================
@router.get("/executives")
def executives(current_user=Depends(get_current_user)):

    pipeline = [
        {
            "$group": {
                "_id": "$ejecutivo_comercial",
                "companies": {"$sum": 1}
            }
        },
        {
            "$sort": {"companies": -1}
        }
    ]

    return [
        {
            "executive": item["_id"],
            "companies": item["companies"]
        }
        for item in predictions_collection.aggregate(pipeline)
    ]


# =====================================================
# Top 10 empresas con mayor riesgo
# GET /dashboard/top-risk
# =====================================================
@router.get("/top-risk")
def top_risk(current_user=Depends(get_current_user)):

    companies = []

    cursor = (
        predictions_collection.find({}, {"_id": 0})
        .sort("risk_score", -1)
        .limit(10)
    )

    for company in cursor:
        companies.append(company)

    return companies


# =====================================================
# Riesgo por sector
# GET /dashboard/risk-by-sector
# =====================================================
@router.get("/risk-by-sector")
def risk_sector(current_user=Depends(get_current_user)):

    pipeline = [
        {
            "$group": {
                "_id": "$sector",
                "average_risk": {"$avg": "$risk_score"}
            }
        },
        {
            "$sort": {"average_risk": -1}
        }
    ]

    return [
        {
            "sector": item["_id"],
            "average_risk": round(item["average_risk"], 4)
        }
        for item in predictions_collection.aggregate(pipeline)
    ]


# =====================================================
# Riesgo por Región
# GET /dashboard/risk-by-region
# =====================================================
@router.get("/risk-by-region")
def risk_region(current_user=Depends(get_current_user)):

    pipeline = [
        {
            "$group": {
                "_id": "$region",
                "average_risk": {"$avg": "$risk_score"}
            }
        },
        {
            "$sort": {"average_risk": -1}
        }
    ]

    return [
        {
            "region": item["_id"],
            "average_risk": round(item["average_risk"], 4)
        }
        for item in predictions_collection.aggregate(pipeline)
    ]