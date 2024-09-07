from discord_webhook import DiscordWebhook, DiscordEmbed
from scrapers.myntra import myntra_data
from setup import KEYWORDS, MONGO, MYNTRA_WEBHOOK_LINK, MYNTRA_RESTOCK_WEBHOOK_LINK
import pymongo

client = pymongo.MongoClient(MONGO)
db = client.myntra_db


list_item = {}
init_value = True
clear_cache = 1


def embedMsg(ele, val, new_size, channel):
    webhook_urls = channel

    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f"MYNTRA {ele['company']}-{ele['prod_name']}",
                         description=f"**Link**: {ele['link']}", color='03b2f8', url=ele['link'])

    embed.set_author(name=f"MYNTRA - {val}")
    embed.set_thumbnail(url=ele['img'])
    embed.add_embed_field(
        name=":dollar: **Price** :dollar:", value=f"Rs.{ele['price']}", inline=False)
    embed.add_embed_field(
        name=":green_circle: **Size** :green_circle:", value="\n".join(new_size), inline=False)

    webhook.add_embed(embed)

    response = webhook.execute()


def clean_myntra():
    global init_value
    global clear_cache
    global list_item

    webhook_urls = MYNTRA_WEBHOOK_LINK+MYNTRA_RESTOCK_WEBHOOK_LINK

    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f'Cache Clear',
                         description="System Cleaned", color='03b2f8')

    embed.set_author(name="MYNTRA")
    webhook.add_embed(embed)

    response = webhook.execute()

    list_item = {}
    init_value = True
    clear_cache = 1


def web_myntra():
    global init_value
    global clear_cache
    global list_item
    try:
        my = myntra_data()[::-1]
        if init_value:
            init_value = False
            for i in range(len(my)):
                ele = my[i]
                db.myntra.update_one({"id": ele['id']}, {'$set': {
                    "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
                list_item[ele['id']] = {
                    "price": ele['price'], "size": ele['size']}
            #embedMsg(ele, "TESTING", ele['size'],MYNTRA_RESTOCK_WEBHOOK_LINK+MYNTRA_WEBHOOK_LINK)
            print("myntra running")
        else:
            for i in range(len(my)):
                ele = my[i]
                if len([i for i in db.myntra.find({"id": ele['id']})]):
                    #for k in KEYWORDS:
                        #if k.lower() in ele['prod_name'].lower():
                    match_item = [i for i in db.myntra.find(
                        {"id": ele['id']})][0]
                    print(f"match item found {match_item}")
                    if match_item['size'] != ele['size']:
                        new_size = [i for i in ele['size']
                                    if i not in match_item['size']]
                        gone = [i for i in match_item['size']
                                if i not in ele['size']]
                        db.myntra.update_one({"id": ele['id']}, {
                            '$set': {'size': ele['size']}})
                        if new_size:
                            embedMsg(ele, 'RESTOCK', new_size,
                                     MYNTRA_RESTOCK_WEBHOOK_LINK)
                        if gone:
                            embedMsg(ele, 'OUT OF STOCK', gone,
                                     MYNTRA_RESTOCK_WEBHOOK_LINK)
                                #continue
                elif not len([i for i in db.myntra.find({"id": ele['id']})]):
                    db.myntra.update_one({"id": ele['id']}, {'$set': {
                        "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
                    embedMsg(ele, 'New Item Added',
                             ele['size'], MYNTRA_WEBHOOK_LINK)
    except Exception as e:
        print(e, "MYNTRA")


if __name__ == "__main__":
    web_myntra()
