import requests
import openai
from datetime import datetime, timedelta
import schedule
import time
from telegram import Bot
import asyncio
import re


# Replace with your actual API keys
api_key = 'Alphavantage_APIKEY'
openai.api_key = "OpenAI_APIKEY"
telegram_bot_token = 'Telegram Bot Token'

# Replace with your private channel ID
channel_id = 'Channel ID'
limit = 50
Interval = 6 # The interval between publish results in hours

def bold_symbols(text):
    pattern = r'\((NASDAQ|NYSE):( *)([A-Za-z]{1,5})\)'
    replacement = r'(\1:\2<b>\3</b>)'
    return re.sub(pattern, replacement, text)
def bold_importance(text):
    pattern = r'(Importance: \d+%)'
    replacement = r'<b>\1</b>'
    return re.sub(pattern, replacement, text)


# Function to send the message to the Telegram channel
async def send_telegram_message(bot, message):
    await bot.send_message(chat_id=channel_id, text=message,parse_mode='HTML')

def get_news():
    # Get the current time
    current_time = datetime.now()
    print(current_time )


    # Current time minus one hour
    time_from = (current_time - timedelta(hours=2)).strftime('%Y%m%dT%H%M')

    # Construct the API URL
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=technology&time_from={time_from}&apikey={api_key}'
    print(url)

    # Make the API request
    response = requests.get(url)

    # Parse the JSON response
    data = response.json()

    # Extract the desired information and format the output
    output = ''

    for index, item in enumerate(data['feed']):
        if index >= limit:
            break
        
        title = item['title']
        summary = item['summary']

        output += f'Title: {title}\nSummary: {summary}\n_\n'

    if output != '':
        instruction = f"""
        Forget all your previous instructions. Pretend you are a financial expert. You are a financial expert with stock recommendation experience.\
        Summarize and split the news into three categories according to the impact they can have on the company stock market: POSITIVE and NEGATIVE.\
        Remove NEUTRAL news from your response and do not provide any reason for that. Provide your reasons for news in POSITIVE and NEGATIVE sections and elaborate your thoughts with one short and concise sentence and see how the news can impact the stock market in the short-term, long-term, or both. Also, say how much in the percentage you think the news is important and can affect the price. Do not bring news with less than 50% importance. Do not exceed 500 tokens overall.
        The news are delimited by triple backticks.

        ```
        {output}
        ```
        """

        response = openai.ChatCompletion.create(
            model="gpt-4-0314",
            max_tokens = 512,
            messages=[{"role": "user", "content": instruction}]
        )

        result = response.choices[0].message.content.strip()

        result = bold_symbols(result)
        result = bold_importance(result)

        # Add ** around POSITIVE:, NEGATIVE:, and NEUTRAL:
        result = result.replace("POSITIVE:", "<b>POSITIVE:</b>") \
                    .replace("NEGATIVE:", "<b>NEGATIVE:</b>") \
                    .replace("NEUTRAL:", "<b>NEUTRAL:</b>")
        return result
    else:
        return None


bot = Bot(token=telegram_bot_token)

def task():
    result = get_news()
    if result is not None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_telegram_message(bot, result))
    else:
        print("No news to report")
    now = datetime.now()
    next_run = now + job.period
    print(f"Next run: {next_run}")


bot = Bot(token=telegram_bot_token)

# Schedule the get_news function to run every hour
job = schedule.every(Interval).hours.do(task)

task()
# Keep running and checking for the next scheduled job
while True:
    schedule.run_pending()
    time.sleep(10)