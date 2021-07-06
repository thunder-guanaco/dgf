import logging
import time

from bs4 import BeautifulSoup
from django.conf import settings
from django.db import IntegrityError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from dgf.models import Friend, UdiscRound

logger = logging.getLogger(__name__)


def get_course_url(course):
    return settings.UDISC_COURSE_BASE_URL.format(course.udisc_id)


def scroll_down(body, times=3):
    for x in range(times):
        body.send_keys(Keys.END)
        time.sleep(5)


def click_show_more_button(driver):
    element = driver.find_element_by_xpath('//h3[text()="Leaderboards"]/..//span[text()="Show More"]/..')
    driver.execute_script('arguments[0].click();', element)


def get_full_page(course):
    udisc_url = get_course_url(course)
    logger.info(f'Crawling {udisc_url}... (this might take a while)')

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(executable_path=settings.SELENIUM_DRIVER_EXECUTABLE_PATH, options=options)

    try:
        driver.get(udisc_url)

        body = driver.find_element_by_tag_name('body')
        scroll_down(body, times=3)
        click_show_more_button(driver)

        soup = BeautifulSoup(body.get_attribute('innerHTML'), 'html.parser')
        driver.quit()

    except Exception as e:
        logger.error(f'Error while crawling udisc page: {e}')
        driver.quit()
        raise e

    return soup


def get_main_layout_par(soup, layout_name):
    logger.info(f'Fetching par for the main layout: {layout_name}')
    par_p = soup.find('p', text=layout_name).parent.parent.find_all('p')[2]
    return int(par_p.text.split(' ')[1])


def get_best_scores(course):
    soup = get_full_page(course)
    par = get_main_layout_par(soup, course.udisc_main_layout)

    players_list = []
    for item in soup.find('h3', text='Leaderboards').parent.find('ol').children:
        player_div, score_div = item.find('div').find_all('div', recursive=False)
        name_div = player_div.find_all('div', recursive=False)[2].find_all('div')[0]
        players_list.append((name_div.get_text(), int(score_div.get_text()) - par))

    return players_list


def update_score_if_wischlingen(course, friend, new_score):
    if course.name == 'Revierpark Wischlingen' and (
            not friend.best_score_in_wischlingen or new_score < friend.best_score_in_wischlingen):
        friend.best_score_in_wischlingen = new_score
        friend.save()
        logger.info(f'Updated best score of {friend} in Wischlingen to {new_score}')


def update_udisc_scores(course):
    """
    :param course: to get information from
    :return: full URL of the course in UDisc and the best 3 friends
    """

    if not course.udisc_id:
        raise UserWarning(f'Course "{course.name}" has no UDisc ID')

    if not course.udisc_main_layout:
        raise UserWarning(f'Course "{course.name}" has no main layout defined for UDisc ID')

    scores = get_best_scores(course)

    # delete all rounds, we are loading new ones
    logger.info(f'Deleting all existing rounds...')
    UdiscRound.objects.filter(course=course).delete()

    logger.info(f'Adding new rounds from UDisc...')
    for username, score in scores:
        try:
            friend = Friend.objects.get(udisc_username=username)
            UdiscRound.objects.create(course=course, friend=friend, score=score)
            update_score_if_wischlingen(course, friend, score)
        except Friend.DoesNotExist:
            pass  # It's ok. This is just not one of the Friends
        except IntegrityError:
            pass  # It's ok. We only want the first round (the best one)
