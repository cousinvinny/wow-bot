import asyncio
import discord
import datetime
import sys
from Database import *
from Scrape import *
from discord.ext import commands

scrape = Scrape()
db = Database()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

with open("/home/vinh/Desktop/wow_discord_bot/token.txt") as file:
    token = file.read()


# this function scrapes, checks and sends the latest post every 5 minutes, if it has not been sent already
@bot.event
async def on_ready():
    print("Bot ready!")
    #while True:
    print("Scraping posts")
    # get the post titles, dates, and links via webscraper
    post_titles = scrape.get_post_titles()
    post_dates = scrape.get_post_dates()
    post_links = scrape.get_post_links()

    # get the item links and item names from the posts in the database
    for post_link in post_links:
        item_links = scrape.get_item_links(post_link)
        item_names = scrape.get_item_names(item_links)
        db.add_items(post_link, item_names, item_links)
        await asyncio.sleep(1)
    db.add_posts(post_titles, post_dates, post_links)
    print("Done Scraping")

    now = datetime.now()
    print("Time: " + str(now))
    then = now + timedelta(minutes=1)
    wait_time = (then - now).total_seconds()
    #await asyncio.sleep(wait_time)
    print("checking if latest post was sent to discord server")
    if db.check_posts_not_posted():
        print("latest posts have not been sent yet, sending now...")
        await send_posts_not_sent(bot)
    else:
        print("latest post has already been automatically posted")
    await bot.close()
    sys.exit()


#async def scrape_posts():

@bot.command(aliases=["latest", "last", "LATEST", "LAST", "first", "FIRST"])
async def send_latest_post(ctx):
    post_data, item_data = db.get_latest_post()
    returned_title = post_data[0]
    returned_link = post_data[1]
    returned_datetime = post_data[2]

    message = "\nNew Post - " + returned_datetime + '\n' + returned_link + '\n' + returned_title
    if item_data:
        message += "\nNotable Items:"
        for item in item_data:
            item_name = item[0]
            item_link = item[1]
            message += '\n' + item_name + " " + item_link
        message += '\n\n'
    await send_message(message)


@bot.command(aliases=["latest5", "last5", "LATEST5", "LAST5", "first5", "FIRST5"])
async def send_latest_post_5(ctx):
    returned_title = []
    returned_link = []
    returned_datetime = []

    post_data, item_data = db.get_5_latest_post()
    for i in range(0, 5):
        returned_title.append(post_data[i][0])
        returned_link.append(post_data[i][1])
        returned_datetime.append(post_data[i][2])

    full_message = ""
    for i in range(0, 5):
        full_message += "\nNew Post - " + returned_datetime[i] + '\n' + returned_link[i] + '\n' + returned_title[i]
        if item_data[i]:
            full_message += "\nNotable Items:"
            for item in item_data[i]:
                item_name = item[0]
                item_link = item[1]
                full_message += "\n" + item_name + " " + item_link
        full_message += '\n\n'
    await send_message(full_message)

@bot.command(aliases=["notsent"])
async def send_posts_not_sent(ctx):
    returned_title = []
    returned_link = []
    returned_datetime = []

    post_data, item_data = db.get_posts_not_sent()
    for i in range(0, len(post_data)):
        returned_title.append(post_data[i][0])
        returned_link.append(post_data[i][1])
        returned_datetime.append(post_data[i][2])

    full_message = ""
    for i in range(0, len(post_data)):
        full_message += '\n' + returned_title[i] + '\n' + returned_link[i]
        if item_data[i]:
            full_message += "\nNotable Items:"
            for item in item_data[i]:
                item_name = item[0]
                item_link = item[1]
                full_message += "\n" + item_name + " " + item_link
        full_message += '\n\n'
    await send_message(full_message)

async def send_message(message):
    my_server_channel = 1259594024529166386
    curious_george_channel = 1101692742830133268
    monkey_channel = bot.get_channel(curious_george_channel)
    my_server = bot.get_channel(my_server_channel)

    alex_id = 277655709066199040
    brandon_id = 273666304458620928
    vin_id = 137724056689442816

    user_alex = await bot.fetch_user(alex_id)
    user_brandon = await bot.fetch_user(brandon_id)
    user_vin = await bot.fetch_user(vin_id)

    #await my_server.send(f"{user_vin.mention}" + message)
    await monkey_channel.send(message)
    print(message)

bot.run(token)
