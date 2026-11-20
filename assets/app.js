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
const funnelIds=['views','profile','clicks','leads','quotes','orders','received','costs'];let funnelReport='',funnelValid=false;
const money=n=>'¥'+n.toLocaleString('zh-CN',{maximumFractionDigits:2});
const pct=(a,b)=>b>0?`${(a/b*100).toFixed(1)}%`:'—';
function renderFunnel(){const el=$('#f-summary');if(!el)return;const v={};for(const k of funnelIds){const node=$(`#f-${k}`);const n=Number(node.value);v[k]=Number.isFinite(n)&&n>=0?n:0}
 const bad=funnelIds.filter(k=>$('#f-'+k).value.trim()==='' || !Number.isFinite(Number($('#f-'+k).value)) || Number($('#f-'+k).value)<0 || (['views','profile','clicks','leads','quotes','orders'].includes(k)&& !Number.isInteger(Number($('#f-'+k).value))));
 const warn=$('#f-warning');if(bad.length){funnelValid=false;updateHistoryControls();warn.textContent='请输入非负的实际数据；人数/次数必须为整数。';el.replaceChildren();funnelReport='';$('#lab-copy-funnel').disabled=true;return}
 funnelValid=true;updateHistoryControls();warn.textContent='注意：站内私信可能绕过外链，跨渠道数据未必是严格包含的漏斗。比率只用于同口径、同时间窗观察。';
 const signals=[['主页访问率',pct(v.profile,v.views)],['链接点击／主页访问',pct(v.clicks,v.profile)],['报价／有效咨询',pct(v.quotes,v.leads)],['付款订单／报价',pct(v.orders,v.quotes)],['贡献毛利（部分成本后）',money(v.received-v.costs)]];
 el.replaceChildren();signals.forEach(([label,val])=>{const box=document.createElement('div');const l=document.createElement('span');l.textContent=label;const n=document.createElement('strong');n.textContent=val;box.append(l,n);el.append(box)});
 funnelReport=`Threads 业务复盘（实际数据，统计期自填）\n帖子浏览 ${v.views}；主页访问 ${v.profile}；链接点击 ${v.clicks}；有效咨询 ${v.leads}；报价 ${v.quotes}；付款订单 ${v.orders}；实收 ${money(v.received)}；已知变动成本 ${money(v.costs)}。\n${signals.map(x=>x.join('：')).join('；')}。\n说明：不能精确跨端归因；贡献毛利未扣固定成本、税费和潜在退款。`;$('#lab-copy-funnel').disabled=false}
funnelIds.forEach(k=>{const el=$('#f-'+k);if(el)el.addEventListener('input',renderFunnel)});
const copyFunnel=$('#lab-copy-funnel');if(copyFunnel)copyFunnel.addEventListener('click',()=>{if(funnelReport)copy(funnelReport)});

