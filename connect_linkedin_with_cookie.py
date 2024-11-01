# -*- coding: utf-8 -*-
"""Connect Linkedin with cookie

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iQ4deYGPUZA4_5U5bx3zIP3_JpD4ynGf

# **CÀI ĐẶT THƯ VIỆN CẦN THIẾT**
"""

pip install selenium
apt-get update
apt install chromium-chromedriver
pip install --upgrade selenium
pip install pandas
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client



import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from IPython.display import Image, display
# import pickle
# from PIL import Image

"""# **HÀM HỖ TRỢ**"""

# # def display_screenshot(driver: webdriver.Chrome, file_name: str = 'screenshot.png'):
# #     driver.save_screenshot(file_name)
# #     time.sleep(5)
# #     display(Image(filename=file_name))
# def display_full_screenshot(driver):
#     # Lấy chiều cao của trang (toàn bộ nội dung)
#     total_height = driver.execute_script("return document.body.scrollHeight")

#     # Điều chỉnh chiều cao của cửa sổ trình duyệt để khớp với chiều cao của trang
#     driver.set_window_size(1920, total_height)  # Đặt chiều rộng và chiều cao mong muốn

#     # Chụp ảnh màn hình
#     driver.save_screenshot('screenshot.png')

#     # Hiển thị ảnh chụp màn hình
#     time.sleep(2)  # Đợi ảnh được lưu
#     display(Image.open('screenshot.png'))

"""# **KẾT NỐI GOOGLE SHEETS**"""

import pickle
import pandas as pd
from google.colab import auth
from google.auth import default
from googleapiclient.discovery import build
import requests

# SPREADSHEET ID.
SPREADSHEET_ID = '1y0G7Oet-dqWvpwNZZTe3Y1thtF9ytAkOTcZp0XsZx-k'
# RANGE.
RANGE_NAME = 'Sheet1!A:D'
# API KEY của bạn
API_KEY = 'AIzaSyBddezm5YRnsrsuF5CzbMgwCap05roO4B4'

# URL API với API Key
url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{RANGE_NAME}?key={API_KEY}"

# Gửi yêu cầu GET để lấy dữ liệu
response = requests.get(url)
data = response.json()

# Xử lý dữ liệu nếu có
values = data.get('values', [])

# Đảm bảo tất cả các hàng có số cột bằng nhau
max_cols = max(len(row) for row in values)
values = [row + [''] * (max_cols - len(row)) for row in values]

# Chuyển thành DataFrame
df = pd.DataFrame(values[1:], columns=values[0])
df = df.fillna('')  # Thay thế các giá trị NaN bằng chuỗi rỗng

print(df)

"""# **HIỂN THỊ KẾT QUẢ GOOGLE SHEETS**"""

df.head()

"""# **CẤU HÌNH DRIVER**"""

options = webdriver.ChromeOptions()

options.add_argument('--no-sandbox')
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--window-size=1920, 1200")
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

"""# **HÀM ĐĂNG NHẬP**"""

COOKIES_FILE = 'linkedin_cookies.pkl'
CREDENTIALS_FILE = 'linkedin_credentials.pkl'

def login_with_cookies(driver):
    """Đăng nhập sử dụng cookies nếu có"""
    driver.get("https://www.linkedin.com")

    # Kiểm tra nếu cookies tồn tại
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, "rb") as cookies_file:
            cookies = pickle.load(cookies_file)

        for cookie in cookies:
            driver.add_cookie(cookie)

        # Sau khi thêm cookies, làm mới trang để áp dụng
        driver.refresh()
        time.sleep(3)
        return True  # Đăng nhập thành công bằng cookies
    return False

def save_cookies(driver):
    """Lưu cookies vào file"""
    with open(COOKIES_FILE, "wb") as cookies_file:
        pickle.dump(driver.get_cookies(), cookies_file)
    print("INFO: COOKIES SAVED!")

def load_cookies(driver: webdriver.Chrome, file_name: str):
    """Đọc cookies từ file pickle và thêm vào browser"""
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)

def load_credentials():
    """Tải thông tin đăng nhập từ file"""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "rb") as f:
            return pickle.load(f)
    return None

def save_credentials(username, password):
    """Lưu thông tin đăng nhập vào file"""
    with open(CREDENTIALS_FILE, "wb") as f:
        pickle.dump({"username": username, "password": password}, f)

def handle_cookie_acceptance(driver: webdriver.Chrome):
    """Xử lý chấp nhận cookies nếu có"""
    try:
        driver.find_element(By.XPATH, "//button[span[text()='Accept']]").click()
        print("INFO: COOKIES IS ACCEPTED!")
    except:
        print("INFO: COOKIES IS NOT REQUIRED!")

