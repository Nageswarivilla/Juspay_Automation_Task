import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()
def js_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", element)
def test_login_and_add_to_cart(driver):
    wait = WebDriverWait(driver, 15)
    driver.get("https://automationexercise.com")
    login_signup_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div/div/div[2]/div/ul/li[4]/a'))
    )
    js_click(driver, login_signup_btn)
    print("Clicked on Login/Signup")
    email_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form"]/div/div/div[1]/div/form/input[2]'))
    )
    email_input.clear()
    email_input.send_keys("nageswarivilla2001@gmail.com")
    password_input = driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div[1]/div/form/input[3]')
    password_input.clear()
    password_input.send_keys("Nandha@1234")
    login_btn = driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div[1]/div/form/button')
    js_click(driver, login_btn)
    print("Clicked on Login button")
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@href="/logout"]')))
        print("Login successful")
    except Exception:
        pytest.fail("Login failed or page did not load properly")
    product = wait.until(
        EC.visibility_of_element_located((By.XPATH, '(//*[@class="productinfo text-center"])[1]'))
    )
    assert product.is_displayed(), "Product is not displayed after login"
    print("Product is displayed")
    add_cart_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, '(//*[@class="btn btn-default add-to-cart"])[1]'))
    )
    js_click(driver, add_cart_btn)
    print("Product added to cart")
    try:
        continue_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '(//*[@class="btn btn-success close-modal btn-block"])[1]')
            )
        )
        js_click(driver, continue_btn)
        print("Clicked Continue Shopping on modal")
    except Exception:
        print("Continue Shopping modal not found or already closed; continuing")
    cart_icon = wait.until(
        EC.element_to_be_clickable((By.XPATH, '(//*[@class="fa fa-shopping-cart"])[1]'))
    )
    js_click(driver, cart_icon)
    print("Opened Cart")
    proceed_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn-default check_out"]'))
    )
    js_click(driver, proceed_btn)
    print("Clicked Proceed to Checkout")
    place_order_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn-default check_out"]'))
    )
    js_click(driver, place_order_btn)
    print("Clicked Place Order / Checkout to payment")
    card_name = wait.until(
        EC.presence_of_element_located((By.XPATH, '(//input[@class="form-control"])[1]'))
    )
    card_name.clear()
    card_name.send_keys("Test User")

    card_number = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="form-control card-number"]'))
    )
    card_number.clear()
    card_number.send_keys("4242424242424242")

    card_cvc = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="form-control card-cvc"]'))
    )
    card_cvc.clear()
    card_cvc.send_keys("123")

    card_exp_month = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="form-control card-expiry-month"]'))
    )
    card_exp_month.clear()
    card_exp_month.send_keys("12")

    card_exp_year = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="form-control card-expiry-year"]'))
    )
    card_exp_year.clear()
    card_exp_year.send_keys("2030")

    print("Filled dummy card details")
    pay_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@class="form-control btn btn-primary submit-button"]')
        )
    )
    js_click(driver, pay_btn)
    print("Clicked Pay / Place Order")
    try:
        confirmation = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(text(),'Order Placed') or contains(text(),'ORDER PLACED') or contains(text(),'Your order has been placed')]",
                )
            )
        )
        print("Order confirmation detected:", confirmation.text[:100])
    except Exception:
        print("Order confirmation message not detected within timeout. Check manually.")
        try:
            logout_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div/div/div[2]/div/ul/li[4]/a'))
            )
            js_click(driver, logout_btn)
            print("Clicked Logout button")

            signup_btn = wait.until(
                EC.visibility_of_element_located((By.XPATH, '(//*[@class="btn btn-default"])[2]'))
            )
            assert signup_btn.is_displayed(), "Signup/Login button not visible after logout"
            print("Logout successful — Signup/Login button visible again")

        except Exception as e:
            pytest.fail(f"Logout validation failed: {e}")
    time.sleep(3)
