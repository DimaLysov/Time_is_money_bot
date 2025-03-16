from .commands import commands_router
from .move_menu import move_menu_router
from .time_zone_hd import time_zone_router
from .Notice_hd.add_notice_hd import add_notice_router
from .Notice_hd.edit_notice_hd import edit_notice_router
from .Notice_hd.view_all_notice_hd import view_notice_router
from .Payment_hd.add_payment_hd import add_payment_router
from .Payment_hd.edit_payment_hd import edit_payment_router
from .Payment_hd.view_all_payment_hd import view_all_payment_router

routers = [commands_router,
           move_menu_router,
           time_zone_router,
           add_notice_router,
           edit_notice_router,
           view_notice_router,
           add_payment_router,
           edit_payment_router,
           view_all_payment_router]