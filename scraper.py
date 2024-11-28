from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
import csv

# 设置 Selenium WebDriver
driver = webdriver.Chrome()

# 打开目标网站
url = "https://www.getmylottoresults.com/lotto-max-past-winning-numbers/"
driver.get(url)

# 打开 CSV 文件进行写入
with open('numbers.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # 遍历年份
    years = range(2009, 2025)  # 替换为实际年份范围
    for year in years:
        # 查找年份选择器并选择年份
        select = Select(driver.find_element(By.ID, 'yr'))  # 替换为实际的下拉菜单 ID
        select.select_by_visible_text(str(year))
        time.sleep(3)  # 等待页面加载
        
        # 获取表格内容
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        
        if not table:
            print(f"{year} 年未找到表格")
            continue
        
        # 提取表头（只在第一次写入）
        if year == years[0]:
            header = table.find_all('th')
            headers = [th.get_text(strip=True) for th in header]
            writer.writerow(headers)  # 写入表头

        # 提取数据
        rows = table.find_all('tr')
        for row in rows[1:]:  # 跳过表头
            cells = row.find_all(['td', 'th'])
            data = [cell.get_text(strip=True) for cell in cells]
            if data:  # 确保该行有数据
                writer.writerow(data)

        print(f"{year} 年的数据已保存。")

# 关闭浏览器
driver.quit()

print("所有数据已保存至 numbers.csv")
