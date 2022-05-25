from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, GroupEventType, GroupTypes, LoopWrapper
from random import randint, choice
from math import floor
import time, pymysql, vkcoin, threading, pyqiwi

merchant = vkcoin.VKCoin(key="O*-tp_yX9u;OskP_s2#P.R-#0LdQmsZNcHHf8g[OQKByOxGyhe", user_id=705783864)
bot = Bot("dd8f8b777c6643b95bccde155cc1b492f0a5c1c07e3f6de99a60561711212f1b474e9b26084dbfba17a95")
admin_ids = [498475943,705783864]
longpoll_handler = None
longpoll_transaction = None

top = ["🥇 1.", "🥈 2.", "🥉 3.", "🏅 4.", "🏅 5.", "🏅 6.", "🏅 7.", "🏅 8.", "🏅 9.", "🏅 10."]

lw = LoopWrapper()
bot.labeler.vbml_ignore_case = True

def getCon():
	try:
		connection = pymysql.connect(
			host="141.8.192.193",
			port=3306,
			user="a0677620_invest",
			password="qwerty123",
			database="a0677620_invest",
			cursorclass=pymysql.cursors.DictCursor)
		return connection
	except Exception as e:
		print(e)

class user:
	def create():
		connection = getCon()
		cursor = connection.cursor()
		cursor.execute("""CREATE TABLE IF NOT EXISTS users
			(
				id int(20) primary key AUTO_INCREMENT,
				tag varchar(50) not null default "[id0|N/D]",
				vk_id int(20) not null default 0,
				balance bigint(20) not null default 0,
				invest_balance bigint(20) not null default 0,
				all_invest bigint(20) not null default 0,
				all_invest_week bigint(20) not null default 0,
				last_time bigint(20) not null default 0,
				vip smallint(6) not null default 0,
				autoinvest smallint(6) not null default 0,
				dohod_everyday bigint(20) not null default 0,
				last_id int(20) not null default 0,
				all_topup bigint(20) not null default 0,
				bonus_time bigint(20) not null default 0,
				subscribe tinyint(4) not null default 0,
				dollars bigint(20) not null default 0,
				CityName varchar(50) not null default "BigCity",
				CityCoffers bigint(20) not null default 0,
				CityPopulation int(20) not null default 0,
				CityHappy tinyint(10) not null default 0,
				CityTaxes bigint(20) not null default 0,
				CityBuildings int(20) not null default 0,
				CityWaterCosts bigint(20) not null default 0,
				CityEnergyCosts bigint(20) not null default 0,
				CityServiceCosts bigint(20) not null default 0,
				City_time bigint(20) not null default 0,
				CityEvent_time bigint(20) not null default 0
			)
			CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci""")
		connection.commit()
		connection.close()

	def insert(id, tag):
		connection = getCon()
		cursor = connection.cursor()
		cursor.execute(f"INSERT INTO users (vk_id, tag) VALUES ({id}, '{tag}')")
		connection.commit()
		connection.close()

	def get(id, var):
		connection = getCon()
		cursor = connection.cursor()
		if var.lower() != "all":
			cursor.execute(f"SELECT {var} FROM users WHERE vk_id = {id}")
			connection.commit()
			return cursor.fetchone()[var]
		else:
			cursor.execute(f"SELECT * FROM users WHERE vk_id = {id}")
			connection.commit()
			return cursor.fetchall()
		connection.close()

	def get_byid(id, var="all"):
		connection = getCon()
		cursor = connection.cursor()
		if var == "all":
			cursor.execute(f"SELECT * FROM users WHERE id = {id}")
			connection.commit()
			return cursor.fetchall()
		else:
			cursor.execute(f"SELECT vk_id, tag, {var} FROM users WHERE id = {id}")
			connection.commit()
			return cursor.fetchall()
		connection.close()

	def update(id, var, val):
		connection = getCon()
		cursor = connection.cursor()
		if isinstance(val, int):
			cursor.execute(f"UPDATE users SET {var} = {val} WHERE vk_id = {id}")
		else:
			cursor.execute(f"UPDATE users SET {var} = '{val}' WHERE vk_id = {id}")
		connection.commit()
		connection.close()

	def uni_update(var, val):
		connection = getCon()
		cursor = connection.cursor()
		cursor.execute(f"UPDATE users SET {var} = {val}")
		connection.commit()
		connection.close()

	def check(id):
		connection = getCon()
		cursor = connection.cursor()
		cursor.execute(f"SELECT balance FROM users WHERE vk_id = {id}")
		connection.commit()
		value = cursor.fetchone()
		if value == None:
			return False
		else:
			return True
		connection.close()

	def counts(var=None):
		connection = getCon()
		cursor = connection.cursor()
		if var == None:
			cursor.execute("SELECT COUNT(1) FROM users")
		else:
			cursor.execute(f"SELECT COUNT(1) FROM users WHERE {var} > 0")
		connection.commit()
		return cursor.fetchone()['COUNT(1)']
		connection.close()

	def get_top(var, limit=10):
		connection = getCon()
		cursor = connection.cursor()
		if limit != None:
			cursor.execute(f"SELECT vk_id, tag, vip, {var} FROM users WHERE vk_id != 498475943 and vk_id != 705783864 ORDER BY {var} DESC LIMIT {limit}")
		else:
			cursor.execute(f"SELECT vk_id, tag, vip, {var} FROM users ORDER BY {var} DESC")
		connection.commit()
		return cursor.fetchall()
		connection.close()

	def get_citytop():
		connection = getCon()
		cursor = connection.cursor()
		cursor.execute(f"SELECT vk_id, tag, vip, CityPopulation FROM users ORDER BY CityPopulation DESC")
		connection.commit()
		return cursor.fetchall()
		connection.close()

class globals:
	def create():
		connection = getCon()
		cursor = connection.cursor()
		cursor.execute("""CREATE TABLE IF NOT EXISTS globals
			(
				ref_bonus int(20) not null default 200000,
				bonus_max int(20) not null default 200000,
				sub_bonus int(20) not null default 100000,
				mnozhitel tinyint(4) not null default 1
			)
			CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci""")
		connection.commit()
		connection.close()

	def insert():
		connection = getCon()
		cursor = connection.cursor()
		cursor.execute("INSERT INTO globals (ref_bonus) VALUES (200000)")
		connection.commit()
		connection.close()

	def get(var):
		connection = getCon()
		cursor = connection.cursor()
		cursor.execute(f"SELECT {var} FROM globals")
		connection.commit()
		return cursor.fetchone()[var]
		connection.close()

	def update(var, value):
		connection = getCon()
		cursor = connection.cursor()
		cursor.execute(f"UPDATE globals SET {var} = {value} WHERE id = 1")
		connection.commit()
		connection.close()

def rezerv():
	return merchant.get_balance(705783864)["705783864"]/1000

def formarter(var, symbol=" "):
	return '{:,}'.format(var).replace(',', symbol)

def number_format(var):
	if str(type(var)) == "<class 'str'>":
		var = var.lower()
		if "к" in var:
			var = var.replace("к", "000")
		elif "." in var:
			var = var.split(".")
		elif " " in var:
			var = var.split(" ")
		elif "-" in var:
			var = var.split("-")
		elif "млн" in var:
			var = var.replace("млн", "000000")
		elif "тыс" in var:
			var = var.replace("тыс", "000")
		elif "млрд" in var:
			var = var.replace("млрд", "000000000")
	return int(var)

@merchant.payment_handler(handler_type='longpoll')
def vkc_payment(data):
	try:
		mnozhitel = globals.get("mnozhitel")
		user_id = int(data['from_id'])
		amounts = floor(int(data['amount']) / 1000)
		amount = amounts
		if amount >= 200000:
			amount = floor(amounts * mnozhitel)
		if amounts >= 1000000 and amounts < 10000000:
			amount = floor(amounts + 350000)
		elif amounts >= 10000000:
			amount = floor(amounts + 5000000)
		dollars_get = floor(amount*10)
		user.update(user_id, 'dollars', user.get(user_id, 'dollars') + dollars_get)
		user.update(user_id, 'invest_balance', user.get(user_id, 'invest_balance') + amount)
		user.update(user_id, 'all_topup', user.get(user_id, 'all_topup') + amounts)
	except:
		pass

