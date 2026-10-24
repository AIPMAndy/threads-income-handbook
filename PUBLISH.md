# 开源发布 · AIPMAndy/threads-income-handbook

本项目已包含 MIT 许可证、GitHub Pages Actions 和静态资源。**只在确认本地质量检查通过后发布。**

## 方式 A：一条命令发布（推荐）

确保本机有 `git`、Python 3，并已使用 GitHub CLI 登录：`gh auth login`。

```bash
bash publish.sh
```

脚本会完成本地校验、Git commit、尝试创建 PUBLIC 仓库、推送 `main`，然后尝试配置 Pages。如果账号无 Pages 配置权限，最后一步需手动完成。

## 方式 B：GitHub 网页建仓库，再推送

1. 打开 [新建仓库](https://github.com/new?name=threads-income-handbook)，所有者选 `AIPMAndy`，仓库名为 `threads-income-handbook`，可见性选 **Public**，不要勾选初始化 README、.gitignore 或 license（项目已有）。
2. 在解压后的项目根目录执行 `bash publish.sh`。如果没有 `gh` 但安装了 Git，脚本会把已有公开仓库作为 `origin` 并推送。
3. 在 GitHub 仓库 `Settings → Pages → Build and deployment → Source` 选择 `GitHub Actions`。
4. 检查 `Actions` 中 `Build, verify, and deploy GitHub Pages` 成功后，再访问 <https://aipmandy.github.io/threads-income-handbook/>。
5. `Settings → General → Social preview` 上传 `assets/social-preview.png`（可选，但推荐）。

## 校验及注意事项

```bash
bash publish.sh --check-only
```

- 不要把 API Key、客户个人信息、账号 Cookie 或私信对话原件提交进公开仓库。
- 仓库不存在时，网页模式必须先由账号所有者创建，不可把本地包或预期页面地址当成已上线。
- 若目标仓库已存在且设为 Private，脚本会停止，不会擅自公开它。
- 发布后如发现 Actions 未运行，可在 GitHub Actions 里手动执行工作流。
- 目前网站的真实浏览器视觉回归尚未完成，本机还应验证移动端展示和关键交互。
