from fastapi import FastAPI
from decouple import config

WEBHOOK_PATH = config('WEBHOOK_PATH')
WEBHOOK_URL = config("WEBHOOK_URL") + WEBHOOK_PATH

app = FastAPI(title="RentRide Client Bot")
