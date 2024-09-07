import schedule
from setup import REFRESH_RATE
from web_hooks.web_hook_nike import web_nike, clean_nike
from web_hooks.web_hook_sk import sk_web, clean_sk
from web_hooks.web_hook_ajio import ajio_web, clean_aj
from web_hooks.web_hook_nike_new import web_nike_new, clean_nike_new
from web_hooks.web_hook_myntra import web_myntra
from web_hooks.web_hook_veg import vnonveg
from web_hooks.web_hook_veg_restock import vegnonveg_Restock
from web_hooks.web_hook_adidas import web_adidas, clean_adidas
from web_hooks.web_hook_superkicks_restock import SuperkicksRestock, clean_sk2

schedule.every(REFRESH_RATE).seconds.do(sk_web)
schedule.every(REFRESH_RATE).seconds.do(SuperkicksRestock)
schedule.every(REFRESH_RATE).seconds.do(web_adidas)
schedule.every(REFRESH_RATE).seconds.do(web_nike)
schedule.every(REFRESH_RATE).seconds.do(ajio_web)
schedule.every(REFRESH_RATE).seconds.do(web_nike_new)
schedule.every(REFRESH_RATE).seconds.do(web_myntra)
schedule.every(REFRESH_RATE).seconds.do(vegnonveg_Restock)
schedule.every(REFRESH_RATE).seconds.do(vnonveg)


while True:
    schedule.run_pending()
