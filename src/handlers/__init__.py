from .start_hd import start_router
from .clear_hd import clear_router
from .Payment_hd.add_payment_hd import add_payment_router


routers = [start_router,
           clear_router,
           add_payment_router]