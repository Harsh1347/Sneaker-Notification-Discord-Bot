from discord_webhook import DiscordWebhook, DiscordEmbed
from scrapers.nike import nikeApi
from setup import MONGO, NIKE_WEBHOOK_LINK
import pymongo

client = pymongo.MongoClient(
    MONGO)
db = client.shoes


webhook_urls = NIKE_WEBHOOK_LINK

list_item = {}
init_value = True
clear_cache = 1


def embedMsg(ele, val, new_size):
    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f"NIKE {ele['title']} {ele['color']}",
                         description=f"Link: {ele['link']}", color='03b2f8', url=ele['link'])

    embed.set_author(name=f"NIKE - {val}")
    embed.set_thumbnail(url=ele['img'])
    embed.add_embed_field(name="Color", value=ele['color'])
    embed.add_embed_field(
        name=":dollar: **Price** :dollar:", value=f"Rs.{ele['price']}", inline=False)
    embed.add_embed_field(
        name=":green_circle: **Size (USA)** :green_circle:", value="\n".join(new_size), inline=False)

    webhook.add_embed(embed)

    response = webhook.execute()


def clean_nike():
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


def web_nike():
    global init_value
    global clear_cache
    global list_item
    try:
        nike = nikeApi()[::-1]
        if init_value:
            init_value = False
            for i in range(len(nike)):
                ele = nike[i]
                db.nike.update_one({"id": ele['id']},  {'$set': {
                    "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['title']}}, upsert=True)
            # embedMsg(ele, "TESTING", ele['size'])
            print("Nike Running")
        else:
            for i in range(len(nike)):
                ele = nike[i]
                if len([i for i in db.nike.find({"id": ele['id']})]):
                    match_item = [i for i in db.nike.find(
                        {"id": ele['id']})][0]
                    if match_item['size'] != ele['size']:

                        new_size = [i for i in ele['size']
                                    if i not in match_item['size']]
                        gone = [i for i in match_item['size']
                                if i not in ele['size']]

                        db.nike.update_one({"id": ele['id']}, {
                            '$set': {'size': ele['size']}})
                        if new_size:
                            embedMsg(ele, 'RESTOCK', new_size=new_size)
                        else:
                            embedMsg(ele, 'OUT OF STOCK', new_size=gone)
                    continue
                else:
                    db.nike.update_one({"id": ele['id']},  {'$set': {
                        "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['title']}}, upsert=True)
                    embedMsg(ele, 'New Item Added', ele['size'])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    web_nike()
