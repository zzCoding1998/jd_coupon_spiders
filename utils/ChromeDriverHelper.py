import logging

from selenium import webdriver


class ChromeDriverHelper:

    @staticmethod
    def get_driver(proxy=None):
        options = webdriver.ChromeOptions()
        # 添加UA
        options.add_argument(
            'user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
        # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument('--disable-gpu')
        # # 不加载图片, 提升速度
        options.add_argument('blink-settings=imagesEnabled=false')
        # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        options.add_argument('--headless')
        # 以最高权限运行
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # 禁用JavaScript
        options.add_argument("--disable-javascript")
        # 设置开发者模式启动，该模式下webdriver属性为正常值
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 禁用浏览器弹窗
        prefs = {
            'profile.default_content_setting_values': {
                'notifications': 2
            }
        }
        options.add_experimental_option('prefs', prefs)

        if proxy is not None:
            ### 别问，问就是我不理解
            logging.getLogger(__name__).warning("init chrome driver, current proxy: " + proxy)
            proxy = proxy.replace(':','：')
            options.add_argument(f'-proxy-server=http://{proxy}')

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(10)

        return driver
