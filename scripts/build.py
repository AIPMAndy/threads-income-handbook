#!/usr/bin/env python3
"""Build static site from typed, locally authored content; zero remote build dependencies."""
from pathlib import Path
from datetime import date
from html import escape
import sys, os, json, re
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from content import CHAPTERS, ROUTES, FAQ, TEMPLATES, SOURCES, BASE
from advanced import DEEP_DIVES, DECISIONS, EXAMPLES
TODAY='2026-10-24'

def e(v): return escape(str(v),quote=True)
def tag(name,s='',**attrs):
    return f'<{name}'+''.join(f' {k.rstrip("_").replace("_","-")}="{e(v)}"' for k,v in attrs.items())+'>'+str(s)+f'</{name}>'
def layout(title,description,body,prefix='',kind='home',url='',js=True):
    canon=BASE+url
    nav='''<header class="topbar"><div class="shell top-inner"><a class="brand" href="%sindex.html" aria-label="返回网站首页"><span class="brand-mark">◉</span><span>THREADS<span class="brand-sub"> / INCOME LAB</span></span></a><nav class="desktop-nav" aria-label="主导航"><a href="%sindex.html#paths">变现方式</a><a href="%shandbook.html">完整教程</a><a href="%slab.html">转化实验室</a><a href="%splan.html">30 天行动</a></nav><div class="top-actions"><a class="nav-website" target="_blank" rel="noopener noreferrer" href="https://metaver.vip/">Andy 官网 ↗</a><button class="btn btn-primary btn-mini js-copy" data-copy="AIPMAndy" aria-label="复制微信号 AIPMAndy">微信咨询 <span>↗</span></button><button class="mobile-toggle" aria-label="展开菜单" aria-expanded="false">☰</button></div></div><div class="mobile-nav" id="mobile-menu"><a href="%sindex.html#paths">变现方式</a><a href="%shandbook.html">完整教程</a><a href="%slab.html">转化实验室</a><a href="%splan.html">30 天行动</a></div></header>''' % ((prefix,)*9)
    footer='''<footer class="footer"><div class="shell"><div class="footer-main"><div><span class="eyebrow">BUILD YOUR OWN INCOME SYSTEM</span><h2>把浏览量，变成可验证的生意。</h2><p>免费开源教程，不承诺收益。由 AI 酋长 Andy 整理，平台规则请以原始来源为准。</p></div><div class="footer-actions"><a class="btn btn-white" href="https://metaver.vip/services" target="_blank" rel="noopener noreferrer">查看服务与陪跑 ↗</a><button class="btn btn-outline js-copy" data-copy="AIPMAndy">复制微信 AIPMAndy</button></div></div><div class="footer-bottom"><span>© 2026 Andy · MIT License · Last reviewed %s</span><div><a href="%shandbook.html">知识库</a><a href="%sindex.html#sources">依据与更新</a><a href="https://github.com/AIPMAndy/threads-income-handbook" target="_blank" rel="noopener noreferrer">GitHub</a><a href="https://metaver.vip/" target="_blank" rel="noopener noreferrer">metaver.vip</a></div></div></div></footer><div class="toast" id="toast" role="status" aria-live="polite"></div>'''%(TODAY,prefix,prefix)
    head='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#090d1a"><meta name="author" content="AI 酋长 Andy"><meta name="robots" content="index,follow,max-image-preview:large"><title>%s</title><meta name="description" content="%s"><link rel="canonical" href="%s"><meta property="og:type" content="website"><meta property="og:locale" content="zh_CN"><meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:image" content="%sassets/social-preview.png"><meta property="og:url" content="%s"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/svg+xml" href="%sassets/favicon.svg"><link rel="stylesheet" href="%sassets/style.css"><script defer src="%sassets/app.js"></script></head><body class="page-%s"><div class="ambient ambient-a"></div><div class="ambient ambient-b"></div><div class="ambient ambient-c"></div><div class="page-grid"></div><a class="skip-link" href="#main">跳转至正文</a>%s'''%(e(title),e(description),e(canon),e(title),e(description),e(BASE),e(canon),prefix,prefix,prefix,kind,nav)
    return head+body+footer+'</body></html>'

def chapter_nav(prefix='../', active=None):
    cats=list(dict.fromkeys(c['category'] for c in CHAPTERS))
    nav='<nav class="toc-links" aria-label="章节目录">'
    for cat in cats:
        nav+=f'<div class="toc-group">{e(cat)}</div>'
        for c in CHAPTERS:
            if c['category']!=cat: continue
            nav+=f'<a class="toc-link {"active" if c["slug"]==active else ""}" data-search="{e(c["title"]+" "+c["summary"])}" href="{prefix}guide/{e(c["slug"])}.html">{e(c["title"])}</a>'
    return nav+'</nav>'

