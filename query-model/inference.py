# If necessary, install the openai Python library by running 
# pip install openai

from openai import OpenAI

## Protect both URL and API Key
client = OpenAI(
	base_url="https://XXXXXX.us-east-1.aws.endpoints.huggingface.cloud/v1/", 
	api_key="hf_XXXXXXXX" 
)

query_to_explain = """
with btc_rewards AS (
select date_trunc('day', block_timestamp) as day_,
avg(block_reward) as avg_block_reward,
sum(block_reward) as sum_block_reward,
avg(fees) as avg_fees,
sum(fees) as sum_fees,
DIV0(sum_fees, sum_fees + sum_block_reward) as fee_reward_ratio
        from bitcoin.gov.ez_miner_rewards 
-- start clean on Jan 2 
where block_timestamp >= '2024-01-01'
-- week needs to be finished before it is included  
and block_timestamp < date_trunc('day', current_date)
group by day_
)

select 
day_ as "Day",
sum_block_reward as "# BTC Block Rewards",
sum_fees as "# BTC Tx Fees",
fee_reward_ratio * 100 as "Fees / (Fees + Rewards) (%)"
from btc_rewards 
"""


chat_completion = client.chat.completions.create(
	model="tgi",
	messages=[
        {
            "role": "system",
            "content": "You are an expert crypto and blockchain analyst versed in Snowflake SQL. You explain code clearly and quickly."
        },
        {
            "role": "user",
            "content": "Given the following SQL code, explain the goals of the code. Do not go line by line. Give a holistic overview of the code. Be concise."
        },
        {
            "role": "system",
            "content": query_to_explain
        }
    ],
	stream=True,
	max_tokens=500
)

for message in chat_completion:
	print(message.choices[0].delta.content, end="")