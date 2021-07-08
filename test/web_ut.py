#!/usr/bin/env python3
# -*- coding:utf -8 -*-
import configparser
import os
import unittest
from time import sleep
import allure

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


@allure.feature('Test BaiDu webui')
class ISelenium(unittest.TestCase):
    def get_config(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.environ['HOME'], 'iselenium.ini'))
        return config

    def setUp(self):
        config = self.get_config()
        try:
            using_headless = os.environ['using_headless']
        except KeyError:
            using_headless = None
            print('没有配置环境变了using_headless,按照有界面运行自动化测试')

        chrome_options = Options()
        if using_headless is not None and using_headless.lower() == 'true':
            print('使用无界面方式运行')
            chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=config.get('driver', 'chrome_driver'),
                                       options=chrome_options)

    def tearDown(self):
        self.driver.quit()

    @allure.story('Test key word 王者荣耀')
    def test_search1(self):
        self._test_baidu('王者荣耀', 'test_search1')

    @allure.story('Test key word 今日头条')
    def test_search2(self):
        self._test_baidu('今日头条', 'test_search2')

    def _test_baidu(self, search_keyword, testcase_name):
        self.driver.get('https://www.baidu.com')

        sleep(5)
        assert '百度一下' in self.driver.title

        elem = self.driver.find_element_by_name('wd')
        elem.send_keys(f'{search_keyword}{Keys.RETURN}')
        print(f'搜索关键字～{search_keyword}')
        sleep(5)
        self.assertTrue(f'{search_keyword}' in self.driver.title, msg=f'{testcase_name}校验点 pass')
