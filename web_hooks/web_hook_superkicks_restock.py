from discord_webhook import DiscordWebhook, DiscordEmbed
from scrapers.superkicks_restock import sk_restock
from setup import MONGO, SUPERKICKS_RESTOCK_WEBHOOK_LINK, SUPERKICKS_WEBHOOK_LINK
import pymongo

client = pymongo.MongoClient(MONGO)
db = client.shoes


def embedMsg(ele, val, channel=SUPERKICKS_RESTOCK_WEBHOOK_LINK):
    webhook_urls = SUPERKICKS_RESTOCK_WEBHOOK_LINK
    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f"Superkicks {ele['prod_name']}",
                         description=f"Link: {ele['link']}", color='03b2f8', url=ele['link'])

    embed.set_author(name=f"Superkicks Restock")
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


def clean_sk2():
    global init_value
    global clear_cache
    global list_item

    webhook = DiscordWebhook(
        url=SUPERKICKS_RESTOCK_WEBHOOK_LINK)

    embed = DiscordEmbed(title=f'Cache Clear',
                         description="System Cleaned", color='03b2f8')

    embed.set_author(name="Superkicks")
    webhook.add_embed(embed)

    response = webhook.execute()

    list_item = {}
    init_value = True
    clear_cache = 1


def SuperkicksRestock():
    global init_value
    global clear_cache
    global list_item
    try:
        sk = sk_restock()[::-1]
        if init_value:
            init_value = False
            for i in range(len(sk)):
                ele = sk[i]
                db.superkicks.update_one({"id": ele['id']},  {'$set': {
                    "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
            #embedMsg(ele, "Testing")
            print("sk restock running")
        else:
            for i in range(len(sk)):
                ele = sk[i]
                if len([i for i in db.superkicks.find({"id": ele['id']})]):
                    match_item = [i for i in db.superkicks.find(
                        {"id": ele['id']})][0]
                    if match_item['size'] != ele['size']:
                        db.superkicks.update_one({"id": ele['id']}, {
                            '$set': {'size': ele['size']}})
                        embedMsg(ele, "Re-stock")
                    continue
                else:
                    embedMsg(ele, "New Product Added",
                             channel=SUPERKICKS_WEBHOOK_LINK)
                    db.superkicks.update_one({"id": ele['id']},  {'$set': {
                        "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
    except Exception as e:
        print(e, "SuperkicksRestock")


if __name__ == "__main__":
    SuperkicksRestock()
