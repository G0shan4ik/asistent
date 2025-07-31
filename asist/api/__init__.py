from .core import app
from .routers import user_router, currency_router, finance_router, check_in_router, debts_router

app.include_router(user_router)
app.include_router(currency_router)
app.include_router(finance_router)
app.include_router(check_in_router)
app.include_router(debts_router)