// Local period history for aggregate funnel numbers (never customer-level data).
const historyKey='andy_threads_funnel_history_v1';
const periodInput=$('#f-period'),saveHistoryButton=$('#f-save'),exportHistoryButton=$('#f-export');
const historyList=$('#f-history-list'),historyStatus=$('#f-history-status');
const countIds=['views','profile','clicks','leads','quotes','orders'];
function realPeriod(value){
  if(!/^\d{4}-\d{2}-\d{2}$/.test(value||''))return false;
  const d=new Date(value+'T00:00:00Z');
  return Number.isFinite(d.getTime())&&d.toISOString().slice(0,10)===value;
}
function validHistoryRow(row){
  return !!(row&&realPeriod(row.period)&&funnelIds.every(k=>{
    const v=row[k];return typeof v==='number'&&Number.isFinite(v)&&v>=0&&
      (countIds.includes(k)?Number.isSafeInteger(v)&&v<=1000000000:v<=1000000000000&&Math.abs(v*100-Math.round(v*100))<0.00001);
  }));
}
const historyStored=getStore(historyKey);
let historyRows=Array.isArray(historyStored)?historyStored.filter(validHistoryRow).slice(0,60):[];
function historyMessage(message){if(historyStatus)historyStatus.textContent=message}
function historySave(next){
  try{localStorage.setItem(historyKey,JSON.stringify(next));historyRows=next;return true}
  catch(_){historyMessage('本机保存失败：请检查浏览器存储空间/隐私设置，并优先导出已有数据。');return false}
}
function updateHistoryControls(){
  if(saveHistoryButton)saveHistoryButton.disabled=!funnelValid||!realPeriod(periodInput?.value);
  if(exportHistoryButton)exportHistoryButton.disabled===undefined?null:exportHistoryButton.disabled=historyRows.length===0;
}
function historyCell(tr,text,tag='td'){
  const cell=document.createElement(tag);cell.textContent=String(text);tr.append(cell);return cell;
}
function renderHistory(){
  if(!historyList)return;
  historyList.replaceChildren();
  updateHistoryControls();
  if(!historyRows.length){const p=document.createElement('p');p.textContent='暂时没有周期记录。填写上方真实数字并选择截止日期，再点击保存。';historyList.append(p);return;}
  const sorted=historyRows.slice().sort((a,b)=>b.period.localeCompare(a.period));
  if(sorted.length>1){
    const a=sorted[0],b=sorted[1],info=document.createElement('p');
    const delta=(a.received-a.costs)-(b.received-b.costs);
    info.className='funnel-history-diff';
    info.textContent='最近两期贡献毛利差额：'+money(delta)+'（'+a.period+' 对比 '+b.period+'；不同周期和口径不可直接推断因果）';
    historyList.append(info);
  }
  const wrap=document.createElement('div');wrap.className='funnel-history-scroll';
  const table=document.createElement('table');table.className='funnel-history-table';
  const caption=document.createElement('caption');caption.textContent='本机已保存 '+sorted.length+' 期汇总（按截止日倒序）';table.append(caption);
  const head=document.createElement('tr');
  for(const label of ['截止日','浏览','咨询','报价','订单','实收','已知成本','贡献毛利','操作'])historyCell(head,label,'th');
  const thead=document.createElement('thead');thead.append(head);table.append(thead);
  const tbody=document.createElement('tbody');
  sorted.forEach(row=>{
    const tr=document.createElement('tr');
    for(const val of [row.period,row.views,row.leads,row.quotes,row.orders,money(row.received),money(row.costs),money(row.received-row.costs)])historyCell(tr,val);
    const td=document.createElement('td'),del=document.createElement('button');
    del.type='button';del.className='funnel-history-delete';del.textContent='删除';
    del.setAttribute('aria-label','删除 '+row.period+' 的本机汇总');
    del.addEventListener('click',()=>{
      if(!window.confirm('删除 '+row.period+' 的本机汇总？此操作不可恢复，请先导出备份。'))return;
      const next=historyRows.filter(x=>x.period!==row.period);
      if(historySave(next)){renderHistory();historyMessage('已删除 '+row.period+' 的本地记录。');}
    });
    td.append(del);tr.append(td);tbody.append(tr);
  });
  table.append(tbody);wrap.append(table);historyList.append(wrap);
}
if(periodInput)periodInput.addEventListener('change',updateHistoryControls);
if(saveHistoryButton)saveHistoryButton.addEventListener('click',()=>{
  const period=periodInput.value;
  if(!realPeriod(period)||!funnelValid){historyMessage('保存失败：请选择真实日期，并修正本期全部数值。');return;}
  if(historyRows.some(x=>x.period===period)){historyMessage('该截止日已经保存过；请先导出备份、删除原记录后再重新保存，避免静默覆盖。');return;}
  if(historyRows.length>=60){historyMessage('已保存 60 期。请先导出 CSV 并删除不需要的旧记录。');return;}
  const data={period};
  for(const k of funnelIds)data[k]=Number($('#f-'+k).value);
  if(!validHistoryRow(data)){historyMessage('保存失败：人数/次数应为安全整数（不超过 10 亿），金额最多两位小数且不超过 1 万亿元。');return;}
  if(historySave([...historyRows,data])){renderHistory();historyMessage('已保存 '+period+' 的本机汇总，请定期导出 CSV 备份。');}
});
if(exportHistoryButton)exportHistoryButton.addEventListener('click',()=>{
  if(!historyRows.length)return;
  // CSV contains only ISO dates and finite numbers. No user-editable text can become a spreadsheet formula.
  const rows=[['截止日','帖子浏览','主页访问','外链点击','有效咨询','实际报价','付款订单','本期实收元','已知变动成本元','贡献毛利元']];
  historyRows.slice().sort((a,b)=>a.period.localeCompare(b.period)).forEach(r=>
    rows.push([r.period,r.views,r.profile,r.clicks,r.leads,r.quotes,r.orders,r.received.toFixed(2),r.costs.toFixed(2),(r.received-r.costs).toFixed(2)]));
  const csv='\uFEFF'+rows.map(row=>row.join(',')).join('\r\n')+'\r\n';
  try{
    const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
    const a=document.createElement('a');a.href=url;a.download='threads-funnel-history.csv';
    document.body.appendChild(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
    historyMessage('CSV 已请求下载（'+historyRows.length+' 期）。请检查浏览器下载列表。');
  }catch(_){historyMessage('CSV 下载失败：请使用“复制复盘摘要”临时备份本期数据。');}
});
renderHistory();

renderFunnel();
})();
