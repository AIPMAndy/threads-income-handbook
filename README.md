# Threads 赚钱保姆级攻略 · 2026

> 24 章可验证实操教程 · 6 条变现路线 · 24 份可改写模板 · 36 FAQ · 收益模型计算器 · 30 天执行清单
>
> 原则：**不要把“浏览量”当收入。先弄清谁愿意为你解决的哪个问题付费。**

本项目是一份**完全开源、可静态部署**的 Threads 商业化教程和苹果风/流动玻璃交互网站，不包含后台、账号爬虫、批量私信或刷量工具。适合通过专业服务、数字产品、B2B 线索、联盟营销、品牌合作与社区会员获利的作者。

- 维护日期：**2026-10-24**。
- 编辑：**AI 酋长 Andy**。
- 微信：**`AIPMAndy`**（网站顶部、手册侧栏与页脚可一键复制）。
- 官网：<https://metaver.vip/> ｜ 服务：<https://metaver.vip/services>。
- 拟部署地址（**只有创建仓库并开启 Pages 后才可访问**）：`https://aipmandy.github.io/threads-income-handbook/`。

## 目录

24 章：平台收入真相、基础注册、安全、赛道、主页、最小服务、首 10 条、开头、真实故事、评论、私信、服务交付、数字产品、联盟营销、品牌合作、B2B、会员、英文市场、30 天计划、归因看板、报价与毛利、文案模板、风控版权、跨境税务、对抗式审核。

网页将它们组织成可检索独立章节，每页包含：**具体操作步骤 → 可复制示例 → 验收产物 → 应追踪指标 → 最容易踩的坑 → 可点击来源**。

## 使用方式

### 一分钟查看网站

在项目根目录运行：

```bash
python3 -m http.server 8080
```

浏览器打开 <http://localhost:8080/>，即可查看已经构建的 `index.html`。

### 修改教程并构建

在 [`src/content.py`](src/content.py) 编辑章节、FAQ、模板或引用，然后运行：

```bash
python3 scripts/build.py
python3 scripts/check.py
python3 scripts/build.py --check
```

**无 pip 依赖、无需 Node、无需数据库。** 构建脚本生成 31 个独立 HTML 页面和站点地图，适合搜索引擎抓取。CSS、JavaScript 均在 `assets/` 内，网站不向第三方上传用户填写的计算器数字。

### 上线 GitHub Pages

**快捷发布（已登录 GitHub CLI）：** 在项目根目录运行 `bash publish.sh`。如果没有 `gh`，先在 GitHub 创建公开空仓库，再运行同一脚本。详情见 [`PUBLISH.md`](PUBLISH.md)。


1. 新建**公开**仓库 `AIPMAndy/threads-income-handbook`，主分支为 `main`。
2. 将本项目文件（包括 `.github/workflows/pages.yml`）提交到 `main`；务必保留 `.github` 隐藏文件夹。
3. 到仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
4. 检查仓库 **Actions → Build, verify, and deploy GitHub Pages** 是否全部通过。
5. 最终访问预期地址 <https://aipmandy.github.io/threads-income-handbook/>，实际可访问性以部署成功为准。
6. 建议到 **Settings → General → Social preview** 手动上传 `assets/social-preview.png`。此步骤不同于网页中的 `og:image`，无法由常规 Pages 构建自动替你设置。

> 当前包仅是**仓库就绪文件**。创建 GitHub 仓库和启用 Pages 需要具有相应权限的仓库操作；不要将拟部署 URL 当作已上线站点。

## 网站功能