def handle_code_verification(driver: webdriver.Chrome):
    """Xử lý yêu cầu nhập mã xác thực nếu có"""
    try:
        # Tìm trường nhập mã xác thực
        ID_FIELD = "input__email_verification_pin"
        CONDITION = EC.presence_of_element_located((By.ID, ID_FIELD))
        verification_field = WebDriverWait(driver, 20).until(CONDITION)

        # Tìm nút submit
        ID_FIELD = "email-pin-submit-button"
        CONDITION = EC.presence_of_element_located((By.ID, ID_FIELD))
        submit_button = WebDriverWait(driver, 20).until(CONDITION)

        # Nhập mã xác thực
        code = input("Verification code required! Check your email and enter the code: ")
        verification_field.send_keys(code)
        time.sleep(1)
        submit_button.click()
        time.sleep(2)
    except:
        print("INFO: NO VERIFICATION DETECTED!")

def login(driver: webdriver.Chrome, username: str, password: str):
    """Đăng nhập vào LinkedIn với username và password mới nếu có sự thay đổi"""
    XPATH_USERNAME = '//*[@id="username"]'
    XPATH_PASSWORD = '//*[@id="password"]'
    XPATH_LOGIN_BUTTON = '//button[contains(@class, "btn__primary--large") and @aria-label="Sign in"]'

    driver.get("https://www.linkedin.com/login")
    time.sleep(2)  # Ensure the page is fully loaded

    # Kiểm tra nếu có cookies và kiểm tra xem username, password có thay đổi không
    credentials = load_credentials()

    if os.path.exists(COOKIES_FILE) and credentials:
        # Kiểm tra nếu username hoặc password đã thay đổi
        if credentials['username'] == username and credentials['password'] == password:
            # Tải cookies và thử đăng nhập
            load_cookies(driver, COOKIES_FILE)
            driver.get("https://www.linkedin.com/feed")
            time.sleep(3)

            # Kiểm tra xem đã đăng nhập chưa bằng cách xem có biểu tượng người dùng không
            try:
                user_icon = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'global-nav__me-photo')))
                print("INFO: Logged in using cookies!")
                # display_screenshot(driver, "status.png")
                return
            except:
                print("INFO: Cookies không hợp lệ, thử đăng nhập lại...")

    # Nếu thông tin đăng nhập đã thay đổi hoặc không có cookies, đăng nhập thủ công
    driver.get("https://www.linkedin.com/login")
    username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, XPATH_USERNAME)))
    password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, XPATH_PASSWORD)))
    login_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, XPATH_LOGIN_BUTTON)))

    username_field.send_keys(username)
    time.sleep(2)
    password_field.send_keys(password)
    time.sleep(2)
    login_button.click()

    time.sleep(5)

    # Lưu cookies và thông tin đăng nhập sau khi đăng nhập thành công
    save_cookies(driver)
    save_credentials(username, password)
    print("INFO: Đăng nhập thành công và đã lưu cookies, thông tin đăng nhập!")
    # display_screenshot(driver, "status.png")
    # display_full_screenshot(driver)

"""# **THỰC HIỆN ĐĂNG NHẬP**"""

# username = "henry.phd@ah-globalgroup.com"
# password = "Henry@2023CA"

username ="Henry.Universes@TAHKfoundation.org"
password = "2024@ThanhddxHenry"

login(driver, username, password)

#display_screenshot(driver)

"""# **XPATH**"""

# XPATH ỨNG VỚI NÚT CONNECT.
STATUS_CONNECT = "/html/body/div/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button[1]"

# XPATH ỨNG VỚI NÚT MESSAGE.
#STATUS_MESSAGE = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[1]/button"
STATUS_MESSAGE = "/html/body/div/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[1]/button"
# XPATH ỨNG VỚI NÚT MORE.
#BUTTON_MORE = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button"
BUTTON_MORE = "/html/body/div/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button"

# XPATH ỨNG VỚI NÚT CONNECT KHI NHẤN NÚT MORE.
MORE_UNCONNECT = "/html/body/div/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[3]/div"
# XPATH ỨNG VỚI NÚT UNCONNECT KHI NHẤN NÚT MORE.
MORE_CONNECT = "/html/body/div/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[3]/div"
# XPATH ỨNG VỚI NÚT ADD A NOTE.
BUTTON_ADD_NOTE = "/html/body/div[3]/div/div/div[3]/button[1]"
# XPATH ỨNG VỚI KHUNG NHẬP NOTE.
TEXTAREA_NOTE = [
    "/html/body/div[3]/div/div/div[3]/div[1]/textarea",         # NORMAL ACCOUNT.
    "/html/body/div[3]/div/div/div[2]/div[2]/div[1]/textarea"   # PR EMIUM ACCOUNT.
]
# XPATH ỨNG VỚI NÚT GỬI NOTE.
BUTTON_SEND_NOTE = [
    "/html/body/div[3]/div/div/div[4]/button[2]",               # NORMAL ACCOUNT.
    "/html/body/div[3]/div/div/div[3]/button[3]"                # PREMIUM ACCOUNT.
]
# XPATH ỨNG VỚI NÚT GỬI CONNECT MÀ KHÔNG DÙNG NOTE.
BUTTON_SEND_WITHOUT_NOTE = "/html/body/div[4]/div/div/div[3]/button[2]"
# XPATH ỨNG VỚI NÚT GỬI CONNECT MÀ DÙNG NOTE.
TEXTFIELD_VERIFY_NOTE = "/html/body/div[3]/div/div/div[2]/label/input"

