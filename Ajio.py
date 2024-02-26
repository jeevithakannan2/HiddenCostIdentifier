from undetected_playwright.async_api import async_playwright


class Ajio:

    async def OTP(self, OTP):
        page = self.page
        print(page)
        while 'login' in page.url:
            if 'exceeded' in await page.content():
                return {"Error": "OTP attempt reached try again after some time"}
            await page.fill("//input[@type='tel']", OTP)
            await page.click("//input[@type='submit']")
            await page.wait_for_timeout(7500)
            if 'exceeded' in await page.content():
                return {"Error": "OTP attempt reached try again after some time"}
            print("URL:", page.url)
            if 'login' in page.url:
                return {"Message": "Wrong OTP"}
            else:
                return {"Message": "Login Success"}

    async def login(self, mobile_number):
        async with async_playwright() as p:

            browser = await p.chromium.launch_persistent_context('./user-data/', headless=True,
                                                                 viewport={'height': 1080, 'width': 1920}, locale='en-US',
                                                                 timezone_id='Asia/Kolkata', permissions=['geolocation'],
                                                                 geolocation={'longitude': 77.24524, 'latitude': 11.507280},
                                                                 color_scheme='dark',
                                                                 user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
            self.page = await browser.new_page()
            page = self.page
            await page.goto("https://ajio.com/login")

            await page.fill("//input[@type='number']", str(mobile_number), timeout=5000)
            await page.click("//input[@class='login-btn']")

            if 'Gender' in await page.content():
                return {"Error": "Not a registered mobile number"}

            url1 = page.url
            while page.url == url1:
                if 'exceeded' in await page.content():
                    return {"Error": "OTP attempt reached try again after some time"}
                await page.wait_for_timeout(2000)

            await browser.close()
            return {"Message": "User logged in"}

    async def main(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch_persistent_context('./user-data/', headless=True, viewport={'height': 1080, 'width': 1920}, locale='en-US', timezone_id='Asia/Kolkata', permissions=['geolocation'], geolocation={'longitude': 77.24524, 'latitude': 11.507280}, color_scheme='dark', user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
            page = await browser.new_page()

            await page.goto(url)
            await page.wait_for_selector("//div[@class=' guest-header']")
            head = await page.query_selector_all("//div[@class=' guest-header']/ul/li")

            if len(head) == 3:

                return {"Message": "User not logged in"}
            url1 = page.url

            await page.click("//div[@class='ic-cart ']")
            while url1 == page.url:
                await page.wait_for_timeout(500)

            if 'Your Shopping Bag is Empty!!' in await page.content():
                return {"Message": "Add items to cart"}

            txt = await page.inner_text("//div[@id='orderSummary']")
            lines = txt.split('\n')
            lines.pop(0)
            lines.pop(4)
            lines.pop(4)
            if 'Free' in lines[5]:
                lines.pop(6)
            if 'Free' in lines[7]:
                lines.pop(8)

            result = {}

            for i in range(0, len(lines), 2):
                key = lines[i]
                value = lines[i+1]
                result[key] = value

            print(result)
            await browser.close()
            return result
