import requests
import pandas as pd


def get_kosis_data():
    url = (
        "https://kosis.kr/openapi/Param/statisticsParameterData.do"
        "?method=getList"
        "&apiKey=ZjA4OTNjZGRlYjFmNWQyMDk5ZGI2ZGY1ODdlMWEzMGM="
        "&itmId=217001+217002+"
        "&objL1=ALL&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8="
        "&format=json"
        "&jsonVD=Y"
        "&prdSe=Y"
        "&newEstPrdCnt=3"
        "&outputFields=ORG_ID+TBL_ID+TBL_NM+OBJ_ID+OBJ_NM+OBJ_NM_ENG+NM+NM_ENG+ITM_ID+ITM_NM+ITM_NM_ENG+UNIT_NM+UNIT_NM_ENG+PRD_SE+PRD_DE+LST_CHN_DE+"
        "&orgId=117"
        "&tblId=DT_117N_B00003"
    )

    print("KOSIS 데이터 수집을 시작합니다...")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and 'err' in data:
            print(f"API 에러 발생: {data['errMsg']}")
            return pd.DataFrame()

        df = pd.DataFrame(data)

        if not df.empty:
            # 사용자님이 제공해주신 응답 필드 + 실제 데이터값(DT) 매핑 사전
            column_mapping = {
                'ORG_ID': '기관코드',
                'TBL_ID': '통계표ID',
                'TBL_NM': '통계표명',
                'C1_OBJ_ID': '분류값ID',  # KOSIS는 objL1의 ID를 C1_OBJ_ID 등으로 반환
                'C1_OBJ_NM': '분류명',
                'C1_OBJ_NM_ENG': '분류영문명',
                'C1': '분류값ID(코드)',  # 실제 분류 코드
                'C1_NM': '분류값명',  # 실제 분류 이름 (예: 전국, 서울특별시 등)
                'C1_NM_ENG': '분류값영문',
                'ITM_ID': '항목ID',
                'ITM_NM': '항목명',
                'ITM_NM_ENG': '항목영문명',
                'UNIT_NM': '단위명',
                'UNIT_NM_ENG': '단위영문명',
                'PRD_SE': '수록주기',
                'PRD_DE': '수록시점',
                'LST_CHN_DE': '최종수정일',
                'DT': '데이터값'  # ★ 가장 중요한 실제 통계 수치
            }

            # API에서 반환된 컬럼 중 매핑 사전에 있는 것만 이름 변경
            df.rename(columns=column_mapping, inplace=True)

            # 분석을 위해 영어로 된 불필요한 원본 컬럼(매핑되지 않은 컬럼) 제거
            mapped_cols = [col for col in df.columns if col in column_mapping.values()]
            df = df[mapped_cols]

            # '데이터값' 컬럼을 문자열에서 숫자형(Float)으로 변환 (결측치는 NaN 처리)
            if '데이터값' in df.columns:
                df['데이터값'] = pd.to_numeric(df['데이터값'], errors='coerce')

        return df

    except Exception as e:
        print(f"오류 발생: {e}")
        return pd.DataFrame()


# 함수 실행
kosis_df = get_kosis_data()

# 결과 확인 및 저장
if not kosis_df.empty:
    print(f"\n데이터 수집 성공! 총 {len(kosis_df)}건")
    print("\n[데이터 미리보기]")

    # 보기 좋게 주요 컬럼만 먼저 출력
    display_cols = ['수록시점', '분류값명', '항목명', '데이터값', '단위명']
    available_cols = [col for col in display_cols if col in kosis_df.columns]
    print(kosis_df[available_cols].head(10))

    # 전체 컬럼 저장
    kosis_df.to_csv("kosis_medical_data_refined.csv", index=False, encoding="utf-8-sig")
    print("\n'kosis_medical_data_refined.csv' 파일로 저장 완료되었습니다.")
else:
    print("데이터 수집에 실패했습니다.")