use project;

CREATE TABLE pohang_namgu_building (
    `관리번호_PK` VARCHAR(50) PRIMARY KEY COMMENT '법정동-번-지',
    `연면적_sqm` DOUBLE,
    `주용도코드명` VARCHAR(100),
    `세대수_세대` INT,
    `가구수_가구` INT,
    `착공일` VARCHAR(20)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE pohang_namgu_electricity (
    `관리번호_PK` VARCHAR(50) COMMENT '법정동-번-지',
    `사용년월` VARCHAR(10) COMMENT '사용년월(YYYYMM)',
    `사용량_KWh` INT COMMENT '전기사용량'
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE pohang_namgu_gas (
    `관리번호_PK` VARCHAR(50) COMMENT '법정동-번-지',
    `사용년월` VARCHAR(10) COMMENT '사용년월(YYYYMM)',
    `사용량_KWh` INT COMMENT '가스사용량'
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
