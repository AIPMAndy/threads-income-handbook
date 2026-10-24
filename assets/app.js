/* Minimal, dependency-free enhancement layer. Never sends data to a server. */
(()=>{'use strict';
const completedKey='andy_threads_guide_completed_v1',planKey='andy_threads_plan_v1';
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
function getStore(key){try{return JSON.parse(localStorage.getItem(key)||'{}')}catch(_){return {}}}
function setStore(key,value){try{localStorage.setItem(key,JSON.stringify(value))}catch(_){}}
let toastT;
function toast(msg){const el=$('#toast');if(!el)return;el.textContent=msg;el.classList.add('show');clearTimeout(toastT);toastT=setTimeout(()=>el.classList.remove('show'),2800)}
async function copy(text){try{if(navigator.clipboard && window.isSecureContext){await navigator.clipboard.writeText(text)}else{const a=document.createElement('textarea');a.value=text;a.setAttribute('readonly','');a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();const ok=document.execCommand('copy');a.remove();if(!ok)throw new Error('copy unavailable')}toast('已复制。发布前请替换占位符并核验事实。')}catch(_){toast('复制失败，请手动选择文案复制。')}}
$$('.js-copy').forEach(b=>b.addEventListener('click',()=>copy(b.getAttribute('data-copy')||'')));
const toggle=$('.mobile-toggle'),menu=$('#mobile-menu');if(toggle&&menu){toggle.addEventListener('click',()=>{const on=menu.classList.toggle('open');toggle.setAttribute('aria-expanded',String(on))});menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.classList.remove('open');toggle.setAttribute('aria-expanded','false')}))}
const calcKeys=['price','cost','leads','rate','hours'];const vals={price:499,cost:99,leads:40,rate:15,hours:2};
function calc(){if(!$('#price'))return;calcKeys.forEach(k=>{const n=Number($('#'+k).value);vals[k]=Number.isFinite(n)?Math.max(0,Math.min(1000000,n)):0});vals.rate=Math.min(100,vals.rate);const sales=vals.leads*vals.rate/100,margin=vals.price-vals.cost;const fmt=n=>'¥'+Math.round(n).toLocaleString('zh-CN');$('#estimated-margin').textContent=fmt(sales*margin);$('#estimated-sales').textContent=sales.toLocaleString('zh-CN',{maximumFractionDigits:1});$('#estimated-revenue').textContent=fmt(sales*vals.price);$('#estimated-unit').textContent=fmt(margin);$('#estimated-hour').textContent=vals.hours>0?fmt(margin/vals.hours):'—';}
calcKeys.forEach(k=>{const el=$('#'+k);if(el)el.addEventListener('input',calc)});const reset=$('#reset-calc');if(reset)reset.addEventListener('click',()=>{const v={price:499,cost:99,leads:40,rate:15,hours:2};for(const k of calcKeys)$('#'+k).value=v[k];calc()});calc();
const plan=$$('[data-plan]');if(plan.length){let state=getStore(planKey);plan.forEach(input=>{input.checked=!!state[input.dataset.plan];input.addEventListener('change',()=>{state[input.dataset.plan]=input.checked;setStore(planKey,state);updatePlan()})});function updatePlan(){const done=plan.filter(i=>i.checked).length;$('#plan-count').textContent=`${done} / ${plan.length} COMPLETED`;$('#plan-bar').style.width=`${done/plan.length*100}%`}updatePlan()}
function progress(){const s=getStore(completedKey),count=Object.values(s).filter(Boolean).length;$$('#overall-progress').forEach(el=>el.textContent=`${count} / 24`);$$('#overall-bar').forEach(el=>el.style.width=`${count/24*100}%`);const mark=$('#mark-read');if(mark){const on=!!s[mark.dataset.chapter];mark.textContent=on?'✓ 已完成 · 点击取消':'标记已学完 ✓';mark.setAttribute('aria-pressed',String(on))}}
const mark=$('#mark-read');if(mark)mark.addEventListener('click',()=>{const s=getStore(completedKey);s[mark.dataset.chapter]=!s[mark.dataset.chapter];setStore(completedKey,s);progress();toast(s[mark.dataset.chapter]?'这一章已标记完成':'已取消完成标记')});
const clear=$('#clear-progress');if(clear)clear.addEventListener('click',()=>{if(!window.confirm('确定清空这台设备的阅读进度？此操作无法撤销。'))return;setStore(completedKey,{});progress();toast('本地阅读进度已清空')});progress();
const chapterSearch=$('#chapter-search');if(chapterSearch){chapterSearch.addEventListener('input',()=>{const q=chapterSearch.value.trim().toLowerCase();const isLibrary=!!$('#handbook-grid');const nodes=isLibrary?$$('.handbook-card'):$$('.toc-link');let visible=0;nodes.forEach(el=>{const yes=(el.dataset.search||el.textContent).toLowerCase().includes(q);el.hidden=!yes;if(yes)visible++});if(isLibrary){$('#chapter-search-count').textContent=`${visible} 章`;$('#empty-chapters').hidden=visible>0}else{$$('.toc-group').forEach(g=>{let n=g.nextElementSibling,any=false;while(n&& !n.classList.contains('toc-group')){if(n.classList.contains('toc-link')&&!n.hidden)any=true;n=n.nextElementSibling}g.hidden=!any})}})}
let currentFilter='全部';const templateInput=$('#template-search');function templateFilter(){const q=(templateInput?.value||'').trim().toLowerCase();let seen=0;$$('.template-card').forEach(card=>{const cat=card.querySelector('.template-tag')?.textContent||'';const t=(card.dataset.search||card.textContent).toLowerCase();const ok=(currentFilter==='全部'||cat===currentFilter)&&t.includes(q);card.hidden=!ok;if(ok)seen++});const empty=$('#empty-templates');if(empty)empty.hidden=seen>0}$$('[data-template-filter]').forEach(btn=>btn.addEventListener('click',()=>{currentFilter=btn.dataset.templateFilter;$$('[data-template-filter]').forEach(el=>el.classList.toggle('active',el===btn));templateFilter()}));if(templateInput)templateInput.addEventListener('input',templateFilter);

