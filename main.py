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
Interval = 6 # The interval between getiing news and publishing results in hours

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
# Function to send the message to the Telegram channel
async def send_telegram_message(bot, message):
    await bot.send_message(chat_id=channel_id, text=message,parse_mode='HTML')

async def get_news():
    # Get the current time
    current_time = datetime.now()
    print(current_time )

    # Current time minus one hour
    time_from = (current_time - timedelta(hours=2)).strftime('%Y%m%dT%H%M')

    # Construct the API URL
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=technology&time_from={time_from}&apikey={api_key}'
    print(url)

    # Make the API request
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()

    # Parse the JSON response
    data = json.loads(data)

    # Extract the desired information and format the output
    output = ''

    for index, item in enumerate(data.get('feed', [])):
        if index >= limit:
            break
        
        title = item.get('title', '')
        summary = item.get('summary', '')

        output += f'Title: {title}\nSummary: {summary}\n_\n'

    if output != '':
        instruction = f"""
        Forget all your previous instructions. Pretend you are a financial expert. You are a financial expert with stock recommendation experience.\
        Summarize and split the news into three categories according to the impact they can have on the company stock market: POSITIVE, NEGATIVE, and NEUTRAL.\
        Remove NEUTRAL news from your response and do not provide any reason for that.\
        Provide your reasons for news in POSITIVE and NEGATIVE sections and elaborate your thoughts with one short and concise sentence and see how the news can impact the stock market in the short-term, long-term, or both.\
        Also, say how much in the percentage you think the news is important and can affect the price.\
        Sort news by their importance in each category and do not bring news with less than 50% importance.
        Write at most 500 words.
        The news are delimited by triple backticks.

        ```
        {output}
        ```
        Write your answer in the folowing format.
        
        <b>POSITIVE</b>:

        - <b>title goes here</b>: ...
          <b>Reason</b>: ...
          <b>Impact</b>: ... (<b>Importance: ?%</b>)
        ...
        <b>NEGATIVE</b>:

        - <b>title goes here</b>
          <b>Reason</b>: ...
          <b>Impact</b>: ... (<b>Importance: ?%</b>)
        ...
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            max_tokens = 600,
            messages=[{"role": "user", "content": instruction}]
        )

        result = response.choices[0].message.content.strip()
        return result
    else:
        return None

bot = Bot(token=telegram_bot_token)

# Create an async schedule task
async def schedule_news():
    while True:
        result = await get_news()
        if result is not None:
            print(type(result))
            print(result)
            await send_telegram_message(bot, result)
        await asyncio.sleep(60)  # Sleep for the interval (in seconds)

# Start the scheduler
asyncio.run(schedule_news())
