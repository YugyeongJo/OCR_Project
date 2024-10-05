import aiohttp
import asyncio

async def fetch_all_foodsafety_data(session, url, headers, show_cnt, start_idx):
    # POST 요청에 필요한 데이터
    data = {
        'menu_grp': 'MENU_NEW01',
        'menu_no': '2823',
        'start_idx': start_idx,
        'show_cnt': show_cnt,
    }

    async with session.post(url, headers=headers, data=data) as response:
        if response.status == 200:
            try:
                json_data = await response.json()
                return json_data['list']  # json의 'list' key에 해당하는 데이터 반환
            except Exception as e:
                print(f"JSON 디코딩 오류: {e}")
                return None
        else:
            print(f"요청 실패. 상태 코드: {response.status}")
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

    show_cnt = 38599  # 한 번에 가져올 데이터 수
    start_idx = 1  # 시작 인덱스
    total_count = None  # 전체 데이터 수
    all_data = []  # 모든 데이터를 저장할 리스트

    async with aiohttp.ClientSession() as session:
        while True:
            response_data = await fetch_all_foodsafety_data(session, url, headers, show_cnt, start_idx)
            if response_data:
                all_data.extend(response_data)

                # 총 데이터 개수를 첫 응답에서 추출
                if total_count is None:
                    total_count = int(response_data[0]["total_count"]) if response_data else 0
                    print(f"총 데이터 개수: {total_count}")

                start_idx += show_cnt

                # 모든 데이터를 수집했으면 종료
                if start_idx > total_count:
                    break
            else:
                break

        print(f"총 {len(all_data)}개의 데이터가 수집되었습니다.")
        
        return all_data

async def main():
    all_data = await scrape_all_data()
    print(all_data[:5])  # 처음 5개의 데이터를 출력

if __name__ == '__main__':
    asyncio.run(main())