"""# **HÀM GỬI KẾT NỐI**"""

def check_status(driver: webdriver.Chrome, xpath: str, *kws):
    try:
        status = driver.find_element(By.XPATH, xpath)
        status_text = status.get_attribute("aria-label")
        if status_text:  # Kiểm tra nếu status_text tồn tại
            for keyword in kws:
                if keyword in status_text:
                    return True
    except NoSuchElementException:
        print(f"Element not found: {xpath}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return False


def check_status_in_more():
    # CHECK UNCONNECTED STATUS IN MORE.
    if check_status(driver, MORE_UNCONNECT, "Invite"):
        return "UNCONNECTED"
    # CHECK CONNECTED STATUS IN MORE.
    if check_status(driver, MORE_CONNECT, "Remove your connection"):
        return "CONNECTED"
    return "UNKNOWN"  # Giá trị trả về mặc định


def find_element_in_list(driver: webdriver.Chrome, e_list: list[str]):
    for e in e_list:
        try:
            return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, e)))
        except TimeoutException:
            print(f"Timeout for element: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    return None

def send_connection(driver: webdriver.Chrome, xpath: str):
    try:
        # CLICK BUTTON CONNECT.
        try:
            e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            e.click()
        except TimeoutException:
            return "ERROR: BUTTON CONNECT NOT FOUND"
        except Exception as ex:
            return f"ERROR: FAILED TO CLICK CONNECT BUTTON: {ex}"

        # Thay thế time.sleep bằng WebDriverWait để đảm bảo trang đã sẵn sàng
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, BUTTON_SEND_WITHOUT_NOTE)))

        # CLICK SEND WITHOUT NOTE.
        try:
            e = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, BUTTON_SEND_WITHOUT_NOTE)))
            e.click()
        except TimeoutException:
            return "ERROR: BUTTON SEND WITHOUT NOTE NOT FOUND"
        except Exception as ex:
            return f"ERROR: FAILED TO CLICK SEND WITHOUT NOTE: {ex}"

        return "SUCCESS: CONNECT WITHOUT NOTE!"

    except Exception as e:
        print(f"\n {e}")
        return "ERROR: UNKNOWN"

def check_connection(driver: webdriver.Chrome, email: str, note: str = None):
    try:
        # CHECK UNCONNECTED STATUS.
        if check_status(driver, STATUS_CONNECT, "Invite"):
            status = send_connection(driver, STATUS_CONNECT)  # Gửi kết nối không có ghi chú
            print(f"STATUS: {status}")
            return status

        # CHECK PENDING STATUS.
        if check_status(driver, STATUS_CONNECT, "Pending"):
            print("STATUS: PENDING")
            return "PENDING"

        # FIND BUTTON MORE.
        print("CHECKING IN MORE", end=" ")
        try:
            button_more = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, BUTTON_MORE)))
            button_more.click()
        except TimeoutException:
            print("ERROR: BUTTON MORE NOT FOUND!")
            return "ERROR: BUTTON MORE NOT FOUND!"
        except NoSuchElementException:
            print("ERROR: BUTTON MORE NOT FOUND!")
            return "ERROR: BUTTON MORE NOT FOUND!"

        # CHECK CONNECTED STATUS.
        if check_status(driver, STATUS_MESSAGE, "Message", "Follow", "Following"):
            status = check_status_in_more()
            if status == "UNCONNECTED":
                status = send_connection(driver, MORE_UNCONNECT)  # Gửi kết nối không có ghi chú
            print(f"STATUS: {status}")
            return status

    except Exception as e:
        print(f"ERROR: {e}")
        return "ERROR: UNKNOWN"

"""# **THỰC HIỆN GỬI KẾT NỐI**"""

for index, row in df.iterrows():
    # GO TO PROFILE LINK.
    profile_link = row['LINK']
    print(f"Visiting profile: {profile_link}", end=" ")
    driver.get(profile_link)
    # display_full_screenshot(driver)
    status = ""
    # Đợi trang tải đầy đủ trước khi kiểm tra kết nối
    try:
      WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, STATUS_CONNECT)))
      # CHECK CONNECTION AND SEND WITHOUT NOTE.
      status = check_connection(driver, row["EMAIL"])  # Không gửi ghi chú
    except:
      status = "CONNECTED"

    df.at[index, 'STATUS'] = status

# UPDATE GOOGLE SHEET DATA.
# updated_values = [df.columns.tolist()] + df.values.tolist()
# body = {'values': updated_values}
# result = service.spreadsheets().values().update(
#     spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
#     valueInputOption='RAW', body=body).execute()

"""# **KẾT THÚC CHƯƠNG TRÌNH**"""

# driver.quit()
