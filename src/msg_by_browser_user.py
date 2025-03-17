#!/usr/bin/python3
# -*- coding: utf-8 -*-

from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio
siliconflow_api_key = "sk-inxxgsdvtsguykkkwkrxqhaaoeqzbjnzcreozjhccsbchgkb"
basic_uri = "https://login.aliexpress.com/user/seller/login?bizSegment=CSP&return_url=http://csp.aliexpress.com/"
# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
        # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        # For Linux, typically: '/usr/bin/google-chrome'
    )
)

# Create the agent with your configured browser
llm=ChatOpenAI(base_url='https://api.siliconflow.cn/v1', model='deepseek-ai/DeepSeek-R1', api_key=siliconflow_api_key)

task_01 = "访问"+ basic_uri +",使用 用户名：zhm1990123@163.com，密码：123.123.Meng 登录,";
task_02 = "在页面 生意参谋 下，找到商品排行，分别获取到 支付榜、访客榜、收藏榜、加购榜的前十的ID,";
task_03 = "转入营销 下的客户营销，点击 新建自定义营销计划,";
task_04 = "找到 选择店铺Code 选择所有选项并点击确认,";
task_05 = "找到 选择商品 以 之前选择的 product_ids，每次4个 ，逐步筛选出产品，并点击确认,";
task_06 = "在选择 智能发送 后，点击一键创建，循环完成 40 个 产品的操作";

agent = Agent(
    task=task_01 + task_02 + task_03 + task_04 +task_05 + task_06,
    llm=llm,
    use_vision=False
)

async def main():
    await agent.run()

    input('Press Enter to close the browser...')
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())