source ./env/bin/activate

export FASTAPI_CONFIG=development

uvicorn src.main:app --reload --host 0.0.0.0 --port 5000 &