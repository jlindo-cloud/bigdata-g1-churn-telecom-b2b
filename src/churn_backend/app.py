from fastapi import Depends, FastAPI, Request
import time

from routers.predictions import router as predictions_router
from routers.companies import router as companies_router
from routers.dashboard import router as dashboard_router
from routers.auth import router as auth_router
from routers.metrics import router as metrics_router
from routers.logs import router as logs_router
from routers.metrics import get_confusion_matrix, get_model_info
from fastapi.middleware.cors import CORSMiddleware

from security import get_current_user
from services.audit_service import save_log


app = FastAPI(

    title="Telecom Churn Prediction API",

    description="""
API para predicción de abandono (Churn Prediction) de clientes B2B.

Proyecto desarrollado utilizando:

• Databricks Community
• Apache Spark MLlib
• MongoDB Atlas
• FastAPI
• Railway
• Vercel
• Power BI
• Machine Learning
""",

    version="1.0.0"

)
# =====================================================
# Middleware de Vercel
# =====================================================


origins = [
    "http://localhost:3000",
    "https://churnb2b.vercel.app",
    "https://v0-churnb2btelecom.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# =====================================================
# Middleware de Auditoría
# =====================================================

@app.middleware("http")
async def audit_middleware(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    end_time = time.time()

    execution_time = round((end_time - start_time) * 1000, 2)

    # Usuario por defecto
    username = "anonymous"

    # Si existe Authorization, se registrará como autenticado.
    # En la siguiente versión leeremos el JWT para obtener el usuario real.
    if request.headers.get("Authorization"):

        username = "authenticated_user"

    try:

        save_log(

            username=username,

            endpoint=request.url.path,

            method=request.method,

            action="HTTP Request",

            ip=request.client.host,

            status_code=response.status_code,

            response_time=execution_time,

            details={

                "query_params": dict(request.query_params)

            }

        )

    except Exception as ex:

        print(f"Audit Error: {ex}")

    return response


# =====================================================
# Routers
# =====================================================

app.include_router(predictions_router)

app.include_router(companies_router)

app.include_router(dashboard_router)

app.include_router(auth_router)

app.include_router(metrics_router)

app.include_router(logs_router)


# =====================================================
# Endpoint Principal
# =====================================================

@app.get("/")
def root():

    return {

        "status": "online",

        "project": "Telecom Churn Prediction",

        "version": "1.0.0",

        "framework": "FastAPI"

    }


# =====================================================
# Health Check
# =====================================================

@app.get("/health")
def health():

    return {

        "status": "healthy",

        "database": "MongoDB Atlas",

        "api": "running"

    }


@app.get("/confusion-matrix")
def confusion_matrix_root(request: Request, current_user=Depends(get_current_user)):
    return get_confusion_matrix(request=request, current_user=current_user)


@app.get("/model-info")
def model_info_root(request: Request, current_user=Depends(get_current_user)):
    return get_model_info(request=request, current_user=current_user)