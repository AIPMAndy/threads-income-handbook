#!/usr/bin/env bash
set -euo pipefail

REPO="AIPMAndy/threads-income-handbook"
REPO_URL="https://github.com/${REPO}.git"
PAGES_URL="https://aipmandy.github.io/threads-income-handbook/"
cd "$(dirname "$0")"

if [[ "${1:-}" == "--help" ]]; then
  cat <<'USAGE'
用法: bash publish.sh [--check-only]
首次发布：自动检查源码，创建本地 Git 提交；已安装且登录 gh 时自动创建公开 GitHub 仓库并推送。
没有 gh 时：如果目标仓库已创建，则使用 git 推送；否则打印建仓库链接并退出。
--check-only  只执行本地质量检查，不发布、不创建任何文件。
USAGE
  exit 0
fi

printf '\n[1/4] 检查生成文件与站内链接...\n'
python3 scripts/build.py --check
python3 scripts/check.py
if command -v node >/dev/null 2>&1; then
  node scripts/js_logic_check.js
else
  echo '提示：未安装 Node.js，跳过可选的 JS 独立逻辑测试。'
fi
[[ "${1:-}" == "--check-only" ]] && exit 0

printf '\n[2/4] 准备本地 git 提交...\n'
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init -b main
fi
BRANCH="$(git branch --show-current)"
if [[ -n "$BRANCH" && "$BRANCH" != "main" ]]; then
  echo "停止：当前分支是 $BRANCH。请在 main 分支执行，避免覆盖既有项目。" >&2
  exit 1
fi
if [[ -z "$(git config user.name || true)" || -z "$(git config user.email || true)" ]]; then
  echo '请先设置 git user.name 和 user.email，再重试。' >&2
  exit 1
fi
git add -A
if ! git diff --cached --quiet; then
  git commit -m "docs: publish Threads income handbook V2"
fi

printf '\n[3/4] 创建或连接公开 GitHub 仓库...\n'
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  if gh repo view "$REPO" >/dev/null 2>&1; then
    PRIVATE="$(gh api "repos/$REPO" --jq '.private')"
    if [[ "$PRIVATE" == "true" ]]; then
      echo '停止：目标仓库存在但为 Private；未自行更改可见性。' >&2
      exit 1
    fi
    if ! git remote get-url origin >/dev/null 2>&1; then
      git remote add origin "$REPO_URL"
    fi
    git push -u origin main
  else
    gh repo create "$REPO" --public --source=. --remote=origin --push --description 'Threads 赚钱保姆级攻略：24章实操、30天计划、转化实验室、开源网站'
  fi
  printf '\n[4/4] 尝试配置 GitHub Pages...\n'
  if gh api "repos/$REPO/pages" >/dev/null 2>&1; then
    if ! gh api -X PUT "repos/$REPO/pages" -f build_type=workflow >/dev/null 2>&1; then
      echo 'Pages 已存在，但无法自动改为 Actions 源，请到 Settings → Pages 手动检查。'
    fi
  else
    if ! gh api -X POST "repos/$REPO/pages" -f build_type=workflow >/dev/null 2>&1; then
      echo 'Pages 无法自动启用，请到 Settings → Pages → Source 选择 GitHub Actions。'
    fi
  fi
  gh workflow run pages.yml -R "$REPO" --ref main >/dev/null 2>&1 || true
else
  if ! git remote get-url origin >/dev/null 2>&1; then
    git remote add origin "$REPO_URL"
  fi
  if ! git ls-remote "$REPO_URL" HEAD >/dev/null 2>&1; then
    echo '目标仓库尚不存在，且没有可用的 GitHub CLI 登录。'
    echo '先在浏览器中创建一个 PUBLIC 的空仓库（不要初始化 README）：'
    echo 'https://github.com/new?name=threads-income-handbook'
    echo '仓库所有者选择 AIPMAndy，创建后再次执行 bash publish.sh。'
    exit 2
  fi
  git push -u origin main
  echo '请到 Settings → Pages → Build and deployment → Source 选择 GitHub Actions。'
fi
printf '\n源码已推送： https://github.com/%s\n' "$REPO"
printf 'Pages 预期地址（只有部署成功后可访问）： %s\n' "$PAGES_URL"
printf '部署检查： https://github.com/%s/actions\n' "$REPO"
printf '社交预览图仍需手动上传 Settings → General → Social preview\n'