def start_vkc():
	merchant.run_longpoll(tx=[1], interval=2)

threading.Thread(target=start_vkc).start()

menu_keyboard = Keyboard(one_time=False)
menu_keyboard.add(Text("🏆 Топы"))
menu_keyboard.add(Text("📈 Инвест"), color=KeyboardButtonColor.POSITIVE)
menu_keyboard.add(Text("📒 Профиль"))
menu_keyboard.row()
menu_keyboard.add(OpenLink("https://vk.com/coin#x705783864_1000_1337_1", "📥 Пополнить"))
menu_keyboard.add(Text("📤 Вывод"), color=KeyboardButtonColor.NEGATIVE)
menu_keyboard.get_json()

profile_keyboard = Keyboard(inline=True)
profile_keyboard.add(Text("👑"))
profile_keyboard.add(Text("🏢"))
profile_keyboard.add(Text("🎫"))
profile_keyboard.add(Text("🎁"), color=KeyboardButtonColor.POSITIVE)
profile_keyboard.row()
profile_keyboard.add(Text("⚙ Настройки"))
profile_keyboard.get_json()

top_keyboard = Keyboard(inline=True)
top_keyboard.add(Text('💸 По доходу'), color=KeyboardButtonColor.POSITIVE)
top_keyboard.add(Text('💰 По долларам'), color=KeyboardButtonColor.PRIMARY)
top_keyboard.row()
top_keyboard.add(Text('🏢 По населению города'), color=KeyboardButtonColor.PRIMARY)
top_keyboard.row()
top_keyboard.add(Text('⏳ Топ недели'))
top_keyboard.add(Text('📑 Общий топ'))
top_keyboard.get_json()

vip_keyboard = Keyboard(inline=True)
vip_keyboard.add(Text('✔ Купить VIP'), color=KeyboardButtonColor.POSITIVE)
vip_keyboard.get_json()

donate_keyboard = Keyboard(inline=True)
donate_keyboard.add(OpenLink('https://vk.com/coin#t705783864', '🤠 Владелец'))
donate_keyboard.row()
donate_keyboard.add(OpenLink('https://vk.com/coin#t498475943', '👻 Кодер'))
donate_keyboard.get_json()

city_keyboard = Keyboard(inline=True)
city_keyboard.add(Text("💰 Снять с казны"), color=KeyboardButtonColor.POSITIVE)
city_keyboard.row()
city_keyboard.add(Text("🏙 Город здания"))
city_keyboard.add(Text("🥳 Город события"))
city_keyboard.get_json()

user.create()
globals.create()
try:
	globals.get("ref_bonus")
except:
	globals.insert()

print("Инвест запущен! Можно закрывать окно и идти дрочить :)")

