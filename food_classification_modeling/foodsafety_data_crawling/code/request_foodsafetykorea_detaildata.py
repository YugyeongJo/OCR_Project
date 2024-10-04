import os
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

# 추가 데이터 수집 함수
async def get_additional_data(session, prdlst_report_ledg_no):
    url = f"https://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHFDetail.do?prdlstReportLedgNo={prdlst_report_ledg_no}&search_code=01&start_idx=1&show_cnt=10&menu_no=2823&menu_grp=MENU_NEW01"
    
    async with session.get(url) as response:
        if response.status == 200:
            soup = BeautifulSoup(await response.text(), 'html.parser')

            item_details = soup.find_all('tbody')
            if not item_details:
                print(f"No data found for {prdlst_report_ledg_no}")
                return None

            item_detail = item_details[0].find_all('td')

            if len(item_detail) >= 7:
                manufacturer_name = item_detail[0].get_text(strip=True)
                product_name = item_detail[1].get_text(strip=True)
                report_number = item_detail[2].get_text(strip=True)
                dosage_usage = item_detail[6].get_text(strip=True)
                standards_specifications = item_detail[-1].get_text(strip=True)

                return {
                    'manufacturer_name': manufacturer_name,
                    'product_name': product_name,
                    'report_number': report_number,
                    'dosage_usage': dosage_usage,
                    'standards_specifications': standards_specifications
                }
            else:
                print(f"잘못된 데이터 구조 for {prdlst_report_ledg_no}")
                return None
        else:
            print(f"상세 페이지 요청 실패. 상태 코드: {response.status}")
        return None

# 추가 정보 수집 함수 - 300개씩 끊어서 수집
async def scrape_additional_info_from_range(json_file_path, start_idx, end_idx):
    async with aiohttp.ClientSession() as session:
        # 저장된 JSON 파일 읽기
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data_dict = json.load(file)

        prdlst_report_ledg_no_list = data_dict['prdlst_report_ledg_no'][start_idx:end_idx]

        collected_data = {}

        for idx, prdlst_report_ledg_no in enumerate(prdlst_report_ledg_no_list):
            print(f"Processing {idx + start_idx}/{end_idx}: {prdlst_report_ledg_no}")
            data = await get_additional_data(session, prdlst_report_ledg_no)
            if data:
                collected_data[prdlst_report_ledg_no] = data
            await asyncio.sleep(1)  # 요청 간 간격 두기
    
        # 새로운 파일로 저장 (업데이트)
        output_file_path = f"./data/additional_data_{start_idx}_{end_idx}.json"
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(collected_data, file, ensure_ascii=False, indent=4)

    print(f"추가 정보가 {output_file_path} 파일에 저장되었습니다.")
    return collected_data

# 메인 실행 함수
async def main(start_range, end_range):
    json_file_path = '../data/prdlst_report_ledg_no.json'

    # 지정된 범위 내에서 300개씩 끊어서 수집
    for i in range(start_range, end_range, 300):
        start_idx = i
        end_idx = min(i + 300, end_range)
        print(f"Processing range: {start_idx} to {end_idx}")
        await scrape_additional_info_from_range(json_file_path, start_idx, end_idx)

if __name__ == "__main__":
    start_range = 0   # 수집 시작 범위 (수동 조정 가능)
    end_range = 38000  # 총 데이터 개수 (수동 조정 가능)
    
    asyncio.run(main(start_range, end_range))
