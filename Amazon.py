from amazoncaptcha import AmazonCaptcha
from undetected_playwright.async_api import async_playwright


class Amazon:

    def __init__(self):
        self.page = None

    async def solve_captcha(self):
        page = self.page
        foo = page.locator('/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img')
        link = await foo.get_attribute('src')
        solution = AmazonCaptcha.fromlink(link).solve()
        await page.fill('//*[@id="captchacharacters"]', solution)
        await page.click('//button[text()="Continue shopping"]')
        return

    async def main(self, url: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch_persistent_context('./user-data/', headless=True,
                                                                 viewport={'height': 1080, 'width': 1920},
                                                                 locale='en-US',
                                                                 timezone_id='Asia/Kolkata',
                                                                 permissions=['geolocation'],
                                                                 geolocation={'longitude': 77.24524,
                                                                              'latitude': 11.507280},
                                                                 color_scheme='dark',
                                                                 user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
            self.page = await browser.new_page()
            page = self.page
            await page.goto(url)

            if 'captcha' in await page.content():
                await self.solve_captcha()

            await page.wait_for_selector("//input[@id='buy-now-button']")
            await page.click("//input[@id='buy-now-button']")
            if 'captcha' in await page.content():
                await self.solve_captcha()

            count = 0
            while url == page.url:
                await page.wait_for_timeout(500)
                count += 1
                if count > 60:
                    return {"Error": "Time out"}
            await page.wait_for_timeout(500)
            if 'New to Amazon?' in await page.content():
                await page.fill("//input[@type='email']", '9894789409')

                await page.click("//input[@id='continue']")

                await page.fill("//input[@type='password']", 'jeeva2005')

                await page.click("//input[@id='signInSubmit']")
                # await page.wait_for_selector("//div[@aria-label='Other UPI Apps']")
                await page.wait_for_timeout(5000)

            if 'Choose special delivery options' in await page.content():
                await page.click("//input[@aria-labelledby='a-autoid-2-announce']")
                while 'section-overwrap' in await page.content():
                    await page.wait_for_timeout(500)

            await page.click("//*[@data-action='a-dropdown-button']")
            ban = await page.query_selector_all("//ul[@role='listbox']/li")
            for bank in ban:
                b = await bank.query_selector("a")
                await page.wait_for_timeout(500)
                if b is None:
                    continue
                else:
                    await b.click()
                await page.wait_for_timeout(500)

                foo = await page.content()
                count = foo.count('not available due to technical issue')
                if count == 2:
                    await page.click("//*[@data-action='a-dropdown-button']")
                else:
                    break

            await page.click("//input[@name='ppw-widgetEvent:SetPaymentPlanSelectContinueEvent']")
            while 'section-overwrap' in await page.content():
                await page.wait_for_timeout(500)

            if 'get unlimited access' in await page.content():
                try:
                    await page.wait_for_selector("//*[@id='prime-interstitial-nothanks-button']", state='visible',
                                                 timeout=8000)
                    await page.wait_for_timeout(500)
                    # await page.evaluate('document.querySelector("#prime-interstitial-nothanks-button").click()')
                    await page.click("//*[@id='prime-interstitial-nothanks-button']")
                except:
                    pass
            while 'section-overwrap' in await page.content():
                await page.wait_for_timeout(500)

            await page.wait_for_selector("//span[@id='subtotals-marketplace-spp-bottom']", timeout=45000)

            data = {}
            rows = await page.query_selector_all("//*[@id='subtotals-marketplace-table']/tbody/tr")
            for row in rows:
                cells = await row.query_selector_all("td")

                if len(cells) == 2:
                    key = await cells[0].inner_text()
                    key.replace('\n', '', ).strip()

                    value = await cells[1].inner_text()
                    value.replace('\n', '').strip()

                    data[key] = value

            await browser.close()
            return data
