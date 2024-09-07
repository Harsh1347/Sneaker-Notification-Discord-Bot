from discord_webhook import DiscordWebhook, DiscordEmbed
from scrapers.ajio_api import ajioApi
from setup import AJIO_WEBHOOK_LINK, AJIO_RESTOCK_WEBHOOK_LINK, KEYWORDS, MONGO
import pymongo

client = pymongo.MongoClient(MONGO)
db = client.shoes


list_item = {}

init_value = True

clear_cache = 1


def embedMsg(ele, val, sizes, channel):
    webhook_urls = channel
    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f"AJIO {ele['company']} {ele['prod_name']}",
                         description=f"**Link**:{ele['link']}", color='03b2f8', url=ele['link'])

    embed.set_author(name=f"AJIO - {val}")
    embed.set_thumbnail(url=ele['img'])
    embed.add_embed_field(
        name=":dollar: **Price** :dollar:", value=f"{ele['price']}", inline=False)
    embed.add_embed_field(
        name=":green_circle: **Size** :green_circle:", value="\n".join(sizes), inline=False)

    webhook.add_embed(embed)

    response = webhook.execute()


def clean_aj():
    global init_value
    global clear_cache
    global list_item
    webhook_urls = AJIO_WEBHOOK_LINK+AJIO_RESTOCK_WEBHOOK_LINK
    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f'Cache Clear',
                         description="System Cleaned", color='03b2f8')
    embed.set_author(name="Ajio")
    webhook.add_embed(embed)
    response = webhook.execute()

    list_item = {}
    init_value = True
    clear_cache = 1


def ajio_web():
    global init_value
    global clear_cache
    global list_item
    try:
        aj = ajioApi()[::-1]
        if init_value:
            init_value = False
            for i in range(len(aj)):
                ele = aj[i]
                db.ajio.update_one({"id": ele['id']},  {'$set': {
                    "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
            print("ajio running")
            # embedMsg(ele, "TESTING", ele['size'],
            #          AJIO_RESTOCK_WEBHOOK_LINK+AJIO_WEBHOOK_LINK)
        else:
            for i in range(len(aj)):
                ele = aj[i]
                if len([i for i in db.ajio.find({"id": ele['id']})]):
                    match_item = [i for i in db.ajio.find(
                        {"id": ele['id']})][0]
                    for k in KEYWORDS:
                        if k.lower() in ele['prod_name'].lower():
                            if match_item['size'] != ele['size']:
                                new_size = [i for i in ele['size']
                                            if i not in match_item['size']]
                                gone = [i for i in match_item['size']
                                        if i not in ele['size']]
                                db.ajio.update_one({"id": ele['id']}, {
                                    '$set': {'size': ele['size']}})
                                if new_size:
                                    embedMsg(ele, 'RESTOCK', new_size,
                                             AJIO_RESTOCK_WEBHOOK_LINK)
                                if gone:
                                    embedMsg(ele, 'OUT OF STOCK', gone,
                                             AJIO_RESTOCK_WEBHOOK_LINK)
                            continue
                elif ele['id'] not in list_item.keys():
                    db.ajio.update_one({"id": ele['id']},  {'$set': {
                        "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
                    embedMsg(ele, 'New Item Added',
                             ele['size'], AJIO_WEBHOOK_LINK)
    except Exception as e:
        print(e, "AJIO")


if __name__ == "__main__":
    ajio_web()
