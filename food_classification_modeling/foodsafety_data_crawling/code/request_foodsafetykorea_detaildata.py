import os
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

# 추가 데이터를 가져오는 함수
async def get_additional_data(session, prdlst_report_ledg_no):
    try:
        # 요청할 URL 설정
        url = f"https://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHFDetail.do?prdlstReportLedgNo={prdlst_report_ledg_no}&search_code=01&start_idx=1&show_cnt=10&menu_no=2823&menu_grp=MENU_NEW01"

        # HTTP GET 요청
        async with session.get(url) as response:
            if response.status == 200:
                # HTML 페이지 파싱
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                # 데이터 추출 (구조에 맞춰 수정)
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

                    # 수집된 데이터를 딕셔너리로 반환
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
                print(f"Failed to retrieve data for prdlst_report_ledg_no: {prdlst_report_ledg_no}, Status code: {response.status}")
                return None
    except Exception as e:
        print(f"Error occurred while fetching data for prdlst_report_ledg_no: {prdlst_report_ledg_no}, Error: {str(e)}")
        return None

# 추가 정보 수집 함수 (300개씩 끊어서 수집)
async def scrape_additional_info_batch(json_file_path, start_idx, batch_size):
    async with aiohttp.ClientSession() as session:
        # 기존 JSON 파일 읽기
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data_dict = json.load(file)

        prdlst_report_ledg_no_list = data_dict['prdlst_report_ledg_no'][start_idx:start_idx + batch_size]

        # 새로운 데이터를 저장할 딕셔너리 초기화
        total_data_dict = {
            "prdlst_report_ledg_no": prdlst_report_ledg_no_list,  # 기존 prdlst_report_ledg_no 리스트 사용
            "manufacturer_name": [],
            "product_name": [],
            "report_number": [],
            "dosage_usage": [],
            "standards_specifications": []
        }

        # 수집한 데이터를 리스트에 추가
        for idx, prdlst_report_ledg_no in enumerate(prdlst_report_ledg_no_list, start=start_idx):
            print(f"Processing index {idx}: {prdlst_report_ledg_no}")
            data = await get_additional_data(session, prdlst_report_ledg_no)
            
            if data:
                total_data_dict["manufacturer_name"].append(data['manufacturer_name'])
                total_data_dict["product_name"].append(data['product_name'])
                total_data_dict["report_number"].append(data['report_number'])
                total_data_dict["dosage_usage"].append(data['dosage_usage'])
                total_data_dict["standards_specifications"].append(data['standards_specifications'])
            else:
                # 데이터가 없을 경우 None을 추가하여 인덱스를 맞춘다
                total_data_dict["manufacturer_name"].append(None)
                total_data_dict["product_name"].append(None)
                total_data_dict["report_number"].append(None)
                total_data_dict["dosage_usage"].append(None)
                total_data_dict["standards_specifications"].append(None)
            
            await asyncio.sleep(1)  # IP 차단 방지를 위해 1초씩 쉬면서 요청

    # end_idx 계산
    end_idx = start_idx + batch_size

    # 새로운 파일에 업데이트된 데이터를 저장
    new_file_path = f"../data/total_foodsafety_data_{start_idx}_{end_idx}.json"
    with open(new_file_path, 'w', encoding='utf-8') as file:
        json.dump(total_data_dict, file, ensure_ascii=False, indent=4)

    print(f"추가 정보가 {new_file_path} 파일에 저장되었습니다.")
    return total_data_dict

# 메인 실행 함수
async def main():
    # 기존 파일 경로 (1개 상위 폴더의 data 폴더 안에 있는 JSON 파일)
    json_file_path = '../data/prdlst_report_ledg_no.json'

    # Batch 수집 설정
    start_idx = 0  ####시작 인덱스 data 폴더 파일명 보고 매번 수정해서 진행
    batch_size = 100  # 300개씩 처리

    # Batch로 추가 정보 수집
    await scrape_additional_info_batch(json_file_path, start_idx, batch_size)

if __name__ == "__main__":
    asyncio.run(main())
