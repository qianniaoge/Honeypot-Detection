# Honeypot Batch Detection Script / 蜜罐批量检测脚本

**English** | [中文](#中文)

A Python-based tool for batch detection of honeypot URLs. It processes a list of URLs, identifies potential honeypots based on specific triggers, and saves categorized results. / 一个基于Python的蜜罐URL批量检测工具。它处理URL列表，根据特定触发规则识别潜在蜜罐，并将结果分类保存。

## Features / 功能
- **URL Deduplication**: Automatically removes duplicate URLs from the input list. / **URL去重**：自动去除输入列表中的重复URL。
- **Configurable Concurrency**: Adjustable thread count for parallel processing (default: 10). / **可配置并发**：可调整线程数以进行并行处理（默认：10线程）。
- **Rate Limiting**: Optional request rate control using a token bucket algorithm. / **速率限制**：使用令牌桶算法可选控制请求速率。
- **Result Categorization**: Saves deduplicated results to `honeypot.txt` (suspected honeypots) and `normal.txt` (normal URLs). / **结果分类**：将去重后的结果保存至`honeypot.txt`（疑似蜜罐）和`normal.txt`（正常URL）。
- **Honeypot Detection**: Flags honeypots based on excessive `Set-Cookie` headers (>5) or large comment blocks (>500 lines). / **蜜罐检测**：根据过多`Set-Cookie`头（>5）或大段注释块（>500行）标记蜜罐。

## Requirements / 依赖
- Python 3.6+
- Required package: `requests`
  ```bash
  pip install requests
