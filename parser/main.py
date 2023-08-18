from selenium import webdriver


chromedriver = '/usr/bin/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

browser.get('https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie')

all_panels_elements = []

all_panels_elements.append(browser.find_elements_by_xpath('//*[@id="mzr-grid-content"]/div/div[2]/div/div[2]/div[1]/div/a'))
all_panels_elements.append(browser.find_elements_by_xpath('//*[@id="mzr-grid-content"]/div/div[2]/div/div[2]/div[2]/div/a'))
all_panels_elements.append(browser.find_elements_by_xpath('//*[@id="mzr-grid-content"]/div/div[2]/div/div[5]/div[1]/div/a'))
all_panels_elements.append(browser.find_elements_by_xpath('//*[@id="mzr-grid-content"]/div/div[2]/div/div[5]/div[2]/div/a'))

all_panel_hrefs = []

for panel_elements in all_panels_elements:
    for panel in panel_elements:
        all_panel_hrefs.append(panel.get_attribute('href'))

for food_href in all_panel_hrefs:
    browser.get(food_href)
    foods_table = browser.find_elements_by_xpath('//*[@id="mzr-grid-content"]/div/div[2]/div/div/table/tbody/tr') 
    for food in foods_table:
        with open('foods.txt', 'a') as f:
            f.write(f'{food.text}\n')

print('done')
browser.quit()
