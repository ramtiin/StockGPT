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


# Function to send the message to the Telegram channel
async def send_telegram_message(bot, message):
    await bot.send_message(chat_id=channel_id, text=message,parse_mode='HTML')



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
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=economy_monetary&time_from={time_from}&apikey={api_key}'
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
        Assume the role of a distinguished financial analyst with a deep understanding of the S&P 500. Utilize the latest 12-hour global economic updates provided by AlphaVantage, clearly segmented with triple backticks. Your task is to conduct a comprehensive yet concise analysis, not exceeding 250 words, encapsulating the nuances of the economic data.
        Your analysis should integrate advanced financial concepts and market trends, offering a nuanced perspective on how these global economic developments are likely to influence the S&P 500 index. Specifically, assess key economic indicators such as GDP growth rates, unemployment figures, inflation trends, and major geopolitical events that could affect market stability.
        Furthermore, take into account any recent fiscal or monetary policy changes that might impact investor sentiment and market dynamics. Your insights should culminate in a well-reasoned and evidence-based buy, hold, or sell decision for the S&P 500 for the upcoming week. This decision should be grounded in your analysis and reflect current market conditions and future projections.

        ```
        {output}
        ```
        Write your answer in the folowing format.

        <b>Expert Analysis</b>:

        - Your analysis

        <b>Investment Decision</b>:

        - Your reasoned decision (buy/hold/sell) for the S&P 500, based on the analysis.
        """
        
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            max_tokens = 400,
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
