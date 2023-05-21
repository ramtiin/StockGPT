Welcome to StockGPT - an innovative Python script designed to analyze financial news. It leverages the power of GPT-4 to extract meaningful insights and publishes them on a dedicated Telegram channel for your convenience.

## Prerequisites

To utilize StockGPT to its full potential, you'll require the following:

1. **Alpha Vantage API Key:** Alpha Vantage is renowned for its service that it provides free of charge, with a generous rate limit of 5 requests per minute and 500 requests per day. To procure your API key, click [here](https://www.alphavantage.co/support/#api-key).

2. **OpenAI API Key:** This is vital to analyze financial news. If you're looking to use the GPT-4 API, you might need to join the GPT-4 waitlist. A comprehensive guide on how to obtain an API key is available [here](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/).

3. **Telegram Bot Token:** You will need a Telegram bot token to publish the analysis results on your channel. The process to acquire this token is explained in this [tutorial](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token). 

In addition, you need to add the bot to a Telegram channel where the results will be published. Therefore, it is also necessary to find your Telegram channel ID and replace it in the designated spot within the code.

Please ensure to set up these prerequisites before you proceed.

## Installation

To get started, you'll first need to install the necessary Python packages that StockGPT relies on. These are listed in the `requirements.txt` file. To install these packages, navigate to the project directory and execute the following command in your terminal:

pip install -r requirements.txt


This will automatically install all the Python dependencies listed in the `requirements.txt` file.

## Running the Script on a Server

If you wish to run this script continuously, even after closing the terminal or SSH connection, you can use the 'screen' utility on your Linux server.

First, start a new screen session:
```
screen -S my_stockgpt_session

```


This creates a new screen session named `my_stockgpt_session`. You can replace 'my_stockgpt_session' with any name you choose.

Next, run the script:

```
python main.py
```

Once the script is running, detach from the screen session by pressing `Ctrl + A`, then `D`. 

To reattach to the screen session, use the command:
```
screen -r my_stockgpt_session
```

Again, replace `my_stockgpt_session` with the name you chose when you created the session.

That's it! Now you can keep your script running in the background on your server, even after closing the terminal or SSH connection.
