# Threads 平台事实核验（2026-10-24）

证据优先级：Meta 官方新闻/帮助中心 > 监管机构 > 可信媒体报道 > 作者经验判断。作者建议与 Meta 平台官方机制分开叙述。

| 命题 | 证据与结论 | 来源 |
|---|---|---|
| Threads 主页最多 5 个链接、可查看链接访问 Insights | Meta 2025-05-15 公布链接功能，2025-07-22 扩展 Insights | https://about.fb.com/news/2025/03/new-threads-features-more-personalized-experience-you-control/ |
| Threads 可以站内私信 | Meta 2025-07-01 公布，功能地区与账号差异以客户端为准 | https://about.fb.com/news/2025/07/introducing-messaging-highlighted-perspectives-threads/ |
| 可以附加最长 10,000 字符文本 | Meta 2025-09-04 公布 | https://about.fb.com/news/2025/09/attach-text-threads-posts-share-longer-perspectives/ |
| Threads Communities | Meta 2025-10-22 公布，后续更新 | https://about.fb.com/news/2025/10/introducing-threads-communities-find-your-people/ |
| 2026-06 月活超 5 亿 | Meta 官方公布，属平台规模，不保证单个账号分发 | https://about.fb.com/news/2026/06/meta-launching-new-features-500-million-monthly-threads-users/ |
| 历史创作者奖金计划已终止 | 2025-07-22 Engadget 根据独立报道确认，**不是官方长期保证** | https://www.engadget.com/social-media/meta-has-ended-its-bonus-program-on-threads-201627935.html |
| Threads 广告扩展全球 | Meta 2026-01 公告，属于广告主投放，不代表所有创作者可以自动获得流量分成 | https://about.fb.com/br/news/2026/01/anuncios-no-threads-um-ano-depois-agora-alcancando-todos-os-usuarios-e-mercados-globalmente/ |
| 付费合作、赠品和联盟推广需要披露 | Meta 商业内容政策及 FTC 指南，适用范围因司法辖区而异 | https://www.facebook.com/help/instagram/616901995832907?locale=en_GB · https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers |
| 图片/视频不能无授权搬运 | Meta 版权指导 | https://www.facebook.com/help/354736791367645/ |
| Web 域名切换至 threads.com | Meta 2025-04 公告 | https://about.fb.com/news/2025/04/new-features-threads-web-experience/ |
| 2026-02 Dear Algo | Meta 公布其用于个人看到的内容偏好，调整期为 3 天；推出地区含美国、英国、澳大利亚、新西兰，不是创作者的流量奖励功能 | https://about.fb.com/news/2026/02/threads-dear-algo/ |
| 2026-06 Your Algo | Meta 公布可私下选择 1/3/7 天调整信息流的主题偏好，初期面向美国、加拿大、英国、澳大利亚、新西兰，不是推荐曝光保证 | https://about.fb.com/news/2026/06/meta-launching-new-features-500-million-monthly-threads-users/ |
| 站内陌生消息请求 | Meta 2025-09 公布陌生请求阶段链接和媒体被限制且有发送频率约束，具体功能因账户与地区有差异 | https://about.fb.com/news/2025/07/introducing-messaging-highlighted-perspectives-threads/ |
| 2026 新播客工具 | Meta 2026-09 公告，说明平台功能仍在迭代 | https://about.fb.com/news/2026/09/threads-expands-podcast-toolkit-for-creators-and-listeners/amp/ |

## 不可证实 / 不该承诺

- “发 × 条/天必涨粉”——没有权威通用阈值；不能冒充算法秘密。
- “Threads 外链一律限流”——没有对所有账号、帖子都适用的已验证定律。
- “有 × 粉丝就能月入 × 元”——商业转化取决于人群、产品、定价、交付和支付。
- “私信 × 次不封号”——风控受行为、内容和用户反馈影响，具体阈值不公开。
- “按浏览量固定拿广告分成”——不能从广告扩张公告推出此结论。
- “30 天出第一单”——应定位为 30 天**验证实验**，不能保证现金结果。

## 更新 SOP

每月检查上述来源最新更新；确认每个新增政策声明的官方文档、发布日期、适用地区、产品功能灰度、是否会影响现有执行建议。只有证据足够才修改网页；运行 `python3 scripts/build.py && python3 scripts/check.py` 后提交变更。

## 使用证据的注意事项

- 本页的 Meta 官方页面包含 2025 年多次更新。May 15 是主页链接功能更新；July 22 才是扩展版 Insights 的公告时间，不能把两个日期互换。
- Instagram 帮助中心的合作标记文档用于说明 Meta 的商业内容定义和利益披露。**不能仅凭该 Instagram 帮助页假设每个 Threads 账号一定有相同的“Paid partnership”按钮**；发布前还需检查 Threads 当期界面及适用政策。
- 官方“主题帖可能有更多浏览”属于平台相关性观察，不构成使用话题标签必涨粉的因果结论。
- 以上功能可能灰度、地区限制或改版，**没有链接能证明 Threads 普遍提供固定阅读分成**。
