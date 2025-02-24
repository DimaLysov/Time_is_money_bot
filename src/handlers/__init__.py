from .start_hd import start_router
from .menu_hd import menu_router
from .Notice_hd.add_notice_hd import add_notice_router
from .Notice_hd.edit_data_notice_hd import edit_notice_router
from .Notice_hd.view_all_notice_hd import view_notice_router
from .Payment_hd.add_payment_hd import add_payment_router
from .Payment_hd.edit_data_payment_hd import edit_payment_router
from .Payment_hd.view_all_payment_hd import view_all_payment_router

routers = [start_router,
           menu_router,
           add_notice_router,
           edit_notice_router,
           view_notice_router,
           add_payment_router,
           edit_payment_router,
           view_all_payment_router]