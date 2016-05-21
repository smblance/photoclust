import json
import telegram
import random
import framework
from webapp2 import Response
from clustering import reduce_colors
from StringIO import StringIO
from poster.encode import multipart_encode
from model import DBSessionBuilder

TELEGRAM_API_TOKEN = "230551380:AAGqv2bMACh8AG3lwYRnSt5Wchi__KOGOCw"

pics = ['\xF0\x9F\x8C\x83', '\xF0\x9F\x8C\x84', '\xF0\x9F\x8C\x85', '\xF0\x9F\x8C\x86', '\xF0\x9F\x8C\x87', '\xF0\x9F\x8C\x88', '\xF0\x9F\x8C\x89']

app = framework.WSGIApplication()
bot = telegram.Bot(token=TELEGRAM_API_TOKEN)
webhook = bot.setWebhook('https://photoclust.appspot.com/messagehandler')
client = datastore.Client('photoclust')

def dbHandler(func):
	def wrapper(request, *args, **kwargs):
		dbSession = DBSessionBuilder()
		ret = func(dbSession, request, *args, **kwargs)
		dbSession.commit()
		dbSession.close()
		return ret

	return wrapper


@app.route("/")
def hi(request, *args, **kwargs):
	return "Feelin' better than ever."

@app.route("/listen")
def setWebhook(request, *args, **kwargs):
	webhook = bot.setWebhook('https://photoclust.appspot.com/messagehandler')
	if webhook:
		return "Webhook set up. Listening"
	else:
		return "Something went wrong"

@app.route("/stop")
def setWebhook(request, *args, **kwargs):
	webhook = bot.setWebhook('')
	if webhook:
		return "Webhook stopped. Stopped listening"
	else:
		return "Something went wrong"


@app.route("/messagehandler")
@dbHandler
def messagehandler(dbSession, request, *args, **kwargs):
	update = telegram.Update.de_json(json.loads(request.body))
	chat_id = update.message.chat.id
	text = update.message.text.encode('utf-8')
	photos = update.message.photo
	user = dbSession.query(User).filter(User.userid == chat_id).first()
	if not user:
		user = User(userid = chat_id)
		dbSession.add(user)

	n_clusters = None

	if photos:
		photo_id = max(photos, lambda x: x.width).photo_id
		if user.n_clusters:
			# give photo
			photo_path = json.loads(urlfetch.fetch(url = "https://api.telegram.org/getFile", payload = json.dumps({'file_id' : photo_id}), method = 'POST', headers = {"Content-Type": "application/json"}).content)['file_path']
			photo = open("https://api.telegram.org/file/bot{}/{}".format(TELEGRAM_API_TOKEN,photo_path))
			orig_n_colors, reduced_photo = reduce_colors(photo, n_clusters)
			body = {'method' : 'sendPhoto',
					'chat_id' : chat_id,
					'photo' : "".join(multipart_encode(reduced_photo)[0]),
					'caption' : "The photo had {} colors, but I reduced it to just {}, and it looks almost the same. Amazing me!"\
						.format(orig_n_colors, n_clusters)}
			return Response(status_int = 200, body = body, headers=to_post[1])
		else:
			# update photo
			# get number
			user.photolink = photo_id
			return getResponse("Give a number", chat_id)
	elif text:
		if not set(text).issubset('1234567890'):
			# not recognized
			return getResponse("Give me a number or a photo", chat_id)
		elif int(text) < 2:
			# not recognized
			return getResponse("Give me a number or a photo", chat_id)
		else:
			n_clusters = int(text)
			if user.photolink:
				# give photo
				photo_path = json.loads(urlfetch.fetch(url = "https://api.telegram.org/getFile", payload = json.dumps({'file_id' : photo_id}), method = 'POST', headers = {"Content-Type": "application/json"}).content)['file_path']
				photo = open("https://api.telegram.org/file/bot{}/{}".format(TELEGRAM_API_TOKEN,photo_path))
				orig_n_colors, reduced_photo = reduce_colors(photo, n_clusters)
				encoded, headers = multipart_encode(reduced_photo)[0]
				body = {'method' : 'sendPhoto',
					'chat_id' : chat_id,
					'photo' : "".join(encoded),
					'caption' : "The photo had {} colors, but I reduced it to just {}, and it looks almost the same. Amazing me!"\
						.format(orig_n_colors, n_clusters)}
				return Response(status_int = 200, body = body, headers = headers, content_type = 'multipart/form-data')
			else:
				# update n_clusters
				# get photo
				user.n_clusters = n_clusters
				return getResponse("Give me a number", chat_id)
	else:
		# not recognized
		return getResponse("Give me a number or a photo", chat_id)

def getResponse(text, chat_id):
	return Response(status_int = 200, body = {'method': 'sendMessage', 'chat_id' : chat_id, 'text' : "I need a number or a photo", content_type : 'application/json'})