def source_list(compact=False):
    s='<div class="source-list">'
    for x in SOURCES:
        id,name,when,url,typ=x
        s+=f'<a class="source-item" href="{e(url)}" target="_blank" rel="noopener noreferrer"><span class="source-type">{"OFFICIAL" if typ=="official" else "REPORT"}</span><span class="source-name">{e(name)}<small>{e(when)}</small></span><span class="source-arrow">↗</span></a>'
    return s+'</div>'

def home():
    paths=''.join(f'''<article class="route-card glass"><div class="route-top"><span class="route-icon">{e(r['icon'])}</span><span class="route-badge">{e(r['badge'])}</span></div><h3>{e(r['name'])}</h3><p>{e(r['money'])}</p><div class="route-divider"></div><div class="route-details"><span>适合谁</span><strong>{e(r['who'])}</strong><span>成交链路</span><strong>{e(r['funnel'])}</strong><span>常见风险</span><strong>{e(r['risk'])}</strong></div><p class="route-example">{e(r['example'])}</p></article>''' for r in ROUTES)
    chapters=''.join(f'''<a class="chapter-card glass" href="guide/{e(c['slug'])}.html"><div class="chapter-meta"><span>{e(c['category'])}</span><span>{c['mins']} min</span></div><h3>{e(c['title'])}</h3><p>{e(c['summary'])}</p><span class="chapter-cta">阅读完整章节 ↗</span></a>''' for c in CHAPTERS[:8])
    templates=''.join(f'''<article class="template-card"><div class="template-heading"><span class="template-tag">{e(cat)}</span><strong>{e(title)}</strong></div><p>{e(body).replace(chr(10),'<br>')}</p><button class="small-copy js-copy" data-copy="{e(body)}">复制文案 <span>↗</span></button></article>''' for cat,title,body in TEMPLATES[:12])
    faqs=''.join(f'<details><summary>{e(q)}<span>+</span></summary><p>{e(a)}</p></details>' for q,a in FAQ[:12])
    plans=[('01','建立最小交易闭环','定位、服务、主页与收款测试','day1'),('02','发布第一轮 10 条内容','方法、故事、反例和服务说明','day2'),('03','验证精准需求','记录真实咨询，补齐交付与报价','day3'),('04','完成数据复盘','据漏斗判断坚持、调整或停止','day4')]
    plan_html=''.join(f'''<label class="plan-item"><input type="checkbox" data-plan="{id}"><span class="plan-num">{n}</span><span><strong>{t}</strong><small>{d}</small></span><span class="plan-check">✓</span></label>''' for n,t,d,id in plans)
    body=f'''<main id="main"><section class="hero shell" aria-labelledby="hero-title">
  <div class="hero-left">
    <div class="ed-kicker">A FIELD GUIDE FOR INDEPENDENT CREATORS / NO. 03</div>
    <h1 id="hero-title">先有客户。<br><span class="hero-accent">再谈流量。</span></h1>
    <p class="ed-hero-lead">在 Threads 上发内容，最后是谁给你付钱？</p>
    <p class="ed-hero-desc">24 章免费教程。从定位、写作、有效互动，到服务、数字产品与业务复盘。只讲可以执行和验证的事。</p>
    <div class="ed-hero-actions">
      <a class="btn btn-primary" href="handbook.html">开始阅读 24 章 ↗</a>
      <a class="btn btn-outline" href="lab.html">打开转化实验室 ↗</a>
    </div>
    <div class="ed-proof"><span><b>24</b> 章教程</span><span><b>06</b> 条变现路径</span><span><b>30</b> 天行动清单</span></div>
  </div>
  <aside class="ed-feature hero-visual" aria-label="Threads 内容商业化的三项判断">
    <div class="ed-feature-head"><span>THE INDEPENDENT JOURNAL</span><span>ISSUE / 03</span></div>
    <div>
      <div class="ed-feature-large" style="font-size:clamp(36px,4vw,63px);letter-spacing:-.075em;line-height:1.13;margin:30px 0">被看见，<br>然后被需要。</div>
      <p class="ed-feature-caption">读者看完一条帖子后，应该知道什么？</p>
      <div class="ed-feature-list">
        <div class="ed-feature-row"><small>01</small><span>你解决什么具体问题</span><em>定位</em></div>
        <div class="ed-feature-row"><small>02</small><span>为什么应该相信你</span><em>证据</em></div>
        <div class="ed-feature-row"><small>03</small><span>需要帮助时去哪找你</span><em>行动</em></div>
      </div>
    </div>
    <p class="ed-feature-note">平台浏览量不等于收入。所有案例、资格、价格和业务结果，均须独立验证。</p>
  </aside>
</section>
<section class="credibility shell"><div><b>先把事实讲清楚</b><p>Threads 历史创作者奖金计划已终止。平台开放广告业务，不等于每个作者按浏览量获得分成。</p></div><a href="#sources">查看平台和监管来源 ↗</a></section>
<section class="lab-promo shell glass"><div class="lab-promo-copy"><span class="eyebrow">NEW / THE CONVERSION WORKBENCH</span><h2>你的账号卡在哪一步？<br><span>30 秒做一次漏斗诊断。</span></h2><p>用真实的汇总数据判断瓶颈，再生成服务卡和下一步行动。全部在本地计算，不要求交出客户隐私。</p></div><a href="lab.html" class="btn btn-primary">进入免费实验室 <span>↗</span></a><div class="lab-orb" aria-hidden="true"></div></section>
<section class="section shell" id="paths"><div class="section-header"><div><div class="eyebrow">01 / MONETIZATION MAP</div><h2>六条变现路径。<br><span>选一条，先跑通。</span></h2></div><p>这六条路径指向不同的付款方、交付模式和时间成本。新手优先选自己已经能交付的能力。</p></div><div class="route-grid">{paths}</div></section>
<section class="section shell pathway-section" id="model"><div class="section-header"><div><div class="eyebrow">02 / REVENUE MODEL</div><h2>别算梦想。<br><span>先算清一单。</span></h2></div><p>收入模型完全由你的假设输入驱动，结果是数学情景，不是收入预测。</p></div><div class="calculator glass" aria-label="Threads 收入情景计算器"><div class="calc-left"><div class="calc-heading"><span class="small-label">SCENARIO CALCULATOR</span><span>数据仅为演示</span></div><div class="calc-field"><label for="price">单笔售价（元）</label><div><input id="price" type="number" min="0" max="1000000" value="499" inputmode="decimal"><span>CNY</span></div></div><div class="calc-field"><label for="cost">每笔变动成本 + 获客成本（元）</label><div><input id="cost" type="number" min="0" max="1000000" value="99" inputmode="decimal"><span>CNY</span></div></div><div class="calc-field"><label for="leads">每月有效询盘数</label><div><input id="leads" type="number" min="0" max="1000000" value="40"><span>LEADS</span></div></div><div class="calc-field"><label for="rate">询盘→成交率（%）</label><div><input id="rate" type="number" min="0" max="100" value="15"><span>%</span></div></div><div class="calc-field"><label for="hours">每单交付小时数</label><div><input id="hours" type="number" min="0.1" step="0.5" max="1000" value="2"><span>HOURS</span></div></div><button class="text-button" id="reset-calc" type="button">恢复示例假设 ↺</button></div><div class="calc-right"><div class="calc-overline">估算月贡献毛利（不含固定成本及税费）</div><div class="calc-big" id="estimated-margin">¥2,400</div><div class="calc-numbers"><div><span>理论成交单数</span><strong id="estimated-sales">6.0</strong></div><div><span>理论营业额</span><strong id="estimated-revenue">¥2,994</strong></div><div><span>每单贡献毛利</span><strong id="estimated-unit">¥400</strong></div><div><span>每小时贡献毛利</span><strong id="estimated-hour">¥200</strong></div></div><div class="calc-caution">⚑ 忽略固定费用、税款、退款、坏账与样本随机波动。实际不会恰好成交小数单。</div><a href="guide/pricing.html" class="inline-link">完整单价与漏斗算法 ↗</a></div></div></section>
<section class="section shell" id="handbook"><div class="section-header"><div><div class="eyebrow">03 / FULL HANDBOOK</div><h2>从注册到复盘。<br><span>一步一步做。</span></h2></div><div class="section-header-action"><span>24 CHAPTERS · BEGINNER FRIENDLY</span><a class="btn btn-outline" href="handbook.html">查看完整目录 ↗</a></div></div><div class="chapter-grid">{chapters}</div></section>
<section class="section shell split-section" id="sprint"><div class="split-title"><div class="eyebrow">04 / THE FIRST 30 DAYS</div><h2>30 天验证计划。<br><span>不承诺 30 天变现。</span></h2><p>每一阶段都有具体产物。完成打勾会只保存在当前浏览器，不需要登录。</p><a class="inline-link" href="guide/content-calendar.html">打开每天详细动作 ↗</a></div><div class="plan-panel glass"><div class="plan-head"><b>YOUR EXECUTION CHECKLIST</b><span id="plan-count">0 / 4 COMPLETED</span></div>{plan_html}<div class="plan-progress"><span id="plan-bar"></span></div><p>结果不足以成交时，不要自责，检查“需求→信任→报价→交付”的具体断点。</p></div></section>
<section class="section shell" id="toolkit"><div class="section-header"><div><div class="eyebrow">05 / COPY · ADAPT · TEST</div><h2>把模板拿走。<br><span>事实自己补上。</span></h2></div><p>所有方括号均为待填字段。禁止拿虚构故事、收入或客户反馈填空。</p></div><div class="template-filter" aria-label="筛选模板"><button class="filter active" data-template-filter="全部">全部</button><button class="filter" data-template-filter="观点">观点</button><button class="filter" data-template-filter="经验">经验</button><button class="filter" data-template-filter="清单">清单</button><button class="filter" data-template-filter="互动">互动</button><button class="filter" data-template-filter="转化">转化</button></div><div class="template-grid" id="template-grid">{templates}</div><a class="inline-link more-templates" href="templates.html">打开全部 24 份可复制模板 ↗</a></section>
<section class="section shell" id="faq"><div class="section-header"><div><div class="eyebrow">06 / COMMON QUESTIONS</div><h2>关键问题。<br><span>不讲玄学。</span></h2></div></div><div class="faq-list">{faqs}</div><a class="inline-link" href="faq.html">查看全部 {len(FAQ)} 个问答 ↗</a></section>
<section class="section shell" id="sources"><div class="section-header"><div><div class="eyebrow">07 / VERIFIED REFERENCES</div><h2>参考依据。<br><span>有出处，才有可信度。</span></h2></div><p>政策、接口与功能可能变动。官方资料标记 OFFICIAL，媒体报道标记 REPORT。最近人工审阅：{TODAY}。</p></div>{source_list()}<p class="source-note">本项目与 Meta、Threads、Instagram 没有关联或官方背书。展示名称只用于说明平台功能。</p></section></main>'''
    return layout('Threads 赚钱保姆级攻略 2026｜从零起号到真实成交 - AI 酋长 Andy','24 章 Threads 实战手册：账号定位、发帖与精准互动、咨询、数字产品、联盟营销、商单、B2B 获客及成本测算。来源可查、不承诺收益。',body)

