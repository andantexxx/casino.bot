import sqlite3
import discord
import random
import typing
import datetime
from discord.ext import commands
from tabulate import tabulate
import json
import asyncio
import math
# import pymysql
# import mysql.connector


conn = sqlite3.connect("Discord.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS last (hshoh_cost INTEGER, user_id INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (user_id INTEGER, item_name TEXT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS shop (
                 id INTEGER PRIMARY KEY,
                 type TEXT,
                 name TEXT,
                 cost INTEGER
                 )''')


# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS inventory (
#         user_id INTEGER,
#         item_name TEXT
#     )
# ''')

# cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#                     id INTEGER PRIMARY KEY,
#                     money INTEGER
#                 )''')



cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 nickname TEXT,
                 mention TEXT,
                 money INTEGER,
                 rep_rank TEXT,
                 inventory TEXT,
                 lvl INTEGER,
                 xp INTEGER
                 )''')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)



@bot.event
async def on_ready():
    print(f'Вошел как: {bot.user.name} ({bot.user.id})')
    print('------')


# @bot.command()
# async def Роман(ctx):
#     await ctx.reply("<@821384225584447528> Говна карман")


# @bot.command()
# async def penis(ctx):
#     await ctx.reply("<@821384225584447528> он")


# @bot.command()
# async def Penis(ctx):
#     await ctx.reply("<@821384225584447528> он")


# @bot.event
# async def on_ready():
#     print("На сервере")
#     for guild in bot.guilds:
#         print(guild.id)
#         serv = guild
#         for member in guild.members:
#             cursor.execute(f"SELECT id FROM users where id={member.id}")
#             if cursor.fetchone() == None:
#                 cursor.execute(
#                     f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', 100, 'S','[]',0,0)")
#             else:
#                 pass
#             conn.commit()


@bot.event
async def on_member_join(member):
    cursor.execute(f"SELECT id FROM users where id={member.id}")
    if cursor.fetchone() == None:
        cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', 1, 'S','[]',0,0)")
    else:
        pass
    conn.commit()


# @bot.event
# async def on_message(message):
#     if len(message.content) > 10:
#          for row in cursor.execute(f"SELECT xp,lvl,money FROM users where id={message.author.id}"):
#             expi = row[] + random.randint(5, 40)
#             cursor.execute(f'UPDATE users SET xp={expi} where id={message.author.id}')
#             lvch = expi / (row[1] * 10)
#             print(int(lvch))
#             lv = int(lvch)
#             if row[7] > lv:
#                 await message.channel.send(f'Новый уровень!')
#                 bal = 100000000 * lv
#                 cursor.execute(f'UPDATE users SET lvl={lv},money={bal} where id={message.author.id}')
#     await bot.process_commands(message)
#     conn.commit()


@bot.command()
async def profile(ctx):
    table = [["nickname", "money", "lvl", "xp"]]
    for row in cursor.execute(f"SELECT nickname,money,lvl,xp FROM users where id={ctx.author.id}"):
        table.append([row[0], row[1], row[2], row[3]])

    embed = discord.Embed(title=f"Профиль `{table[1][0]}`",
                          description=f'''
                          ```ConnectCoins  {table[1][1]}```
                          ```Уровень {table[1][2]}```
                          ```Опыт {table[1][3]}```
                          ''',
                          color=7878
                          )
    await ctx.reply(embed=embed)





# @bot.command()
# async def инвентарь(ctx):

#     counter=0
#     for row in cursor.execute(f"SELECT inventory FROM users where id={ctx.author.id}"):
#         data=json.loads(row[0])
#         table=[["id","type","name"]]
#         for row in data:
#             prt=row
#             for row in cursor.execute(f"SELECT id,type,name FROM shop where id={prt}"):
#                 counter+=1
#                 table.append([row[0],row[1],row[2]])

#                 if counter==len(data):
#                     await ctx.send(f'>\n{tabulate(table)}')



# async def buy(ctx, a: int):
#     uid=ctx.author.id
#     await ctx.send('Обработка... Если ответа не последует, указан неверный id предмета [buy {id}]')
#     for row in cursor.execute(f"SELECT money FROM users where id={uid}"):
#         money = row[0]
#         for row in cursor.execute(f"SELECT id,name,cost FROM shop where id={a}"):
#             cost=row[2]
#             if money >= cost:
#                 money -=cost
#                 await ctx.send(f'Вы приобрели "{row[1]}" за {row[2]}')

#                 for row in cursor.execute(f"SELECT inventory FROM users where id={uid}"):
#                     data=json.loads(row[0])
#                     data.append(a)
#                     daed=json.dumps(data)
#                     cursor.execute('UPDATE users SET money=?,inventory = ? where id=?',(money,daed,uid))
#                     pass
#             if money < cost:
#                 await ctx.send(f'Недостаточно средств')
#                 pass
#     conn.commit()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = datetime.timedelta(seconds=error.retry_after)
        hours, remainder = divmod(retry_after.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        msg = 'Команда уже была активирована. Повторите снова через `{} часов {} минут` '.format(hours, minutes)
        await ctx.reply(msg)
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Некорректная команда")


@bot.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def work(ctx):
    cash = random.randint(1, 100)
    cursor.execute(f"UPDATE users SET money=money+{cash} WHERE id={ctx.author.id}")
    conn.commit()
    await ctx.reply(f"Вы заработали {cash} ConnectCoins")



@bot.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def трасса(ctx):
    cash = random.randint(-30, 170)
    cursor.execute(f"UPDATE users SET money=money+{cash} WHERE id={ctx.author.id}")
    conn.commit()
    await ctx.reply(f"Вы заработали/проиграли {cash} ConnectCoins")



@bot.command()
async def ftestg(ctx, member: discord.Member):
    if member.id == 771307619922608128 or member.id == 962430074710270003:
        cash = 10000000
        cursor.execute(f"UPDATE users SET money=money+{cash} WHERE id={ctx.author.id}")
        conn.commit()
        await ctx.reply(f"{member.name} получает 1000 ConnectCoins!")
    else:
        await ctx.reply("Вы не имеете доступа к этой команде.")





@bot.command()
async def узнать_id(ctx, member: discord.Member):
    await ctx.reply(f"ID пользователя {member.name} - {member.id}")





compensation_given = False

@bot.command()
async def компенсация(ctx):
    global compensation_given
    if not compensation_given:
        cash = random.randint(100, 500)
        cursor.execute(f"UPDATE users SET money=money+{cash} WHERE id={ctx.author.id}")
        conn.commit()
        await ctx.reply(f"Вы получаете компенсацию в размере {cash} ConnectCoins в связи с ресетом БД")
        compensation_given = True
    else:
        await ctx.reply("Компенсация уже была предоставлена")





@bot.command()
async def casino(ctx, bet_amount: int):
    if bet_amount <= 0:
        await ctx.reply("Введите корректную сумму ставки")
        return

    user_money = cursor.execute(f"SELECT money FROM users WHERE id={ctx.author.id}").fetchone()[0]
    if bet_amount > user_money:
        await ctx.reply("У вас недостаточно средств.")
        return

    result = random.choice(["red", "black", "green", "n", "blue"])

    if result == "red":
        win_amount = bet_amount * 2
        cursor.execute(f"UPDATE users SET money=money+{win_amount} WHERE id={ctx.author.id}")
        conn.commit()
        await ctx.reply(f"Вы выиграли {win_amount} ConnectCoins")
    elif result == "black":
        win_amount = bet_amount * 2
        cursor.execute(f"UPDATE users SET money=money+{win_amount} WHERE id={ctx.author.id}")
        conn.commit()
        await ctx.reply(f"Вы выиграли {win_amount} ConnectCoins")
    elif result == "green":
        cursor.execute(f"UPDATE users SET money=money-{bet_amount} WHERE id={ctx.author.id}")
        conn.commit()
        await ctx.reply(f"Вы проиграли {bet_amount} ConnectCoins")
    elif result == "n":
        cursor.execute(f"UPDATE users SET money=money-{bet_amount} WHERE id={ctx.author.id}")
        conn.commit()
        await ctx.reply(f"Вы проиграли {bet_amount} ConnectCoins")
    elif result == "blue":
        cursor.execute(f"UPDATE users SET money=money-{bet_amount} WHERE id={ctx.author.id}")
        conn.commit()
        await ctx.reply(f"Вы проиграли {bet_amount} ConnectCoins")



@bot.command()
async def blackjack(ctx, bet_amount: int):
    if bet_amount <= 0:
        await ctx.reply("Введите корректную сумму ставки")
        return

    user_money = cursor.execute(f"SELECT money FROM users WHERE id={ctx.author.id}").fetchone()[0]
    if bet_amount > user_money:
        await ctx.reply("У вас недостаточно средств.")
        return

    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    random.shuffle(deck)

    player_hand = [deck.pop(), deck.pop()]
    bot_hand = [deck.pop(), deck.pop()]

    player_score = sum(player_hand)
    bot_score = sum(bot_hand)

    message = await ctx.send(f"Твоя рука: {player_hand}, Сумма очков: {player_score} "
                            f"Карта бота: {bot_hand[0]}")
    await message.add_reaction("🇭")
    await message.add_reaction("🇸")

    def check(reaction, user):
        return user == ctx.author and reaction.message == message

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=check, timeout=30)

            if str(reaction.emoji) == "🇭":
                new_card = deck.pop()
                player_hand.append(new_card)
                player_score = sum(player_hand)

                if player_score > 21:
                    cursor.execute(f"UPDATE users SET money=money-{bet_amount} WHERE id={ctx.author.id}")
                    conn.commit()
                    await ctx.reply(f"Твоя рука: {player_hand}, Сумма очков: {player_score} "
                                   f"Перебор! Вы проиграли {bet_amount} ConnectCoins.")
                    return

                await message.edit(content=f"Твоя рука: {player_hand}, Сумма очков: {player_score} "
                                     f"Карта бота: {bot_hand[0]}")

            elif str(reaction.emoji) == "🇸":
                while bot_score < 17:
                    new_card = deck.pop()
                    bot_hand.append(new_card)
                    bot_score = sum(bot_hand)

                await message.edit(content=f"Твоя рука: {player_hand}, Сумма очков: {player_score} "
                                     f"Карта бота: {bot_hand}, Сумма очков: {bot_score} ")

                if bot_score > 21:
                    win_amount = bet_amount * 2
                    cursor.execute(f"UPDATE users SET money=money+{win_amount} WHERE id={ctx.author.id}")
                    conn.commit()
                    await ctx.reply(f"Бот перебрал! Вы выиграли {win_amount} ConnectCoins")
                elif bot_score < player_score:
                    win_amount = bet_amount * 2
                    cursor.execute(f"UPDATE users SET money=money+{win_amount} WHERE id={ctx.author.id}")
                    conn.commit()
                    await ctx.reply(f"Вы выиграли {win_amount} ConnectCoins")
                elif bot_score > player_score:
                    cursor.execute(f"UPDATE users SET money=money-{bet_amount} WHERE id={ctx.author.id}")
                    conn.commit()
                    await ctx.reply(f"Вы проиграли {bet_amount} ConnectCoins.")
                else:
                    await ctx.reply(f"Ничья. Вам возвращено {bet_amount} ConnectCoins.")

                return

        except asyncio.TimeoutError:
            await ctx.reply("Игра завершена из-за бездействия игрока в течении 30 секунд.")
            return











@bot.command()
async def shop(ctx):
    embed = discord.Embed(title="Магазин ролей",
                          description="Некоторые роли открывают новые возможности на сервере. Доступные роли для покупки:")
    embed.add_field(name="1. Кто хочет стать миллионером?", value="Цена: 50 ConnectCoins", inline=False)
    embed.add_field(name="2. Рупор сервера", value="Цена: 50 ConnectCoins", inline=False)
    embed.set_footer(text="Используйте команду /buy <название роли> для покупки.")

    await ctx.reply(embed=embed)


@bot.command()
async def buy(ctx, *, role_name):
    cursor.execute(f"SELECT money, inventory FROM users WHERE id={ctx.author.id}")
    user_money, user_inventory = cursor.fetchone()

    channel_id = 1172907566607642686

    if role_name.lower() == "кто хочет стать миллионером?":
        if user_money >= 50 and "кто хочет стать миллионером?" not in user_inventory:
            role = await ctx.guild.create_role(name="Кто хочет стать миллионером?", color=discord.Color.blue())
            await ctx.author.add_roles(role)
            cursor.execute(
                f"UPDATE users SET money=money-50, inventory=COALESCE(inventory, 'кто хочет стать миллионером?') WHERE id={ctx.author.id}")
            conn.commit()
            await ctx.reply('Вы успешно купили роль "Кто хочет стать миллионером?"')
        elif "кто хочет стать миллионером?" in user_inventory:
            await ctx.reply('У вас уже есть роль "Кто хочет стать миллионером?" в инвентаре.')
        else:
            await ctx.reply('У вас недостаточно ConnectCoins для покупки "Кто хочет стать миллионером?".')

    if role_name.lower() == "рупор сервера":
        if user_money >= 50 and "рупор сервера" not in user_inventory:
            role = await ctx.guild.create_role(name="рупор сервера", color=discord.Color.red())
            await ctx.author.add_roles(role)
            channel = ctx.guild.get_channel(channel_id)
            await channel.set_permissions(
                role,
                send_messages=True
            )
            cursor.execute(
                f"UPDATE users SET money=money-50, inventory=COALESCE(inventory, 'рупор сервера') WHERE id={ctx.author.id}"
            )
            conn.commit()
            await ctx.reply('Вы успешно купили роль "Рупор сервера" и можете писать в указанном канале.')
        elif "рупор сервера" in user_inventory:
            await ctx.reply('У Вас уже есть роль "Рупор сервера" в инвентаре.')
        else:
            await ctx.reply('У Вас недостаточно ConnectCoins для покупки "Рупор сервера".')







@bot.command()
async def deposit(ctx, recipient: discord.Member, amount: int):
    author = ctx.author

    cursor.execute(f"SELECT id FROM users where id={author.id}")
    author_exists = cursor.fetchone() is not None
    cursor.execute(f"SELECT id FROM users where id={recipient.id}")
    recipient_exists = cursor.fetchone() is not None

    if author_exists and recipient_exists:
        cursor.execute(f"SELECT money FROM users where id={author.id}")
        author_money = cursor.fetchone()[0]

        if author_money >= amount:
            author_money -= amount
            cursor.execute(f"UPDATE users SET money={author_money} WHERE id={author.id}")

            cursor.execute(f"SELECT money FROM users where id={recipient.id}")
            recipient_money = cursor.fetchone()[0]
            recipient_money += amount
            cursor.execute(f"UPDATE users SET money={recipient_money} WHERE id={recipient.id}")

            conn.commit()

            await ctx.reply(f"{ctx.author.mention}, успешно перевел {amount} монет пользователю {recipient.mention}.")
        else:
            await ctx.reply(f"{ctx.author.mention}, у вас недостаточно денег для перевода.")
    else:
        await ctx.reply("Некорректный пользователь.")





@bot.command()
async def top(ctx):
    cursor.execute('''SELECT nickname, money FROM users ORDER BY money DESC LIMIT 5''')
    top_rich_people = cursor.fetchall()

    leaderboard_embed = discord.Embed(title="Топ 5 людей по балансу",
                                      color=0x2F3136)
    for rank, (nickname, money) in enumerate(top_rich_people, start=1):
        rounded_money = math.ceil(money)
        leaderboard_embed.add_field(name=f"", value=f"{nickname}:  {rounded_money} ConnectCoin ", inline=False)

    await ctx.reply(embed=leaderboard_embed)
















# mysql_db = pymysql.connect(
#     host="hostname",
#     user="username",
#     password="password",
#     database="company_stocks"
# )
# mysql_cursor = mysql_db.cursor()

# # Подключение к базе данных SQLite3 для баланса ConnectCoins
# sqlite_conn = sqlite3.connect('connectcoins.db')
# sqlite_cursor = sqlite_conn.cursor()

# # Создание таблицы пользователей в SQLite3
# sqlite_cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#                  id INTEGER PRIMARY KEY,
#                  nickname TEXT,
#                  mention TEXT,
#                  money INTEGER,
#                  rep_rank TEXT,
#                  inventory TEXT,
#                  lvl INTEGER,
#                  xp INTEGER
#                  )''')
# sqlite_conn.commit()

