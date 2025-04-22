# Honeypot Batch Detection Script / 蜜罐批量检测脚本

**English** | [中文](#中文)

A Python tool for batch detection of honeypot URLs, identifying potential honeypots based on specific triggers and saving categorized results. / 基于Python的蜜罐URL批量检测工具，根据触发规则识别蜜罐并分类保存结果。

## Features / 功能
- **URL Deduplication**: Removes duplicate URLs from input. / **URL去重**：去除输入列表中的重复URL。
- **Adjustable Concurrency**: Configurable thread count (default: 10). / **可调并发**：可配置线程数（默认：10）。
- **Rate Control**: Optional request rate limit via token bucket. / **速率控制**：通过令牌桶限制请求速率。
- **Categorized Output**: Deduplicated results saved to `honeypot.txt` and `normal.txt`. / **分类输出**：去重结果保存至`honeypot.txt`和`normal.txt`。
- **Honeypot Detection**: Flags honeypots based on >5 `Set-Cookie` headers or >500 comment lines. / **蜜罐检测**：基于超过5个`Set-Cookie`头或500行注释标记蜜罐。

## Requirements / 依赖
- Python 3.6+
- Package: `requests`
  ```bash
  pip install requests

Installation / 安装
Clone the repository / 克隆仓库:
bash

git clone https://github.com/<your-username>/honeypot-detector.git
cd honeypot-detector

Install dependencies / 安装依赖:
bash

pip install -r requirements.txt

Usage / 使用方法
Run with command-line arguments / 使用命令行参数运行:
bash

python honeypot_detector.py -i <input_file> [-t <threads>] [-r <rate>]

Arguments / 参数
-i, --input (required): File path with URLs (one per line). / 输入文件路径（每行一个URL）。

-t, --threads (optional): Concurrent threads (default: 10). / 并发线程数（默认：10）。

-r, --rate (optional): Requests per second (e.g., 2.5). / 每秒请求数（例如2.5）。

Example / 示例
bash

python honeypot_detector.py -i urls.txt -t 20 -r 5

Processes urls.txt with 20 threads and 5 requests/second. / 使用20线程和每秒5次请求处理urls.txt。
Input Format / 输入格式
Text file with one URL per line / 每行一个URL的文本文件:

http://example.com
https://test.com
http://suspicious-site.com

Output / 输出
honeypot.txt: Suspected honeypots with trigger details. / 疑似蜜罐及其触发规则。

normal.txt: Normal URLs. / 正常URL。

Console Summary: Counts of honeypots, normal URLs, and errors. / 控制台统计：蜜罐、正常URL和错误数量。

Example honeypot.txt:

http://suspicious-site.com
# Triggers / 触发规则: Set-Cookie(6), Comments(600 lines)

Detection Logic / 检测逻辑
A URL is flagged as a honeypot if: / URL满足以下条件被标记为蜜罐：
5 Set-Cookie headers in response. / 响应含超过5个Set-Cookie头。

HTML comments exceed 500 lines. / HTML注释超过500行。

Notes / 注意事项
SSL warnings disabled (verify=False); use cautiously in production. / 禁用SSL警告（verify=False），生产环境需谨慎。

Errors (e.g., timeouts) logged to console only. / 错误（例如超时）仅记录到控制台。

Ensure resources for high thread counts or rates. / 高线程或速率需确保资源充足。

Contributing / 贡献
Submit pull requests or issues for bugs/features. / 欢迎提交拉取请求或问题报告。
License / 许可证
MIT License. See LICENSE. / MIT许可证，详见LICENSE。
Disclaimer / 免责声明
For research/education only. Comply with laws and terms of service. / 仅限研究/教育用途，遵守法律和服务条款。
中文
简介
一个Python工具，用于批量检测蜜罐URL，根据特定规则识别潜在蜜罐并将结果分类保存。
功能
URL去重：自动去除输入中的重复URL。

可调并发：支持配置线程数（默认：10）。

速率控制：通过令牌桶算法限制请求速率。

分类输出：去重结果保存至honeypot.txt（疑似蜜罐）和normal.txt（正常URL）。

蜜罐检测：基于超过5个Set-Cookie头或500行注释标记蜜罐。

依赖
Python 3.6+

所需包：
bash

pip install requests

安装
克隆仓库：
bash

git clone https://github.com/<your-username>/honeypot-detector.git
cd honeypot-detector

安装依赖：
bash

pip install -r requirements.txt

使用方法
使用命令行参数运行：
bash

python honeypot_detector.py -i <输入文件> [-t <线程数>] [-r <速率>]

参数
-i, --input（必需）：URL列表文件（每行一个URL）。

-t, --threads（可选）：并发线程数（默认：10）。

-r, --rate（可选）：每秒请求数（例如2.5）。

示例
bash

python honeypot_detector.py -i urls.txt -t 20 -r 5

以20线程和每秒5次请求处理urls.txt。
输入格式
每行一个URL的文本文件：

http://example.com
https://test.com
http://suspicious-site.com

输出
honeypot.txt：疑似蜜罐URL及其触发规则。

normal.txt：正常URL。

控制台统计：蜜罐、正常URL和错误的计数。

示例honeypot.txt：

http://suspicious-site.com
# 触发规则: Set-Cookie(6), Comments(600 lines)

检测逻辑
URL满足以下条件被标记为蜜罐：
响应含超过5个Set-Cookie头。

HTML注释超过500行。

注意事项
禁用SSL警告（verify=False），生产环境谨慎使用。

错误（例如超时）仅记录到控制台。

高线程或速率需确保资源充足。

###A 贡献
欢迎提交拉取请求或问题报告错误/新功能。
许可证
MIT许可证，详见LICENSE。
免责声明
仅限研究/教育用途，遵守相关法律和服务条款。