def handbook():
    cards=''.join(f'''<a class="handbook-card glass" data-search="{e(c['title']+' '+c['summary']+' '+c['category'])}" href="guide/{e(c['slug'])}.html"><div><span>{e(c['category'])}</span><span>{e(c['mins'])} MIN</span></div><h2>{e(c['title'])}</h2><p>{e(c['summary'])}</p><span class="handbook-card-foot">进入阅读 <span>↗</span></span></a>''' for c in CHAPTERS)
    body=f'''<main id="main" class="shell library"><div class="library-head"><div class="eyebrow">THE OPEN-SOURCE KNOWLEDGE BASE</div><h1>完整实操手册<span> / 24 章</span></h1><p>按照“理解商业 → 定位与产品 → 内容与互动 → 成交交付 → 数据风控”的顺序读。所有案例与数字示例都标注适用边界。</p><div class="library-tools"><div class="search-wrap"><span>⌕</span><input id="chapter-search" type="search" placeholder="搜索章节、转化、商单、报价、风控…" aria-label="搜索章节"></div><span id="chapter-search-count">24 章</span><button class="btn btn-outline btn-mini" id="clear-progress" type="button">清空本地进度</button></div><div class="library-progress"><div><span>LEARNING PROGRESS</span><strong id="overall-progress">0 / 24</strong></div><div class="bar-track"><span id="overall-bar"></span></div></div></div><div class="handbook-grid" id="handbook-grid">{cards}</div><p id="empty-chapters" class="empty-state" hidden>没有找到匹配章节。试试“咨询”“报价”或“风控”。</p></main>'''
    return layout('Threads 赚钱教程 · 24 章完整手册｜AI 酋长 Andy','系统阅读 Threads 赚钱保姆级攻略：选赛道、账号定位、内容获客、私信成交、商单与数字产品、财务测算、合规风险与对抗式审核。',body,kind='handbook',url='handbook.html')

