"""
蜜罐批量检测脚本 v2025.06.05
更新说明：
1. 结果文件自动保存至report目录
2. 正常结果文件追加当天日期
3. 新增错误日志记录功能
"""

import re
import os
import time
import argparse
import threading
import datetime
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL警告
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class TokenBucket:
    """令牌桶算法实现速率控制"""
    def __init__(self, rate):
        self._rate = rate  # 令牌生成速率（个/秒）
        self._tokens = 0.0
        self._last_time = time.time()
        self._lock = threading.Lock()

    def consume(self):
        with self._lock:
            now = time.time()
            elapsed = now - self._last_time
            self._tokens += elapsed * self._rate
            self._tokens = min(self._tokens, self._rate)

            if self._tokens < 1.0:
                sleep_time = (1.0 - self._tokens) / self._rate
                time.sleep(sleep_time)
                self._tokens = 0.0
                self._last_time = now + sleep_time
            else:
                self._tokens -= 1.0
                self._last_time = now

def load_urls_from_file(file_path):
    """加载并去重URL列表"""
    try:
        with open(file_path, 'r') as f:
            return list({line.strip() for line in f if line.strip()})
    except Exception as e:
        print(f"[!] 文件读取失败: {str(e)}")
        exit(1)

def detect_honeypot(url, bucket=None):
    """执行蜜罐检测"""
    if bucket:
        bucket.consume()  # 速率控制

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml'
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15,
            verify=False,
            allow_redirects=True,
            stream=True
        )
        response.raise_for_status()
    except Exception as e:
        return {'status': 'error', 'reason': str(e)}

    # 检测逻辑
    set_cookie_count = len(response.raw.headers.getlist('Set-Cookie'))
    comment_blocks = re.findall(r'<!--(.*?)-->', response.text, re.DOTALL)
    comment_lines = sum(len(block.split('\n')) for block in comment_blocks)

    triggers = []
    if set_cookie_count > 5:
        triggers.append(f"Set-Cookie({set_cookie_count})")
    if comment_lines > 500:
        triggers.append(f"Comments({comment_lines} lines)")

    return {
        'status': 'honeypot' if triggers else 'normal',
        'triggers': triggers,
        'url': response.url  # 获取最终URL（处理重定向）
    }

def save_results(results, filename):
    """去重保存结果"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # 自动创建目录
    seen = set()
    with open(filename, 'w') as f:
        for item in results:
            if item['url'] not in seen:
                seen.add(item['url'])
                f.write(f"{item['url']}\n")
                if item.get('triggers'):
                    f.write(f"# 触发规则: {', '.join(item['triggers'])}\n")

def main():
    parser = argparse.ArgumentParser(description='蜜罐批量检测工具')
    parser.add_argument('-i', '--input', required=True, help='URL列表文件路径')
    parser.add_argument('-t', '--threads', type=int, default=10, 
                       help='并发线程数 (默认: 10)')
    parser.add_argument('-r', '--rate', type=float, 
                       help='请求速率限制 (请求数/秒)')
    args = parser.parse_args()

    # 初始化令牌桶
    bucket = TokenBucket(args.rate) if args.rate else None

    # 加载并去重URL
    urls = load_urls_from_file(args.input)
    print(f"[*] 已加载 {len(urls)} 个去重后的URL")

    # 执行检测
    honeypots = []
    normals = []
    errors = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(detect_honeypot, url, bucket): url for url in urls}

        for i, future in enumerate(as_completed(futures), 1):
            try:
                result = future.result()
                if result['status'] == 'honeypot':
                    honeypots.append(result)
                elif result['status'] == 'normal':
                    normals.append(result)
                else:
                    errors.append(result)
                print(f"[进度 {i}/{len(urls)}] 蜜罐:{len(honeypots)} 正常:{len(normals)} 错误:{len(errors)}", end='\r')
            except Exception as e:
                errors.append({'url': futures[future], 'reason': str(e)})

    # 生成日期标识
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # 保存结果
    save_results(honeypots, os.path.join('report', 'honeypot.txt'))
    save_results(normals, os.path.join('report', f'normal-{current_date}.txt'))
    save_results(errors, os.path.join('report', 'errors.txt'))

    print("\n\n[检测报告]")
    print(f"检测日期: {current_date}")
    print(f"疑似蜜罐: {len(honeypots)} 个 (路径: report/honeypot-{current_date}.txt)")
    print(f"正常URL : {len(normals)} 个 (路径: report/normal-{current_date}.txt)")
    print(f"错误记录: {len(errors)} 个 (路径: report/errors-{current_date}.txt)")

if __name__ == "__main__":
    main()
