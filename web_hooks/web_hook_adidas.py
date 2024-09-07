from discord_webhook import DiscordWebhook, DiscordEmbed
from scrapers.adidas import adidas
from setup import ADIDAS_WEBHOOK_LINK, MONGO
import pymongo

client = pymongo.MongoClient(MONGO)
db = client.shoes


webhook_urls = ADIDAS_WEBHOOK_LINK


list_item = {}
init_value = True
clear_cache = 1


def clean_adidas():
    global init_value
    global clear_cache
    global list_item

    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f'Cache Clear',
                         description="System Cleaned", color='03b2f8')

    embed.set_author(name="Adidas")
    webhook.add_embed(embed)

    response = webhook.execute()

    list_item = {}
    init_value = True
    clear_cache = 1
    print("done")


def embedMsg(ele, val, new_size):
    webhook = DiscordWebhook(
        url=webhook_urls)

    embed = DiscordEmbed(title=f"ADIDAS {ele['prod_name']}",
                         description=f"Link: {ele['link']}", color='03b2f8', url=ele['link'])

    embed.set_author(name=f"ADIDAS - {val}")
    embed.set_thumbnail(url=ele['img'])
    embed.add_embed_field(
        name=":dollar: **Price** :dollar:", value=ele['price'])
    embed.add_embed_field(
        name=":green_circle: **Size** :green_circle:", value="\n".join(new_size), inline=False)

    webhook.add_embed(embed)

    response = webhook.execute()


def web_adidas():
    global init_value
    global clear_cache
    global list_item
    try:
        Adidas = adidas()[::-1]
        if init_value:
            init_value = False
            for i in range(len(Adidas)):
                ele = Adidas[i]
                # list_item[ele['id']] = {
                #     "price": ele['price'], "size": ele['size']}
                db.adidas.update_one({"id": ele['id']},  {'$set': {
                                     "id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']}}, upsert=True)
            print("Adidas Running")
            # embedMsg(ele, "TESTING", ele['size'])
        else:
            for i in range(len(Adidas)):
                ele = Adidas[i]
                if len([i for i in db.adidas.find({"id": ele['id']})]):
                    match_item = [i for i in db.adidas.find(
                        {"id": ele['id']})][0]
                    if match_item['size'] != ele['size']:
                        new_size = [i for i in ele['size']
                                    if i not in match_item['size']]
                        #list_item[ele['id']]['size'] = ele['size']
                        db.adidas.update_one({"id": ele['id']}, {
                                             '$set': {'size': ele['size']}})
                        if new_size:
                            embedMsg(ele, 'Re-Stock', new_size=new_size)
                    continue
                else:
                    db.adidas.insert_one(
                        {"id": ele['id'], "price": ele['price'], "size": ele['size'], "prod_name": ele['prod_name']})

                    embedMsg(ele, 'New Item Added', ele['size'])
    except Exception as e:
        print(e, "Adidas")


if __name__ == '__main__':
    web_adidas()