def chapter_page(c,i):
    prev=CHAPTERS[i-1] if i>0 else None
    nxt=CHAPTERS[i+1] if i<len(CHAPTERS)-1 else None
    steps=''.join(f'<li><span class="step-n">{j:02}</span><p>{e(item)}</p></li>' for j,item in enumerate(c['steps'],1))
    source=next((s for s in SOURCES if s[0]==c['source']),None)
    deep=DEEP_DIVES.get(c['slug'])
    deep_html=''
    if deep:
        items=''.join(f'<li>{e(t)}</li>' for t in deep['steps'])
        deep_html=f'<section class="article-section deep-dive"><div class="section-index">PRACTICAL LAB / STEP BY STEP</div><h2>{e(deep["title"])}</h2><ol class="deep-list">{items}</ol><div class="action-note"><strong>完成时你应该拿到</strong><p>{e(deep["result"])}</p></div></section>'
    src=f'<p class="chapter-source">平台依据与扩展阅读：<a target="_blank" rel="noopener noreferrer" href="{e(source[3])}">{e(source[1])} ↗</a>。章节含作者的实操建议，不代表平台承诺或官方算法规则。</p>' if source else ''
    body=f'''<main id="main" class="shell reading-layout"><aside class="reading-sidebar glass"><a href="../handbook.html" class="back-link">← 完整目录</a><div class="reading-progress-head"><span>MY READING PROGRESS</span><strong id="overall-progress">0 / 24</strong></div><div class="bar-track"><span id="overall-bar"></span></div><div class="search-wrap"><span>⌕</span><input id="chapter-search" type="search" placeholder="搜索章节..." aria-label="搜索目录"></div>{chapter_nav(active=c['slug'])}</aside><article class="article" data-chapter="{e(c['slug'])}"><div class="article-kicker">{e(c['category'])} <span> / </span> {e(c['mins'])} MIN READ <span> / </span> LAST VERIFIED {TODAY}</div><h1>{e(c['title'])}</h1><p class="article-summary">{e(c['summary'])}</p><div class="article-actions"><button id="mark-read" class="btn btn-primary btn-mini" data-chapter="{e(c['slug'])}">标记已学完 ✓</button><a href="../templates.html" class="btn btn-outline btn-mini">全部文案模板 ↗</a></div><div class="article-divider"></div><section class="article-section"><div class="section-index">01 / EXECUTION</div><h2>照着做：具体操作步骤</h2><ol class="steps-list">{steps}</ol></section>{deep_html}<section class="article-section"><div class="section-index">02 / COPYABLE TEMPLATE</div><h2>可直接改写的示范</h2><div class="copy-panel"><p>{e(c['copy']).replace(chr(10),'<br>')}</p><button class="small-copy js-copy" data-copy="{e(c['copy'])}">复制这段示范 ↗</button></div></section><section class="article-section"><div class="section-index">03 / DEFINITION OF DONE</div><h2>怎样算完成？</h2><div class="action-note"><strong>你的验收产物</strong><p>{e(c['output'])}</p><strong>必须追踪的信号</strong><p>{e(c['metrics'])}</p></div></section><section class="article-section"><div class="section-index">04 / ADVERSARIAL REVIEW</div><h2>这一章最容易踩的坑</h2><div class="caution-box"><span>!</span><p>{e(c['risk'])}</p></div>{src}</section><div class="article-end"><div><span>读完后，下一步</span><strong>{e(nxt['title'] if nxt else '你已完成全部 24 章，可以执行 30 天实验')}</strong></div>{f'<a class="btn btn-primary" href="{e(nxt["slug"])}.html">下一章 ↗</a>' if nxt else '<a class="btn btn-primary" href="../plan.html">打开 30 天行动表 ↗</a>'}</div><nav class="article-pagination" aria-label="章节翻页">{f'<a href="{e(prev["slug"])}.html">← {e(prev["title"])}</a>' if prev else '<span>已经是第一章</span>'}{f'<a href="{e(nxt["slug"])}.html">{e(nxt["title"])} →</a>' if nxt else '<span>教程全部完成</span>'}</nav></article><aside class="reading-right"><div class="glass sticky-contact"><div class="eyebrow">NEED A HUMAN SECOND OPINION?</div><h3>自己学，或者找 Andy 交流。</h3><p>专业内容与实操服务分开。先看免费教程，再决定是否需要咨询。</p><a href="https://metaver.vip/services" target="_blank" rel="noopener noreferrer">查看服务内容 ↗</a><button class="small-copy js-copy" data-copy="AIPMAndy">复制微信 AIPMAndy ↗</button></div></aside></main>'''
    return layout(f'{c["title"]}｜Threads 赚钱保姆级攻略',c['summary'],body,prefix='../',kind='reading',url=f'guide/{c["slug"]}.html')

