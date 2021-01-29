from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import unittest, time, re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


class Amazon(unittest.TestCase):
    @classmethod
    def setUp(cls):
        req_proxy = RequestProxy()  # you may get different number of proxy when  you run this at each time
        proxies = req_proxy.get_proxy_list()  # this will create proxy list
        PROXY = proxies[0].get_address()
        print(proxies[0].country)
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,

            "proxyType": "MANUAL",

        }
        cls.driver = webdriver.Chrome(ChromeDriverManager().install())
        cls.driver.get('http://amazon.com')
        cls.driver.implicitly_wait(30)
        cls.driver.maximize_window()

    def test_amazon(self):
        self.driver.find_element_by_xpath("//input[@id='twotabsearchtextbox']").send_keys("data catalog")
        self.driver.find_element_by_xpath("//input[@id='twotabsearchtextbox']").submit()
        self.driver.implicitly_wait(5)
        elements = self.driver.find_elements_by_xpath('//div[contains(@class,"a-row a-size-base a-color-base")]')
        price = elements[0].find_elements_by_xpath('//span[contains(@class,"a-price-whole")]')
        price_text = price[0].text
        print("Hard Cover Price = ", price_text)
    @classmethod
    def tearDown(cls):
        # Close the browser
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
