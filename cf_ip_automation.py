import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime, timezone, timedelta

class CFIPAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.setup_driver()
    
    def setup_driver(self):
        """设置Chrome浏览器驱动"""
        print(f"当前环境: GITHUB_ACTIONS={os.getenv('GITHUB_ACTIONS')}")
        
        if os.getenv('GITHUB_ACTIONS'):
            print("检测到GitHub Actions环境，初始化Chrome...")
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.7390.107 Safari/537.36')
            
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                self.wait = WebDriverWait(self.driver, 20)
                print("Chrome浏览器驱动初始化成功")
            except Exception as e:
                print(f"Chrome初始化失败: {e}")
                self.driver = None
                self.wait = None
        else:
            self.driver = None
            self.wait = None
            print("本地环境，跳过Chrome初始化")
    
    def get_utc_minus_8_time(self):
        """获取UTC-8时间"""
        utc_time = datetime.now(timezone.utc)
        utc_minus_8 = utc_time - timedelta(hours=8)
        return utc_minus_8.strftime('%Y-%m-%d %H:%M:%S UTC-8')
    
    def open_website(self):
        """打开优选IP网站"""
        if not self.driver:
            print("本地环境，跳过网站访问")
            return True
        
        print("正在打开优选IP网站...")
        self.driver.get('https://t1.y130.icu/t1/bestip')
        time.sleep(5)
        print("网站加载完成")
        return True
    
    def select_cf_official(self):
        """选择CF官方列表"""
        if not self.driver:
            print("本地环境，跳过CF官方列表选择")
            return True
        
        print("正在选择CF官方列表...")
        
        try:
            # 根据实际HTML结构，使用id选择器
            ip_select = self.driver.find_element(By.ID, "ip-source-select")
            
            # 检查当前选中的值
            current_value = ip_select.get_attribute('value')
            print(f"当前IP库选择: {current_value}")
            
            if current_value == 'official':
                print("CF官方列表已选中")
                return True
            else:
                # 选择CF官方列表
                from selenium.webdriver.support.ui import Select
                select = Select(ip_select)
                select.select_by_value('official')
                print("已选择CF官方列表")
                return True
                
        except Exception as e:
            print(f"CF官方列表选择失败: {e}")
            return False
    
    def select_port_443(self):
        """选择443端口"""
        if not self.driver:
            print("本地环境，跳过端口选择")
            return True
        
        print("正在选择443端口...")
        
        try:
            # 根据实际HTML结构，使用id选择器
            port_select = self.driver.find_element(By.ID, "port-select")
            
            # 检查当前选中的值
            current_value = port_select.get_attribute('value')
            print(f"当前端口选择: {current_value}")
            
            if current_value == '443':
                print("443端口已选中")
                return True
            else:
                # 选择443端口
                from selenium.webdriver.support.ui import Select
                select = Select(port_select)
                select.select_by_value('443')
                print("已选择443端口")
                return True
                
        except Exception as e:
            print(f"443端口选择失败: {e}")
            return False
    
    def start_test(self):
        """开始延迟测试"""
        if not self.driver:
            print("本地环境，跳过延迟测试")
            return True
        
        print("正在开始延迟测试...")
        
        try:
            # 根据实际HTML结构，使用id选择器
            start_button = self.driver.find_element(By.ID, "test-btn")
            start_button.click()
            print("延迟测试已开始")
            return True
            
        except Exception as e:
            print(f"开始测试失败: {e}")
            return False
    
    def wait_for_test_completion(self):
        """等待测试完成，先等待350秒，然后每30秒检查一次"""
        if not self.driver:
            print("本地环境，跳过测试等待")
            return True
        
        print("等待测试完成...")
        
        # 先等待350秒让测试充分进行
        print("测试需要时间，先等待350秒...")
        time.sleep(350)
        print("350秒等待完成，开始检查测试结果...")
        
        max_wait_time = 300  # 再等待最多5分钟
        check_interval = 30  # 每30秒检查一次
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            try:
                # 检查IP列表内容
                ip_list_element = self.driver.find_element(By.ID, "ip-list")
                ip_text = ip_list_element.text
                
                print(f"当前IP列表内容: {ip_text[:200]}...")
                
                # 检查是否还在加载中
                if '正在加载IP列表，请稍候' in ip_text or '请选择端口和IP库' in ip_text:
                    print(f"测试仍在进行中... 已检查 {elapsed_time} 秒")
                    time.sleep(check_interval)
                    elapsed_time += check_interval
                    continue
                
                # 检查是否有实际的IP内容（包含端口和延迟信息）
                if ip_text and len(ip_text.strip()) > 0 and (':' in ip_text or 'ms' in ip_text):
                    print("IP列表已加载完成！")
                    return True
                
                print(f"等待IP列表加载... 已检查 {elapsed_time} 秒")
                time.sleep(check_interval)
                elapsed_time += check_interval
                
            except Exception as e:
                print(f"检查测试状态时出错: {e}")
                time.sleep(check_interval)
                elapsed_time += check_interval
        
        print("测试等待超时")
        return False
    
    def get_test_results(self):
        """获取测试结果"""
        if not self.driver:
            print("本地环境，无法获取真实测试结果")
            return None
        
        print("正在获取测试结果...")
        
        try:
            # 获取统计信息
            stats_info = self.get_stats_info()
            
            # 获取测试进度
            progress_info = self.get_progress_info()
            
            # 获取IP列表
            ip_list = self.get_ip_list()
            
            if not ip_list:
                print("获取IP列表失败")
                return None
            
            results = {
                'stats': stats_info,
                'progress': progress_info,
                'ips': ip_list
            }
            
            print(f"获取到 {len(ip_list)} 个IP结果")
            return results
            
        except Exception as e:
            print(f"获取测试结果失败: {e}")
            return None
    
    def get_stats_info(self):
        """获取统计信息"""
        try:
            # 查找统计信息区域
            stats_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '统计信息') or contains(text(), '获取到的IP总数') or contains(text(), '您的国家')]")
            if stats_elements:
                return stats_elements[0].text.strip()
            return "统计信息获取失败"
        except:
            return "统计信息获取失败"
    
    def get_progress_info(self):
        """获取测试进度"""
        try:
            # 查找测试进度区域，尝试多种选择器
            selectors = [
                "//*[contains(text(), '测试进度')]",
                "//*[contains(text(), '完成')]",
                "//*[contains(text(), '有效IP')]",
                "//div[contains(@class, 'stats')]//*[contains(text(), '测试')]"
            ]
            
            for selector in selectors:
                try:
                    progress_elements = self.driver.find_elements(By.XPATH, selector)
                    if progress_elements:
                        progress_text = progress_elements[0].text.strip()
                        if progress_text and len(progress_text) > 5:  # 确保不是空文本
                            print(f"获取到的测试进度: {progress_text}")
                            return progress_text
                except:
                    continue
            
            return "测试进度获取失败"
        except Exception as e:
            print(f"获取测试进度失败: {e}")
            return "测试进度获取失败"
    
    def get_ip_list(self):
        """获取IP列表"""
        try:
            # 根据实际HTML结构，使用id选择器
            ip_list_element = self.driver.find_element(By.ID, "ip-list")
            
            ip_list_text = ip_list_element.text
            print(f"IP列表原始文本: {ip_list_text}")
            
            # 检查是否还是提示文本
            if '请选择端口和IP库' in ip_list_text:
                print("IP列表尚未加载")
                return []
            
            # 直接返回原始文本，不做任何处理
            return [ip_list_text]
            
        except Exception as e:
            print(f"获取IP列表失败: {e}")
            return []
    
    def save_results_to_file(self, results):
        """保存结果到文件"""
        if not results:
            print("没有结果可保存")
            return False
        
        with open('ip.txt', 'a', encoding='utf-8') as f:
            # 使用UTC-8时间
            utc_minus_8_time = self.get_utc_minus_8_time()
            f.write(f"\n# CF官方列表优选IP - {utc_minus_8_time}\n")
            f.write(f"# 统计信息: {results.get('stats', '获取失败')}\n")
            f.write(f"# 测试进度: {results.get('progress', '获取失败')}\n")
            f.write(f"# {'='*50}\n")
            
            # 直接保存网站原始输出，不做任何处理
            ip_text = results.get('ips', [''])[0]
            f.write(ip_text)
        
        print(f"结果已保存到 ip.txt 文件")
        return True
    
    def run_automation(self):
        """运行完整的自动化流程"""
        try:
            print("开始CloudFlare IP优选自动化流程...")
            
            # 1. 打开网站
            if not self.open_website():
                return False
            
            # 2. 检查CF官方列表
            if not self.select_cf_official():
                return False
            
            # 3. 选择443端口
            if not self.select_port_443():
                return False
            
            # 4. 开始测试
            if not self.start_test():
                return False
            
            # 5. 等待测试完成
            if not self.wait_for_test_completion():
                return False
            
            # 6. 获取结果
            results = self.get_test_results()
            if not results:
                return False
            
            # 7. 保存到文件
            if not self.save_results_to_file(results):
                return False
            
            print("自动化流程完成")
            return True
            
        except Exception as e:
            print(f"自动化流程执行出错: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                print("浏览器已关闭")

def main():
    """主函数"""
    print("CloudFlare IP优选自动化工具")
    print("=" * 50)
    
    automation = CFIPAutomation()
    success = automation.run_automation()
    
    if success:
        print("自动化执行成功")
    else:
        print("自动化执行失败")

if __name__ == "__main__":
    main()
