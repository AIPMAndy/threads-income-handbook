#!/usr/bin/env python3
"""Optional local Chromium regression checks. Requires playwright and an installed chromium."""
from contextlib import contextmanager
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading, os, time
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
@contextmanager
def local_server():
    os.chdir(ROOT)
    server = ThreadingHTTPServer(('127.0.0.1',0),SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    try:yield f'http://127.0.0.1:{server.server_port}'
    finally:server.shutdown(); server.server_close()

def audit():
    issues=[];assertions=0
    def ok(value,message):
        nonlocal assertions
        assertions+=1
        assert value,message
    with local_server() as url, sync_playwright() as p:
        launch={'headless':True,'args':['--no-sandbox']}
        if Path('/usr/bin/chromium').exists():launch['executable_path']='/usr/bin/chromium'
        browser=p.chromium.launch(**launch)
        try:
            for vw in [1440,390,360]:
                page=browser.new_page(viewport={'width':vw,'height':920},device_scale_factor=1)
                page.on('pageerror',lambda e:issues.append(f'pageerror {e}'))
                for route in ['/index.html','/lab.html','/plan.html','/guide/dm.html','/handbook.html','/templates.html']:
                    page.goto(url+route, wait_until='domcontentloaded')
                    page.wait_for_timeout(350)
                    right=page.evaluate('document.documentElement.scrollWidth-document.documentElement.clientWidth')
                    ok(right<3,f'horizontal scroll {vw} {route}: {right}px')
                    ok(page.locator('h1').count()==1, f'h1 {vw} {route}')
                page.goto(url+'/lab.html',wait_until='domcontentloaded')
                ok('当前瓶颈' in page.locator('#lab-diagnosis').inner_text(),'diagnostic content')
                page.select_option('#lab-stage','sales')
                ok('报价' in page.locator('#lab-diagnosis').inner_text(),'diagnosis selection')
                ok(page.locator('#lab-copy-offer').is_disabled(),'default offer should not copy')
                for k, val in [('who','有目标岗位的社招求职者'),('issue','简历投了十次没反馈'),('deliver','一次45分钟诊断和一页建议清单'),('limit','不承诺录用')]:page.fill('#offer-'+k,val)
                ok(page.locator('#lab-copy-offer').is_enabled(),'offer enabled after required data')
                ok('不承诺录用' in page.locator('#lab-offer-result').inner_text(),'offer preview')
                for k,val in [('views','2000'),('profile','100'),('clicks','20'),('leads','10'),('quotes','5'),('orders','2'),('received','900'),('costs','200')]: page.fill('#f-'+k,val)
                report=page.locator('#f-summary').inner_text()
                for v in ['5.0%','20.0%','50.0%','40.0%','¥700']:
                    ok(v in report,f'funnel missing {v}: {report}')
                page.fill('#f-orders','-1')
                ok(page.locator('#lab-copy-funnel').is_disabled(),'negative order blocked')
                page.fill('#f-orders','2.5')
                ok(page.locator('#lab-copy-funnel').is_disabled(),'fractional order blocked')
                page.fill('#f-orders','2')
                ok(page.locator('#lab-copy-funnel').is_enabled(),'corrected report enabled')
                # Record two actual aggregate periods, export spreadsheet-safe CSV,
                # reload, and verify persistence. This does not create customer data.
                page.fill('#f-period','2026-11-14')
                ok(page.locator('#f-save').is_enabled(),'period save enabled')
                page.locator('#f-save').click()
                ok('已保存 2026-11-14' in page.locator('#f-history-status').inner_text(),'period saved')
                page.locator('#f-save').click()
                ok('已经保存过' in page.locator('#f-history-status').inner_text(),'duplicate not overwritten')
                page.fill('#f-period','2026-11-21')
                page.fill('#f-received','1200')
                page.locator('#f-save').click()
                ok('¥300' in page.locator('#f-history-list').inner_text(),'latest contribution delta')
                ok(page.locator('.funnel-history-delete').count()==2,'two period rows')
                with page.expect_download() as got_download:
                    page.locator('#f-export').click()
                download=got_download.value
                ok(download.suggested_filename=='threads-funnel-history.csv','download filename')
                content=Path(download.path()).read_bytes()
                ok(content.startswith(b'\xef\xbb\xbf'),'UTF-8 BOM CSV')
                ok(b'2026-11-14' in content and b'2026-11-21' in content,'CSV includes both periods')
                page.reload(wait_until='domcontentloaded')
                ok(page.locator('.funnel-history-delete').count()==2,'local history persists across reloads')
                page.on('dialog',lambda dialog:dialog.accept())
                if vw==1440: page.screenshot(path=str(ROOT.parent/'threads-v2-lab-desktop.png'),full_page=True)
                if vw==390: page.screenshot(path=str(ROOT.parent/'threads-v2-lab-mobile.png'),full_page=True)
                page.locator('.funnel-history-delete').first.click()
                ok(page.locator('.funnel-history-delete').count()==1,'explicit deletion removes one period')
                page.goto(url+'/index.html',wait_until='domcontentloaded')
                if vw==1440:page.screenshot(path=str(ROOT.parent/'threads-v2-home-desktop.png'),full_page=False)
                page.close()
        finally:browser.close()
    ok(not issues,'JS errors '+str(issues))
    print(f'BROWSER PASS: {assertions} assertions · desktop and mobile · interactions · screenshots')
if __name__=='__main__':audit()