try:

	@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
	async def joingroup(event: GroupTypes.GroupJoin):
		user_id = event.object.user_id
		if user.check(user_id):
			if user.get(user_id, 'subscribe') == 0:
				subscribe_bonus = globals.get("sub_bonus")
				user.update(user_id, 'invest_balance', user.get(user_id, 'invest_balance') + subscribe_bonus)
				user.update(user_id, 'subscribe', 1)
				await bot.api.messages.send(peer_id=user_id, message=f"✅ Спасибо за подписку! Лови бонус: {formarter(subscribe_bonus)} VK Coin", random_id=randint(-1000000000,1000000000))
			else:
				await bot.api.messages.send(peer_id=user_id, message="❌ Зачем так хитрить?) Ты уже поймал бонус за подписку)", random_id=randint(-1000000000,1000000000))

	@bot.on.message(text = "гор <number:int> <amount:int>")
	async def city_build(message: Message, number=1, amount=1):
		user_id = message.from_id
		if user.check(user_id):
			balance = user.get(user_id, 'dollars')
			number = int(number)
			amount = int(amount)
			types = 1
			population_plus = 0
			if number == 1:
				house = "Деревянный дом"
				price = 50000
				population_plus = randint(1,3)
				income = 500
			elif number == 2:
				house = "Хижина"
				price = 100000
				population_plus = randint(1,5)
				income = 1000
			elif number == 3:
				house = "Двухэтажка"
				price = 500000
				population_plus = randint(1,20)
				income = 50000
			elif number == 4:
				house = "Трёхэтажка"
				price = 750000
				population_plus = randint(1,30)
				income = 75000
			elif number == 5:
				house = "Многоэтажка"
				price = 1000000
				population_plus = randint(1,50)
				income = 100000
			elif number == 6:
				house = "Небоскрёб"
				price = 2500000
				population_plus = randint(1,100)
				income = 250000
			elif number == 7:
				house = "Деревообрабатывающый завод"
				price = 100000
				service_costs = 1000
				happy_low = 1
				income = 10000
				types = 2
			elif number == 8:
				house = "Маталлообрабатывающий завод"
				price = 150000
				service_costs = 1500
				happy_low = 1
				income = 15000
				types = 2
			elif number == 9:
				house = "Машиностроительный завод"
				price = 300000
				service_costs = 3000
				happy_low = 2
				income = 30000
				types = 2
			elif number == 10:
				house = "Механический завод"
				price = 350000
				service_costs = 3500
				happy_low = 3
				income = 35000
				types = 2
			elif number == 11:
				house = "Вагоностроительный завод"
				price = 400000
				service_costs = 4000
				happy_low = 3
				income = 40000
				types = 2
			elif number == 12:
				house = "Медицинский завод"
				price = 420000
				service_costs = 4200
				happy_low = 3
				income = 42000
				types = 2
			elif number == 13:
				house = "Нефтеперерабатывающий завод"
				price = 800000
				service_costs = 8000
				happy_low = 4
				income = 80000
				types = 2
			elif number == 14:
				house = "Химический завод"
				price = 1200000
				service_costs = 12000
				happy_low = 4
				income = 120000
				types = 2
			elif number == 15:
				house = "Детский сад"
				price = 100000
				service_costs = 2000
				population_plus = randint(1,10)
				happy_up = 1
				income = 10000
				types = 3
			elif number == 16:
				house = "Младшая школа"
				price = 150000
				service_costs = 2500
				population_plus = randint(1,15)
				happy_up = 1
				income = 15000
				types = 3
			elif number == 17:
				house = "Средняя школа"
				price = 250000
				service_costs = 3500
				population_plus = randint(1,25)
				happy_up = 1
				income = 25000
				types = 3
			elif number == 18:
				house = "Гимназия"
				price = 300000
				service_costs = 4000
				population_plus = randint(1,30)
				happy_up = 1
				income = 30000
				types = 3
			elif number == 19:
				house = "Лицей"
				price = 400000
				service_costs = 5000
				population_plus = randint(1,40)
				happy_up = 2
				income = 40000
				types = 3
			elif number == 20:
				house = "Колледж"
				price = 500000
				service_costs = 6000
				population_plus = randint(1,50)
				happy_up = 2
				income = 50000
				types = 3
			elif number == 21:
				house = "Университет"
				price = 750000
				service_costs = 7500
				population_plus = randint(1,75)
				happy_up = 2
				income = 75000
				types = 3
			elif number == 22:
				house = "Городской парк"
				price = 200000
				population_plus = randint(1,50)
				happy_up = 1
				income = 2000
				types = 4
			elif number == 23:
				house = "Детская площадка"
				price = 350000
				population_plus = randint(1,85)
				happy_up = 1
				income = 3500
				types = 4
			elif number == 24:
				house = "Пляж"
				price = 500000
				population_plus = randint(1,120)
				happy_up = 1
				income = 5000
				types = 4
			elif number == 25:
				house = "Набережная"
				price = 800000
				population_plus = randint(1,300)
				happy_up = 1
				income = 8000
				types = 4
			elif number == 26:
				house = "Парк аттракционов"
				price = 1000000
				population_plus = randint(1,800)
				happy_up = 2
				income = 10000
				types = 4
			elif number == 27:
				house = "Музей"
				price = 2000000
				population_plus = randint(1,2000)
				happy_up = 2
				income = 20000
				types = 4
			elif number == 28:
				house = "Театр"
				price = 2200000
				population_plus = randint(1,2200)
				happy_up = 2
				income = 22000
				types = 4
			elif number == 29:
				house = "Отель"
				price = 2500000
				population_plus = randint(1,3000)
				happy_up = 3
				income = 25000
				types = 4
			elif number == 30:
				house = "Ветряная электростанция"
				price = 25000
				service_costs = 500
				happy_low = 1
				income = 2500
				types = 5
			elif number == 31:
				house = "Блочно-контейнерная электростанция"
				price = 100000
				service_costs = 2000
				happy_low = 2
				income = 10000
				types = 5
			elif number == 32:
				house = "Волновая электростанция"
				price = 300000
				service_costs = 6000
				happy_low = 2
				income = 30000
				types = 5
			elif number == 33:
				house = "Дизельная электростанция"
				price = 650000
				service_costs = 13000
				happy_low = 3
				income = 65000
				types = 5
			elif number == 34:
				house = "Приливная электростанция"
				price = 800000
				service_costs = 16000
				happy_low = 3
				income = 80000
				types = 5
			elif number == 35:
				house = "Солнечная электростанция"
				price = 900000
				service_costs = 18000
				happy_low = 4
				income = 90000
				types = 5
			elif number == 36:
				house = "Тепловая электростанция"
				price = 1300000
				service_costs = 26000
				happy_low = 5
				income = 130000
				types = 5
			elif number == 37:
				house = "Атомная электростанция"
				price = 1600000
				service_costs = 32000
				happy_low = 5
				income = 160000
				types = 5
			elif number == 38:
				house = "Водонапорная башня"
				price = 25000
				service_costs = 500
				happy_up = 1
				income = 2500
				types = 6
			elif number == 39:
				house = "Водонасосная станция"
				price = 120000
				service_costs = 2400
				happy_up = 1
				income = 12000
				types = 6
			elif number == 40:
				house = "Водоочистная станция"
				price = 400000
				service_costs = 8000
				happy_up = 1
				income = 40000
				types = 6
			elif number == 41:
				house = "Экологичная водоочистная станция"
				price = 800000
				service_costs = 16000
				happy_up = 3
				income = 80000
				types = 6
			elif number == 42:
				house = "Урна"
				price = 10000
				happy_up = 0
				income = 1000
				types = 7
			elif number == 43:
				house = "Мусорный контейнер"
				price = 50000
				happy_up = 1
				income = 5000
				types = 7
			elif number == 44:
				house = "Малая станция переработки"
				price = 100000
				happy_up = 1
				income = 10000
				types = 7
			elif number == 45:
				house = "Обычная станция переработки"
				price = 250000
				happy_up = 1
				income = 25000
				types = 7
			elif number == 46:
				house = "Большая станция переработки"
				price = 550000
				happy_up = 1
				income = 55000
				types = 7
			try:
				price *= amount
				if balance >= price:
					if types == 1:
						balance -= price
						user.update(user_id, 'CityBuildings', user.get(user_id, 'CityBuildings') + amount)
						user.update(user_id, 'CityPopulation', user.get(user_id, 'CityPopulation') + (population_plus * amount))
						user.update(user_id, 'dollars', balance)
						user.update(user_id, 'CityTaxes', user.get(user_id, 'CityTaxes') + (income * amount))
						await message.answer(f"✅ Вы успешно построили {amount} шт. <<{house}>> за {formarter(price)}$")
					elif types == 2:
						balance -= price
						happy = user.get(user_id, 'CityHappy')
						happy_low *= amount
						if happy >= happy_low:
							user.update(user_id, 'CityHappy', happy - happy_low)
						else:
							user.update(user_id, 'CityHappy', 0)
						user.update(user_id, 'CityBuildings', user.get(user_id, 'CityBuildings') + amount)
						user.update(user_id, 'dollars', balance)
						user.update(user_id, 'CityTaxes', user.get(user_id, 'CityTaxes') + (income * amount))
						user.update(user_id, 'CityServiceCosts', user.get(user_id, 'CityServiceCosts') + (service_costs * amount))
						await message.answer(f"✅ Вы успешно построили {amount} шт. <<{house}>> за {formarter(price)}$")
					elif types == 3:
						balance -= price
						happy = user.get(user_id, 'CityHappy')
						happy_up *= amount
						if happy <= 90:
							if happy_up > 10:
								user.update(user_id, 'CityHappy', 100)
							else:
								user.update(user_id, 'CityHappy', happy + happy_up)
						user.update(user_id, 'CityBuildings', user.get(user_id, 'CityBuildings') + amount)
						user.update(user_id, 'dollars', balance)
						user.update(user_id, 'CityTaxes', user.get(user_id, 'CityTaxes') + (income * amount))
						user.update(user_id, 'CityServiceCosts', user.get(user_id, 'CityServiceCosts') + (service_costs * amount))
						user.update(user_id, 'CityPopulation', user.get(user_id, 'CityPopulation') + (population_plus * amount))
						await message.answer(f"✅ Вы успешно построили {amount} шт. <<{house}>> за {formarter(price)}$")
					elif types == 4:
						balance -= price
						happy = user.get(user_id, 'CityHappy')
						happy_up *= amount
						if happy <= 90:
							if happy_up > 10:
								user.update(user_id, 'CityHappy', 100)
							else:
								user.update(user_id, 'CityHappy', happy + happy_up)
						user.update(user_id, 'CityBuildings', user.get(user_id, 'CityBuildings') + amount)
						user.update(user_id, 'dollars', balance)
						user.update(user_id, 'CityTaxes', user.get(user_id, 'CityTaxes') + (income * amount))
						user.update(user_id, 'CityPopulation', user.get(user_id, 'CityPopulation') + (population_plus * amount))
						await message.answer(f"✅ Вы успешно построили {amount} шт. <<{house}>> за {formarter(price)}$")
					elif types == 5:
						balance -= price
						happy = user.get(user_id, 'CityHappy')
						happy_low *= amount
						if happy >= happy_low:
							user.update(user_id, 'CityHappy', happy - happy_low)
						else:
							user.update(user_id, 'CityHappy', 0)
						user.update(user_id, 'CityBuildings', user.get(user_id, 'CityBuildings') + amount)
						user.update(user_id, 'dollars', balance)
						user.update(user_id, 'CityTaxes', user.get(user_id, 'CityTaxes') + (income * amount))
						user.update(user_id, 'CityEnergyCosts', user.get(user_id, 'CityEnergyCosts') + (service_costs * amount))
						await message.answer(f"✅ Вы успешно построили {amount} шт. <<{house}>> за {formarter(price)}$")
					elif types == 6:
						balance -= price
						happy = user.get(user_id, 'CityHappy')
						happy_up *= amount
						if happy <= 90:
							if happy_up > 10:
								user.update(user_id, 'CityHappy', 100)
							else:
								user.update(user_id, 'CityHappy', happy + happy_up)
						user.update(user_id, 'CityBuildings', user.get(user_id, 'CityBuildings') + amount)
						user.update(user_id, 'dollars', balance)
						user.update(user_id, 'CityTaxes', user.get(user_id, 'CityTaxes') + (income * amount))
						user.update(user_id, 'CityWaterCosts', user.get(user_id, 'CityWaterCosts') + (service_costs * amount))
						await message.answer(f"✅ Вы успешно построили {amount} шт. <<{house}>> за {formarter(price)}$")
					elif types == 7:
						balance -= price
						happy = user.get(user_id, 'CityHappy')
						happy_up *= amount
						if happy <= 90:
							if happy_up > 10:
								user.update(user_id, 'CityHappy', 100)
							else:
								user.update(user_id, 'CityHappy', happy + happy_up)
						user.update(user_id, 'CityBuildings', user.get(user_id, 'CityBuildings') + amount)
						user.update(user_id, 'dollars', balance)
						user.update(user_id, 'CityTaxes', user.get(user_id, 'CityTaxes') + (income * amount))
						await message.answer(f"✅ Вы успешно построили {amount} шт. <<{house}>> за {formarter(price)}$")
					else:
						await message.answer("❌ Введите: Гор (Номер постройки)")
				else:
					await message.answer("❌ У вас недостаточно средств для построения!")
			except:
				pass
		else:
			await message.answer("❌ А может для начала зарегистрируемся по команде <<Начать>>?")

	@bot.on.message(text = "событие <number:int>")
	async def city_event(message: Message, number=1):
		user_id = message.from_id
		if user.check(user_id):
			balance = user.get(user_id, 'dollars')
			number = int(number)
			types = 1
			if number == 1:
				event = "Праздничный концерт"
				price = 100000
				population_plus = randint(1,100)
			elif number == 2:
				event = "Ярмарку"
				price = 350000
				population_plus = randint(1,500)
			elif number == 3:
				event = "Недельный отдых"
				price = 750000
				happy_up = randint(1,5) 
				types = 2
			elif number == 4:
				event = "Парад к 9 мая"
				price = 1000000
				happy_up = randint(1,5)
				types = 2
			elif number == 5:
				event = "Туристический поход"
				price = 1350000
				population_plus = randint(1,2000)
			elif number == 6:
				event = "День эколога"
				price = 2000000
				population_plus = randint(1,5000)
			try:
				last_time = user.get(user_id, 'CityEvent_time')
				now = floor(time.time())
				timer = now-last_time
				if timer >= 86400:
					if balance >= price:
						if types == 1:
							balance -= price
							user.update(user_id, 'dollars', balance)
							user.update(user_id, 'CityEvent_time', floor(time.time()))
							chance = randint(1,100)
							if chance <= 70:
								user.update(user_id, 'CityPopulation', user.get(user_id, 'CityPopulation') + population_plus)
								await message.answer(f"✅ Вы провели {event} и получили +{formarter(population_plus)} новых жителей!")
							else:
								await message.answer(f"❌ Вы провели событие <<{event}>>, которое никому не понравилось :<")
						else:
							balance -= price
							user.update(user_id, 'dollars', balance)
							user.update(user_id, 'CityEvent_time', floor(time.time()))
							chance = randint(1,100)
							if chance <= 50:
								if user.get(user_id, 'CityHappy') <= 95:
									user.update(user_id, 'CityHappy', user.get(user_id, 'CityHappy') + happy_up)
									await message.answer(f"✅ Вы провели {event} и получили +{formarter(happy_up)} счастья!")
								else:
									rand_bucks = randint(100000,350000)
									user.update(user_id, 'dollars', balance+rand_bucks)
									await message.answer(f"✅ Вы провели {event} и получили +{formarter(rand_bucks)}$!")
							else:
								await message.answer(f"❌ Вы провели событие <<{event}>>, которое никому не понравилось :<")
					else:
						await message.answer("❌ У вас недостаточно средств для проведения события!")
				else:
					format_time = time.gmtime(86400-timer)
					timer = time.strftime("%H час. %M мин. %S сек.", format_time)
					await message.answer(f"⏱ Следующее событие можно будет провести через {timer}")
			except:
				pass
		else:
			await message.answer("❌ А может для начала зарегистрируемся по команде <<Начать>>?")

	@bot.on.message(text = "ник <nick>")
	async def newnickname(message: Message, nick):
		user_id = message.from_id
		if user.check(user_id):
			now = user.get(user_id, 'tag')
			if len(nick) <= 20:
				if "[" in now:
					tag = f"[id{user_id}|{nick}]"
				else:
					tag = nick
				user.update(user_id, "tag", tag)
				await message.answer(f"😏 {tag}, крутой никнейм!")
			else:
				await message.answer("❌ Длина никнейма не должна превышать 20 Символов!")
		else:
			await message.answer("❌ А может для начала зарегистрируемся по команде <<Начать>>?")
	
	@bot.on.message(text = "гипер")
	async def gipperlink(message):
		user_id = message.from_id
		if user.check(user_id):
			now = user.get(user_id, 'tag')
			if not "[" in now:
				tag = f"[id{user_id}|{now}]"
				user.update(user_id, 'tag', tag)
				await message.answer(f"✅ {tag}, теперь ваш никнейм содержит ссылку!")
			else:
				tag = "".join(now.split("|")[1]).split("]")[0]
				user.update(user_id, 'tag', tag)
				await message.answer(f"❌ {tag}, теперь ваш никенйм не содержит ссылку!")
		else:
			await message.answer("❌ А может для начала зарегистрируемся по команде <<Начать>>?")


	@bot.on.message(text = "автоинвест")
	async def autoinvest(message):
		user_id = message.from_id
		if user.check(user_id):
			if user.get(user_id, 'autoinvest'):
				user.update(user_id, 'autoinvest', 0)
				await message.answer("❌ Авто инвестирование отключено!")
			else:
				user.update(user_id, 'autoinvest', 1)
				await message.answer("✅ Авто инвестирование включено!")
		else:
			await message.answer("❌ А может для начала зарегистрируемся по команде <<Начать>>?")

	@bot.on.message(text = ["реф <amount>", "реф <amount:int>"])
	async def newrefbonus(message: Message, amount=1):
		user_id = message.from_id
		if user_id in admin_ids:
			try:
				try:
					amount = number_format(amount)
				except:
					amount = 150000
				globals.update("ref_bonus", amount)
				await message.answer(f"👥 Теперь бонус за реферала: {formater(amount)} VK Coin")
			except:
				pass

	@bot.on.message(text = ["бонус <amount>", "бонус <amount:int>"])
	async def newbonus(message: Message, amount=1):
		user_id = message.from_id
		if user_id in admin_ids:
			try:
				try:
					amount = number_format(amount)
				except:
					amount = 200000
				globals.update("bonus_max", amount)
				await message.answer(f"🎁 Теперь максимальный ежедневный бонус: {formarter(amount)} VK Coin")
			except:
				pass

	@bot.on.message(text = ["подписка <amount>", "подписка <amount:int>"])
	async def newsubbonus(message: Message, amount=1):
		user_id = message.from_id
		if user_id in admin_ids:
			try:
				try:
					amount = number_format(amount)
				except:
					amount = 100000
				globals.update("sub_bonus", amount)
				await message.answer(f"🔥 Теперь бонус за подписку: {formarter(amount)} VK Coin")
			except:
				pass

	@bot.on.message(text = ["выдать <id:int> <amount>", "выдать <id:int> <amount:int>", "выдать <id> <amount>", "выдать <id> <amount:int>", "выдать <amount>", "выдать <amount:int>"])
	async def give(message: Message, id=0, amount=1):
		user_id = message.from_id
		if user_id in admin_ids:
			try:
				id = message.reply_message.from_id
			except:
				try:
					id = int(id)
				except:
					try:
						id = int("".join(id.split("|")[:-1]).split("id")[1])
					except:
						id = 0
			if id > 0:
				try:
					amount = number_format(amount)
				except:
					amount = 0
				if amount > 0:
					try:
						user.update(id, 'invest_balance', user.get(id, 'invest_balance') + amount)
						tag = user.get(id, 'tag')
						if "[" in tag:
							await message.answer(f"💸 Игроку {tag} было выдано {formarter(amount)} VK Coin на инвест. баланс")
						else:
							await message.answer(f"💸 [id{id}|Игроку] было выдано {formarter(amount)} VK Coin на инвест. баланс")
					except:
						await message.answer("❌ Пользователь не зарегистрирован :<")
				else:
					await message.answer("❌ Смысл выдачи 0 VK Coin?)")
			else:
				await message.answer("❌ Указан неверный VK ID!")

	@bot.on.message(text = ["обнулить <id>", "обнулить <id:int>", "обнулить"])
	async def go_default(message: Message, id=0):
		user_id = message.from_id
		if user_id in admin_ids:
			try:
				id = message.reply_message.from_id
			except:
				try:
					id = int(id)
				except:
					try:
						id = int("".join(id.split("|")[:-1]).split("id")[1])
					except:
						id = 0
			if id > 0:
				try:
					user.update(id, 'invest_balance', 0)
					tag = user.get(user_id, 'tag')
					if "[" in tag:
						await message.answer(f"😓 Игрок {user.get(id, 'tag')} лишился инвест. баланса")
					else:
						await message.answer(f"😓 [id{id}|Игрок] лишился инвест. баланса")
				except:
					await message.answer("❌ Пользователь не зарегистрирован :<")
			else:
				await message.answer("❌ Указан неверный VK ID!")

	@bot.on.message(text = ["акция <x:int>", "а <x:int>"])
	async def promotion_start(message: Message, x=1):
		user_id = message.from_id
		if user_id in admin_ids:
			globals.update('mnozhitel', x)
			await message.answer(f"🤑 Теперь при пополнении от 200 000 VK Coin, игрок получит в {x}x раз больше!")

	@bot.on.message(text = ["переводы <id>", "переводы <id:int>", "п <id>", "п <id:int>", "переводы", "п"])
	async def transactions(message: Message, id=0):
		user_id = message.from_id
		if user_id in admin_ids:
			try:
				id = message.reply_message.from_id
			except:
				try:
					id = int(id)
				except:
					try:
						id = int("".join(id.split("|")[:-1]).split("id")[1])
					except:
						id = 0
			if id > 0:
				transactions = merchant.get_transactions(tx=[1])
				text = f"💲 Переводы от {user.get(id, 'tag')}:\n"
				amounts = 0
				for num, us in enumerate(transactions):
					if us['from_id'] == id:
						amount = floor(int(us['amount']) / 1000)
						amounts += amount
						data = time.strftime("%m-%d %H:%M:%S", time.gmtime(int(us['created_at'])))
						text += f"💸 VKC: {formarter(amount)} ({data})\n"
				await message.answer(f"{text}\n💰 +{formarter(amounts)} VK Coin")
			else:
				await message.answer("❌ Указан неверный VK ID!")

	@bot.on.message()
	async def main(message):
		text = message.text.lower()
		user_id = message.from_id
		if user.check(user_id):
			tag = user.get(user_id, 'tag')
			if text in ["проф", "профиль", "👤 профиль", "📒 профиль"]:
				invest_balance = user.get(user_id, 'invest_balance')
				last_time = user.get(user_id, 'last_time')
				if last_time == 0:
					last_time = floor(time.time())
					user.update(user_id, 'last_time', last_time)
				now = floor(time.time())
				cash = user.get(user_id, 'dohod_everyday')
				cash_hours = floor(cash/86400*3600)
				cash_hours = 1 if cash_hours < 1 else cash_hours
				balance = user.get(user_id, 'balance')
				timer = now - last_time
				if timer >= 3600:
					cash_get = floor(timer/3600*cash_hours)
					if user.get(user_id, 'autoinvest'):
						all_invest = user.get(user_id, 'all_invest')
						invest_balance += cash_get
						if invest_balance >= 1000:
							all_invest += invest_balance
							invest = floor(invest_balance/30) if user.get(user_id, 'vip') == 1 else floor(invest_balance/35)
							cash += invest
							user.update(user_id, 'dohod_everyday', cash)
							user.update(user_id, 'invest_balance', 0)
							user.update(user_id, 'all_invest', all_invest)
							user.update(user_id, 'all_invest_week', user.get(user_id, 'all_invest_week') + invest_balance)
							user.update(user_id, 'last_time', floor(time.time()))
							invest_balance = 0
						else:
							balance += cash_get
							user.update(user_id, 'balance', balance)
							user.update(user_id, 'last_time', floor(time.time()))
					else:
						balance += cash_get
						user.update(user_id, 'balance', balance)
						user.update(user_id, 'last_time', floor(time.time()))
				vip = "✔" if user.get(user_id, 'vip') else "🚫"
				await message.answer(f"""📒 {user.get(user_id, 'tag')}:
⠀💸 Инвестиционный баланс: {formarter(invest_balance)} VK Coin
⠀🔥 Заработано: {formarter(balance)} VK Coin
⠀⏲ В час: {formarter(cash_hours)} VK Coin

💰 Долларов: {formarter(user.get(user_id, 'dollars'))}$
👑 VIP Статус: {vip}"""	, keyboard=profile_keyboard)

			elif text in ["меню", "м"]:
				await message.answer("📄 Главное меню:", keyboard=menu_keyboard)

			elif text == "⚙ настройки":
				await message.answer("""⚙ Настройки:

📒 Мой профиль:
⠀👤 Ник [Новый никнейм] - изменить никнейм
⠀📌 Гипер - вкл/выкл гиперссылку в нике

📚 Другое:
⠀📈 Автоинвест - вкл/выкл авто инвестирование средств из <<баланса для вывода>>""")

			elif text in ["📈 инвестировать", "инвест", "инвестировать", "📈 инвест"]:
				invest_balance = user.get(user_id, 'invest_balance')
				all_invest = user.get(user_id, 'all_invest')
				if invest_balance >= 1000:
					cash = user.get(user_id, 'dohod_everyday')
					all_invest += invest_balance
					invest = floor(invest_balance/30) if user.get(user_id, 'vip') == 1 else floor(invest_balance/35)
					cash += invest
					user.update(user_id, 'dohod_everyday', cash)
					user.update(user_id, 'invest_balance', 0)
					user.update(user_id, 'all_invest', all_invest)
					user.update(user_id, 'all_invest_week', user.get(user_id, 'all_invest_week') + invest_balance)
					await message.answer(f"""💸 {tag}, вы инвестировали {formarter(invest_balance)} VK Coin
⏲ Теперь вы получаете: {formarter(floor(cash/86400*3600))} VKC/Час""")
				else:
					await message.answer(f"💸 {tag}, инвестировать можно от 1000 VK Coin")

			elif text in ["👑", "вип", "випка"]:
				if not user.get(user_id, 'vip'):
					await message.answer("""👑 Преимущества VIP Статуса:
- Больше процентов при инвестировании;
- 1% от суммы вывода (До 500 000 VK Coin) на инвестиционный баланс;
- Отметка в топах;

💸 Цена: 8 500 000 VK Coin""", keyboard=vip_keyboard)
				else:
					await message.answer("👑 У вас уже имеется VIP Статус :)")

			elif text == "✔ купить vip":
				if not user.get(user_id, 'vip'):
					invest_balance = user.get(user_id, 'invest_balance')
					if invest_balance >= 8500000:
						invest_balance -= 8500000
						user.update(user_id, 'invest_balance', invest_balance)
						user.update(user_id, 'vip', 1)
						await message.answer(f"✔ {tag}, спасибо за покупку VIP Статуса! Теперь вы официально являетесь ещё одним обладателем VIP :)")
					else:
						await message.answer(f"💰 Нехватка {formarter(8500000 - invest_balance)} VK Coin для покупки VIP!")
				else:
					await message.answer("👑 У вас уже имеется VIP Статус :)")

			elif text in ["вывод", "вывести", "📤 вывести", "📤 вывод"]:
				vip = user.get(user_id, 'vip')
				balance = user.get(user_id, 'balance')
				rezerv_s = floor(rezerv())
				if balance >= 1:
					if rezerv_s > balance:
						user.update(user_id, 'balance', 0)
						if vip:
							if balance <= 500000:
								procent=floor(balance/100)
								user.update(user_id, 'invest_balance', user.get(user_id, 'invest_balance') + procent)
						merchant.send_payment(to_id=user_id, amount=balance*1000, mark_as_merchant=True)
						await message.answer(f"""🔥 Было переведено: {formarter(balance)} VK Coin :)
🥺 Может оставите свой отзыв? - https://vk.cc/ccFl2i""")
						if not user_id in admin_ids:
							if "[" in tag:
								await bot.api.messages.send(peer_id=2000000001, message=f"""😭 Новый вывод на сумму {formarter(balance)} VK Coin
👤: {tag}""", random_id=randint(-1000000000,1000000000))
							else:
								await bot.api.messages.send(peer_id=2000000001, message=f"""😭 Новый вывод на сумму {formarter(balance)} VK Coin
👤: [id{user_id}|{tag}]""", random_id=randint(-1000000000,1000000000))
					else:
						await message.answer("😲 На балансе бота недостаточно средств для вывода")
				else:
					await message.answer(f"🥺 {tag}, ваш баланс пуст :(")

			elif text in ["админка", "админ", "адм"]:
				if user_id in admin_ids:
					await message.answer(f"""📄 {tag}, список админ команд:
⠀💰 Выдать (VK ID) (Сумма)
⠀💸 Обнулить (VK ID)
⠀✅ Акция (Множитель) | А (Множитель)
⠀🚫 Акция стоп | Ас
⠀💳 Резерв | Рез
⠀💲 Переводы (VK ID) | П (VK ID)
---------------------------------------------
⠀👥 Реф (Сумма)
⠀🎁 Бонус (Сумма)
⠀🔥 Подписка (Сумма)""")
			
			elif text in ["акция стоп", "ас"]:
				if user_id in admin_ids:
					globals.update("mnozhitel", 1)
					await message.answer(f"❌ Акция завершена! Те, кто не успели пополнить с акцией - лошки :>")

			elif text in ["резерв", "рез"]:
				if user_id in admin_ids:
					await message.answer(f"""🌀: {formarter(rezerv())} VK Coin""")

			elif text in ["реф", "рефка", "реферал", "рефералка", "👥 рефералка", "🎫"]:
				await message.answer(f"""🎫 {user.get(user_id, 'tag')}, за одного реферала вы получаете: {formarter(globals.get("ref_bonus"))} VK Coin.
📌 Ссылка: https://vk.me/public212419708?ref={user_id}""")

			elif text in ["топ", "топы", "🏆 топы"]:
				await message.answer("❔ Какой топ вас интересует?", keyboard=top_keyboard)

			elif text == "💸 по доходу":
				users = user.get_top('dohod_everyday', None)
				text = "💸 Топ по доходу VKC/Сутки:\n\n"
				for num, us in enumerate(users):
					if num <= 9:
						text += f"\n{top[num]} 👑 {us['tag']} - {formarter(us['dohod_everyday'])} VK Coin" if us['vip'] else f"\n{top[num]} {us['tag']} - {formarter(us['dohod_everyday'])} VK Coin"
					else:
						if us['vk_id'] == user_id:
							text += f"\n------------------------------------------------------\n🔢 Вы находитесь на {num+1} месте, имея доход: {formarter(us['dohod_everyday'])} VKC/Сутки"
							break
				await message.answer(text)

			elif text == "⏳ топ недели":
				users = user.get_top('all_invest_week', None)
				text = "⏳ Топ по инвесту за неделю:\n\n"
				for num, us in enumerate(users):
					if num <= 9:
						text += f"\n{top[num]} 👑 {us['tag']} - {formarter(us['all_invest_week'])} VK Coin" if us['vip'] else f"\n{top[num]} {us['tag']} - {formarter(us['all_invest_week'])} VK Coin"
					else:
						if us['vk_id'] == user_id:
							text += f"\n------------------------------------------------------\n🔢 Вы находитесь на {num+1} месте, инвестировав: {formarter(us['all_invest_week'])} VKC"
							break
				await message.answer(text)
			elif text == "📑 общий топ":
				users = user.get_top('all_invest', None)
				text = "💸 Топ по инвесту за всё время:\n\n"
				for num, us in enumerate(users):
					if num <= 9:
						text += f"\n{top[num]} 👑 {us['tag']} - {formarter(us['all_invest'])} VK Coin" if us['vip'] else f"\n{top[num]} {us['tag']} - {formarter(us['all_invest'])} VK Coin"
					else:
						if us['vk_id'] == user_id:
							text += f"\n------------------------------------------------------\n🔢 Вы находитесь на {num+1} месте, инвестировав: {formarter(us['all_invest'])} VKC"
							break
				await message.answer(text)

			elif text == "💰 по долларам":
				users = user.get_top('dollars', None)
				text = "💰 Топ по долларам:\n\n"
				for num, us in enumerate(users):
					if num <= 9:
						text += f"\n{top[num]} 👑 {us['tag']} - {formarter(us['dollars'])}$" if us['vip'] else f"\n{top[num]} {us['tag']} - {formarter(us['dollars'])}$"
					else:
						if us['vk_id'] == user_id:
							text += f"\n------------------------------------------------------\n🔢 Вы находитесь на {num+1} месте, имея: {formarter(us['dollars'])}$"
							break
				await message.answer(text)

			elif text == "🏢 по населению города":
				users = user.get_citytop()
				text = "🏢 Топ по населению города:\n\n"
				for num, us in enumerate(users):
					if num <= 9:
						text += f"\n{top[num]} 👑 У {us['tag']} - {formarter(us['CityPopulation'])} чел." if us['vip'] else f"\n{top[num]} У {us['tag']} - {formarter(us['CityPopulation'])} чел."
					else:
						if us['vk_id'] == user_id:
							text += f"\n------------------------------------------------------\n🔢 Вы находитесь на {num+1} месте, имея население: {formarter(us['CityPopulation'])} чел."
							break
				await message.answer(text)

			elif text == "топ поп":
				if user_id in admin_ids:
					users = user.get_top('all_topup', 30)
					text = "🔥 Топ по пополнениям:\n\n"
					for num, us in enumerate(users):
						place = f"🏅 {num+1}" if num >= 10 else top[num]
						text += f"{place} 👑 {us['tag']} - {formarter(us['all_topup'])} VK Coin\n" if us['vip'] else f"{place} {us['tag']} - {formarter(us['all_topup'])} VK Coin\n"
					await message.answer(text)

			elif text in ["бонус", "🎁 бонус", "🎁"]:
				all_topup = user.get(user_id, 'all_topup')
				if all_topup >= 2000000:
					bonus_time = user.get(user_id, 'bonus_time')
					now = floor(time.time())
					timer = now - bonus_time
					if timer >= 86400:
						rand = randint(1, globals.get("bonus_max"))
						user.update(user_id, 'invest_balance', user.get(user_id, 'invest_balance') + rand)
						user.update(user_id, 'bonus_time', floor(time.time()))
						await message.answer(f"🎁 {tag}, вы получили: {formarter(rand)} VK Coin")
					else:
						format_time = time.gmtime(86400 - timer)
						timer = time.strftime("%H час. %M мин. %S сек.", format_time)
						await message.answer(f"⏱ {tag}, следующий бонус можно забрать через: {timer}")
				else:
					await message.answer(f"📥 Для получения бонуса вам необходимо пополнить: {formarter(2000000 - all_topup)} VK Coin")
			
			elif text in ["пополнить", "📥 пополнить"]:
				await message.answer(f"📥 https://vk.com/coin#x705783864_1000_1337_1")

			elif text in ["стат", "стата"]:
				await message.answer(f"""📊 Статистика:
⠀👥 Зарегистрровано: {formarter(user.counts())} пользователей
⠀💰 Баланс: {formarter(rezerv())} VK Coin
""")

			elif text in ["🔥 поддержать", "поддержать", "пожертвовать", "жертва", "жертвы"]:
				await message.answer("🙃 Кого хотите поблагодарить?)", keyboard=donate_keyboard)

			elif text in ["топнеделя" "топнеделя"]:
				if user_id in admin_ids:
					now = floor(time.time())
					time_format = time.gmtime(now)
					now = time.strftime("%A", time_format)
					now_time = time.strftime("%H", time_format)
					if now == "Sunday" and now_time == 17:
						users = user.get_top("all_invest_week", 10)
						text = "🔥 Итоги топа по инвесту за неделю:\n\n"
						for num, us in enumerate(users):
							id = us['vk_id']
							prize = floor(us['all_invest_week']/100*5)
							user.update(id, 'invest_balance', user.get(id, 'invest_balance') + prize)
							text += f"\n{top[num]} {us['tag']} - {formarter(us['all_invest_week'])} VK Coin (Приз: {formarter(prize)} VKC)"
						user.uni_update('all_invest_week', 0)
						await message.answer(f"{text}\n\n🤑 Все призы были выданы на инвестиционный баланс! Следующее итоги будут в следующее Воскресенье.")
					else:
						await message.answer("🏆 Подвести итоги топа по инвесту за неделю можно только в Воскресенье в 20:00 По Мск!")

			elif text in ["рес", "рест"]:
				if user_id in admin_ids:
					threading.Thread(target=start_vkc).start()
					await message.answer("✅ Теперь пополнения VKC работают в очном режиме!")

			elif text in ["qiwires", "resqiwi"]:
				if user_id == admin_ids[0]:
					threading.Thread(target=start_qiwi).start()
					await message.answer("✅ Теперь оплата через QIWI работает в очном режиме!")

			elif text in ["город", "🏢", "гор", "сити", "city"]:
				text = ""
				CityBuildings = user.get(user_id, 'CityBuildings')
				CityPopulation = user.get(user_id, 'CityPopulation')
				CityHappy = user.get(user_id, "CityHappy")
				CityTaxes = user.get(user_id, 'CityTaxes')
				CityWaterCosts = user.get(user_id, 'CityWaterCosts')
				CityEnergyCosts = user.get(user_id, 'CityEnergyCosts')
				CityServiceCosts = user.get(user_id, 'CityServiceCosts')
				if CityPopulation <= 100000 and CityTaxes >= 1000000000:
					CityTaxes = floor(CityTaxes / 1.2)
				elif CityPopulation > 100000 and CityPopulation <= 350000 and CityTaxes >= 1000000000:
					CityTaxes = floor(CityTaxes / 1.2)
				elif CityPopulation > 350000 and CityPopulation <= 700000 and CityTaxes >= 4000000000:
					CityTaxes = floor(CityTaxes / 1.2)
				elif CityPopulation > 700000 and CityPopulation <= 1000000 and CityTaxes >= 5000000000:
					CityTaxes = floor(CityTaxes / 1.2)
				elif CityPopulation > 1000000 and CityPopulation <= 5000000 and CityTaxes >= 8000000000:
					CityTaxes = floor(CityTaxes / 1.2)
				elif CityPopulation > 5000000 and CityPopulation <= 8000000 and CityTaxes >= 9000000000:
					CityTaxes = floor(CityTaxes / 1.3)
				elif CityPopulation > 8000000 and CityPopulation <= 12000000 and CityTaxes >= 15000000000:
					CityTaxes = floor(CityTaxes / 1.3)
				elif CityPopulation > 12000000 and CityPopulation <= 20000000 and CityTaxes >= 20000000000:
					CityTaxes = floor(CityTaxes / 1.3)
				elif CityPopulation > 20000000 and CityPopulation <= 50000000 and CityTaxes >= 30000000000:
					CityTaxes = floor(CityTaxes / 1.4)
				elif CityPopulation > 50000000 and CityPopulation <= 100000000 and CityTaxes >= 50000000000:
					CityTaxes = floor(CityTaxes / 1.4)
				CityTaxesNonCosts = CityTaxes - CityWaterCosts - CityEnergyCosts - CityServiceCosts
				if CityWaterCosts == 0:
					text += "\n❌ Постройте хотя-бы Водонапорную башню для добычи воды!"
				if CityEnergyCosts == 0:
					text += "\n❌ Постройте хотя-бы Ветряную электростанцию для добычи энергии!"
				if CityServiceCosts == 0:
					text += "\n❌ Постройте хотя-бы Детский сад для образования!"
				if CityHappy > 2 and CityHappy <= 40:
					text += "\n❌ Процент счастья вашего города меньше 40! Скоро люди начнут съезжать с вашего поселения!"
					chance = randint(1,100)
					if chance <= 40:
						if CityPopulation >= 100 and CityPopulation < 10000:
							CityPopulation -= randint(1,80)
						elif CityPopulation >= 10000:
							CityPopulation -= randint(1,5000)
						elif CityPopulation >= 1 and CityPopulation < 100:
							CityPopulation -= 1
						user.update(user_id, 'CityPopulation', CityPopulation)
				if CityWaterCosts > 0 and CityEnergyCosts > 0:
					chance = randint(1,100)
					if CityPopulation > 20 and CityPopulation <= 1000:
						if CityWaterCosts < 50000:
							text += "\n❌ В городе не хватает воды! Постройте Водоснабжающую постройку!"
							if chance <= 30:
								CityPopulation -= randint(1,20)
								user.update(user_id, 'CityPopulation', CityPopulation)
						if CityEnergyCosts < 50000:
							text += "\n❌ В городе не хватает электричества! Постройте Энергоснабжающую постройку!"
							if chance <= 30:
								CityPopulation -= randint(1,20)
								user.update(user_id, 'CityPopulation', CityPopulation)
					elif CityPopulation > 10000 and CityPopulation <= 50000:
						if CityWaterCosts < 150000:
							text += "\n❌ В городе не хватает воды! Постройте Водоснабжающую постройку!"
							if chance <= 30:
								CityPopulation -= randint(1,3500)
								user.update(user_id, 'CityPopulation', CityPopulation)
						if CityEnergyCosts < 150000:
							text += "\n❌ В городе не хватает электричества! Постройте Энергоснабжающую постройку!"
							if chance <= 30:
								CityPopulation -= randint(1,3500)
								user.update(user_id, 'CityPopulation', CityPopulation)
					elif CityPopulation > 50000 and CityPopulation <= 100000:
						if CityWaterCosts < 250000:
							text += "\n❌ В городе не хватает воды! Постройте Водоснабжающую постройку!"
							if chance <= 30:
								CityPopulation -= randint(1,10000)
								user.update(user_id, 'CityPopulation', CityPopulation)
						if CityEnergyCosts < 250000:
							text += "\n❌ В городе не хватает электричества! Постройте Энергоснабжающую постройку!"
							if chance <= 30:
								CityPopulation -= randint(1,10000)
								user.update(user_id, 'CityPopulation', CityPopulation)
					elif CityPopulation > 100000 and CityPopulation <= 500000:
						if CityWaterCosts < 450000:
							text += "\n❌ В городе не хватает воды! Постройте Водоснабжающую постройку!"
							if chance <= 30:
								CityPopulation -= randint(1,30000)
								user.update(user_id, 'CityPopulation', CityPopulation)
						if CityEnergyCosts < 450000:
							text += "\n❌ В городе не хватает электричества! Постройте Энергоснабжающую постройку!"
							if chance <= 30:
								CityPopulation -= randint(1,30000)
								user.update(user_id, 'CityPopulation', CityPopulation)
					elif CityPopulation > 500000 and CityPopulation <= 1000000:
						if CityWaterCosts < 800000:
							text += "\n❌ В городе не хватает воды! Постройте Водоснабжающую постройку!"
							if chance <= 30:
								CityPopulation -= randint(1,50000)
								user.update(user_id, 'CityPopulation', CityPopulation)
						if CityEnergyCosts < 800000:
							text += "\n❌ В городе не хватает электричества! Постройте Энергоснабжающую постройку!"
							if chance <= 30:
								CityPopulation -= randint(1,50000)
								user.update(user_id, 'CityPopulation', CityPopulation)
				chance = randint(1,100)
				if chance <= 10:
					if CityPopulation >= 100 and CityPopulation < 1000:
						rand = randint(1,20)
						CityPopulation -= rand
						CityBuildings -= 1
						user.update(user_id, 'CityPopulation', CityPopulation)
						user.update(user_id, 'CityBuildings', CityBuildings)
						text += f"\n❌ В вашем городе сгорел дом! Погибло: {rand} чел."
					elif CityPopulation >= 1000 and CityPopulation < 10000:
						rand = randint(1,200)
						CityPopulation -= rand
						CityBuildings -= randint(1,5) if CityBuildings >= 5 else 1
						user.update(user_id, 'CityPopulation', CityPopulation)
						user.update(user_id, 'CityBuildings', CityBuildings)
						text += f"\n❌ В вашем городе сгорело несколько домов! Погибло: {rand} чел."
					elif CityPopulation >= 10000 and CityPopulation < 100000:
						rand = randint(1,2000)
						CityPopulation -= rand
						CityBuildings -= randint(1,20) if CityBuildings >= 20 else 5
						user.update(user_id, 'CityPopulation', CityPopulation)
						user.update(user_id, 'CityBuildings', CityBuildings)
						text += f"\n❌ Случилось наводнение! Погибло: {rand} чел."
					elif CityPopulation >= 100000 and CityPopulation <= 500000:
						rand = randint(1,20000)
						CityPopulation -= rand
						CityBuildings -= randint(1,100) if CityBuildings >= 100 else 10
						user.update(user_id, 'CityPopulation', CityPopulation)
						user.update(user_id, 'CityBuildings', CityBuildings)
						text += f"\n❌ Пришло цунами и убило {rand} чел.!"
					elif CityPopulation > 500000:
						rand = randint(1,100000)
						CityPopulation -= rand
						CityBuildings -= randint(1,1000) if CityBuildings >= 1000 else 50
						user.update(user_id, 'CityPopulation', CityPopulation)
						user.update(user_id, 'CityBuildings', CityBuildings)
						text += f"\n❌ Упал метеорит и убил {rand} чел.!"
				CityCoffers = user.get(user_id, 'CityCoffers')
				CityTime = user.get(user_id,  'City_time')
				now = time.time()
				timer = now-CityTime
				if timer >= 3600:
					taxes_get = floor(timer/3600*CityTaxesNonCosts)
					CityCoffers += taxes_get
					user.update(user_id, 'CityCoffers', CityCoffers)
					user.update(user_id, 'City_time', floor(time.time()))
				await message.answer(f"""🏢 {user.get(user_id, 'tag')}, ваш город:
💰 В казне: {formarter(CityCoffers)}$

👥 Население: {formarter(CityPopulation)} чел.
⠀😀 Счастье: {formarter(CityHappy)}%
⠀💸 Прибыль: {formarter(CityTaxes)}$/Час
⠀💸 Чистая прибыль (С учётом затрат): {formarter(CityTaxesNonCosts)}$/Час

🌇 Зданий: {formarter(CityBuildings)}

🧾 Затраты:
⠀💧 На добычу воды: {formarter(CityWaterCosts)}$
⠀⚡ На добычу энергии: {formarter(CityEnergyCosts)}$
⠀👔 На обслуживание: {formarter(CityServiceCosts)}$
{text}""", keyboard=city_keyboard)

			elif text in ["город казна", "город снять", "💰 снять с казны"]:
				balance = user.get(user_id, 'dollars')
				coffers = user.get(user_id, 'CityCoffers')
				if coffers >= 1:
					balance += coffers
					user.update(user_id, 'dollars', balance)
					user.update(user_id, 'CityCoffers', 0)
					await message.answer(f"✅ Вы успешно сняли с казны города {formarter(coffers)}$!")
				else:
					await message.answer("❌ Казна вашего города пуста!")

			elif text in ["город события", "город ивенты", "город евент", "город соб", "🥳 город события"]:
				await message.answer("""🥳 Список событий:

🏛 1 >> Праздничный концерт - 100 000$
🏘 2 >> Ярмарка - 350 000$
🎡 3 >> Недельный отдых - 750 000$
🎖 4 >> Парад к 9 мая - 1 000 000$
⛰ 5 >> Туристический поход - 1 350 000$
🛠 6 >> День эколога - 2 000 000$

🔍 Чтобы начать событие, введите: Событие (Номер события)""")

			elif text in ["обменник", "обмен"]:
				await message.answer("""💱 Обменник $ на VKC
📈 Курс: 1 VKC - 1 000 000$""")

			elif text in ["город построить", "город здания", "город стройка", "город строить", "🏙 город здания"]:
				await message.answer(f"""🌇 Список зданий:

🏕 Жилые:
⠀🏠 1 >> Деревянный дом - 50 000$
⠀🏡 2 >> Хижина - 100 000$
⠀🏢 3 >> Двухэтажка - 500 000$
⠀🏢 4 >> Трёхэтажка - 750 000$
⠀🏙 5 >> Многоэтажка - 1 000 000$
⠀🗼 6 >> Небоскрёб - 2 500 000$

🏭 Заводы:
⠀🌲 7 >> Деревообрабатывающый завод - 100 000$
⠀⛓ 8 >> Маталлообрабатывающий завод - 150 000$
⠀🚗 9 >> Машиностроительный завод - 300 000$
⠀🏗 10 >> Механический завод - 350 000$
⠀🚂 11 >> Вагоностроительный завод - 400 000$
⠀🌡 12 >> Медицинский завод - 420 000$
⠀🌫 13 >> Нефтеперерабатывающий завод - 800 000$
⠀🧪 14 >> Химический завод - 1 200 000$

🧠 Образование:
⠀👶 15 >> Детский сад - 100 000$
⠀😵 16 >> Младшая школа - 150 000$
⠀👨‍🏫 17 >> Средняя школа - 250 000$
⠀🤓 18 >> Гимназия - 300 000$
⠀🧐 19 >> Лицей - 400 000$
⠀🏫 20 >> Колледж - 500 000$
⠀👨‍🔬 21 >> Университет - 750 000$

😀 Развлечение и отдых:
⠀🌳 22 >> Городской парк - 200 000$
⠀🎲 23 >> Детская площадка - 350 000$
⠀🏖 24 >> Пляж - 500 000$
⠀🌉 25 >> Набережная - 800 000$
⠀🎡 26 >> Парк аттракционов - 1 000 000$
⠀🏰 27 >> Музей - 2 000 000$
⠀🏛 28 >> Театр - 2 200 000$
⠀🏩 29 >> Отель - 2 500 000$

⚡ Энергоснабжение:
⠀💨 30 >> Ветряная электростанция - 25 000$
⠀🔳 31 >> Блочно-контейнерная электростанция - 100 000$
⠀🌊 32 >> Волновая электростанция - 300 000$
⠀💥 33 >> Дизельная электростанция - 650 000$
⠀🌉 34 >> Приливная электростанция - 800 000$
⠀☀ 35 >> Солнечная электростанция - 900 000$
⠀🔥 36 >> Тепловая электростанция - 1 300 000$
⠀☢ 37 >> Атомная электростанция - 1 600 000$

💧 Водоснабжение:
⠀🗼 38 >> Водонапорная башня - 25 000$
⠀⛲ 39 >> Водонасосная станция - 120 000$
⠀🏭 40 >> Водоочистная станция - 400 000$
⠀🌎 41 >> Экологичная водоочистная станция - 800 000$

♻ Отходы:
⠀🗑 42 >> Урна - 10 000$
⠀📦 43 >> Мусорный контейнер - 50 000$
⠀🏚 44 >> Малая станция переработки - 100 000$
⠀🏭 45 >> Обычная станция переработки - 250 000$
⠀🚯 46 >> Большая станция переработки - 550 000$

🛒 Чтобы построить здание, введите: Гор (Номер постройки) (Кол-во)""")

		else:
			tag = await bot.api.users.get(user_id)
			name = tag[0].first_name
			try:
				name = name.split("'")[:1][0]
			except:
				pass
			tag = f"[id{user_id}|{name}]"
			user.insert(user_id, tag)
			try:
				ref = message.ref
			except:
				ref = False
			try:
				if ref:
					ref_bonus = globals.get("ref_bonus")
					bonus = floor(ref_bonus/2)
					user.update(user_id, 'invest_balance', bonus)
					user.update(ref, 'invest_balance', user.get(ref, 'invest_balance') + ref_bonus)
					await message.answer(f"""✅ {tag}, вы были зарегистрированы! Ознакомьтесь с Пользовательским Соглашением: https://vk.com/@investorvkc-terms-of-use
👥 Вы перешли по реферальной ссылке {user.get(ref, 'tag')} и получили {formarter(bonus)} Coin!""", keyboard=menu_keyboard)
					await bot.api.messages.send(peer_id=ref, message=f"👥 {tag} перешёл по вашей реферальной ссылке и вы получили {formarter(ref_bonus)} VK Coin!", random_id=randint(-1000000000,1000000000))
				else:
					await message.answer(f"""✅  {tag}, вы были зарегистрированы! Ознакомьтесь с Пользовательским Соглашением: https://vk.com/@investorvkc-terms-of-use""", keyboard=menu_keyboard)
			except:
				await message.answer("❌ Произошла непредвиденная ошибка! Повторите попытку ещё раз!")

except Exception as error:
	print(error)
	pass

bot.loop_wrapper = lw
bot.run_forever()
