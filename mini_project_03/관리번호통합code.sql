use project;

-- 건물 정보와 전기 사용량 데이터를 '관리번호_PK'를 기준으로 join
SELECT 
	b.관리번호_PK,
    b.주용도코드명,
    b.연면적_sqm,
    b.세대수_세대,
    b.가구수_가구,
    b.착공일,
    e.사용년월,
    e.사용량_KWh
FROM pohang_namgu_building b
	JOIN pohang_namgu_electricity e 
        ON b.관리번호_PK = e.관리번호_PK;

select count(*) from pohang_namgu_building;
select count(*) from pohang_namgu_electricity;
select count(*) from pohang_namgu_gas;

-- 건물 정보와 가스 사용량 데이터를 '관리번호_PK'를 기준으로 join
SELECT 
	b.관리번호_PK,
    b.주용도코드명,
    b.연면적_sqm,
    b.세대수_세대,
    b.가구수_가구,
    b.착공일,
    g.사용년월,
    g.사용량_KWh
FROM pohang_namgu_building b
	JOIN pohang_namgu_gas g
        ON b.관리번호_PK = g.관리번호_PK;
