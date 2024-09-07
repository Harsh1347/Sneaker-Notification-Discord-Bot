from discord_webhook import DiscordWebhook, DiscordEmbed
from scrapers.vegnonveg_restock import vegnonRestock
from setup import MONGO, VEGNONVEG_WEBHOOK_LINK, VEGNONVEG_RESTOCK_WEBHOOK_LINK
import pymongo

client = pymongo.MongoClient(MONGO)
db = client.shoes


def embedMsg(ele, val):
    webhook_urls = VEGNONVEG_RESTOCK_WEBHOOK_LINK
    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f"Vegnonveg {ele['prod_name']}",
                         description=f"Link: {ele['link']}", color='03b2f8', url=ele['link'])

    embed.set_author(name=f"VegNonVeg Restock")
    embed.set_thumbnail(url=ele['img'])
    embed.add_embed_field(
        name=":dollar: **Price** :dollar:", value=ele['price'])
    embed.add_embed_field(
        name=":green_circle: **Size** :green_circle:", value=" \n ".join(ele['size']), inline=False)

    webhook.add_embed(embed)

    response = webhook.execute()


list_item = {}
init_value = True
clear_cache = 1


def clean_vnv2():
    global init_value
    global clear_cache
    global list_item

    webhook = DiscordWebhook(
        url=VEGNONVEG_RESTOCK_WEBHOOK_LINK + VEGNONVEG_WEBHOOK_LINK)

    embed = DiscordEmbed(title=f'Cache Clear',
                         description="System Cleaned", color='03b2f8')

    embed.set_author(name="Vegnonveg")
    webhook.add_embed(embed)

    response = webhook.execute()

    list_item = {}
    init_value = True
    clear_cache = 1


def vegnonveg_Restock():
    global init_value
    global clear_cache
    global list_item
    try:
        veg = vegnonRestock()[::-1]
        if init_value:
            init_value = False
            for i in range(len(veg)):
                ele = veg[i]
                db.vegnonveg.update_one({"id": ele['id']},  {'$set': {
                    "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
            print("veg non veg restock running")
        else:
            for i in range(len(veg)):
                ele = veg[i]
                if len([i for i in db.vegnonveg.find({"id": ele['id']})]):
                    match_item = [i for i in db.vegnonveg.find(
                        {"id": ele['id']})][0]
                    if match_item['size'] != ele['size']:
                        db.vegnonveg.update_one({"id": ele['id']}, {
                            '$set': {'size': ele['size']}})
                        embedMsg(ele, "Re-stock")
                    continue
                else:
                    db.vegnonveg.update_one({"id": ele['id']},  {'$set': {
                        "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
    except Exception as e:
        print(e, "vegnonveg Restock")


if __name__ == "__main__":
    vegnonveg_Restock()