def templates_page():
    cards=''.join(f'''<article class="template-card" data-search="{e(cat+' '+title+' '+body)}"><div class="template-heading"><span class="template-tag">{e(cat)}</span><strong>{e(title)}</strong></div><p>{e(body).replace(chr(10),'<br>')}</p><button class="small-copy js-copy" data-copy="{e(body)}">复制后填入真实事实 ↗</button></article>''' for cat,title,body in TEMPLATES)
    body=f'''<main id="main" class="shell library"><div class="library-head"><div class="eyebrow">THE COPY LIBRARY</div><h1>24 份文案模板<span> / 免费复制</span></h1><p>模板用于整理你的真实经验，不能代替实际经历。请替换方括号中的变量，并遵守原创、隐私和商业披露要求。</p><div class="library-tools"><div class="search-wrap"><span>⌕</span><input id="template-search" type="search" placeholder="搜索观点、故事、私信、联盟披露..." aria-label="搜索文案模板"></div></div></div><div class="template-grid all-templates" id="template-grid">{cards}</div><p class="empty-state" id="empty-templates" hidden>没有匹配的模板。</p></main>'''
    return layout('24 份 Threads 发帖与私信文案模板｜AI 酋长 Andy','免费下载和复制 24 份 Threads 内容获客、观点、案例、英语内容与私信成交模板；支持查找并标注需要替换的真实事实。',body,kind='templates',url='templates.html')

