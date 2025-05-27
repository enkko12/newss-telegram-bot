import telebot
import requests
from bs4 import BeautifulSoup
import time
import threading
from datetime import datetime
from deep_translator import GoogleTranslator

# === Настройки ===
BOT_TOKEN = '7771251393:AAEw4EYcaZ5ejTyH7QbtZp4gsqulQjhUTFI'
GROUP_ID = -1002508111413
bot = telebot.TeleBot(BOT_TOKEN)

posted_links = set()
send_now_event = threading.Event()

# === Источники ===

def get_lenta():
    news = []
    try:
        r = requests.get("https://lenta.ru/rubrics/russia/politics/", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for card in soup.select('a.card-full-news')[:5]:
            link = card['href']
            full_link = 'https://lenta.ru' + link if link.startswith('/') else link
            title = card.get_text(strip=True)
            news.append(("Lenta.ru", title, full_link))
    except Exception as e:
        print("Lenta error:", e)
    return news

def get_rbc():
    news = []
    try:
        r = requests.get("https://www.rbc.ru/politics/", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for card in soup.select('.item__wrap')[:5]:
            a = card.find('a')
            if not a: continue
            title = a.get_text(strip=True)
            link = a['href']
            news.append(("RBC.ru", title, link))
    except Exception as e:
        print("RBC error:", e)
    return news

def get_pravda():
    news = []
    try:
        r = requests.get("https://www.pravda.com.ua/rus/news/", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.select('.article_news_list .article__title a')[:5]:
            title = a.get_text(strip=True)
            link = "https://www.pravda.com.ua" + a['href']
            news.append(("Украинская правда", title, link))
    except Exception as e:
        print("Pravda error:", e)
    return news

def get_24tv():
    news = []
    try:
        r = requests.get("https://24tv.ua/politika_tag1123/", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for li in soup.select('li.news-feed__item')[:5]:
            a = li.find('a')
            if not a: continue
            title = a.get_text(strip=True)
            link = "https://24tv.ua" + a['href']
            news.append(("24 Канал", title, link))
    except Exception as e:
        print("24TV error:", e)
    return news

def get_bbc():
    news = []
    try:
        r = requests.get("https://www.bbc.com/news/politics", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.select('a.gs-c-promo-heading')[:5]:
            title = a.get_text(strip=True)
            link = "https://www.bbc.com" + a['href'] if a['href'].startswith('/') else a['href']
            news.append(("BBC", title, link))
    except Exception as e:
        print("BBC error:", e)
    return news

def get_cnn():
    news = []
    try:
        r = requests.get("https://edition.cnn.com/politics", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for h in soup.select('h3.cd__headline')[:5]:
            a = h.find('a')
            if not a: continue
            title = a.get_text(strip=True)
            link = "https://edition.cnn.com" + a['href'] if a['href'].startswith('/') else a['href']
            news.append(("CNN", title, link))
    except Exception as e:
        print("CNN error:", e)
    return news

def get_aljazeera():
    news = []
    try:
        r = requests.get("https://www.aljazeera.com/news/politics/", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.select('a.u-clickable-card__link')[:5]:
            title = a.get_text(strip=True)
            link = "https://www.aljazeera.com" + a['href'] if a['href'].startswith('/') else a['href']
            news.append(("Al Jazeera", title, link))
    except Exception as e:
        print("Al Jazeera error:", e)
    return news

def get_dw():
    news = []
    try:
        r = requests.get("https://www.dw.com/en/top-stories/politics/s-7228", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.select('a.headline')[:5]:
            title = a.get_text(strip=True)
            link = "https://www.dw.com" + a['href']
            news.append(("DW", title, link))
    except Exception as e:
        print("DW error:", e)
    return news

def get_guardian():
    news = []
    try:
        r = requests.get("https://www.theguardian.com/politics", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.select('a.u-faux-block-link__overlay')[:5]:
            title = a.get_text(strip=True)
            link = a['href']
            news.append(("The Guardian", title, link))
    except Exception as e:
        print("Guardian error:", e)
    return news

def get_reuters():
    news = []
    try:
        r = requests.get("https://www.reuters.com/politics/", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.select('a.story-title, a.story-content__link')[:5]:
            title = a.get_text(strip=True)
            link = "https://www.reuters.com" + a['href'] if a['href'].startswith('/') else a['href']
            news.append(("Reuters", title, link))
    except Exception as e:
        print("Reuters error:", e)
    return news

def get_unian():
    news = []
    try:
        r = requests.get("https://www.unian.net/politics", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for item in soup.select('.list-thumbs__item')[:5]:
            a = item.find('a')
            if not a: continue
            title = a.get_text(strip=True)
            link = "https://www.unian.net" + a['href'] if a['href'].startswith('/') else a['href']
            news.append(("UNIAN", title, link))
    except Exception as e:
        print("UNIAN error:", e)
    return news

def get_nv():
    news = []
    try:
        r = requests.get("https://nv.ua/ukr/ukraine.html", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for article in soup.select('article')[:5]:
            a = article.find('a')
            if not a: continue
            title = a.get_text(strip=True)
            link = "https://nv.ua" + a['href'] if a['href'].startswith('/') else a['href']
            news.append(("НВ", title, link))
    except Exception as e:
        print("NV error:", e)
    return news

def send_article(source, title, link):
    now = datetime.now()
    timestamp = now.strftime('%H:%M:%S')
    try:
        translated_title = GoogleTranslator(source='auto', target='ru').translate(title)
    except Exception:
        translated_title = title

    text = (
        f"📰 *{translated_title}*
"
        f"🕒 _{timestamp}_

"
        f"📄 Нажмите ниже, чтобы узнать подробности:
"
        f"🔗 [Читать полностью]({link})

"
        f"🏷️ _Источник: {source}_"
    )
    try:
        bot.send_message(GROUP_ID, text, parse_mode="Markdown", disable_web_page_preview=False)
    except Exception as e:
        print("Ошибка отправки:", e)

def news_cycle():
    all_news = (
        get_lenta() + get_rbc() + get_pravda() + get_24tv() +
        get_bbc() + get_cnn() + get_aljazeera() + get_dw() +
        get_guardian() + get_reuters() + get_unian() + get_nv()
    )
    new_sent = 0
    for source, title, link in all_news:
        if link not in posted_links:
            send_article(source, title, link)
            posted_links.add(link)
            new_sent += 1
            time.sleep(2)
    if new_sent == 0:
        try:
            bot.send_message(GROUP_ID, "🕊️ В данный момент всё спокойно. Можно жить 😊")
        except Exception as e:
            print("Ошибка отправки спокойного сообщения:", e)
    try:
        msg = bot.send_message(GROUP_ID, "⏳ До новой партии новостей: 5 минут")
    except Exception as e:
        print("Ошибка отправки таймера:", e)
        time.sleep(300)
        return
    for minutes_left in range(4, -1, -1):
        for _ in range(60):
            if send_now_event.is_set():
                send_now_event.clear()
                return
            time.sleep(1)
        try:
            bot.edit_message_text(
                f"⏳ До новой партии новостей: {minutes_left} минут",
                chat_id=GROUP_ID,
                message_id=msg.message_id
            )
        except Exception as e:
            print("Ошибка обновления таймера:", e)
            break

def auto_send_news():
    while True:
        news_cycle()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "✅ Бот будет присылать новости каждые 5 минут.")

@bot.message_handler(commands=['rec'])
def rec(message):
    bot.send_message(message.chat.id, "♻️ Немедленная отправка свежих новостей.")
    send_now_event.set()

threading.Thread(target=auto_send_news, daemon=True).start()
print("🤖 Бот запущен.")
bot.polling(non_stop=True)