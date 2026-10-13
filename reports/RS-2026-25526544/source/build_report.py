from pathlib import Path
import html, json, csv, re

ROOT = Path('/workspace/outputs/rd_platform')
FIG = ROOT / 'figures'
ESC = html.escape
NAVY='#142d4e'; BLUE='#2563a6'; TEAL='#087e8b'; ORANGE='#b95b23'; PURPLE='#7554a3'; GRAY='#607186'

class SVG:
    def __init__(self, title, sub, h=1060):
        self.h=h
        self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{h}" viewBox="0 0 1600 {h}" role="img" aria-label="{ESC(title)}">',
        '<defs>'+''.join(f'<marker id="a{i}" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M0,0 L10,4 L0,8 Z" fill="{c}"/></marker>' for i,c in enumerate([BLUE,TEAL,ORANGE,PURPLE,GRAY]))+'</defs>',
        '<rect width="1600" height="100%" fill="#ffffff"/>',
        '<style>text {font-family:"Noto Sans CJK KR",sans-serif;} .node-title{font-weight:700;} </style>']
        self.text(54,55,title,32,NAVY,weight=700)
        self.text(54,93,sub,17,GRAY)
    def text(self,x,y,t,size=21,color=NAVY,anchor='start',weight=400):
        lines=t.split('\n')
        self.s.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.45}">{ESC(v)}</tspan>' for i,v in enumerate(lines))+'</text>')
    def rect(self,x,y,w,h,fill='#f2f6fb',stroke='#d9e2ed',dash=False,r=14):
        self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"'+(' stroke-dasharray="8 6"' if dash else '')+'/>')
    def box(self,x,y,w,h,title,body='',color=BLUE,fill='#f1f6fc',size=21):
        self.rect(x,y,w,h,fill,color)
        self.s.append(f'<rect x="{x}" y="{y+15}" width="5" height="{h-30}" rx="2" fill="{color}"/>')
        self.text(x+22,y+36,title,23,color,weight=700)
        if body: self.text(x+22,y+72,body,size,NAVY)
    def path(self,pts,color=BLUE,dash=False,both=False,label=None,lx=0,ly=0,size=18):
        idx=[BLUE,TEAL,ORANGE,PURPLE,GRAY].index(color)
        d='M'+' L'.join(f'{x},{y}' for x,y in pts)
        self.s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round" marker-end="url(#a{idx})"'+(f' marker-start="url(#a{idx})"' if both else '')+(' stroke-dasharray="9 6"' if dash else '')+'/>')
        if label:
            # White underlay keeps labels readable across a line.
            lines=label.split('\n'); width=max(len(x) for x in lines)*size*.7+18
            self.rect(lx-7,ly-size,width,size*1.45*len(lines)+7,'white','white',r=3)
            self.text(lx,ly,label,size,color)
    def foot(self,text):
        self.text(54,self.h-39,text,16,GRAY)
    def save(self,name):
        p=FIG/(name+'.svg'); p.write_text('\n'.join(self.s+['</svg>']))
        return p.name

def diagrams():
    g=SVG('01  기관별 기술 정보흐름','실선: 계획서에 명시된 흐름  ·  점선: 기관별 기능을 연결한 설계 재구성  ·  F번호: 정보교환 표와 연결')
    g.box(50,145,330,185,'한국전자기술연구원 · KETI','총괄 아키텍처·소재 DB\nMaterial Studio / DFT\n성능·보안·통합 검증',color=NAVY if False else BLUE)
    g.box(590,145,430,185,'인실리코','통합 DB / REST API\n물성 예측 모델 / MLOps\n소재 표현 변환·접근 이력',color=TEAL,fill='#eef8f7')
    g.box(1220,145,330,185,'성균관대학교','다음 실험 조건·전략 결정\n능동학습 / Workflow\n3차년도 Multi-agent',color=PURPLE,fill='#f6f2fb',size=20)
    g.box(50,605,400,225,'세부 1·2·3 실험실','피엔에이치테크 · OLED Premix\n동진쎄미켐 · TFE 유기소재\n이엠테크 · 식각 소재·공정\n장비·로봇·센서 / 기업 로컬',color=BLUE,size=20)
    g.box(640,605,380,225,'한양대학교','ROS2 / 장비 Node\n실험 실행·자원 스케줄링\n재시도·상태 전이\n데이터·이벤트 Hub',color=ORANGE,fill='#fff7ef')
    g.box(1210,605,340,225,'이즈파크','디지털트윈 / 3D / KPI\n수신·제어 어댑터\n시계열·배치·메타 DB\n세부별 현장 실증',color=BLUE,size=20)
    g.path([(380,233),(590,233)],TEAL,label='F04 기초 소재·\n시뮬레이션 DB',lx=397,ly=208,size=18)
    g.path([(1020,220),(1220,220)],PURPLE,dash=True,both=True,label='F05 학습 데이터·\n예측 결과 / 모델 연계',lx=1033,ly=171,size=17)
    g.path([(450,667),(640,667)],TEAL,label='F01 결과·센서·로그',lx=453,ly=645,size=17)
    g.path([(640,768),(450,768)],ORANGE,label='F09 실행 명령',lx=476,ly=752,size=18)
    g.path([(770,605),(770,330)],TEAL,label='F02 REST API\n공유 대상 데이터 저장',lx=542,ly=451,size=18)
    g.path([(1385,330),(1385,442),(960,442),(960,605)],PURPLE,dash=True,label='F06 실험 조건·워크플로 → 실행 계층',lx=962,ly=427,size=18)
    g.path([(1020,666),(1210,666)],TEAL,label='F03 상태·측정값',lx=1029,ly=645,size=17)
    g.path([(1210,768),(1020,768)],ORANGE,label='F08 제어 이벤트',lx=1031,ly=750,size=17)
    g.path([(1020,295),(1130,295),(1130,515),(1270,515),(1270,605)],BLUE,both=True,label='F07 실험 조건 ⇄ 예측 결과\n디지털트윈 연동 API',lx=1145,ly=365,size=17)
    g.box(50,880,1500,105,'한국디스플레이연구조합 · 별도 접근/사업관리 흐름','회원 로그인·등급·2차 인증 → 권한별 디지털트윈 접속  |  성과·진도 → 성과 DB·협의체 (그림 04)',color=GRAY,fill='#f6f8fa',size=20)
    g.foot('근거: PDF 21–28, 34–41, 45–50, 62–67쪽. KETI의 전 기관 통합 검증은 화살표 혼잡을 줄이기 위해 상단 역할로 표시.')
    g.save('01_institution_flow')

    g=SVG('02  전체 플랫폼 논리 구조','개발 책임과 데이터 저장 목적을 기준으로 재구성한 구조도 · 물리 서버 수나 제품 스택을 확정한 배치도가 아님',h=1190)
    g.box(50,132,480,120,'회원 접근 포털 · 연구조합','등급별 접근 정책 / 2차 인증 / DT 접속',GRAY,'#f6f8fa',20)
    g.box(560,132,480,120,'연구자 웹 · 인실리코','데이터 등록·검색·관리 / 추론 실행',TEAL,'#eef8f7',20)
    g.box(1070,132,480,120,'현장 화면 · 이즈파크','세부별 3D 디지털트윈 / KPI / DID',BLUE,size=20)
    g.text(50,297,'서비스 계층',20,NAVY,weight=700)
    g.box(50,326,330,180,'데이터 API · 인실리코','인증된 CRUD / 검색\n공개·보안 등급 / 로그\n소재-공정-소자 연계',TEAL,'#eef8f7',20)
    g.box(410,326,345,180,'물성 예측 · 인실리코','소재·조성·공정 → 물성\n모델 추론 / 결과·버전\n재학습·검증·배포',TEAL,'#eef8f7',20)
    g.box(785,326,345,180,'실험 의사결정 · 성균관대','탐색·능동학습·최적화\nWorkflow / 전략 개선\nMulti-agent (3차년도)',PURPLE,'#f6f2fb',19)
    g.box(1160,326,390,180,'디지털트윈 · 이즈파크','수신·분석·3D·KPI\n시뮬레이션 파라미터 처리\n제어 이벤트 송신',BLUE,size=20)
    g.path([(290,252),(290,275),(215,275),(215,326)],GRAY,dash=True)
    g.path([(800,252),(800,272),(583,272),(583,326)],TEAL)
    g.path([(1310,252),(1310,326)],BLUE,both=True)
    g.text(50,558,'데이터 계층',20,NAVY,weight=700)
    g.box(50,582,1080,170,'총괄 데이터 호수·통합 DB · KETI + 인실리코','실험 결과 ↔ 시뮬레이션 결과를 구분 관리  |  소재·공정·소자 / 학습 데이터\n입력 조건·예측 결과·모델 버전 / 접근 이력  |  KETI 기초 소재 DB 연계\n공유 학습 데이터와 Private 데이터의 범위·접근권한 분리',TEAL,'#eef8f7',21)
    g.box(1160,582,390,170,'DT 전용 저장소 · 이즈파크','시계열 DB: 실시간 장비 값\n관계형 DB: 배치·결과 데이터\n레지스트리: 메타·참조 정보',BLUE,size=19)
    for x in [215,583,955]: g.path([(x,506),(x,582)],TEAL,both=True,dash=(x==955))
    g.path([(1350,506),(1350,582)],BLUE,both=True)
    g.box(50,827,1500,120,'현장 실행·연동 계층 · 한양대학교','ROS2 Node / Topics·Services·Actions / 실험 Orchestration / Resource & Schedule Manager / 데이터·이벤트 Hub',ORANGE,'#fff7ef',21)
    g.path([(355,827),(355,752)],TEAL,label='공유 대상 업링크',lx=371,ly=793,size=17)
    g.path([(1030,506),(1146,506),(1146,827)],PURPLE,dash=True,label='실험 계획',lx=1000,ly=799,size=17)
    g.path([(1465,827),(1465,752)],BLUE,both=True,label='실시간 상태 / 제어',lx=1240,ly=793,size=17)
    for x,title,body in [(50,'세부 1 · 피엔에이치테크','OLED 증착 Premix'),(560,'세부 2 · 동진쎄미켐','TFE 박막봉지 유기소재'),(1070,'세부 3 · 이엠테크','고정세 패턴 식각 소재·공정')]:
        g.box(x,995,480,112,title,body,BLUE,size=21)
        g.path([(x+240,947),(x+240,995)],ORANGE,both=True)
    g.foot('근거: PDF 9–11, 21–24, 28–29, 34–50, 63, 65, 127쪽. Private 로컬모드와 포털 접근 흐름은 그림 04 참조.')
    g.save('02_platform_architecture')

    g=SVG('03  자율실험의 한 사이클과 두 피드백 루프','기능 순서를 재구성한 도식 · 점선의 기관 간 직접 호출 규격은 계획서에 미확정 · DT 경유 제어는 병행 가능한 경로',h=1190)
    cols=[(140,'연구자 / KETI',BLUE),(410,'성균관대',PURPLE),(685,'인실리코',TEAL),(960,'이즈파크',BLUE),(1235,'한양대',ORANGE),(1480,'세부 실험실',BLUE)]
    for x,t,c in cols:
        g.rect(x-108,132,216,73,'#f3f6fa',c)
        g.text(x,176,t,21,c,'middle',700)
        g.s.append(f'<path d="M{x},213 V1015" stroke="#c9d5e3" stroke-width="1.5" stroke-dasharray="5 6"/>')
    rows=[(265,140,410,'① 목표 물성·제약 / 초기 탐색 범위',PURPLE,True),
          (335,410,685,'② 데이터 조회·후보 조건 평가',PURPLE,True),
          (405,685,410,'③ 물성 예측 / 축적 실험 데이터',TEAL,True),
          (475,410,1235,'④ 다음 조건·워크플로 결정 → 실행 연동',PURPLE,True),
          (545,685,960,'보조 경로: 추론 결과·파라미터',BLUE,False),
          (605,960,1235,'DT 제어 이벤트',ORANGE,False),
          (680,1235,1480,'⑤ 장비 명령·실행',ORANGE,False),
          (750,1480,1235,'⑥ 결과·센서·상태',TEAL,False),
          (815,1235,685,'⑦ 공유 대상 데이터·로그 저장 (REST API)',TEAL,False),
          (875,1235,960,'동작·상태 실시간 반영',BLUE,False),
          (945,685,410,'⑧ 새 결과 반영 → 다음 실험 선택',PURPLE,True)]
    for y,a,b,t,c,d in rows:
        g.path([(a,y),(b,y)],c,dash=d)
        # Labels live above arrows, with enough room for short neighboring messages.
        g.text((a+b)/2,y-14,t,18 if abs(a-b)>260 else 16,c,'middle')
    g.box(50,1025,735,94,'루프 A · 실험 의사결정 갱신','성균관대: 결과 → 다음 조건·탐색 정책 변경',PURPLE,'#f6f2fb',20)
    g.box(815,1025,735,94,'루프 B · 예측 모델 갱신','인실리코: 신규 데이터 → 재학습 → 비교 검증 → 배포',TEAL,'#eef8f7',19)
    g.foot('근거: PDF 26–28, 34–41, 45–50, 62–63쪽. KETI는 예측-실측·가상-실물 정합성과 전체 통합 결과를 검증.')
    g.save('03_closed_loop')

    g=SVG('04  사용자 접근·데이터 보안·사업관리의 분리','일반데이터 = 총괄 공유 학습용으로 분류된 데이터 · 대외 무조건 공개를 뜻하지 않음',h=1120)
    boxes=[(50,300,'회원·연구자','기업 회원 로그인'),(410,350,'연구조합 접근 체계','Operator / Affiliate / Insight'),(820,325,'고위험 접근','2차 인증·접근권한 확인'),(1205,345,'허용된 DT 기능','영상·분석·실데이터 등')]
    for x,w,t,b in boxes:g.box(x,140,w,115,t,b,GRAY,'#f6f8fa',18)
    for a,b in [(350,410),(760,820),(1145,1205)]:g.path([(a,197),(b,197)],GRAY)
    g.text(50,298,'접근 정책: 연구조합  |  DB/API 권한·접근로그: 인실리코  |  작동·기록 누락 점검: KETI',21,NAVY,weight=700)
    g.rect(50,335,690,455,'#fff8f0','#d6ac81',True)
    g.text(78,375,'기업 현장 · 각 세부 로컬 보안모드',26,ORANGE,weight=700)
    g.box(80,408,630,125,'현장 원료·레시피·실험 결과','일반/Private 분류 · Private는 자체 서버 실험\n공유 허용 데이터만 외부 경로로 분기',ORANGE,'#fffdf9',20)
    g.box(80,593,630,125,'로컬 실험·배포된 AI·ROS2·디지털트윈','기업 보안모드 운영을 지원하는 구성으로 해석\n세부별 설치 범위·모델 배포 방식은 상세 설계 필요',ORANGE,'#fffdf9',20)
    g.path([(395,533),(395,593)],ORANGE,both=True)
    g.rect(845,335,705,455,'#f0f8f8','#83b8b4',True)
    g.text(873,375,'공유 연계 경로 · 변환 후 총괄 전송',26,TEAL,weight=700)
    g.box(875,408,645,125,'전송 전 공유 선별·소재 표현 변환','SMILES·Descriptor → 암호화/Embedding 벡터\n총괄 전송 이전에 수행 / 위치·방식은 상세 합의',TEAL,'#fbfefe',20)
    g.box(875,593,645,125,'중앙 통합 DB · 학습·예측·모델 갱신','일반데이터 기반 학습 / 최적 레시피·AI SW 하향 제공\n변환·벡터화 자체가 비복원성을 입증하는 것은 아님',TEAL,'#fbfefe',19)
    g.path([(1197,533),(1197,593)],TEAL)
    g.path([(740,460),(845,460)],TEAL,label='공유 허용분',lx=746,ly=437,size=15)
    g.path([(1197,718),(1197,758),(395,758),(395,718)],BLUE,dash=True,label='레시피·AI SW 제공 (세부 배포 절차는 미확정)',lx=510,ly=742,size=18)
    g.text(50,847,'사업관리·성과확산 흐름  |  연구용 원천 DB와 성과관리 DB를 구분',23,NAVY,weight=700)
    g.box(50,885,420,125,'총괄·세부 수행기관','진도·특허·논문·고용·사업화 성과\n개발 결과·기술 이슈·애로사항',GRAY,'#f6f8fa',20)
    g.box(595,885,430,125,'한국디스플레이연구조합','성과 DB / 진도점검 / 워크숍\n수요-공급 협의체 / 공개범위 관리',GRAY,'#f6f8fa',20)
    g.box(1150,885,400,125,'수요기업·회원사','개발성과 활용 검토·의견 환류\n인증·활용 확인 / 승인된 성과 열람',GRAY,'#f6f8fa',19)
    g.path([(470,946),(595,946)],GRAY)
    g.path([(1025,946),(1150,946)],GRAY,both=True)
    g.foot('근거: PDF 11, 15, 17, 28–30, 42, 51, 63, 132, 140쪽. 포털 등급별 세부 허용표와 Private 반출 규격은 미확정.')
    g.save('04_access_security_governance')

PAGES=[]
MD=[]
def para(t, cls=''):
    return f'<p class="{cls}">{t}</p>'
def callout(t): return f'<div class="callout">{t}</div>'
def table(headers,rows,cls=''):
    return '<table class="'+cls+'"><thead><tr>'+''.join('<th>'+h+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in r)+'</tr>' for r in rows)+'</tbody></table>'