def plan_page():
    # Reuse docs/30_DAY_PLAN.md as the sole maintained daily-plan source.
    raw=(ROOT/'docs/30_DAY_PLAN.md').read_text(encoding='utf-8')
    daily=[]
    for line in raw.splitlines():
        if not re.match(r'^\| D\d+ \|',line):continue
        cells=[x.strip() for x in line.split('|')[1:-1]]
        if len(cells)==4:daily.append(cells)
    if len(daily)!=30:raise ValueError(f'Expected 30 daily tasks, got {len(daily)}')
    groups=[]
    for week, start in enumerate([0,7,14,21],1):
        end=7 if week==1 else 14 if week==2 else 21 if week==3 else 30
        items=''.join(f'<label class="daily-item"><input type="checkbox" data-plan="plan-day-{e(n)}"><span class="daily-day">{e(n)}</span><span class="daily-main"><strong>{e(task)}</strong><small>验收：{e(output)}</small><em>判断：{e(decision)}</em></span><span class="daily-check" aria-hidden="true">✓</span></label>' for n,task,output,decision in daily[start:end])
        groups.append(f'<section class="daily-week glass"><div class="daily-week-heading"><span class="eyebrow">SPRINT / WEEK 0{week}</span><h2>{["准备最小产品与账号","内容获客第一轮","建立真实转化链路","复盘与决策"][week-1]}</h2></div><div class="daily-items">{items}</div></section>')
    body=f'''<main id="main" class="shell daily-page"><header class="daily-intro"><div class="eyebrow with-dot">30 DAY EXPERIMENT / ZERO GUARANTEES</div><h1>30 天行动计划。<br><span>每天只做一件对的事。</span></h1><p>这份清单跟着你在本机保存，不需要创建账户。30 天是检验生意闭环的观察期，不承诺 30 天获得第一单。不要在这里填写真实客户个人资料。</p><div class="daily-progress glass"><div><span>LOCAL PROGRESS · 仅本机</span><strong id="plan-count">0 / 30 COMPLETED</strong></div><div class="bar-track"><span id="plan-bar"></span></div></div><div class="daily-intro-actions"><a class="btn btn-primary" href="lab.html">打开转化实验室 ↗</a><a class="btn btn-outline" href="docs/30_DAY_PLAN.md">阅读 Markdown 全文 ↗</a></div></header><div class="daily-weeks">{''.join(groups)}</div><div class="daily-end glass"><h2>30 天结束，你应该拥有 4 个真实答案。</h2><p>有人真的为此问题付费吗？哪一种内容带来了目标咨询？每单贡献毛利是否为正？继续投入的机会成本是多少？</p><a class="btn btn-primary" href="lab.html#funnel-tool">核对实收与转化 ↗</a></div></main>'''
    return layout('Threads 30 天可勾选行动计划｜AI 酋长 Andy','从定位、内容、互动，到服务报价与真实实收，30 天逐日清单、验收产物和停止条件。清单进度只保存在本机。',body,kind='plan',url='plan.html')

