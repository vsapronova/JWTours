from selenium import webdriver

def get_month_days(days_divs):
    days_divs_text = [day.text for day in days_divs]

    start = days_divs_text.index('1')
    end = len(days_divs_text)
    if '1' in days_divs_text[start + 1:]:
        sublist = days_divs_text[start + 1:]
        end = sublist.index('1') + start + 1

    month_days = days_divs[start:end]
    return month_days


class JWBookSite:
    def __init__(self):
        driver = webdriver.Chrome('/Users/victoria/Downloads/chromedriver')
        driver.implicitly_wait(30)
        driver.get('https://www.peek.com/s/9d74ebc1-e4fa-48de-917b-797d62c0ac27/rddM')
        frame = driver.find_element_by_id('_pbf_1')
        driver.switch_to.frame(frame)
        self.driver = driver

    def next_month(self):
        div = self.driver.find_element_by_class_name('right-arrow-wrap')
        a = div.find_element_by_css_selector('a')
        a.click()

    def current_month_dates(self):
        self.driver.find_element_by_class_name('availability-tile')

        month_divs = self.driver.find_elements_by_css_selector('div.month')
        month_div = month_divs[0]
        month_name = month_divs[0].find_element_by_class_name('month-title').text
        days_divs = month_div.find_elements_by_css_selector('div.day')
        month_days = get_month_days(days_divs)

        dates = []
        for day in month_days:
            cal_day = day.find_element_by_css_selector('div.calendar-day')
            class_attr = cal_day.get_attribute('class')
            if 'has-availability' in class_attr:
                dates.append(int(day.text))
        return (month_name, dates)


if __name__ == '__main__':
    site = JWBookSite()
    avail_dates = site.current_month_dates()
    print(avail_dates)
    site.next_month()
    avail_dates = site.current_month_dates()
    print(avail_dates)