// Practical workbench — plain DOM, no data collection, no automatic marketing.
const stage=$('#lab-stage');
function renderStage(){if(!stage)return;const selected=stage.selectedOptions[0];const el=$('#lab-diagnosis');const title=selected.textContent;const advice=selected.dataset.advice;const url=selected.dataset.link;el.replaceChildren();const h=document.createElement('strong');h.textContent=`当前瓶颈：${title}`;const p=document.createElement('p');p.textContent=advice;const a=document.createElement('a');a.href=url;a.textContent='打开对应实操章节 ↗';el.append(h,p,a)}
if(stage){stage.addEventListener('change',renderStage);renderStage()}
const offerIds=['who','issue','deliver','price','limit','link'];
function offerText(){const values={};for(const k of offerIds)values[k]=($(`#offer-${k}`)?.value||'').trim();return values}
function offerReady(v){return !!(v.who&&v.issue&&v.deliver&&v.limit)}
function formatOffer(v){return `【服务说明】\n适合：${v.who}\n解决：${v.issue}\n交付：${v.deliver}\n费用：${v.price||'请以正式报价为准'}\n边界：${v.limit}\n规则与联系：${v.link||'详见正式服务说明'}\n\n说明：上述为我真实可交付的范围，不承诺第三方决策或未来收益。`}
function renderOffer(){const el=$('#lab-offer-result');if(!el)return;const v=offerText();el.textContent=offerReady(v)?formatOffer(v):'至少填写“适合谁、解决什么、实际交付、服务边界”，才能生成可使用的服务卡。';$('#lab-copy-offer').disabled=!offerReady(v)}
for(const k of offerIds){const el=$(`#offer-${k}`);if(el)el.addEventListener('input',renderOffer)}
const copyOffer=$('#lab-copy-offer');if(copyOffer)copyOffer.addEventListener('click',()=>{const v=offerText();if(offerReady(v))copy(formatOffer(v))});renderOffer();
const funnelIds=['views','profile','clicks','leads','quotes','orders','received','costs'];let funnelReport='';
const money=n=>'¥'+n.toLocaleString('zh-CN',{maximumFractionDigits:2});
const pct=(a,b)=>b>0?`${(a/b*100).toFixed(1)}%`:'—';
function renderFunnel(){const el=$('#f-summary');if(!el)return;const v={};for(const k of funnelIds){const node=$(`#f-${k}`);const n=Number(node.value);v[k]=Number.isFinite(n)&&n>=0?n:0}
 const bad=funnelIds.filter(k=>$('#f-'+k).value.trim()==='' || !Number.isFinite(Number($('#f-'+k).value)) || Number($('#f-'+k).value)<0 || (['views','profile','clicks','leads','quotes','orders'].includes(k)&& !Number.isInteger(Number($('#f-'+k).value))));
 const warn=$('#f-warning');if(bad.length){warn.textContent='请输入非负的实际数据；人数/次数必须为整数。';el.replaceChildren();funnelReport='';$('#lab-copy-funnel').disabled=true;return}
 warn.textContent='注意：站内私信可能绕过外链，跨渠道数据未必是严格包含的漏斗。比率只用于同口径、同时间窗观察。';
 const signals=[['主页访问率',pct(v.profile,v.views)],['链接点击／主页访问',pct(v.clicks,v.profile)],['报价／有效咨询',pct(v.quotes,v.leads)],['付款订单／报价',pct(v.orders,v.quotes)],['贡献毛利（部分成本后）',money(v.received-v.costs)]];
 el.replaceChildren();signals.forEach(([label,val])=>{const box=document.createElement('div');const l=document.createElement('span');l.textContent=label;const n=document.createElement('strong');n.textContent=val;box.append(l,n);el.append(box)});
 funnelReport=`Threads 业务复盘（实际数据，统计期自填）\n帖子浏览 ${v.views}；主页访问 ${v.profile}；链接点击 ${v.clicks}；有效咨询 ${v.leads}；报价 ${v.quotes}；付款订单 ${v.orders}；实收 ${money(v.received)}；已知变动成本 ${money(v.costs)}。\n${signals.map(x=>x.join('：')).join('；')}。\n说明：不能精确跨端归因；贡献毛利未扣固定成本、税费和潜在退款。`;$('#lab-copy-funnel').disabled=false}
funnelIds.forEach(k=>{const el=$('#f-'+k);if(el)el.addEventListener('input',renderFunnel)});
const copyFunnel=$('#lab-copy-funnel');if(copyFunnel)copyFunnel.addEventListener('click',()=>{if(funnelReport)copy(funnelReport)});renderFunnel();
})();
