import logging
import os
import random
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Ensure the log directory exists
if not os.path.exists('log'):
    os.makedirs('log')

# Enable logging to file and console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("log/bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# User-Agent list for rotating (Ubuntu)
USER_AGENTS = [
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    # Add more Ubuntu user agents if necessary
]

def simulate_human_behavior():
    # Simulate random delay
    time.sleep(random.uniform(0.5 , 1.5))

def set_up_selenium():
    options = Options()
    user_agent = random.choice(USER_AGENTS)
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--headless')  # Uncomment if you want to run in headless mode
    driver = webdriver.Firefox(options=options)
    return driver

def save_cookies(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookies(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Halo! Saya adalah bot Google Scholar Anda. Kirimkan kata kunci untuk mencari jurnal akademis. 📝🔍')
    context.user_data['search_mode'] = False

def search(update: Update, context: CallbackContext) -> None:
    context.user_data['search_mode'] = True
    update.message.reply_text('Masukkan kata kunci untuk mencari jurnal.')

def handle_message(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('search_mode', False):
        query = update.message.text
        if query:
            update.message.reply_text('Mohon tunggu sebentar, saya sedang mencari jurnal... ⏳')
            results = []
            driver = set_up_selenium()
            try:
                driver.get('https://scholar.google.com/')
                simulate_human_behavior()

                # Load cookies if available
                if os.path.exists('cookies.pkl'):
                    load_cookies(driver, 'cookies.pkl')
                    driver.refresh()
                    simulate_human_behavior()

                search_box = driver.find_element(By.NAME, 'q')
                search_box.send_keys(query)
                simulate_human_behavior()
                search_box.send_keys(Keys.RETURN)
                simulate_human_behavior()

                articles = driver.find_elements(By.CSS_SELECTOR, 'div.gs_r.gs_or.gs_scl')

                for article in articles[:5]:  # Limit to first 5 results
                    try:
                        title_element = article.find_element(By.CSS_SELECTOR, 'h3.gs_rt a')
                        title = title_element.text
                        url = title_element.get_attribute('href')
                    except Exception as e:
                        logger.error(f"Error extracting title and URL: {e}")
                        title = 'Title not available'
                        url = 'URL not available'

                    try:
                        author = article.find_element(By.CSS_SELECTOR, 'div.gs_a').text
                    except Exception as e:
                        logger.error(f"Error extracting author: {e}")
                        author = 'Penulis tidak tersedia'

                    try:
                        year = author.split()[-1]
                    except Exception as e:
                        logger.error(f"Error extracting year: {e}")
                        year = 'Tahun tidak tersedia'

                    result = f'📚 *Judul:* *{title}*\n👨‍🎓 *Penulis:* _{author}_\n📅 *Tahun:* {year}\n🔗 [Baca lebih lanjut]({url})'
                    logger.info(f"Result: {result}")
                    results.append(result)
                    simulate_human_behavior()

                # Save cookies for future sessions
                save_cookies(driver, 'cookies.pkl')

                if results:
                    update.message.reply_text('\n\n'.join(results), parse_mode='Markdown')
                else:
                    update.message.reply_text('Tidak ada hasil yang ditemukan. Coba dengan kata kunci yang berbeda.')

            except Exception as e:
                update.message.reply_text('Terjadi kesalahan saat mengambil data dari Google Scholar. ⚠️')
                logger.error(f"Error fetching data from Google Scholar: {e}")
            finally:
                driver.quit()
        else:
            update.message.reply_text('Silakan berikan kata kunci pencarian setelah perintah /search. 📝')
    else:
        update.message.reply_text('Gunakan perintah /search untuk memulai pencarian.')

def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    TOKEN = "7482991810:AAEEDjhdfoFC-TryYfYZmwTSWbVrJeDOm-w"  # Ganti ini dengan token bot Anda
    if not TOKEN:
        logger.error("Bot token is not set. Please set the TELEGRAM_BOT_TOKEN environment variable.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    dp.add_error_handler(error)

    # Timer to stop the bot after 6 hours
    def stop_bot_after_time():
        time.sleep(300)  # 6 hours in seconds
        updater.stop()
        logger.info("Bot has been stopped after 5 min")

    import threading
    threading.Thread(target=stop_bot_after_time).start()

    logger.info("Starting bot")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
