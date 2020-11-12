import traceback
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

new_path = "C:\Program Files\chromedriver.exe"


def __init__(self):
    self.init_driver()


globalContAndCommit = []


def get_contrib_list(driver, list_of_repos, total_contributors):
    try:
        popular_repos = []
        for link in list_of_repos:
            contributors_and_commit = []
            driver.get(link['repo-link'])
            print("link opened")
            time.sleep(5)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Contributors'))).click()
            print('contributor link opened')
            time.sleep(10)

            contrib_list = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'contrib-person')))
            total_contrib = contrib_list[-1].find_element_by_class_name('text-normal')
            print('total number of contrib = ', total_contrib.text)
            for contrib in contrib_list:
                a = contrib.find_elements_by_tag_name('a')
                contributors_and_commit.append({'contributor': a[1].text, 'commits': a[-1].text})
                print(a[1].text)    # contrib name
                print(a[-1].text)   # contrib commit count
            popular_repos.append({"repository": link['repo-name'].split('/', 1)[1],
                                  "contributers_&_commits": contributors_and_commit})
            time.sleep(5)
        return popular_repos
    except:
        traceback.print_exc()
        return []


def init_driver(org, no_of_repos, no_of_contributors):
    try:
        driver = webdriver.Chrome(new_path)
    except:
        driver = webdriver.Firefox(executable_path='geckodriver.exe')

    try:
        driver.get("https://github.com/")
        driver.maximize_window()
        list_of_repo = []
        counter_for_repo = 0
        search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js-site-search-form")))
        search_field = search.find_element_by_class_name("js-site-search-focus")
        search_field.send_keys(org)
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
            if counter_for_repo == no_of_repos:
                break

            repo = li.find_element_by_class_name("text-normal")
            a = repo.find_element_by_tag_name('a')
            pair_of_repo_and_link = {
                'repo-name': repo.text,
                'repo-link': a.get_attribute("href")
            }
            list_of_repo.append(pair_of_repo_and_link)
            counter_for_repo = counter_for_repo + 1

        time.sleep(10)

        page_number = 1

        while True:
            if counter_for_repo == no_of_repos:
                break
            page_number = page_number + 1
            next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next_page")))
            next_page.click()
            print('+++++++++++++ Page', page_number, '++++++++++++++')

            time.sleep(10)

            org_repo_list = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "repo-list")))
            repo_list = org_repo_list.find_elements_by_tag_name("li")
            for li in repo_list:
                if counter_for_repo == no_of_repos:
                    break
                repo = li.find_element_by_class_name("text-normal")
                a = repo.find_element_by_tag_name('a')
                pair_of_repo_and_link = {
                    'repo-name': repo.text,
                    'repo-link': a.get_attribute("href")
                }
                list_of_repo.append(pair_of_repo_and_link)
                counter_for_repo = counter_for_repo + 1

        repo_list = get_contrib_list(driver, list_of_repo, no_of_contributors)
        driver.quit()
        return repo_list
    except:
        traceback.print_exc()
        driver.quit()


# def get_popular_repos():
def index(request):
    init_driver()
    return HttpResponse("Hello, world. You're at the scrapper index.")
