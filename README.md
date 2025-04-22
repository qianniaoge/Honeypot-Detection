Honeypot Detector v2025.04
Python 3.8+
Last Updated: 2025-04-22
🔍 项目概述

工业级蜜罐检测工具，支持自动化URL去重、多线程控制及智能速率限制。基于2025年最新蜜罐特征库开发，可精准识别伪装服务。
🚀 核心功能
功能模块	技术实现
URL去重	输入文件哈希去重 + 结果文件增量校验
智能限速	令牌桶算法（支持动态速率调整）
并发控制	ThreadPoolExecutor 线程池管理
异常处理	7大类错误分类统计（含QUIC协议错误）
蜜罐识别	Cookie堆叠检测 + 注释密度分析
📦 快速开始
环境要求

# 依赖安装（2025年兼容版本）  
pip install requests>=2.32.0 urllib3>=2.0.0  

基础使用

# 基本扫描（10线程）  
python detector.py -i urls.txt  

# 生产模式（20线程 + 5请求/秒限速）  
python detector.py -i urls.txt -t 20 -r 5  

⚙️ 参数说明
参数	必需	默认值	说明
-i/--input
	✅	无	输入文件路径（UTF-8编码）
 
-t/--threads
	❌	10	并发线程数（建议≤50）
 
-r/--rate
	❌	无	请求速率限制（请求数/秒）
 
📂 输出文件
文件名	内容格式
honeypot.txt
	确认蜜罐URL（含触发规则标注）
normal.txt
	已验证安全URL
自动去重	基于响应最终URL过滤重复记录

示例输出片段：

https://example.com/honeypot  
# 触发规则: Set-Cookie(8), Comments(623 lines)  

🛠️ 检测逻辑

    网络层验证
        自动处理3xx重定向（最多30次跳转）
        302临时跳转不计入错误统计（2025 RFC 9110标准）

    蜜罐特征检测
        Cookie数量阈值：
        >5
        个Set-Cookie头
        注释密度阈值：
        >500
        行HTML注释

    错误分类

    graph TD  
      A[请求异常] --> B{错误类型}  
      B --> C[网络错误]  
      B --> D[协议错误]  
      B --> E[资源限制]  
      C --> F(连接超时/拒绝)  
      D --> G(SSL证书异常)  
      E --> H(内存溢出)  

📌 最佳实践

    动态速率调整建议

    # 示例：响应延迟超过2秒时自动降速  
    if response.elapsed.total_seconds() > 2:  
        bucket.rate *= 0.8  


📜 开源协议

MIT License - 详见 LICENSE
