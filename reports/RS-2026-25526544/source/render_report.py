from pathlib import Path
from playwright.sync_api import sync_playwright
import base64, re, json

root=Path('/workspace/outputs/rd_platform')
doc=(root/'report_ko.html').read_text()
def embed(m):
    data=(root/m.group(1)).read_bytes()
    return 'src="data:image/svg+xml;base64,'+base64.b64encode(data).decode()+'"'
doc=re.sub(r'src="(figures/[^" ]+\.svg)"',embed,doc)
(root/'report_ko.html').write_text(doc)
results={}
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1600,'height':1250},device_scale_factor=1)
    page.set_content(doc,wait_until='load')
    page.evaluate('document.fonts.ready')
    for media in ['screen','print']:
        page.emulate_media(media=media)
        results[media]=page.evaluate('''() => [...document.querySelectorAll('.page')].map(p=>({page:p.id,footerTop:Math.round(p.querySelector('footer').getBoundingClientRect().top-p.getBoundingClientRect().top),contentBottom:Math.round(p.querySelector('main').lastElementChild.getBoundingClientRect().bottom-p.getBoundingClientRect().top)}))''')
    page.pdf(path=str(root/'report_ko.pdf'),print_background=True,prefer_css_page_size=True)
    page.emulate_media(media='screen')
    for n in [1,2,4,6,8,10,11,12,13]:
        page.locator(f'#p{n}').screenshot(path=f'/workspace/analysis/rd_platform/report_{n}.png')
    results['svg_bounds']={}
    for f in sorted((root/'figures').glob('*.svg')):
        page.set_content('<html><body style="margin:0">'+f.read_text()+'</body></html>',wait_until='load')
        page.evaluate('document.fonts.ready')
        results['svg_bounds'][f.name]=page.evaluate('''() => [...document.querySelectorAll('text')].map(e=>({text:e.textContent,box:e.getBBox()})).filter(x=>x.box.x<0 || x.box.x+x.box.width>1600)''')
        page.locator('svg').screenshot(path=str(f.with_suffix('.png')))
    browser.close()
(root/'source/layout_validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps(results,ensure_ascii=False))
