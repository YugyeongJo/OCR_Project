import os
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

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

            # Content-Type이 JSON이 아니지만 실제 데이터는 JSON 형식일 때
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

            # 파싱하고자 하는 데이터 추출
            item_details = soup.find_all('tbody')
            if not item_details:
                print(f"No data found for {prdlst_report_ledg_no}")
                return None

            item_detail = item_details[0].find_all('td')

            if len(item_detail) >= 7:
                # 데이터 추출
                manufacturer_name = item_detail[0].get_text(strip=True)  # 업소명
                product_name = item_detail[1].get_text(strip=True)  # 제품명
                report_number = item_detail[2].get_text(strip=True)  # 신고번호
                dosage_usage = item_detail[6].get_text(strip=True)  # 섭취량/섭취방법
                standards_specifications = item_detail[-1].get_text(strip=True)  # 기준 및 규격

                # 데이터 반환
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

async def scrape_all_data():
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

    show_cnt = 100
    start_idx = 1
    total_count = None
    all_data = []

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

# 모든 prdlst_report_ledg_no에 대해 추가 정보를 요청하고 1초씩 딜레이를 주는 함수
async def scrape_additional_info(data_dict):
    
    async with aiohttp.ClientSession() as session:
        for prdlst_report_ledg_no in data_dict['prdlst_report_ledg_no']:
            data = await get_additional_data(session, prdlst_report_ledg_no)
            if data:
                data_dict[prdlst_report_ledg_no] = data
            await asyncio.sleep(1)  # 1초 간격으로 요청 전송
    
    return data_dict

async def main():
    all_food_data = await scrape_all_data()

    # prdlst_report_ledg_no 값들만 추출
    prdlst_report_ledg_no_list = [item['prdlst_report_ledg_no'] for item in all_food_data]

    # prdlst_report_ledg_no를 key로 하고, list를 value로 가지는 딕셔너리 생성
    data_dict = {
        'prdlst_report_ledg_no': prdlst_report_ledg_no_list
    }

    # prdlst_report_ledg_no를 json 파일로 저장
    
    # 추가 데이터 스크래핑하여 딕셔너리에 저장
    await scrape_additional_info(data_dict)

    # 상대 경로에 저장할 폴더 경로 설정
    folder_path = './data'

    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # JSON 파일로 저장
    file_path = os.path.join(folder_path, 'prdlst_report_ledg_no.json')
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)

    print(f"데이터가 {file_path} 파일로 저장되었습니다.")

# 비동기 코드 실행
if __name__ == "__main__":
    asyncio.run(main())