def grid(items):
    return '<div class="cards">'+''.join('<div class="card"><h3>'+t+'</h3><p>'+b+'</p></div>' for t,b in items)+'</div>'
def add(title,body,sub=''):
    n=len(PAGES)+1
    PAGES.append(f'<section class="page" id="p{n}"><header><span>RS-2026-25526544 · 계획서 근거 분석</span><span>{n:02d} / 13</span></header><h1>{title}</h1>'+ (f'<p class="subtitle">{sub}</p>' if sub else '')+f'<main>{body}</main><footer><span>근거 표기: PDF 파일 순번. 본문 인쇄 쪽수는 대체로 PDF 순번 − 1.</span><span>계획 내용의 구조화 · 구축 완료나 실제 성능을 뜻하지 않음</span></footer></section>')
    MD.append('## '+title+'\n\n'+html_to_md(body)+'\n')
def html_to_md(s):
    # Preserve table contents as readable Markdown for later editing.
    def convert(m):
        rows=re.findall(r'<tr>(.*?)</tr>',m.group(0),re.S)
        rows=[[re.sub('<[^>]+>',' ',c).strip() for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>',r,re.S)] for r in rows]
        if not rows:return ''
        return '\n'+'\n'.join(['| '+' | '.join(rows[0])+' |','| '+' | '.join(['---']*len(rows[0]))+' |']+['| '+' | '.join(r)+' |' for r in rows[1:]])+'\n'
    s=re.sub(r'<table.*?</table>',convert,s,flags=re.S)
    s=re.sub(r'<img[^>]+src="([^"]+)"[^>]*>',lambda m:f'\n![구조도]({m.group(1)})\n',s)
    s=re.sub(r'<h[23]>(.*?)</h[23]>',r'\n### \1\n',s)
    s=s.replace('<br>',' / ').replace('</p>','\n\n').replace('</div>','\n').replace('</li>','\n')
    return html.unescape(re.sub('<[^>]+>','',s)).strip()

FLOW_ROWS=[
['F01','세부 1·2·3 → 한양대 미들웨어','실험 조건·결과, 센서값, 상태·로그','장비별 Node / ROS2 Topics. 장비 실행 결과를 표준화해 수집','28, 41, 50, 62'],
['F02','한양대 미들웨어 → 인실리코 통합 DB','공유 대상으로 분류된 공정·실험 데이터 및 로그','RESTful API 저장. 암호화·표현 변환 후 총괄 업링크','23–24, 34, 63'],
['F03','한양대 미들웨어 → 이즈파크 DT','실시간 상태, 측정값, 장비 동작·이벤트','수신 어댑터 → 시계열 DB → 3D·KPI. Tag List로 항목 정의','25–26, 38–39, 46–47'],
['F04','KETI → 공통 DB·AI 활용 계층','Material Studio/DFT 기반 소재 특성·표준 학습 데이터','기초 DB 구축·갱신, 실험 데이터와 결합. 전송 규격은 미기재','21–22, 32–33, 60, 65'],
['F05','인실리코 데이터·예측 ↔ 성균관대 의사결정','축적 실험 데이터, 후보 조건, 예측 결과, 학습용 갱신 정보','기능상 필요한 연계로 재구성. 직접 호출 방식·공통 모델 범위는 미확정','26–27, 35–40, 48–49'],
['F06','성균관대 운영 계층 → 한양대 실행 계층','다음 실험 조건·순서, 워크플로, 재실행·전략 판단','상위 실험 결정과 장비 실행의 연결로 해석. 두 orchestration의 경계 합의 필요','39–41, 49–50, 67'],
['F07','이즈파크 DT ↔ 인실리코 추론 API','DT 실험 조건 → 예측 결과','조건 입력·결과 반환 API 명시. 입력 조건·추론 결과·모델 버전은 DB에 기록','34–35, 38–39, 46–47'],
['F08','이즈파크 DT → 한양대 미들웨어','시뮬레이션/화면 입력에서 유래한 제어 파라미터·이벤트','DT가 제어 이벤트를 송신하고 미들웨어가 장비 명령으로 변환','11, 26, 47'],
['F09','한양대 미들웨어 → 세부 장비·로봇','실험 실행·설정·작업 명령, 실행 순서·자원 배정','ROS2 Services/Actions 및 장비 Node. 재시도·대체 시나리오 지원','28 그림, 41, 50, 63'],
['F10','각 세부 → 이즈파크','장비 목록, 3D CAD·2D 도면, 배치·동작·Takt, KPI 요구','DT 제작·현장 적용용 설계 자료. 실시간 센서 흐름과 구분','24–25, 39, 47'],
['F11','총괄 플랫폼 → 각 세부','최적 레시피, AI 분석 SW·학습 모델, 성능 개선 내용','Down-link 및 현장 활용 명시. 패키징·배포·버전 전환 절차는 미정','15 그림, 33 그림, 44, 63'],
['F12','회원·연구자 ↔ 연구조합 접근 체계 ↔ DT','인증·회원등급, 접근 요청, 허용된 영상·분석·실데이터','포털 연동·2차 인증. 세부 권한표·토큰 전달 규격은 미정','11, 28–29, 42, 51, 63'],
['F13','수행기관 → 연구조합 ↔ 수요기업·회원사','진도·특허·논문·사업화, 기술 이슈·수요 의견·활용 확인','성과 DB·협의체·워크숍·확산. 연구 원천데이터 수집과 별도 목적','17, 29–30, 42, 51, 132'],
]

def report():
    add('기관별 정보흐름과 전체 플랫폼 구조',
        '<div class="hero"><div class="eyebrow">AI 자율실험실용 가상공간 구축 및 디스플레이 소재 개발 플랫폼 기술 개발</div><h2>3개 소재 실험실의 결과가<br>다음 실험과 예측 모델을 함께 개선하는 구조</h2><p>총괄 6개 기관의 공통 플랫폼 + 세부 3개 실험실 + 회원 접근·성과확산 체계</p></div>'+
        grid([('데이터의 상향 흐름','세부 실험실 → 한양대 ROS2·Hub → 총괄 통합 DB / 이즈파크 디지털트윈'),('의사결정의 하향 흐름','성균관대 실험 조건·전략 / 인실리코 물성 예측 → 실행 연동 → 한양대 → 세부 장비'),('검증과 접근관리','KETI: 전체 구조·소재 DB·정합성 검증 / 연구조합: 회원 접근·진도·성과확산')])+
        callout('<b>해석의 핵심:</b> 인실리코의 물성 예측, 성균관대의 실험 의사결정, 한양대의 장비 실행, 이즈파크의 디지털트윈을 구분한다. 전체 플랫폼을 단일 웹사이트나 단일 DB로 보면 책임과 정보 경계가 사라진다.')+
        para('<b>근거와 범위.</b> 업로드된 협약용 통합형 총괄 계획서 141쪽을 대상으로 기술개발 본문·원문 도표·팀 편성도·수정대비표를 대조했다. 본문 인용은 PDF 순번 기준이다. 세부 1·2·3의 별도 계획서는 제공되지 않아 세부 참여기관의 내부 데이터 분담은 확정하지 않는다.')+
        para('<b>표시 원칙.</b> <span class="pill">명시</span> 문서에 적힌 역할·구성·흐름 / <span class="pill purple">재구성</span> 명시된 기능을 연결한 논리 설계 / <span class="pill orange">확인 필요</span> 구현 규격 또는 문서 내 불일치. 모든 수치는 개발 목표이며 달성 실적이 아니다.'),
        '대상 기간: 2026.04.01–2028.12.31 · 과제번호 RS-2026-25526544 · 근거: PDF 1, 9–15, 62–67쪽')

    rows=[
    ['한국전자기술연구원<br><b>KETI · 총괄</b>','기존 실험·시뮬레이션, 세부 요구, 실측·예측, 보안·운영 로그','전체 아키텍처, 기초 소재 DB, AI 알고리즘·소재 표현 적합성 검토, 통합·보안·가상화 검증','각 개발기관·세부과제에 DB·방향·평가 피드백','21–22, 32–33, 44, 65, 67'],
    ['<b>인실리코</b>','원료·조성·공정·실측, 시뮬레이션, 추론 조건','통합 DB·REST API·웹, 물성 예측 모델, MLOps, 소재 암호화 모듈, 접근 이력','데이터 서비스·예측 결과·모델을 AI/DT/세부에 제공','22–24, 33–38, 45–46, 65'],
    ['<b>이즈파크</b>','장비 CAD·도면·시퀀스, 상태·센서, 시뮬레이션·추론 결과','실시간 3D·KPI, 전용 저장소·어댑터, 제어 이벤트, 현장 DT','연구자·현장·권한 있는 회원에 화면; 미들웨어에 제어 이벤트','24–26, 38–39, 46–47'],
    ['<b>성균관대학교</b>','실험 workflow·로그·센서·조건·결과, 축적 학습 데이터','표준 데이터, 탐색·능동학습, 다음 실험 결정, 상위 운영, Multi-agent·전략 개선','실행 계층에 실험 계획; 공통 저장소로 분석·학습 정보 환류','26–27, 39–41, 48–50'],
    ['<b>한양대학교</b>','장비별 I/O·측정·상태, 실행 조건·시나리오·명령','ROS2·Node, 순차/병렬 실행, 자원·일정, 재시도, 데이터·이벤트 Hub','장비에 실행; DB·DT·AI에 결과·상태·이벤트 연계','28, 41, 50, 65, 67'],
    ['<b>한국디스플레이연구조합</b>','회원 정보·접속 요청, 세부 진도·성과·애로, 수요기업 의견','등급별 접근·2차 인증·연동 규격 직접 개발, 성과 DB, 협의체·홍보','권한별 DT 접근; 총괄·세부·수요기업에 협의·성과 환류','28–30, 42, 51, 132, 140'],
    ]
    body=table(['총괄 수행기관','받는 정보','담당 기능·생산 정보','보내는 대상·결과','PDF'],rows,'dense')
    body+='<h2>세부 실험실과 참여기관의 범위</h2>'
    body+=table(['세부 / 주관기관','개발 대상','편성도에 기재된 참여기관'],[
    ['1 / 피엔에이치테크','OLED 증착 소재 사전 혼합(Premix)','한국전자기술연구원, 경희대, 충남테크노파크, 삼성디스플레이'],
    ['2 / 동진쎄미켐','OLED 박막봉지(TFE) 유기소재','경기대, 성균관대, 고려대, 중앙대, 충남테크노파크, 삼성디스플레이'],
    ['3 / 이엠테크','디스플레이 고정세 패턴 식각 소재·공정','한국전자기술연구원, 경상대(원문 표기), 연세대, 삼성디스플레이'],
    ],'dense')
    body+=para('세부 주관은 PDF 1쪽, 참여기관 목록은 PDF 66쪽(본문 65쪽). 세부 참여기관별 입력·출력·서버 운영자는 이 총괄 계획서만으로 특정할 수 없다. 같은 기관이 총괄과 세부에 함께 참여하더라도 책임 범위와 데이터 권한을 자동으로 동일시하지 않는다.','note')
    add('기관별 책임과 정보의 소유 범위',body)

    add('누가 누구에게 무엇을 보내는가', '<img class="diagram" src="figures/01_institution_flow.svg" alt="기관별 기술 정보흐름도">', '기관을 기능 책임자로 표시했다. 화살표가 기관별 독립 서버나 기관 간 직접 네트워크를 뜻하지는 않는다.')

    add('정보교환 목록 · 입력·출력·전달 목적',table(['ID','보내는 쪽 → 받는 쪽','정보 / 산출물','경로·활용·확정 수준','PDF'],FLOW_ROWS,'dense flow')+para('F05·F06은 기관별 업무를 연결한 논리적 인터페이스이며 직접 API 호출 계약이 아니다. F11의 AI SW/모델 하향 제공은 원문 개념도에 있으나 배포 운영 규격은 명시되지 않았다.','note'))

    add('플랫폼은 어떤 구성요소로 이루어지는가','<img class="diagram" src="figures/02_platform_architecture.svg" alt="전체 플랫폼 논리 구조도">','중앙 통합·학습 기능과 각 세부 현장 실행·가시화 기능을 함께 가진다. 그림의 계층과 배치는 설명을 위한 재구성이다.')

    add('저장소와 운영 책임을 구분한 상세 구조',
        table(['구성요소','보관·처리할 정보','계획서상 담당 / 구조 해석','근거 PDF'],[
        ['기초 소재 DB','Material Studio/DFT 시뮬레이션, 구조·광학·전기적 특성, 초기 학습 데이터','KETI 구축·갱신. 통합 DB로 연결할 입력 자산','22, 32–33, 60, 130'],
        ['데이터 호수 / 통합 DB','소재-공정-소자, 실험·시뮬레이션, 권한·이력, 모델 추론 기록','KETI + 인실리코 통합 플랫폼. DB/API 구현은 인실리코','14–15, 22–24, 33–35, 65'],
        ['모델 관리·재학습 체계','모델 버전, 학습·평가 성능, 배포 대상, 모니터링 결과','인실리코 MLOps. 별도 제품명이나 독립 물리 DB는 미확정','24, 38, 45–46'],
        ['실험 의사결정 공유 메모리','기획·실행 관리·분석·전략 Agent가 공유하는 데이터·의사결정','성균관대 3차년도 구상. 중앙 저장소와의 동일성·연계 방식은 미정','48–50'],
        ['DT 시계열 DB','실시간 장비 수집값','이즈파크. 실시간 표시·3D 동기화 목적','46–47'],
        ['DT 관계형·레지스트리 DB','배치/비주기 결과, 장비·공정 시나리오, 코드·분류, 메타데이터','이즈파크. 통합 DB와 별도 논리 저장 목적을 가진다','46–47'],
        ['실험 데이터·이벤트 Hub','현재 상태, 실행·측정 결과, 장비·실험 로그·이벤트','한양대. 실시간 실행·상태 통합의 책임; 별도 저장제품은 미기재','41, 50'],
        ['회원·접속 및 성과관리','접근등급·정책·인증 흐름; 진도·특허·논문·고용·사업화','연구조합. 연구 원천 DB와 목적이 다른 업무 저장 영역으로 해석','28–30, 42, 51, 132'],
        ['기업 Private 영역','기업 고유 원료·핵심 레시피 및 보안모드 실험 정보','기업 자체 서버/로컬모드. 배포·공유·권한 정책 상세 합의 필요','11, 63'],
        ],'dense')+
        '<h2>물리 배치에 대해 문서가 말하는 범위</h2>'+
        grid([('총괄','PDF 127쪽: KETI 내 DB 서버·AI 서버 설치 계획. “총괄 중앙 서버”는 PDF 63쪽에 명시.'),('각 실험실','PDF 47쪽: 각 세부 현장 DT 서버·DID 세팅. PDF 15쪽: 배포 AI SW·미들웨어·장비 구성.'),('아직 정해지지 않음','클라우드 사업자, HA·백업 배치, 네트워크 망 분리, 포털 호스팅, 서버·DB 간 복제 구조.')])+
        para('총괄 통합 DB가 DT 저장소·성과 DB·기업 Private 원본을 물리적으로 모두 흡수한다고 해석하지 않는다. 데이터셋 단위 원본 관리 책임과 동기화 방향은 상세 설계에서 합의해야 한다.','note'))

    add('실험은 어떻게 반복되고 개선되는가','<img class="diagram" src="figures/03_closed_loop.svg" alt="자율실험 순서도">','이 그림은 메시지 API 명세가 아니라 기능 순서도다. DT를 통한 제어와 AI 운영 계층의 실행 요청이 함께 존재하므로 제어 우선순위가 필요하다.')

    add('세부별 공유 데이터와 데이터 계약 초안',
        table(['출처','올라오는 정보','돌아가는 정보 / 활용','근거'],[
        ['공통','원료 정보, 성분·배합비·공정조건, 센서·측정·장비 상태·로그','예측 물성, 후보 조성·최적 레시피, AI 분석 SW, 실험 조건·제어','PDF 15, 62–63'],
        ['1세부 · 피엔에이치테크','Premix 배합비, 두께·굴절률·PL 특성 등','배합비별 물성 예측과 다음 조성·조건 추천','PDF 35, 45, 62'],
        ['2세부 · 동진쎄미켐','TFE 유기소재·단량체/나노입자 배합비, 분산도·두께·유전율 등','봉지 소재 조성별 특성 예측과 후속 실험 추천','PDF 35, 45, 62'],
        ['3세부 · 이엠테크','식각액 조성·배합비, 두께·식각 bias·패턴 특성; 모델 예시에는 전도도도 제시','식각 소재·공정의 물성 예측과 조성·조건 추천','PDF 35, 45, 62'],
        ['KETI 시뮬레이션','Material Studio/DFT 계산값, 표준화된 기초 소재 데이터셋','초기 학습·후보 스크리닝, 실측과 예측의 검증','PDF 22, 32–33, 60'],
        ],'dense')+
        callout('<b>예측 물성을 모두 개발한다고 단정하면 안 된다.</b> PDF 35·45쪽은 각 세부에서 필요한 물성 중 연차별 모델을 선정하는 계획이다. 2차년도 세부당 1개, 3차년도 추가 1개로 누적 6개 모델을 목표로 한다.')+
        '<h2>기관 간 합의할 데이터 계약 · 아래 필드 묶음은 설계 제안</h2>'+
        table(['계약 영역','최소 합의 항목(제안)','문서상 출발점'],[
        ['실험·시료 식별','과제/기관, experiment_id, sample_id, recipe_id, 장비 ID, 원본 출처','소재-공정-소자 ENTITY와 세부별 스키마 (22–23, 33쪽)'],
        ['측정값·상태','Tag ID, 의미, 자료형, 값·단위·정상범위, 측정시각, 갱신주기, 품질·오류 상태','Tag List의 ID·설명·타입·범위·주기·중요도 (38쪽)'],
        ['실행 요청','요청 ID, 조건·단위, 순서·자원, 실행 허용범위, 취소·중단·실패 상태, 중복 실행 방지','순차/병렬 실행·재시도·Resource Manager (28, 41쪽)'],
        ['예측·학습 기록','입력 조건, 출력 물성, 모델 버전, 학습 데이터 버전, 평가 기준, 실측 연결 ID','입력·추론 결과·모델 버전 저장 및 MLOps (35, 38, 45쪽)'],
        ['공유·권한','일반/Private 분류, 데이터 소유기관, 허용 목적·대상, 변환 방식·버전, 접근 이력','데이터 등급·접근로그·소재 표현 변환 (11, 23, 34, 63쪽)'],
        ],'dense')+
        para('실험 원본, 시뮬레이션, AI 예측치를 서로 구분해 저장해야 평가 과정에서 예측값이 실측값으로 섞이지 않는다. 통합 검색 기능과 데이터 출처 분리는 함께 구현할 수 있다. 근거: PDF 9–10, 33–35쪽.','note'))

    add('회원 접근·보안모드·성과관리의 정보흐름','<img class="diagram" src="figures/04_access_security_governance.svg" alt="접근권한과 보안 및 성과관리 정보흐름">','데이터를 모으는 기술 흐름, 사용자에게 기능을 허용하는 접근 흐름, 연구성과를 관리하는 업무 흐름을 구분했다.')

    add('접근 권한과 공개 범위를 어떻게 적용하는가',
        table(['영역','계획서에 명시된 내용','책임과 해석','확정할 내용'],[
        ['회원 인증·등급','기업 회원 로그인, Operator / Affiliate / Insight, 단계별 권한, 고위험 구간 2차 인증','연구조합이 연동 규격·정책·인증 체계를 직접 개발','등급별 열람·다운로드·제어 권한표, 소속/과제별 범위'],
        ['연구 DB·API','직책·임무별 열람 차등, 인증된 사용자만 CRUD, 데이터 접근로그','인실리코가 플랫폼·API·웹에 적용, KETI가 검증','포털 인증과 API 인가의 전달·검증 방식'],
        ['디지털트윈','구동 영상·실데이터 고위험 접근 추가 인증; 모니터링·분석·제어 기능','연구조합 접근체계와 이즈파크 DT 기능 연동','조회 권한과 장비 제어 권한의 구분, 현장 허용 조건'],
        ['공유 학습 데이터','일반데이터는 총괄 공유 학습, 소재 구조 등은 변환된 벡터로 공유','인실리코 소재 변환/플랫폼 + KETI 적합성 평가 + 기업 분류 기준','공유 가능한 필드·기간·목적·재사용 범위, 변환 검증'],
        ['Private·로컬모드','기업 핵심 레시피는 자체 서버 실험; 충분한 총괄 학습 이후 보안모드 지원','기업별 보호 영역과 총괄 공유 영역을 분리','모델 반입·로컬 운영·로그 반출·결과 공유 경계'],
        ['업무 성과 DB','특허·논문·학술대회(반기), 고용·사업화·매출(연차), 진도·성과 추적','연구조합이 성과 수집·보고·협의체 운영','성과 공개 승인, 원천 실험 데이터와 연결 범위'],
        ['수요기업 피드백','분석 결과 제공 및 활용의 유의미함을 이메일 등으로 확인하는 인증 계획','세부/총괄 성과 검증 + 연구조합 수요-공급 협의 지원','누가 어떤 자료를 제공하고 최종 활용 확인을 받는지'],
        ],'dense')+
        grid([('회원등급은 장비 제어권 자체가 아님','Operator 등의 명칭과 단계적 접근은 명시되어 있다. 명칭만으로 모든 장비·레시피에 대한 접근 권한을 배정할 근거는 부족하다.'),('Embedding은 보안성 검증을 대체하지 않음','계획서는 암호화·Embedding·비식별 벡터를 함께 표현한다. 복원 위험, 키 관리, 변환 위치와 학습 유용성은 별도 검증 항목이다.'),('외주 범위는 웹 구현·유지보수','연구조합이 핵심 규격·정책·인증을 직접 설계·개발한다. 외주는 UI·퍼블리싱·연차별 수정·보완으로 제한된다.')])+
        para('근거: PDF 11, 17, 23, 28–30, 32, 34, 42, 51, 63, 65, 132, 140쪽. 데이터 접근은 목적·소속·과제 범위까지 함께 고려하는 상세 권한표가 필요하다.','note'))

    add('연차별 연결 범위와 검증 목표',
        table(['담당 / 축','2026 · 1차년도','2027 · 2차년도','2028 · 3차년도'],[
        ['KETI','전체 흐름·공유 시스템, 소재 코드 적합성, 기초 DB','DT·접근이력 점검, DB 기반 능동학습 적용·검증','알고리즘·보안 소재 예측·가상화 평가 및 개선'],
        ['인실리코','통합 DB·API 프로토타입, 보안분류, MLOps 설계','통합 DB·웹·추론 API, 모델 3개, 자동 재학습','안정화·백업·알림, 모델 누적 6개, 재학습·배포 완성'],
        ['이즈파크','범위·도면·KPI·연동 협의, 송수신 모듈 프로토타입','Tag·어댑터 검증, 우선 1개 DT 프로토타입','공통 DT·저장소·3D·KPI, 3개 세부 적용·실증'],
        ['성균관대','표준 데이터·파이프라인, Bayesian Optimization','실험 운영·Workflow, 적응적 계획·폐루프','Multi-agent, 전략 자기개선, 장기 자율운영'],
        ['한양대','단일 장비 Node·Topic, 순차 실행','다중 장비·병렬 실행·동기화·자원·재시도','데이터·이벤트 Hub, 실제 환경 폐루프 실증'],
        ['연구조합','접근·연동 설계, 협의체·성과 DB','접속·권한 고도화, 진도·성과 관리','3개 DT 접속 검증·확립, 지속 운영·성과확산'],
        ],'dense')+
        '<h2>정량 목표 · 성능목표표(PDF 16쪽)를 기준으로 기재</h2>'+
        table(['평가 항목','1차년도','2차년도','3차년도','해석 시 주의'],[
        ['디지털트윈 수 / 물성 AI 모델 수','— / —','1 / 3','3 / 6','누적 개수. 모델은 R² > 0.85 기준'],
        ['소재 예측 정합성','—','70%','85%','AI 모델 수 산정의 R²와 다른 성능 지표'],
        ['실험 가상화 구현율','30%','70%','85%','본문 일부 90% 표현과 불일치; 최종 기준 확인'],
        ['특성 최적화 소재 레시피','—','3종','9종','누적 목표'],
        ['접근 제어·이력 관리율','—','80%','100%','권한 시나리오 및 실제 이벤트-로그 일치 평가'],
        ['수요기업 인증 / AI 모델 평가 기준','— / —','1 / 1','3 / 3','각각 누적 개수'],
        ['디지털트윈 동시성 지표','—','—','≤ 60ms','대상 구간: DT 수신 시점 → 3D 렌더링 처리 명령'],
        ['진도점검 / 협의체','각 1회','각 2회','각 2회','연별. 요약의 일부 연 2회 표현과 차이'],
        ],'dense')+
        para('연차별 기능 근거: PDF 20–51, 65쪽. 측정 방법: PDF 17–19쪽. ≤60ms는 전체 AI 추론·네트워크 왕복·로봇 동작 완료 시간의 목표가 아니다. 시험 대상은 선정된 1개 라인/장비 시나리오의 1,000개 이상 샘플 평균으로 제시되어 있다.','note'))

    add('구현 전에 확인해야 할 경계와 문서 불일치',
        table(['구분','계획서에서 확인한 상태','이번 도식의 처리 / 합의할 사항','PDF'],[
        ['기관 명칭','일정 그림에는 영남대 표기가 남아 있으나 본문·편성도·수정표는 한양대','한양대로 통일. 영남대를 별도 수행기관으로 추가하지 않음','53, 65, 67, 140–141'],
        ['연구조합과 협회','공식 공동기관은 한국디스플레이연구조합. 편성도·포털 설명에는 협회 명칭 병기','개발 책임은 연구조합, 협회 회원 로그인은 연동 기반으로 구분','28–29, 66–67, 132'],
        ['AI·오케스트레이션 경계','KETI·인실리코·성균관대 모두 AI 업무; 성균관대·한양대 모두 orchestration 표현','예측 서비스 / 실험 전략 / 실행 관리로 구분해 설명. 모델 소유·중단·재시도·제어 우선권 합의','32, 35–41, 44, 49–50, 67'],
        ['중앙 DB·DT DB·Hub','통합 DB, DT TSDB·관계형·레지스트리, 장비 Hub, 성과 DB가 각각 등장','동일 DB로 합치지 않음. 데이터별 원본 저장소·동기화 방향·보존기간 정의','23, 30, 46–50, 63'],
        ['공유와 Private','공통 학습 데이터 업링크와 기업 로컬모드가 모두 명시','필드별 반출 범위, 변환 위치, 로컬 AI 반입·업데이트, 데이터 재사용 범위 확정','11, 15, 63'],
        ['암호화·Embedding','문서는 비식별 벡터로 유출 방지를 지향하지만 구체 방식·키·위협모델은 미기재','보호 목적을 표현하되 보안 완성을 보증하지 않음. 복원 가능성과 모델 정합성 검증','21–22, 35, 63, 136'],
        ['기술 스택','Vue/Bootstrap, Spring Boot/Security/JPA, JWT, PostgreSQL, RDKit은 구성 “예시”; Unity/Unreal은 선정 예정','확정 제품으로 표시하지 않음. ROS2·RESTful API와 요구 기능을 기준으로 구조화','23 그림, 24, 46'],
        ['실험 가상화 목표','목표표와 전략은 85%; 3차년도 설명은 90% 이상','목표표의 85%를 기준으로 표기하고 불일치 공개. 협약 KPI 확정 필요','16, 44, 60'],
        ['세부 물성·지표','식각 예시는 전도도와 식각 bias·패턴이 병존. 정합성·R²·예측오차도 서로 다른 표현','세부별 예측 타깃, 단위, 시험 데이터, 산식·합격 범위 확정','16–18, 32, 35, 44–45, 62'],
        ['기술 범위와 참고 기술','엣지 AI·지식그래프는 최신기술 검토 영역. 적용 예정으로 특정한 것은 C1~C3','엣지 AI·지식그래프를 필수 개발 모듈로 추가하지 않음','64'],
        ['규격과 배포','기능·방향은 명시하나 endpoint·이벤트 스키마·재전송·HA·모델 배포계약은 부족','정보교환 표를 기준으로 기관 간 상세 인터페이스 명세 작성 필요','25–26, 34, 38, 41, 63'],
        ],'dense')+
        para('부록 PDF 130쪽 Material Studio 장비 계획에는 네트워크 패킷 캡처 사양 문구도 혼재한다. 본문에 일관되게 제시된 소재 시뮬레이션 용도만 구조에 반영했으며, 장비 사양 근거로 패킷 캡처 기능을 채택하지 않았다.','note'))

    source_rows=[
    ['S01','1, 66–67','표지·기술개발팀 편성도','총괄/세부 주관, 총괄 6개 기관, 세부 참여기관 목록'],
    ['S02','9–11, 14–15','개발 대상 정의·최종목표·총괄-세부 그림','양방향 순환, DB/API, 미들웨어, 보안·로컬모드, 배포 AI SW'],
    ['S03','16–19','성능 목표·평가 방법','연차 목표, 정합성/모델 수 구분, 지연 측정 범위'],
    ['S04','21–24, 32–33, 44','KETI/인실리코 개발 내용','기초 소재 DB, 전체 흐름, CRUD, 보안·검증 책임'],
    ['S05','24–26, 38–39','이즈파크 요구·연계·프로토타입','CAD·Tag·수신 어댑터·제어 이벤트 경로'],
    ['S06','26–27, 39–41, 48–50','성균관대 데이터·알고리즘·운영','표준 데이터·탐색·상위 workflow·Agent·전략 개선'],
    ['S07','28, 41, 50','한양대 미들웨어·오케스트레이션·Hub','ROS2 Node·Topic·Services·Actions, 자원·재시도·상태 수집'],
    ['S08','28–30, 42, 51','연구조합 접근·성과관리','회원/2차 인증, 성과 DB, 협의체·홍보·접속체계'],
    ['S09','34–38, 45–46','인실리코 추론·예측 모델·MLOps','DT 조건↔예측 API, 모델 3→6, 재학습·버전·배포·모니터링'],
    ['S10','46–47','이즈파크 공통 시스템·데이터흐름 그림','DT TSDB·관계형·레지스트리, 3D/KPI, 현장 서버·DID'],
    ['S11','60–65','추진전략·데이터 공유·추진체계','공유 데이터 목록·ROS2/REST 업링크·다운링크·보안·기관별 역할'],
    ['S12','127, 130','설치·구매 계획','KETI DB/AI 서버, Material Studio 도입·활용 범위'],
    ['S13','132, 140–141','외주 계획·협약 수정대비표','연구조합 직접 개발 vs 웹 외주, 한양대 변경, 수정 근거'],
    ]
    add('근거 색인과 산출물 활용 방법',
        table(['근거 ID','PDF 순번','원문 위치','보고서에 반영한 사항'],source_rows,'dense')+
        '<h2>회의·설계에 바로 사용할 산출물</h2>'+
        grid([('네 가지 그림','① 기관별 기술 흐름 ② 플랫폼 계층 ③ 자율실험 순서 ④ 접근·보안·성과관리. SVG는 확대·편집, PNG는 발표자료 삽입에 사용.'),('기관 간 정보교환 표','F01–F13을 CSV로 제공. 협의 시 담당자·스키마·전달주기·권한·시험기준 열을 추가하면 인터페이스 명세의 출발점이 된다.'),('편집 가능한 보고서','HTML은 브라우저에서 열람·인쇄, PDF는 공유, Markdown은 내용 수정용. 생성용 Python 소스도 함께 제공.')])+
        callout('<b>전체 구조의 결론:</b> 총괄의 데이터·AI·검증 플랫폼이 각 세부 실험실의 실행·측정·가상화와 양방향으로 연결되고, 연구조합의 권한·성과관리 체계가 그 위에서 접속과 확산을 관리한다. 기업 Private 모드는 이 연결의 별도 보안 경계다.')+
        para('자료명: (RS-2026-25526544)1_2. 연구개발계획서(통합형 총괄)_협약용_클린본.pdf. 본 보고서는 계획서의 요구·역할을 분석한 결과이며, 별도 세부계획서·실제 구현 현황·기관 간 합의서는 검증 범위에 포함하지 않는다.','note'))

    css='''
    *{box-sizing:border-box}body{margin:0;background:#e8edf3;color:#213149;font-family:"Noto Sans CJK KR",sans-serif;font-size:12px;line-height:1.52}nav{position:sticky;top:0;background:#142d4e;color:white;padding:12px 22px;z-index:2;display:flex;justify-content:space-between;align-items:center}nav a,nav button{color:white;background:#2d4b6e;border:0;border-radius:5px;padding:7px 12px;text-decoration:none;margin-left:5px;cursor:pointer}section.page{width:1122px;height:794px;background:white;margin:22px auto;padding:34px 38px;position:relative;box-shadow:0 5px 24px #152e4a1c;overflow:hidden}header{display:flex;justify-content:space-between;color:#62748c;font-size:10px;letter-spacing:.4px;border-bottom:1px solid #dce4ed;padding-bottom:8px}h1{font-size:25px;line-height:1.25;color:#142d4e;margin:15px 0 13px;font-weight:700}h2{font-size:16px;margin:15px 0 8px;color:#142d4e}h3{font-size:13px;margin:0 0 6px;color:#1b527c}p{margin:9px 0}.subtitle{font-size:11px;color:#526781;margin:-3px 0 9px}main{max-height:630px}footer{position:absolute;bottom:20px;left:38px;right:38px;display:flex;justify-content:space-between;border-top:1px solid #e1e7ef;padding-top:6px;color:#77859a;font-size:8px}table{border-collapse:collapse;width:100%;table-layout:auto;margin:8px 0}th{background:#edf3f9;text-align:left;color:#193e60;font-weight:700;padding:8px;border-top:2px solid #295b8a;white-space:nowrap}td{vertical-align:top;padding:8px;border-bottom:1px solid #e1e8ef}tr:nth-child(even) td{background:#f9fbfd}.dense{font-size:10.5px;line-height:1.5}.dense td,.dense th{padding:6px 7px}.flow{font-size:10px;line-height:1.45}.flow td,.flow th{padding:5px 6px}.flow td:nth-child(1){font-weight:700;color:#2563a6;white-space:nowrap}.flow td:nth-child(2){width:19%}.flow td:nth-child(3){width:25%}.flow td:nth-child(5){width:8%}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:14px 0}.card{border:1px solid #d9e4ed;border-radius:10px;background:#f6f9fc;padding:13px 15px}.card p{font-size:11px;margin:0;line-height:1.7}.hero{background:#142d4e;color:white;padding:27px 32px;border-radius:13px;margin-top:18px}.hero h2{color:white;font-size:30px;line-height:1.5;margin:12px 0}.hero p{color:#cbdcea;margin:7px 0 0}.eyebrow{font-size:11px;color:#9fc4df}.callout{border-left:4px solid #168594;background:#eef8f8;padding:12px 16px;margin:12px 0;font-size:11.5px;line-height:1.75}.note{font-size:10px;color:#607186;line-height:1.7}.pill{display:inline-block;border-radius:4px;background:#e8f3f1;padding:1px 6px;color:#087e8b;font-size:10px}.pill.purple{background:#f1eaf8;color:#7554a3}.pill.orange{background:#fff0dd;color:#a65b20}.diagram{width:100%;height:596px;object-fit:contain;object-position:center top}#p13 .dense td,#p13 .dense th{padding:4px 6px}#p13 .card{padding:10px 12px}.controls{white-space:nowrap}@page{size:A4 landscape;margin:10mm}@media print{body{background:white}nav{display:none}section.page{width:auto;height:189mm;margin:0;padding:0;box-shadow:none;break-after:page;overflow:hidden}section.page:last-child{break-after:auto}footer{left:0;right:0;bottom:0}.diagram{height:151mm}main{max-height:164mm}}
    '''
    doc='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>기관별 정보흐름 및 플랫폼 구조 분석</title><style>'+css+'</style></head><body><nav><b>계획서 근거 분석 · 13쪽</b><div class="controls"><a href="#p3">정보흐름도</a><a href="#p5">플랫폼 구조</a><a href="#p9">보안·접근</a><button onclick="window.print()">PDF 인쇄</button></div></nav>'+''.join(PAGES)+'</body></html>'
    (ROOT/'report_ko.html').write_text(doc)
    (ROOT/'report_ko.md').write_text('# 기관별 정보흐름 및 전체 플랫폼 구조\n\n'+ '\n'.join(MD))
    with (ROOT/'interface_matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(['ID','송신 → 수신','교환 정보','방식·용도·확정 수준','PDF 페이지']); w.writerows(FLOW_ROWS)
    (ROOT/'README.txt').write_text('RS-2026-25526544 계획서 기반 구조 분석\n\nreport_ko.pdf: 13쪽 공유용 보고서\nreport_ko.html: 그림을 포함한 단일 파일, 브라우저 열람·인쇄용\nreport_ko.md: 편집용 본문\ninterface_matrix.csv: 기관 간 정보교환 F01–F13 (UTF-8 BOM)\nfigures/: 그림 4종, SVG·PNG\nsource/build_report.py: SVG·HTML·Markdown·CSV 생성 코드\n\n근거 페이지는 PDF 파일 순번이며 본문 인쇄 쪽수는 대체로 1 작습니다.\n계획서상 요구·목표를 구조화한 결과로, 실제 구축 완료 여부는 평가하지 않았습니다.\n')

if __name__=='__main__':
    diagrams()
    report()
