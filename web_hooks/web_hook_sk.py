from discord_webhook import DiscordWebhook, DiscordEmbed
from scrapers.superkicks import superkick
from setup import MONGO, SUPERKICKS_WEBHOOK_LINK, SUPERKICKS_RESTOCK_WEBHOOK_LINK
import pymongo

client = pymongo.MongoClient(MONGO)
db = client.shoes


list_item = {}

init_value = True

clear_cache = 1


def embedMsg(ele, val, channel):
    webhook_urls = channel
    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f"Superkicks  - {ele['prod_name']}",
                         description=f"Link: {ele['link']}", color='03b2f8', url=ele['link'])

    embed.set_author(name=f"SuperKicks -{val}")
    embed.set_thumbnail(url=ele['img'])
    embed.add_embed_field(
        name=":dollar: **Price** :dollar:", value=ele['price'])
    embed.add_embed_field(
        name=":green_circle: **Size** :green_circle:", value="\n".join(ele['size']), inline=False)

    webhook.add_embed(embed)

    response = webhook.execute()


def clean_sk():
    global init_value
    global clear_cache
    global list_item
    webhook_urls = SUPERKICKS_WEBHOOK_LINK + SUPERKICKS_RESTOCK_WEBHOOK_LINK
    if len(list_item) > 60:
        list_item = {}
        init_value = True
        clear_cache = 1

        webhook = DiscordWebhook(
            url=webhook_urls)

        embed = DiscordEmbed(title=f'Cache Clear',
                             description="System Cleaned", color='03b2f8')
        embed.set_author(name="Superkicks")
        webhook.add_embed(embed)
        response = webhook.execute()
    else:
        webhook = DiscordWebhook(
            url=webhook_urls)

        embed = DiscordEmbed(title=f'System Check Done',
                             description="System Cleaned", color='03b2f8')
        embed.set_author(name="Superkicks")
        webhook.add_embed(embed)
        response = webhook.execute()


def sk_web():
    global init_value
    global clear_cache
    global list_item
    try:
        sk = superkick()[::-1]
        if init_value:
            init_value = False
            for i in range(len(sk)):
                ele = sk[i]
                db.superkicks.update_one({"id": ele['id']},  {'$set': {
                    "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
            print("sk running")
            # embedMsg(ele, "TESTING", SUPERKICKS_WEBHOOK_LINK +
            #          SUPERKICKS_RESTOCK_WEBHOOK_LINK)
        else:
            for i in range(len(sk)):
                ele = sk[i]
                if len([i for i in db.superkicks.find({"id": ele['id']})]):
                    match_item = [i for i in db.superkicks.find(
                        {"id": ele['id']})][0]
                    if match_item['size'] != ele['size'] or (match_item['size'][0] == 'Sold Out' and ele['size'][0] != 'Sold Out'):
                        db.superkicks.update_one({"id": ele['id']}, {
                            '$set': {'size': ele['size']}})
                        embedMsg(ele, "Re-stock",
                                 SUPERKICKS_RESTOCK_WEBHOOK_LINK)
                    continue
                else:
                    db.superkicks.update_one({"id": ele['id']},  {'$set': {
                        "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
                    embedMsg(ele, "New Item Added", SUPERKICKS_WEBHOOK_LINK)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    sk_web()
