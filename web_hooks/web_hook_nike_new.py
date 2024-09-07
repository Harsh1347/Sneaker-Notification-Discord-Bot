from discord_webhook import DiscordWebhook, DiscordEmbed
from scrapers.nike_new import nike_new
from setup import MONGO, NIKE_NEW_WEBHOOK_LINK

import pymongo
client = pymongo.MongoClient(MONGO)
db = client.shoes
webhook_urls = NIKE_NEW_WEBHOOK_LINK

list_item = {}
init_value = True
clear_cache = 1


def embedMsg(ele, val):
    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f"NIKE {ele['prod_name']} {ele['color']}",
                         description=f"Link: {ele['link']}", color='03b2f8', url=ele['link'])

    embed.set_author(name=f"NIKE - {val}")
    embed.set_thumbnail(url=ele['img'])
    embed.add_embed_field(name="Color", value=ele['color'])
    embed.add_embed_field(
        name=":dollar: **Price** :dollar:", value=f"Rs.{ele['price']}", inline=False)
    embed.add_embed_field(
        name=":green_circle: **Size available?** :green_circle:", value=f"Check Out sizes at: {ele['link']}", inline=False)

    webhook.add_embed(embed)

    response = webhook.execute()


def clean_nike_new():
    global init_value
    global clear_cache
    global list_item

    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f'Cache Clear',
                         description="System Cleaned", color='03b2f8')

    embed.set_author(name="NIKE")
    webhook.add_embed(embed)

    response = webhook.execute()

    list_item = {}
    init_value = True
    clear_cache = 1


def web_nike_new():
    global init_value
    global clear_cache
    global list_item
    try:
        nike = nike_new()[::-1]
        if init_value:
            init_value = False
            for i in range(len(nike)):
                ele = nike[i]
                db.nikenew.update_one({"id": ele['id']},  {'$set': {
                    "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
            # embedMsg(ele, "TESTING")
            print("nike-new running")
        else:
            for i in range(len(nike)):
                ele = nike[i]
                if len([i for i in db.nikenew.find({"id": ele['id']})]):
                    match_item = [i for i in db.nikenew.find(
                        {"id": ele['id']})][0]
                    if match_item['size'] != ele['size']:
                        db.nikenew.update_one({"id": ele['id']}, {
                            '$set': {'size': ele['size']}})
                        if ele['size'] == "True":
                            embedMsg(ele, 'RESTOCK')
                        else:
                            embedMsg(ele, 'OUT OF STOCK')
                    continue
                else:
                    db.nikenew.update_one({"id": ele['id']},  {'$set': {
                        "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
                    embedMsg(ele, 'New Item Added')
    except Exception as e:
        print(e, "NIKE")


if __name__ == "__main__":
    web_nike_new()
