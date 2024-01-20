from openai import OpenAI
from datetime import datetime, timedelta
from telegram import Bot
import asyncio
import aiohttp
import json
import os


# Replace with your actual API keys
api_key = 'ALPHA VANTAGE API KEY'
openai_api_key = "OPENAI KEY"
telegram_bot_token = 'TELEGRAM BOT TOKEN'


client = OpenAI(
  api_key=openai_api_key  
)


# Replace with your private channel ID
channel_id = 'YOUR CHANNEL ID ( e.g. -00000000000)'
limit = 50
Interval = 12 # The interval between getiing news and publishing results in hours



# Function to send the message to the Telegram channel
async def send_telegram_message(bot, message):
    await bot.send_message(chat_id=channel_id, text=message,parse_mode='HTML')

def get_news():
    # Get the current time
    current_time = datetime.now()
    print(current_time )


    # Current time minus one hour
    time_from = (current_time - timedelta(hours=Interval)).strftime('%Y%m%dT%H%M')

    # Construct the API URL
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=economy_macro&time_from={time_from}&apikey={api_key}'
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

    # Current time minus interval
    time_from = (current_time - timedelta(interval=2)).strftime('%Y%m%dT%H%M')

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


# Function to send the message to the Telegram channel
async def send_telegram_message(bot, message):
    await bot.send_message(chat_id=channel_id, text=message,parse_mode='HTML')

async def get_news():
    # Get the current time
    current_time = datetime.now()
    print(current_time )

    # Current time minus one hour
    time_from = (current_time - timedelta(hours=Interval)).strftime('%Y%m%dT%H%M')

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
        Adopt the persona of an experienced financial analyst with expertise in stock market insights, particularly the S&P 500. Upon receiving a summary of the most recent global economic updates from the past 12 hours, provided by you and sourced from AlphaVantage, my objective will be to compose a detailed analysis. This analysis, constrained to 500 words, will focus on predicting the effects of these economic developments on the S&P 500 index. The news items will be distinctly separated for ease of reference, marked by triple backticks. In cases where there are no relevant updates concerning the S&P 500, I will simply reply with 'No new news' for clarity.
        ```
        {output}
        ```
        Write your answer in the folowing format.

        <b>Gold</b>:

        - Your analysis
        ...
        """
        
        completion = client.chat.completions.create(
            model="gpt-4",
            max_tokens = 600,
            messages=[{"role": "system", "content": instruction}]
        )

        result = completion.choices[0].message.content.strip()
        return result
    else:
        return None

bot = Bot(token=telegram_bot_token)

# Create an async schedule task
async def schedule_news():
    while True:
        result = await get_news()
        if result is not None:
            await send_telegram_message(bot, result)
        await asyncio.sleep(Interval*3600)  # Sleep for the interval (in seconds)

# Start the scheduler
asyncio.run(schedule_news())
