# 기관별 정보흐름 및 플랫폼 구조 분석

첨부 연구개발계획서 **RS-2026-25526544**를 바탕으로 작성한 13쪽 보고서와 그림·표입니다. 계획서의 명시 사항, 설명을 위한 설계 재구성, 확인이 필요한 내용을 구분했습니다.

## 수요일 회의 준비자료

[1쪽 협의표 PDF](meeting_preparation/discussion_sheet.pdf?raw=true) · [기록용 엑셀](meeting_preparation/meeting_workbook.xlsx?raw=true) · [준비·진행안](meeting_preparation/meeting_prep.md) · [회의자료 ZIP](meeting_preparation/meeting_preparation.zip?raw=true)

계획서 근거와 회의 질문을 구분한 결정 전 양식입니다. [자료 안내](meeting_preparation/README.md)에서 확인할 수 있으며, 아래 기존 분석 ZIP과는 별도 패키지입니다.

## 한 장 요약

**[A4 가로 1쪽 PDF](overview_1page_ko.pdf?raw=true)** · [고해상도 PNG](overview_1page_ko.png?raw=true) · [편집용 SVG](overview_1page_ko.svg?raw=true) · [단일 파일 HTML](overview_1page_ko.html?raw=true)

기관별 역할과 데이터·제어 흐름, 디지털트윈, 접근·보안 체계를 한 장에 배치했습니다. PDF는 실제 1쪽이며 PNG는 3200 × 2240 해상도입니다.

![기관별 정보흐름과 플랫폼 구조 한 장 요약](overview_1page_ko.png)

## 다운로드

- **[전체 파일 ZIP](rd_platform_analysis.zip?raw=true)**
- **[13쪽 분석 보고서 PDF](report_ko.pdf?raw=true)**
- [단일 파일 HTML 보고서](report_ko.html?raw=true)
- [편집용 Markdown 본문](report_ko.md)
- [기관 간 정보교환 표 CSV](interface_matrix.csv?raw=true)

파일 화면에서 다운로드 아이콘 또는 **Download raw file**을 선택할 수도 있습니다.

## 그림

### 1. 기관별 정보흐름

![기관별 정보흐름도](figures/01_institution_flow.png)

[PNG](figures/01_institution_flow.png?raw=true) · [SVG](figures/01_institution_flow.svg?raw=true)

### 2. 전체 플랫폼 구조

![전체 플랫폼 구조도](figures/02_platform_architecture.png)

[PNG](figures/02_platform_architecture.png?raw=true) · [SVG](figures/02_platform_architecture.svg?raw=true)

### 3. 자율실험 반복 과정

![자율실험 반복 과정](figures/03_closed_loop.png)

[PNG](figures/03_closed_loop.png?raw=true) · [SVG](figures/03_closed_loop.svg?raw=true)

### 4. 접근권한·보안·성과관리

![접근권한·보안·성과관리](figures/04_access_security_governance.png)

[PNG](figures/04_access_security_governance.png?raw=true) · [SVG](figures/04_access_security_governance.svg?raw=true)

## 근거와 범위

- 근거 페이지는 원본 PDF의 파일 순번입니다. 본문 인쇄 쪽수는 대체로 PDF 순번보다 1 작습니다.
- 총괄 계획서에 근거한 구조 분석이며 실제 구축 완료·성능 달성 여부를 평가한 자료는 아닙니다.
- 세부과제별 별도 계획서에만 있는 내부 업무 분담은 확정하지 않았습니다.
- 그림 4종은 SVG·PNG로, 보고서는 PDF·HTML·Markdown으로 제공합니다.
- `source/`에는 산출물 생성 코드가 있습니다. 코드의 기본 경로와 실행 도구는 작성 당시 클라우드 환경 기준입니다.