def lab_page():
    options=''.join(f'<option value="{e(key)}" data-advice="{e(advice)}" data-link="{e(link)}">{e(title)}</option>' for key,title,advice,link in DECISIONS)
    cards=''.join(f'<article class="case-card glass"><div class="eyebrow">{e(x["tag"])}</div><h3>{e(x["title"])}</h3><dl><dt>谁会付钱</dt><dd>{e(x["audience"])}</dd><dt>内容怎么写</dt><dd>{e(x["post"])}</dd><dt>卖什么</dt><dd>{e(x["offer"])}</dd><dt>核算口径</dt><dd>{e(x["measure"])}</dd></dl><p class="case-limit">边界：{e(x["caution"])}</p></article>' for x in EXAMPLES)
    body=f'''<main id="main" class="shell lab-page"><div class="lab-intro"><div class="eyebrow with-dot">INCOME LAB / PRACTICAL WORKBENCH</div><h1>从流量到订单。<br><span>每一步有据可查。</span></h1><p>一个免费、浏览器内运行的工具台。先诊断卡点，再写明服务，最后用真实数据复盘。下面的示例只是演练，绝非收入案例或平台预测。</p><div class="lab-intro-actions"><a href="#diagnose" class="btn btn-primary">开始诊断 ↘</a><a href="handbook.html" class="btn btn-outline">阅读实操教程 ↗</a></div></div>
    <div class="lab-panels"><section id="diagnose" class="glass lab-panel"><div class="lab-panel-meta">01 / BOTTLENECK DIAGNOSIS</div><h2>我应该先改哪里？</h2><p>只选你现在真实遇到的问题，不用假装自己已经有客户。</p><label class="lab-label" for="lab-stage">当前最主要的瓶颈</label><select id="lab-stage" aria-label="当前瓶颈">{options}</select><div class="lab-result" id="lab-diagnosis" role="status" aria-live="polite"></div></section>
    <section id="offer-tool" class="glass lab-panel"><div class="lab-panel-meta">02 / YOUR FIRST OFFER</div><h2>一分钟生成服务说明</h2><p>先写清交付，再决定要不要收费。下面的数据不会上传，也不会自动保存。</p><div class="lab-field-grid"><label>适合谁<input id="offer-who" maxlength="100" placeholder="例：找工作 3 个月没有面试的社招候选人"></label><label>解决什么问题<input id="offer-issue" maxlength="100" placeholder="例：确认简历/岗位匹配存在什么问题"></label><label>实际交付<input id="offer-deliver" maxlength="130" placeholder="例：一次诊断 + 一页行动清单"></label><label>价格（请填真实报价）<input id="offer-price" maxlength="80" placeholder="例：按个人实际报价，不必照抄"></label><label>服务边界<input id="offer-limit" maxlength="130" placeholder="例：不保证拿到 Offer"></label><label>规则与联系入口<input id="offer-link" maxlength="130" placeholder="例：退款说明与预约见服务主页"></label></div><div class="lab-preview" id="lab-offer-result" aria-live="polite">填写上面的字段，即可生成一份真实可改写的服务卡。</div><button class="btn btn-primary" id="lab-copy-offer" type="button">复制服务卡 <span>↗</span></button></section></div>
    <section id="funnel-tool" class="glass lab-panel lab-wide"><div class="lab-panel-meta">03 / RECONCILE THE FUNNEL</div><div class="section-header"><div><h2>真实业务漏斗</h2><p>填同一统计周期的实际数据。不混用浏览、询盘、订单和到账。</p></div></div><div class="funnel-fields"><label>帖子浏览（可选）<input id="f-views" type="number" min="0" step="1" value="0"></label><label>主页访问<input id="f-profile" type="number" min="0" step="1" value="0"></label><label>外链点击<input id="f-clicks" type="number" min="0" step="1" value="0"></label><label>有效咨询<input id="f-leads" type="number" min="0" step="1" value="0"></label><label>实际报价<input id="f-quotes" type="number" min="0" step="1" value="0"></label><label>付款订单<input id="f-orders" type="number" min="0" step="1" value="0"></label><label>本期实收总额（元）<input id="f-received" type="number" min="0" step="0.01" value="0"></label><label>已知变动成本（元）<input id="f-costs" type="number" min="0" step="0.01" value="0"></label></div><p id="f-warning" class="funnel-warning" role="status"></p><div class="funnel-summary" id="f-summary" aria-live="polite"></div><div class="funnel-footer"><span>贡献毛利不等于净利润；未计入固定成本、税费和未预见退款。跨设备转化不一定能准确归因。</span><button id="lab-copy-funnel" class="btn btn-outline btn-mini" type="button">复制复盘摘要 ↗</button></div></section>
    <section id="case-studies" class="section lab-cases"><div class="section-header"><div><div class="eyebrow">04 / WORKED EXAMPLES</div><h2>三种真实场景。<br><span>全是模拟案例。</span></h2></div><p>不编造粉丝、收款或平台分发数据。读者自行替换业务条件。</p></div><div class="case-grid">{cards}</div></section>
    <div class="glass lab-bottom"><div><div class="eyebrow">CONTINUE / FREE RESOURCES</div><h2>还需要具体执行细则？</h2><p>读 24 章保姆级手册，或直接打开 30 天行动表与空白 CRM 模板。</p></div><div><a class="btn btn-primary" href="handbook.html">完整教程 ↗</a><a class="btn btn-outline" href="plan.html">30 天计划 ↗</a></div></div></main>'''
    return layout('Threads 转化实验室｜定位、服务卡、实际业务漏斗 · AI 酋长 Andy','免费的 Threads 赚钱转化工具：诊断瓶颈、生成清晰服务卡、记录实际线索与实收，全部本地运行；不提供收益承诺。',body,kind='lab',url='lab.html')

