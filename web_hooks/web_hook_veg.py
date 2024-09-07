from discord_webhook import DiscordWebhook, DiscordEmbed
from scrapers.vegnonveg import vegnon
from setup import MONGO, VEGNONVEG_WEBHOOK_LINK, VEGNONVEG_RESTOCK_WEBHOOK_LINK
import pymongo

client = pymongo.MongoClient(MONGO)
db = client.shoes


def embedMsg(ele, val, channel):
    webhook_urls = channel
    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f"Vegnonveg {ele['company']} - {ele['prod_name']}",
                         description=f"Link: {ele['link']}", color='03b2f8', url=ele['link'])

    embed.set_author(name=f"VegNonVeg {val}")
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


def clean_vnv():
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


def vnonveg():
    global init_value
    global clear_cache
    global list_item
    try:
        veg = vegnon()[::-1]
        if init_value:
            init_value = False
            for i in range(len(veg)):
                ele = veg[i]
                db.vegnonveg.update_one({"id": ele['id']},  {'$set': {
                    "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
                # list_item[ele['id']] = {
                #     "price": ele['price'], "size": ele['size']}
            # embedMsg(ele, "TESTING", VEGNONVEG_RESTOCK_WEBHOOK_LINK +
            #          VEGNONVEG_WEBHOOK_LINK)
            print("veg non veg running")
        else:
            for i in range(len(veg)):
                ele = veg[i]
                if len([i for i in db.vegnonveg.find({"id": ele['id']})]):
                    match_item = [i for i in db.vegnonveg.find(
                        {"id": ele['id']})][0]
                    if len(match_item['size']) < len(ele['size']) or (match_item['size'][0] == 'Sold Out' and ele['size'][0] != 'Sold Out'):
                        db.vegnonveg.update_one({"id": ele['id']}, {
                            '$set': {'size': ele['size']}})
                        embedMsg(ele, "Re-stock",
                                 VEGNONVEG_RESTOCK_WEBHOOK_LINK)
                    elif (match_item['size'][0] == 'Launching Soon' and ele['size'][0] != 'Launching Soon'):
                        db.vegnonveg.update_one({"id": ele['id']}, {
                            '$set': {'size': ele['size']}})
                        embedMsg(ele, "Now Available",
                                 VEGNONVEG_RESTOCK_WEBHOOK_LINK)
                    elif (match_item['size'][0] != 'Sold Out' and ele['size'][0] == 'Sold Out'):
                        db.vegnonveg.update_one({"id": ele['id']}, {
                            '$set': {'size': ele['size']}})

                        embedMsg(ele, "Sold Out",
                                 VEGNONVEG_RESTOCK_WEBHOOK_LINK)
                    continue
                else:
                    db.vegnonveg.update_one({"id": ele['id']},  {'$set': {
                        "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
                    embedMsg(ele, "New Product Added", VEGNONVEG_WEBHOOK_LINK)
    except Exception as e:
        print(e, "vegnonveg")


if __name__ == "__main__":
    vnonveg()
