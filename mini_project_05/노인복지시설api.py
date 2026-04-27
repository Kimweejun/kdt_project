import requests
import pandas as pd
import time


def get_vworld_senior_facilities(api_key, domain_url):
    url = "https://api.vworld.kr/req/data"
    all_data = []
    page = 1
    total_pages = 1

    print("데이터 수집을 시작합니다...")

    while page <= total_pages:
        params = {
            "service": "data",
            "request": "GetFeature",
            "data": "LT_P_MGPRTFB",  # 노인복지시설 레이어명
            "key": api_key,
            "domain": domain_url,
            "format": "json",
            "geomFilter": "BOX(124,33,132,43)",
            "crs": "EPSG:4326",
            "size": 1000,
            "page": page
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            req_data = response.json()

            status = req_data.get('response', {}).get('status')

            if status == 'OK':
                result = req_data['response']['result']

                # ★ 수정된 부분: API가 준 문자열을 정수형(int)으로 강제 변환 ★
                total_pages = int(req_data['response']['page']['total'])

                features = result['featureCollection']['features']

                for feature in features:
                    properties = feature['properties']
                    geometry = feature['geometry']

                    row = {
                        '분류': properties.get('cat_nam'),
                        '시설명': properties.get('fac_nam'),
                        '전화번호': properties.get('fac_tel'),
                        '구주소': properties.get('fac_o_add'),
                        '새주소': properties.get('fac_n_add'),
                        '경도': geometry['coordinates'][0] if geometry else None,
                        '위도': geometry['coordinates'][1] if geometry else None
                    }
                    all_data.append(row)

                print(f"[{page}/{total_pages}] 페이지 수집 완료 (누적: {len(all_data)}건)")
                page += 1
                time.sleep(0.5)

            elif status == 'NOT_FOUND':
                print("더 이상 데이터가 없습니다.")
                break
            else:
                error_msg = req_data.get('response', {}).get('error', {}).get('text', 'Unknown Error')
                print(f"API 에러 발생: {error_msg}")
                break

        except Exception as e:
            print(f"요청 중 오류 발생: {e}")
            break

    return pd.DataFrame(all_data)


# 인증키 및 도메인 설정
my_api_key = "F8F1453D-7FE0-3F20-866C-4F947260054B"
my_domain = "https://datainstitute.knu.ac.kr/contents/main.do"  # 정상 작동했던 도메인 유지

# 함수 실행
senior_facility_df = get_vworld_senior_facilities(my_api_key, my_domain)

# 결과 저장
if not senior_facility_df.empty:
    print("\n데이터 수집 완료! 총 데이터 건수:", len(senior_facility_df))
    senior_facility_df.to_csv("senior_facilities_vworld.csv", index=False, encoding="utf-8-sig")
    print("'senior_facilities_vworld.csv' 파일로 저장되었습니다.")
else:
    print("데이터를 수집하지 못했습니다.")