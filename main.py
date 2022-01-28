import asyncio
import base64
import random

import ddddocr

from browser import MyBrowser
from track import Track


class Config:
    # 手机号输入框
    phone_input = '//*[@id="app"]/div/div[3]/p[1]/input'
    # 验证码输入框
    code_input = '//*[@id="authcode"]'
    # 同意协议
    policy_checkbox = '//*[@id="app"]/div/p[2]/input'
    # 获取手机验证码
    get_msg_btn = '//*[@id="app"]/div/div[3]/p[2]/button'
    # 登录
    login_btn = '//*[@id="app"]/div/a'
    # 人机识别验证码
    captcha_div = '//*[@id="captcha_modal"]'
    # 缺口
    target_img = '//*[@id="small_img"]'
    # 背景
    background_img = '//*[@id="cpc_img"]'
    # 滑块按钮
    slider_img = '//*[@id="captcha_modal"]/div/div[3]/div/img'
    # 验证结果
    error_p = '//*[@id="captcha_modal"]/div/div[2]/div[1]/div/p'


async def slider_validation(page):
    det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    target_b64 = await page.get_attribute(Config.target_img, 'src')
    background_b64 = await page.get_attribute(Config.background_img, 'src')
    target_bytes = base64.b64decode(target_b64.split(',')[1])
    background_bytes = base64.b64decode(background_b64.split(',')[1])
    res = det.slide_match(target_bytes, background_bytes)
    x = res.get('target')[0]
    x = x / 275 * 302
    tracks = Track().get_tracks1(x, random.randint(2, 4))
    slider = await page.wait_for_selector(Config.slider_img)
    slider_box = await slider.bounding_box()
    mouse_x = slider_box['x'] + slider_box['width'] / random.uniform(1.5, 2.5)
    mouse_y = slider_box['y'] + slider_box['height'] / random.uniform(1.5, 2.5)
    await page.mouse.move(mouse_x, mouse_y)
    await page.mouse.down()
    await page.wait_for_timeout(random.randint(15, 55))
    start_x = mouse_x
    for i in tracks:
        start_x += i
        await page.mouse.move(start_x, mouse_y, steps=1)
    await page.wait_for_timeout(random.randint(900, 1500))
    await page.mouse.up()
    await page.wait_for_timeout(random.randint(800, 1000))
    error = await page.text_content(Config.error_p)
    print('人机验证结果: {}'.format(error))
    if error == "验证成功":
        return True
    else:
        return False


async def run():
    my_browser = MyBrowser()
    context = await my_browser.new_context(False)
    page = await my_browser.new_page(context)
    print('初始化浏览器页面完成')
    await page.goto("https://wq.jd.com/passport/Login?returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&")
    phone = input('请输入要登陆的手机号: ')
    await page.fill(Config.phone_input, phone)
    await page.click(Config.policy_checkbox)
    await page.click(Config.get_msg_btn)
    try:
        await page.wait_for_selector(Config.captcha_div)
    except Exception as e:
        print(e)
    slider_type = False
    if await page.is_visible(Config.captcha_div):
        for i in range(5):
            print('正在进行第{}次人机验证'.format(i + 1))
            slider_type = await slider_validation(page)
            if slider_type:
                break
    if slider_type:
        code = input('请输入获取到的验证码: ')
        await page.fill(Config.code_input, code)
        await page.click(Config.login_btn)
    if "home.m.jd.com" in page.url:
        print('登陆成功,进入首页')
        await page.wait_for_timeout(5000)
        cookie = ''
        storage = await context.storage_state()
        for temp in storage['cookies']:
            if temp.get('name') == 'pt_key' or temp.get('name') == 'pt_pin':
                cookie += '{}={};'.format(temp.get('name'), temp.get('value'))
        print(cookie)
    await my_browser.close()


asyncio.run(run())
