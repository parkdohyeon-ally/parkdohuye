"""Render a single A4 landscape summary, with editable vector artwork."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
STEM = 'overview_1page_ko'
NAVY = '#16324F'
MUTED = '#536B80'
TEAL = '#067B80'
PURPLE = '#7453A4'
ORANGE = '#AD551D'
BLUE = '#285EA8'


class Drawing:
    def __init__(self):
        self.parts = [
            '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1120" viewBox="0 0 1600 1120" role="img" aria-labelledby="title desc">',
            '<title id="title">AI 자율실험실 — 기관별 정보흐름과 플랫폼 구조 한 장 요약</title>',
            '<desc id="desc">세부 실험실, 한양대, 인실리코, 성균관대의 순환 정보흐름과 이즈파크 디지털트윈, KETI 총괄, 연구조합 접근 및 성과관리 역할을 보여주는 계획서 기반 개념도.</desc>',
            '<defs>' + ''.join(
                f'<marker id="arrow-{i}" markerWidth="12" markerHeight="10" refX="11" refY="5" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M0 0 L12 5 L0 10 Z" fill="{c}"/></marker>'
                for i, c in enumerate([TEAL, PURPLE, ORANGE, BLUE])
            ) + '</defs>',
            '<style>text{font-family:"Noto Sans CJK KR",sans-serif}</style>',
            '<rect width="1600" height="1120" fill="white"/>',
        ]

    def text(self, x, y, text, size=23, color=NAVY, weight=400, anchor='start'):
        self.parts.append(
            f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{html.escape(text)}</text>'
        )

    def rect(self, x, y, w, h, fill, stroke='none', radius=16):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def arrow(self, points, color=TEAL, dashed=False, both=False):
        index = [TEAL, PURPLE, ORANGE, BLUE].index(color)
        d = 'M' + ' L'.join(f'{x},{y}' for x, y in points)
        self.parts.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3.2" stroke-linejoin="round" marker-end="url(#arrow-{index})"'
            + (f' marker-start="url(#arrow-{index})"' if both else '')
            + (' stroke-dasharray="9 7"' if dashed else '') + '/>'
        )

    def card(self, x, step, title, lines, color, fill):
        self.rect(x, 345, 330, 240, fill, color)
        self.text(x+24, 379, step, 21, color, 700)
        self.text(x+24, 425, title, 29, color, 700)
        for i, line in enumerate(lines):
            self.text(x+24, 471+i*37, line, 22)

    def output(self):
        return '\n'.join(self.parts + ['</svg>'])


def make_svg():
    d = Drawing()
    d.text(50, 61, 'AI 자율실험실', 43, NAVY, 800)
    d.text(378, 61, '기관별 정보흐름과 플랫폼 구조', 35, NAVY, 700)
    d.text(50, 106, '실험 결과 → 예측 개선 → 다음 실험 결정 → 실행으로 이어지는 순환 구조', 25, MUTED)
    d.text(1550, 103, 'RS-2026-25526544', 19, MUTED, anchor='end')

    # Governance spans the workflow instead of becoming an operational hop.
    d.rect(50, 145, 1500, 77, '#16324F')
    d.text(77, 193, '총괄  |  한국전자기술연구원', 27, '#FFFFFF', 700)
    d.text(550, 192, '전체 설계 · 소재/시뮬레이션 DB · 알고리즘·통합·보안 검증', 24, '#E4EEF7')

    d.text(50, 321, '현장 실험·실행', 22, MUTED, 700)
    d.text(830, 321, '총괄 데이터·AI 기능', 22, MUTED, 700)
    d.card(50, '01  실험·측정', '세부 3개 실험실', [
        '피엔에이치테크 · Premix', '동진쎄미켐 · TFE', '이엠테크 · 식각 소재·공정',
    ], BLUE, '#F3F7FC')
    d.card(440, '02  장비 실행·데이터 수집', '한양대학교', [
        'ROS2 · 장비·로봇 실행', '자원·일정·실패 대응', '결과·상태·로그 수집',
    ], ORANGE, '#FFF7ED')
    d.card(830, '03  데이터 관리·물성 예측', '인실리코', [
        '통합 DB · API · 물성 예측', '신규 데이터 → 모델 재학습', '예측 결과·모델 버전 관리',
    ], TEAL, '#EEF8F7')
    d.card(1220, '04  다음 실험 결정', '성균관대학교', [
        '실험 조건·탐색 전략 선택', '결과 분석 → 실험 계획 갱신', '능동학습 · 다중 에이전트',
    ], PURPLE, '#F6F2FB')

    # Data flows left to right. Labels fit the narrow gaps between cards.
    for x, labels in [(410, ('결과·', '상태')), (800, ('공유', '데이터')), (1190, ('예측', '결과'))]:
        color = PURPLE if x == 1190 else TEAL
        d.text(x, 422, labels[0], 18, color, anchor='middle')
        d.text(x, 447, labels[1], 18, color, anchor='middle')
        d.arrow([(x-30, 472), (x+30, 472)], color, dashed=(x == 1190))

    # Strategic decisions return to the actual equipment execution layer.
    d.arrow([(1385, 345), (1385, 270), (605, 270), (605, 345)], PURPLE, dashed=True)
    d.text(995, 254, '다음 실험 조건·순서', 23, PURPLE, 700, 'middle')
    d.arrow([(570, 585), (570, 651), (215, 651), (215, 585)], ORANGE)
    d.text(392, 635, '장비 실행 명령', 23, ORANGE, 700, 'middle')

    # A twin is both a display and a controlled input path; it has its own data store.
    d.rect(910, 739, 640, 145, '#F3F7FC', BLUE)
    d.text(938, 780, '관찰·제어  |  이즈파크', 29, BLUE, 700)
    d.text(938, 824, '디지털트윈 · 3D · KPI · 전용 저장소', 24)
    d.text(938, 861, '장비 상태 시각화 / 제어 이벤트 송신', 24)
    d.arrow([(750, 585), (750, 697), (1040, 697), (1040, 739)], TEAL)
    d.text(890, 682, '실시간 상태·측정값', 23, TEAL, anchor='middle')
    d.arrow([(1120, 585), (1120, 739)], BLUE, both=True)
    d.text(1144, 643, '실험 조건 ↔ 예측 결과', 23, BLUE)
    d.arrow([(910, 846), (700, 846), (700, 585)], ORANGE)
    d.text(723, 812, '제어 이벤트', 21, ORANGE)

    # Data boundary remains visible without placing private originals in the lake.
    d.rect(50, 739, 640, 145, '#F7F9FB', '#D7E0E8')
    d.text(76, 780, '데이터 공유 경계', 27, NAVY, 700)
    d.text(76, 824, '공유 허용 데이터만 총괄에 전송', 24)
    d.text(76, 861, '기업 핵심 레시피는 Private·로컬모드로 관리', 24)

    d.rect(50, 925, 1500, 96, '#EEF2F6')
    d.text(77, 968, '한국디스플레이연구조합', 28, NAVY, 700)
    d.text(77, 998, '회원 접근 · 사업관리', 21, MUTED)
    d.text(545, 963, '회원 등급·2차 인증 → 권한별 디지털트윈 접속', 24)
    d.text(545, 997, '진도·성과 DB · 수요기업 협의·성과확산', 24)

    d.arrow([(52, 1054), (94, 1054)], TEAL)
    d.text(108, 1061, '계획서 명시 흐름', 18, MUTED)
    d.arrow([(314, 1054), (356, 1054)], PURPLE, dashed=True)
    d.text(370, 1061, '기관별 기능을 연결한 재구성', 18, MUTED)
    d.text(1550, 1061, '기능 중심 개념도 · 실제 서버 배치와 API 규격은 별도 설계', 18, MUTED, anchor='end')
    d.text(50, 1094, '근거: 원본 PDF 21–28, 34–41, 46–50, 62–67쪽  |  개발 계획을 요약한 것으로 구축 완료·성능 달성을 의미하지 않음', 17, MUTED)
    return d.output()


def render(svg):
    from playwright.sync_api import sync_playwright
    import fitz
    svg_path = ROOT / f'{STEM}.svg'
    svg_path.write_text(svg)
    html_document = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>AI 자율실험실 한 장 요약</title><style>
    *{box-sizing:border-box}body{margin:0;background:white}.sheet{width:297mm;height:210mm;padding:8mm;margin:0}.sheet svg{width:100%;height:100%;display:block}
    @page{size:A4 landscape;margin:0}@media screen{body{background:#e8edf3}.sheet{background:white;margin:20px auto;box-shadow:0 4px 24px #16324f18}}
    </style></head><body><main class="sheet">''' + svg + '</main></body></html>'
    (ROOT / f'{STEM}.html').write_text(html_document)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1700, 'height': 1200}, device_scale_factor=2)
        page.set_content('<html><body style="margin:0">' + svg + '</body></html>', wait_until='load')
        page.evaluate('document.fonts.ready')
        # Report boundaries and text boxes for visual layout review.
        text_bounds = page.evaluate('''() => [...document.querySelectorAll('svg text')].map(e => {
          const b=e.getBBox();return {text:e.textContent,x:b.x,y:b.y,width:b.width,height:b.height}
        })''')
        escaped = [b for b in text_bounds if b['x'] < 0 or b['x']+b['width'] > 1600 or b['y']+b['height'] > 1120]
        if escaped:
            raise ValueError(escaped)
        page.locator('svg').screenshot(path=str(ROOT / f'{STEM}.png'))
        page.set_content(html_document, wait_until='load')
        page.evaluate('document.fonts.ready')
        page.emulate_media(media='print')
        page.pdf(path=str(ROOT / f'{STEM}.pdf'), prefer_css_page_size=True, print_background=True)
        browser.close()
    pdf = fitz.open(ROOT / f'{STEM}.pdf')
    assert len(pdf) == 1, f'Expected one page, got {len(pdf)}'
    content = pdf[0].get_text()
    for name in ['한국전자기술연구원','한양대학교','인실리코','성균관대학교','이즈파크','한국디스플레이연구조합','피엔에이치테크','동진쎄미켐','이엠테크']:
        assert name in content, f'Missing PDF text: {name}'
    assert '\ufffd' not in content
    print(json.dumps({'pages':len(pdf),'size_mm':[round(x*25.4/72,1) for x in [pdf[0].rect.width,pdf[0].rect.height]],'text_boxes':text_bounds}, ensure_ascii=False))


if __name__ == '__main__':
    render(make_svg())
