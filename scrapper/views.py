import traceback
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


def __init__(self):
    self.init_driver()


def init_driver():
    try:
        driver = webdriver.Firefox(executable_path='geckodriver')
    except:
        driver = webdriver.Firefox(executable_path='geckodriver.exe')
    try:
        driver.get("https://github.com/")

        search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js-site-search-form")))
        search_field = search.find_element_by_class_name("js-site-search-focus")
        search_field.send_keys("org:google")
        search_field.send_keys(Keys.ENTER)

        dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "select-menu-button")))
        dropdown.click()

        sort_menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/main/div/div[3]/div/div[1]/details/details-menu/div[2]/a[4]')))
        sort_menu.click()

        print('+++++++++++++ Page 1 ++++++++++++++')
        time.sleep(10)

        org_repo_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "repo-list")))
        repo_list = org_repo_list.find_elements_by_tag_name("li")
        for li in repo_list:
            repo = li.find_element_by_class_name("text-normal")
            a = repo.find_element_by_tag_name('a')
            print(repo.text, ' --> ', a.get_attribute("href"))

        time.sleep(10)

        next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next_page")))
        next_page.click()
        print('+++++++++++++ Page 2 ++++++++++++++')

        time.sleep(10)

        org_repo_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "repo-list")))
        repo_list = org_repo_list.find_elements_by_tag_name("li")
        for li in repo_list:
            repo = li.find_element_by_class_name("text-normal")
            a = repo.find_element_by_tag_name('a')
            print(repo.text, ' --> ', a.get_attribute("href"))

    except:
        traceback.print_exc()
    driver.maximize_window()


# def get_popular_repos():
def index(request):
    init_driver()
    return HttpResponse("Hello, world. You're at the scrapper index.")