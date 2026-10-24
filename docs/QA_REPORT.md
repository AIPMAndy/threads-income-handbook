# Threads Income Handbook V2 · Quality Verification

日期：2026-10-24。

## 已执行

```bash
python3 scripts/build.py
python3 scripts/check.py
python3 scripts/build.py --check
node --check assets/app.js
node scripts/js_logic_check.js
```

结果：**35 个构建产物**、**31 个 HTML 页面**、**24 个教程章节**、**14 条参考来源**；独立静态检查 **1522 项通过**；Node 无浏览器依赖的 JS 测试 **20 项通过**。重点验证了：导航与锚点、SEO 必需标签、来源 HTTPS、页面数量、网页联系方式、转化实验室存在、每日计划数量、服务卡必填字段、漏斗 5 个关键计算指标、负值与非整数交易单数拒绝、零分母保护、30 天清单本地进度。

## 尚未完成

- **浏览器真实渲染、移动端全屏截图、交互点击与性能测试**：此执行环境的 Chromium 对 `localhost`、`file:` 和 `data:` 的导航均返回 `ERR_BLOCKED_BY_ADMINISTRATOR`。这属于运行环境访问限制，不能当作网页测试通过，也不能据此判定网页本身有错。
- GitHub Pages 线上部署、索引及 SEO 收录：目前没有创建本项目远程仓库，也没有线上域名可检验。
- 第三方官方链接是否可在每个用户所在地区打开：需要目标市场实际网络、账户及设备核验。

## 发布前检查建议

在具备浏览器能力的常规开发机运行：

```bash
pip install playwright
python -m playwright install chromium
python scripts/browser_check.py
```

`browser_check.py` 会通过本地 HTTP 服务打开 6 类网页，检查 390px 和 1440px 版式、横向溢出、诊断推荐、服务卡、漏斗、错误输入和 JS 控制台，若通过会输出本地截图。但**本次环境未能执行成功**，不能把它列入“已通过”结果。

## 数据/法律局限

业务测算是用户输入的情况演练或回顾，绝非预测。内容表达不保证流量、收入、账号风控结果、法律税务合规；所有个人/客户信息需由使用者依照实际制度处理。