| 功能 | 处理方式 |
| --- | --- |
| 24 篇独立静态 SEO 章节 | 每篇有独立 canonical、description、导航和上一章/下一章 |
| 苹果风玻璃质感 | 背景深空渐变、渐透玻璃、流动光晕、响应式布局、减少动态效果支持 |
| 10 章重点实操进阶 | 补齐账号设置、主页、前 10 条、私信、报价、真实数据等细节验收 |
| 30 天互动执行计划 | 逐日步骤、验收件、停止条件，并将勾选进度存于当前浏览器 |
| 转化实验室 | 诊断漏斗瓶颈、生成可复制服务卡、使用实际数据核对报价/付款/到账/部分成本；不保存客户个人资料 |
| 章节搜索与模板搜索 | 浏览器本地过滤，不连接外部 API |
| 阅读进度、30 天 checklist | 保存浏览器 `localStorage`，可清空，不同步账号 |
| 实时价格与线索模型 | 输入定价、成本、询盘、转化率、工时计算，严格标注“情景演示” |
| 可复制微信与内容模板 | 网页复制，发布前须人工替换真实事实 |
| 来源与证据说明 | 官方来源优先；历史奖金终止依据引用媒体报道并标注证据等级 |
| 自动部署与校验 | GitHub Actions 构建、检查内部链接、检查 SEO 和输出一致性 |

## 关于赚钱的五个重要事实

1. Threads 曾有的创作者奖金计划已停止，不能按固定播放分成计算收入。见 `docs/SOURCES.md`。
2. Meta Threads 广告投放面向广告主，不意味着所有内容创作者可从广告里自动分到收入。
3. 变现重点是清晰的付款方和交付件，实收与净利润是最终信号。
4. 未经过同意的群发私信、虚假成交截图、买粉刷量不属于本教程支持的增长手段。
5. **任何报价、销售单量、转化率和收入计算都只是用户输入的假设，不构成收益预测或承诺。**

## 目录结构

```text
index.html                网站首页（构建生成）
handbook.html             全部章节目录
faq.html                  全部常见问题
lab.html                  转化实验室（新增）
plan.html                 30 天可勾选行动计划（新增）
templates.html            24 条可复制内容模板
guide/*.html              24 篇 SEO 独立章节
assets/style.css          响应式 Liquid Glass 样式
assets/app.js             浏览器本地交互
src/advanced.py           实操进阶、诊断建议与示范场景
assets/social-preview.png 社交分享预览图
src/content.py            唯一内容源
scripts/build.py          零依赖静态构建器
scripts/check.py          自动质量验证
.github/workflows/pages.yml 构建与 Pages 发布
sitemap.xml / robots.txt / 404.html
```

## 项目边界

平台功能与政策经公开链接人工检查，截至 **2026-10-24**。不同地区、账号和客户端的可用性可能不同；涉及收款、税务、用户数据和商业披露时，应遵循实际业务主体所在地的法律及服务条款。

**品牌声明：** 本项目与 Meta / Threads / Instagram 无合作或官方背书关系。网站使用独立设计的抽象符号，不冒用 Threads 官方商标或资质。

- 许可：MIT（仅对本项目原创代码及文字适用）；第三方商标、链接指向内容不在许可范围内。
- 源链接与审稿：[`docs/SOURCES.md`](docs/SOURCES.md)、[`docs/ADVERSARIAL_AUDIT.md`](docs/ADVERSARIAL_AUDIT.md)。

## 离线阅读与编辑

- [`HANDBOOK.md`](HANDBOOK.md)：24 章全文，可直接在 GitHub 阅读。
- [`TEMPLATES.md`](TEMPLATES.md)：24 份可复制文案。
- [`docs/30_DAY_PLAN.md`](docs/30_DAY_PLAN.md)：逐日执行与每周停止条件。
- [`docs/SALES_SOP.md`](docs/SALES_SOP.md)：客户资格判断、报价、履约与验收。
- [`docs/THREADS_CRM_TEMPLATE.csv`](docs/THREADS_CRM_TEMPLATE.csv)：空白业务数据记录表。

## V2 对话式审查

见 [`docs/ADVERSARIAL_AUDIT.md`](docs/ADVERSARIAL_AUDIT.md)，包含五角色反对意见、具体修改证据与未解决风险。新的 [`lab.html`](lab.html) 免费实操工具台已随源码打包，实际部署之前并非线上可访问。

## 本轮质量检查与局限

参见 [`docs/QA_REPORT.md`](docs/QA_REPORT.md)。已完成静态生成、链接完整性、Node 业务逻辑测试；该执行环境阻止 Chromium 对本地页面导航，**未完成真实浏览器视觉回归**。如在自己的电脑部署，请额外执行可选的 `python scripts/browser_check.py`（需 Chromium 与 Playwright）。