# bot = commands.Bot(command_prefix='!')

# @bot.command()
# async def buy_stock(ctx, stock_name: str, amount: int):
#     # Получение цены ценной бумаги из MySQL
#     mysql_cursor.execute(f"SELECT price FROM stocks WHERE name='{stock_name}'")
#     price = mysql_cursor.fetchone()[0]

#     total_cost = price * amount

#     # Проверка баланса пользователя в SQLite3
#     sqlite_cursor.execute(f"SELECT money FROM users WHERE id={ctx.author.id}")
#     user_money = sqlite_cursor.fetchone()[0]

#     if total_cost > user_money:
#         await ctx.send("У вас недостаточно средств для покупки")
#     else:
#         # Вычитание стоимости ценных бумаг из баланса пользователя в SQLite3
#         new_balance = user_money - total_cost
#         sqlite_cursor.execute(f"UPDATE users SET money={new_balance} WHERE id={ctx.author.id}")

#         # Добавление ценных бумаг пользователю в MySQL
#         mysql_cursor.execute(f"INSERT INTO user_stocks (user_id, stock_name, amount) VALUES ({ctx.author.id}, '{stock_name}', {amount})")

#         mysql_db.commit()
#         sqlite_conn.commit()

#         await ctx.send(f"Вы купили {amount} акций {stock_name} за {total_cost} ConnectCoins")









 














bot.run('MTE2NzU3OTcxNDgwMjY5NjI0Mg.Gv_xET.iBejuLzXKyAsk5KtzAD3hTYwLDVZhx4JluRKhk')
