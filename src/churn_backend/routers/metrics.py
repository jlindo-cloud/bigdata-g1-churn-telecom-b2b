from fastapi import APIRouter, Depends, HTTPException, Request

from database import confusion_matrix_collection, metrics_collection, model_info_collection
from security import get_current_user
from services.audit_service import save_log

router = APIRouter(

    prefix="/metrics",

    tags=["Model Metrics"]

)


@router.get("/model")
def get_model_metrics(

    request: Request,

    current_user=Depends(get_current_user)

):

    metric = metrics_collection.find_one(

        {},

        {"_id": 0}

    )

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

    save_log(

        username=current_user["username"],

        endpoint="/metrics/model",

        method="GET",

        action="Consulta métricas del modelo",

        ip=request.client.host

    )

    return metric


@router.get("/confusion-matrix")
def get_confusion_matrix(
    request: Request,
    current_user=Depends(get_current_user)
):
    document = confusion_matrix_collection.find_one({}, {"_id": 0})

    if document is None:
        raise HTTPException(status_code=404, detail="No existen datos de matriz de confusión.")

    save_log(
        username=current_user["username"],
        endpoint="/metrics/confusion-matrix",
        method="GET",
        action="Consulta matriz de confusión",
        ip=request.client.host if request.client else None
    )

    return document


@router.get("/model-info")
def get_model_info(
    request: Request,
    current_user=Depends(get_current_user)
):
    document = model_info_collection.find_one({}, {"_id": 0})

    if document is None:
        raise HTTPException(status_code=404, detail="No existen datos de información del modelo.")

    save_log(
        username=current_user["username"],
        endpoint="/metrics/model-info",
        method="GET",
        action="Consulta información del modelo",
        ip=request.client.host if request.client else None
    )

    return document