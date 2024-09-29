import asyncio
import aiohttp
from playwright.async_api import async_playwright
import requests
from bs4 import BeautifulSoup

# main 함수
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 첫 번째 페이지에서 value 가져오기
        await page.goto('https://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHF.do?menu_grp=MENU_NEW01&menu_no=2823')
        result = await foodsafety(page)

        # value 기반으로 상세 페이지 크롤링
        await crawl_details(result['item_values'])

        # 브라우저 닫기
        await browser.close()

if __name__ == '__main__':
    print(foodsafety())
    # asyncio.run(main())