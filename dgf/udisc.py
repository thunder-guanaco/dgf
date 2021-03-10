import time

from bs4 import BeautifulSoup
from django.conf import settings
from django.db import IntegrityError
from django.utils.translation import ugettext as _
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from dgf.models import Friend, UdiscRound


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
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(executable_path=settings.SELENIUM_DRIVER_EXECUTABLE_PATH, options=options)
    driver.get(get_course_url(course))

    body = driver.find_element_by_tag_name('body')

    scroll_down(body, times=3)
    click_show_more_button(driver)

    return body


def get_standard_layout_par(soup):
    par_p = soup.find('p', text='Standard Layout').parent.parent.find_all('p')[2]
    return int(par_p.text.split(' ')[1])


def get_best_rounds(course):
    page_body = get_full_page(course)
    soup = BeautifulSoup(page_body.get_attribute('innerHTML'), 'html.parser')

    par = get_standard_layout_par(soup)

    players_list = []
    for item in soup.find('h3', text='Leaderboards').parent.find('ol').children:
        player_div, score_div = item.find('div').find_all('div', recursive=False)
        name_div = player_div.find_all('div', recursive=False)[2].find_all('div')[0]
        players_list.append((name_div.get_text(), int(score_div.get_text()) - par))

    return players_list


def update_udisc_rounds(course):
    """
    :param course: to get information from
    :return: full URL of the course in UDisc and the best 3 friends
    """

    if not course.udisc_id:
        raise UserWarning('{} {} {}'.format(_('Course'), course.name, _('has no UDisc ID.')))

    rounds = get_best_rounds(course)

    # delete all rounds, we are loading new ones
    UdiscRound.objects.filter(course=course).delete()

    for username, score in rounds:
        try:
            friend = Friend.objects.get(udisc_username=username)
            UdiscRound.objects.create(course=course, friend=friend, score=score)
        except Friend.DoesNotExist:
            pass  # It's ok. This is just not one of the Friends
        except IntegrityError:
            pass  # It's ok. We only want the first round (the best one)
