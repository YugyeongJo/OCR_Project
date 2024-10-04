import os
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

# 데이터 수집 함수들
async def fetch_all_foodsafety_data(session, url, headers, show_cnt, start_idx):
    data = {
        'menu_grp': 'MENU_NEW01',
        'menuNm': '',
        'copyUrl': 'https://www.foodsafetykorea.go.kr:443/portal/healthyfoodlife/searchHomeHF.do?menu_grp=MENU_NEW01&amp;menu_no=2823',
        'search_code': '01',
        'search_word': '',
        'show_cnt': show_cnt,
        'start_idx': start_idx
    }

    async with session.post(url, headers=headers, data=data) as response:
        if response.status == 200:
            content_type = response.headers.get('Content-Type')

            if 'application/json' in content_type or 'text/plain' in content_type:
                text_data = await response.text()
                try:
                    return json.loads(text_data)  # JSON 파싱
                except json.JSONDecodeError:
                    print(f"JSON 파싱에 실패했습니다. 응답 내용: {text_data[:500]}")
                    return None
            else:
                print(f"예상치 못한 Content-Type: {content_type}. 응답 내용: {await response.text()[:500]}")
                return None
        else:
            print(f"요청 실패. 상태 코드: {response.status}")
            return None

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

# 메인 scraping 함수
async def scrape_all_data(url, headers, show_cnt, start_idx, total_count=None, all_data=None):
    all_data = all_data if all_data is not None else []

    async with aiohttp.ClientSession() as session:
        while True:
            response_data = await fetch_all_foodsafety_data(session, url, headers, show_cnt, start_idx)
            if response_data:
                all_data.extend(response_data)

                if total_count is None:
                    total_count = int(response_data[0]["total_count"]) if response_data else 0
                    print(f"총 데이터 개수: {total_count}")
                
                start_idx += show_cnt

                if start_idx > total_count:
                    break
            else:
                break

        print(f"총 {len(all_data)}개의 데이터가 수집되었습니다.")
        
        return all_data

# 추가 정보 수집 함수
async def scrape_additional_info_from_file(json_file_path):
    async with aiohttp.ClientSession() as session:
        # 저장된 JSON 파일 읽기
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data_dict = json.load(file)

        for prdlst_report_ledg_no in data_dict['prdlst_report_ledg_no']:
            data = await get_additional_data(session, prdlst_report_ledg_no)
            if data:
                data_dict[prdlst_report_ledg_no] = data
            await asyncio.sleep(1)
    
        # 다시 파일에 저장 (업데이트)
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data_dict, file, ensure_ascii=False, indent=4)

    print(f"추가 정보가 {json_file_path} 파일에 저장되었습니다.")
    return data_dict

# 메인 실행 함수
async def main(show_cnt, start_idx, total_count=None, all_data=None):
    url = 'https://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHFProc.do'
    
    headers = {
        'Cookie': 'mykeyword=; elevisor_for_j2ee_uid=a7q2xjh45ywqc; mykeyword=; _ga=GA1.3.2039212263.1727073061; _ga_Z9ZVQ5VQFN=GS1.3.1727133706.3.0.1727133706.60.0.0; JSESSIONID=yvQFIqGhc8QjkrPnn9OpeuYhpYsjjbOZIrMspR77aeQDfB5CzyT6I7eZzXe7u6zv.amV1c19kb21haW4veGNvd2FzMDFfSVBPMDE=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.foodsafetykorea.go.kr',
        'Origin': 'https://www.foodsafetykorea.go.kr',
        'Referer': 'https://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHF.do?menu_grp=MENU_NEW01&amp;menu_no=2823',
        'X-Requested-With': 'XMLHttpRequest'
    }

    all_food_data = await scrape_all_data(url, headers, show_cnt, start_idx, total_count, all_data)

    prdlst_report_ledg_no_list = [item['prdlst_report_ledg_no'] for item in all_food_data]

    data_dict = {
        'prdlst_report_ledg_no': prdlst_report_ledg_no_list
    }

    folder_path = './data'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, 'prdlst_report_ledg_no.json')
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)

    print(f"데이터가 {file_path} 파일로 저장되었습니다.")

    # 나중에 파일을 다시 읽어서 추가 정보 수집
    # await scrape_additional_info_from_file(file_path)

if __name__ == "__main__":
    show_cnt = 38616  # 사용자 지정 파라미터
    start_idx = 1   # 사용자 지정 파라미터
    asyncio.run(main(show_cnt, start_idx))
