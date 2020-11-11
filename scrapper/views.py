import traceback
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

newPath = "C:\Program Files\chromedriver.exe"


def __init__(self):
    self.init_driver()


globalContAndCommit = []


def my_function2(listOfRepo,total_contributors):
    try:
        driver = webdriver.Chrome(newPath)
    except:
        driver = webdriver.Chrome(newPath)

    try:
        for link in listOfRepo:
            driver.get(link['repo-link'])
            print("link opened")
            time.sleep(5)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Contributors'))).click()
            print('contributor link opened')



    except:
        traceback.print_exc()


def init_driver():
    try:
        driver = webdriver.Chrome(newPath)
    except:
        driver = webdriver.Chrome(newPath)
    try:
        driver.get("https://github.com/")
        listofrepo = []
        noOfRepo = 10
        noOfcontributors = 1
        counterForRepo = 0
        search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js-site-search-form")))
        search_field = search.find_element_by_class_name("js-site-search-focus")
        search_field.send_keys("org:google")
        search_field.send_keys(Keys.ENTER)

        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "select-menu-button")))
        dropdown.click()

        sort_menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[4]/main/div/div[3]/div/div[1]/details/details-menu/div[2]/a[4]')))
        sort_menu.click()

        print('+++++++++++++ Page 1 ++++++++++++++')
        time.sleep(10)

        org_repo_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "repo-list")))
        repo_list = org_repo_list.find_elements_by_tag_name("li")
        for li in repo_list:
            if counterForRepo == noOfRepo:
                break

            repo = li.find_element_by_class_name("text-normal")
            a = repo.find_element_by_tag_name('a')
            pairOfRepoAndLink = {
                'repo-name': repo.text,
                'repo-link': a.get_attribute("href")
            }
            listofrepo.append(pairOfRepoAndLink)
            counterForRepo = counterForRepo + 1

        time.sleep(10)

        pageNumber = 1

        while True:
            if counterForRepo == noOfRepo:
                break
            pageNumber = pageNumber + 1
            next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next_page")))
            next_page.click()
            print('+++++++++++++ Page', pageNumber, '++++++++++++++')

            time.sleep(10)

            org_repo_list = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "repo-list")))
            repo_list = org_repo_list.find_elements_by_tag_name("li")
            for li in repo_list:
                if counterForRepo == noOfRepo:
                    break
                repo = li.find_element_by_class_name("text-normal")
                a = repo.find_element_by_tag_name('a')
                pairOfRepoAndLink = {
                    'repo-name': repo.text,
                    'repo-link': a.get_attribute("href")
                }
                listofrepo.append(pairOfRepoAndLink)
                counterForRepo = counterForRepo + 1

        # print(listofrepo)
        print(len(listofrepo))
        my_function2(listofrepo, noOfcontributors)
    except:
        traceback.print_exc()

    driver.maximize_window()
    driver.quit()


# def get_popular_repos():
def index(request):
    init_driver()
    return HttpResponse("Hello, world. You're at the scrapper index.")
