// Dependency-free client logic checks. Does not need a browser or network.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const els=new Map();
class Element{
  constructor(id){this.id=id;this.listeners={};this.value='';this.dataset={};this.children=[];this.hidden=false;this.disabled=false;this.style={};this.classList={add(){},remove(){},toggle(){return true}};}
  addEventListener(t,f){this.listeners[t]=f}
  trigger(t='input'){this.listeners[t]?.()}
  append(...nodes){this.children.push(...nodes)}
  replaceChildren(...nodes){this.children=[...nodes]}
  get innerText(){return (this.textContent||'') + this.children.map(c=>c.innerText||c.textContent||'').join(' ')}
  click(){this.clicked=true}
  remove(){this.removed=true}
  getAttribute(k){return this[k]}
  setAttribute(k,v){this[k]=v}
}
const ids=['lab-stage','lab-diagnosis','lab-copy-offer','lab-offer-result','lab-copy-funnel','f-warning','f-summary','toast','plan-count','plan-bar','f-period','f-save','f-export','f-history-status','f-history-list',
 ...['who','issue','deliver','price','limit','link'].map(x=>'offer-'+x),
 ...['views','profile','clicks','leads','quotes','orders','received','costs'].map(x=>'f-'+x)];
ids.forEach(id=>els.set('#'+id,new Element(id)));
for(const id of ['f-views','f-profile','f-clicks','f-leads','f-quotes','f-orders','f-received','f-costs'])els.get('#'+id).value='0';
const option={textContent:'没有产品 / 没有公开作品',dataset:{advice:'先做真实案例拆解',link:'guide/positioning.html'}};
els.get('#lab-stage').selectedOptions=[option];
const planElements=Array.from({length:30},(_,i)=>{const el=new Element('plan'+i);el.dataset.plan='plan-day-'+String(i+1).padStart(2,'0');el.checked=false;return el});
const document={querySelector:(s)=>els.get(s)||null,querySelectorAll:(s)=>s==='[data-plan]'?planElements:[],createElement:(tag)=>new Element(tag),body:{appendChild(){}}};
const storage={};const localStorage={getItem:(k)=>storage[k]??null,setItem:(k,v)=>storage[k]=v};
const csvDownloads=[];
class FakeBlob{constructor(parts){this.parts=parts;csvDownloads.push(parts.join(''))}}
const sandbox={document,localStorage,window:{isSecureContext:false,confirm:()=>true},navigator:{},URL:{createObjectURL:()=> 'blob:test',revokeObjectURL(){}},Blob:FakeBlob,console,clearTimeout,setTimeout};
const source=fs.readFileSync(require('path').join(__dirname,'../assets/app.js'),'utf8');
vm.runInNewContext(source,sandbox,{timeout:2000});
let checks=0;const ok=(v,msg)=>{assert.ok(v,msg);checks++};const by=id=>els.get('#'+id);
ok(by('lab-diagnosis').innerText.includes('真实案例'),'initial diagnostic');
ok(by('plan-count').textContent==='0 / 30 COMPLETED','initial 30-day progress');
planElements[0].checked=true;planElements[0].trigger('change');
ok(by('plan-count').textContent==='1 / 30 COMPLETED','daily plan count');
ok(by('plan-bar').style.width.startsWith('3.3'),'daily progress bar');
ok(localStorage.getItem('andy_threads_plan_v1').includes('plan-day-01'),'local plan saved');
option.textContent='有人询盘，但没成交';option.dataset.advice='查产品与报价';by('lab-stage').trigger('change');
ok(by('lab-diagnosis').innerText.includes('查产品与报价'),'switch diagnostic');
ok(by('lab-copy-offer').disabled,'empty offer disabled');
for(const [k,v] of Object.entries({who:'社招候选人',issue:'投递无反馈',deliver:'一次诊断和清单',limit:'不保证录用'})){by('offer-'+k).value=v;by('offer-'+k).trigger()}
ok(!by('lab-copy-offer').disabled,'valid offer allowed');
ok(by('lab-offer-result').textContent.includes('不保证录用'),'offer limits rendered');
for(const [k,v] of Object.entries({views:2000,profile:100,clicks:20,leads:10,quotes:5,orders:2,received:900,costs:200})){by('f-'+k).value=String(v);by('f-'+k).trigger()}
let report=by('f-summary').innerText;
for(const exp of ['5.0%','20.0%','50.0%','40.0%','¥700'])ok(report.includes(exp),'funnel value '+exp);
ok(!by('lab-copy-funnel').disabled,'correct funnel allowed');
by('f-orders').value='-1';by('f-orders').trigger();ok(by('lab-copy-funnel').disabled,'negative blocked');
by('f-orders').value='2.5';by('f-orders').trigger();ok(by('lab-copy-funnel').disabled,'fractional count blocked');
by('f-orders').value='2';by('f-orders').trigger();ok(!by('lab-copy-funnel').disabled,'corrected count allowed');
by('f-quotes').value='0';by('f-quotes').trigger();ok(by('f-summary').innerText.includes('—'),'zero denominator safe');
by('f-received').value='0';by('f-costs').value='200';by('f-costs').trigger();ok(by('f-summary').innerText.includes('¥-200'),'negative contribution shown');

// Local-only period history: invalid dates, duplicate prevention, and persisted aggregation.
by('f-quotes').value='5';by('f-received').value='900';by('f-costs').value='200';by('f-costs').trigger();
by('f-period').value='2026-11-14';by('f-period').trigger('change');
ok(!by('f-save').disabled,'history save is ready with valid date and counts');
by('f-save').trigger('click');
ok(storage.andy_threads_funnel_history_v1.includes('2026-11-14'),'history persisted');
ok(!by('f-export').disabled,'CSV enabled after saved history');
let saved=JSON.parse(storage.andy_threads_funnel_history_v1);
ok(saved.length===1&&saved[0].received===900,'history stores aggregate numbers');
by('f-save').trigger('click');
ok(JSON.parse(storage.andy_threads_funnel_history_v1).length===1,'duplicate date does not overwrite');
by('f-period').value='2026-11-31';by('f-period').trigger('change');
ok(by('f-save').disabled,'invalid calendar date blocked');
by('f-period').value='2026-11-21';by('f-period').trigger('change');
by('f-received').value='1200';by('f-received').trigger();
by('f-save').trigger('click');
ok(JSON.parse(storage.andy_threads_funnel_history_v1).length===2,'second period saved');
ok(by('f-history-list').innerText.includes('¥300'),'period comparison renders value');
by('f-orders').value='2.5';by('f-orders').trigger();
ok(by('f-save').disabled,'fractional orders block period save');
by('f-orders').value='2';by('f-orders').trigger();
by('f-received').value='12.345';by('f-received').trigger();
by('f-save').trigger('click');
ok(JSON.parse(storage.andy_threads_funnel_history_v1).length===2,'excess decimal places rejected');
by('f-received').value='1200';by('f-received').trigger();
by('f-export').trigger('click');
ok(csvDownloads.length===1,'CSV download requested');
ok(csvDownloads[0].includes('2026-11-14')&&csvDownloads[0].includes('2026-11-21'),'CSV contains both periods');
ok(csvDownloads[0].charCodeAt(0)===0xFEFF,'UTF-8 BOM retained');

console.log(`PASS: ${checks} browser-independent JS business logic checks`);
