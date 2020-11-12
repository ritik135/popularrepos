# importing necessary libraries
import traceback
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

# setting new_path as chrome webdriver path
new_path = "C:\Program Files\chromedriver.exe"

# declaring constructor
def __init__(self):
    self.init_driver()

# function to fetch and return the list containing the M most forked repos and N contributors and commit counts This
# function is taking 3 inputs 1.selenium webdriver 2.list containing repos name and links 3.no of contributors required
def get_contrib_list(driver, list_of_repos, total_contributors):
    try:
        # list to store our final result
        popular_repos = []

        # loop to traverse through each & every repository saved in list_of_repos
        for link in list_of_repos:

            # list to store contributors name and commit counts as dictionary for each repository
            contributors_and_commit = []
            driver.get(link['repo-link'])
            time.sleep(5)

            # try block to try clicking on the Contributors element if there is atleast 1 contributor
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Contributors'))).click()
                time.sleep(10)

            # except block to handle exception when there is no contributor for the given repository
            except:
                popular_repos.append({"repository": link['repo-name'].split('/', 1)[1],
                                      "contributers_&_commits": {'contributor': 0, 'commits': 0}})
                continue

            time.sleep(10)

            # locating element using Class Name to get the info of all contributors name and their commits count
            contrib_list = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'contrib-person')))
            time.sleep(10)

            # storing the total number of contributors in variable all_contrib by removing # from the string and converiting into integer form
            # for eg. we will be getting #100 in total_contrib so we are making it 100 and storing the same in all_contrib
            total_contrib = contrib_list[-1].find_element_by_class_name('text-normal').text
            all_contrib = 0
            total_contrib = total_contrib[1:]
            all_contrib = int(total_contrib)

            # if number of required contributors is greater than total contributors for a given repository
            if total_contributors >= all_contrib:

                # loop to traverse through each and every contributor info one by one
                for contrib in contrib_list:
                    a = contrib.find_elements_by_tag_name('a')
                    contributors_and_commit.append({'contributor': a[1].text, 'commits': a[-1].text})
                popular_repos.append({"repository": link['repo-name'].split('/', 1)[1],
                                    "contributers_&_commits": contributors_and_commit})
                time.sleep(5)

            # if number of required contributors is not greater than total contributors for a given repository
            else:
                contrib_counter = 1
                for contrib in contrib_list:

                    # break condition to come out of the loop when our requirements for contributors met
                    if contrib_counter > total_contributors:
                        break
                    a = contrib.find_elements_by_tag_name('a')
                    contributors_and_commit.append({'contributor': a[1].text, 'commits': a[-1].text})
                    contrib_counter = contrib_counter + 1
                popular_repos.append({"repository": link['repo-name'].split('/', 1)[1],
                                      "contributers_&_commits": contributors_and_commit})
                time.sleep(5)

        # returning the list as our final answer for a given organization, number of repos, nonumber of contributors
        return popular_repos

    except:
        traceback.print_exc()
        return []

# function with 3arguements organization name, number of repos, number of contributors taking input from API
def init_driver(org, no_of_repos, no_of_contributors):

    # if chrome webdriver is installed it will get invoked
    try:
        driver = webdriver.Chrome(new_path)

    # otherwise firefox window will get open
    except:
        driver = webdriver.Firefox(executable_path='geckodriver.exe')

    # input github link in the browser window and sending keys to it for further work
    try:
        driver.get("https://github.com/")
        driver.maximize_window()

        # list to store {repository name & repository link}
        list_of_repo = []
        counter_for_repo = 0

        # locating search box to send keys and then hit enter. Everything will be automated.
        search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js-site-search-form")))
        search_field = search.find_element_by_class_name("js-site-search-focus")
        search_field.clear()
        search_field.send_keys(org)
        search_field.send_keys(Keys.ENTER)

        # selecting dropdown element and clicking it
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "select-menu-button")))
        dropdown.click()

        # choosing most forked option in the dropdown and clicking it
        sort_menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[4]/main/div/div[3]/div/div[1]/details/details-menu/div[2]/a[4]')))
        sort_menu.click()

        # print('+++++++++++++ Page 1 ++++++++++++++')
        time.sleep(10)

        #getting repository list in repo_list by using Class Name
        org_repo_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "repo-list")))
        repo_list = org_repo_list.find_elements_by_tag_name("li")

        # To check whether number of repos required is not fulfilled in the first page itself
        try:
            for li in repo_list:
                if counter_for_repo == no_of_repos:
                    break

                # fetching and storing repo name and repo link
                repo = li.find_element_by_class_name("text-normal")
                a = repo.find_element_by_tag_name('a')
                pair_of_repo_and_link = {
                    'repo-name': repo.text,
                    'repo-link': a.get_attribute("href")
                }
                list_of_repo.append(pair_of_repo_and_link)
                counter_for_repo = counter_for_repo + 1

            time.sleep(10)

        # handling exception when repos required are greater than total repos for a given organization
        except:
            # calling get_contrib_list() function to get the required result
            repo_list = get_contrib_list(driver, list_of_repo, no_of_contributors)
            driver.quit()
            return repo_list

        # A variable to store page number on which we are right now for a particular organization
        page_number = 1

        # getting repos data from multiple pages starting from page 2 and handling exception when there are no more
        # repos
        try:

            # infinite loop with base condition to break out when number of repos fetched will become equal to the
            # required repos
            while True:
                if counter_for_repo == no_of_repos:
                    break
                page_number = page_number + 1
                next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next_page")))
                next_page.click()

                # printing our current page number on which we are right now
                # print('+++++++++++++ Page', page_number, '++++++++++++++')

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

            # calling get_contrib_list() function to get the required result
            repo_list = get_contrib_list(driver, list_of_repo, no_of_contributors)
            driver.quit()
            return repo_list
        except:
            # calling get_contrib_list() function to get the required result
            repo_list = get_contrib_list(driver, list_of_repo, no_of_contributors)
            driver.quit()
            return repo_list

    except:
        traceback.print_exc()
        driver.quit()

def index(request):
    init_driver()
    return HttpResponse("Hello, world. You're at the scrapper index.")