def faq_page():
    q=''.join(f'<details><summary>{e(a)}<span>+</span></summary><p>{e(b)}</p></details>' for a,b in FAQ)
    body=f'''<main id="main" class="shell library"><div class="library-head"><div class="eyebrow">COMMON QUESTIONS · ZERO HYPE</div><h1>高频问题<span> / {len(FAQ)} 问</span></h1><p>回答按 2026 年 10 月可查信息整理；平台政策随时可能调整。对于未知算法参数，明确保留未知。</p></div><div class="faq-list faq-wide">{q}</div><div class="section spaced">{source_list()}</div></main>'''
    return layout('Threads 赚钱常见问题与政策核验｜AI 酋长 Andy','Threads 变现常见疑问：是否按阅读量分钱、如何接商单、付费合作披露、私信风控和 30 天实验。',body,kind='faq',url='faq.html')

def run(check=False):
    files={'index.html':home(),'handbook.html':handbook(),'templates.html':templates_page(),'faq.html':faq_page(),'lab.html':lab_page(),'plan.html':plan_page()}
    for i,c in enumerate(CHAPTERS):files[f'guide/{c["slug"]}.html']=chapter_page(c,i)
    files['404.html']=layout('页面未找到｜Threads 赚钱保姆级攻略','该页面不存在，请返回教程首页。','<main id="main" class="shell error-page"><div class="eyebrow">404 / PAGE NOT FOUND</div><h1>这条路暂时走不通。</h1><p>内容可能已移动。回到教程首页，继续从能验证的事情开始。</p><a class="btn btn-primary" href="index.html">返回教程首页 ↗</a></main>',kind='error',url='404.html')
    urls=['']+['handbook.html','templates.html','faq.html','lab.html','plan.html']+[f'guide/{c["slug"]}.html' for c in CHAPTERS]
    files['sitemap.xml']='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls)+'</urlset>\n'
    files['robots.txt']='User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n'
    # Full offline Markdown copies keep the source useful even before Pages is enabled.
    md=['# Threads 赚钱保姆级攻略 · 2026','', '> 24 章实操 · 6 条变现路线 · 免费开源 · 不承诺收益','', '**作者：AI 酋长 Andy｜微信：AIPMAndy｜官网：https://metaver.vip/**','', '最后核验：2026-10-24。具体政策以原始链接为准。','']
    for c in CHAPTERS:
        md.extend([f'## {c["title"]}', '',c['summary'],'','### 操作步骤',''])
        md.extend(f'{k}. {v}' for k,v in enumerate(c['steps'],1))
        deep=DEEP_DIVES.get(c['slug'])
        if deep:
            md.extend(['','### 进阶实操：'+deep['title'],''])
            md.extend(f'{k}. {v}' for k,v in enumerate(deep['steps'],1))
            md.extend(['','**实操验收：** '+deep['result'],''])
        md.extend(['','### 可改写的示范','', '```text',c['copy'],'```','',f'**验收产物：** {c["output"]}','',f'**观察指标：** {c["metrics"]}','',f'**风险：** {c["risk"]}',''])
    md.extend(['## 来源与延伸阅读',''])
    md.extend(f'- [{x[1]}]({x[3]})（{x[2]}）' for x in SOURCES)
    files['HANDBOOK.md']='\n'.join(md)+'\n'
    templates_md=['# Threads 可改写模板 24 份','','所有占位符都需要换成自己真实的经历、数据和服务。','']
    for idx,(kind,title,body) in enumerate(TEMPLATES,1):
        templates_md.extend([f'## {idx:02}. [{kind}] {title}','','```text',body,'```',''])
    files['TEMPLATES.md']='\n'.join(templates_md)+'\n'
    for path,data in files.items():
        p=ROOT/path
        if check:
            if not p.exists() or p.read_text()!=data: raise SystemExit(f'OUT OF DATE: {path} (run python scripts/build.py)')
        else:
            p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data,encoding='utf8')
    print(f'{"CHECKED" if check else "BUILT"}: {len(files)} static outputs · {len(CHAPTERS)} chapters · {len(TEMPLATES)} templates · {len(FAQ)} FAQ · {len(SOURCES)} sources')
if __name__=='__main__':run('--check' in sys.argv)
