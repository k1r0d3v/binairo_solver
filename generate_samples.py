from selenium import webdriver
from bs4 import BeautifulSoup
import math


def format_board(html):
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.find_all('div')
    size = int(math.sqrt(len(divs)))
    r = '{}'.format(size)

    for i, div in enumerate(divs):
        if i % size == 0:
            r += '\n'

        t = div['class'][-1]

        if t == 'cell-off':
            r += '.'
        elif t == 'cell-0':
            r += '0'
        elif t == 'cell-1':
            r += '1'
        else:
            raise Exception('Unexpected value')
    return size, r

def save_to_file(filename, text):
    with open(filename, mode='w') as file:
        file.write(text)

# use firefox to get page with javascript generated content
browser = webdriver.Firefox()

for i in range(1, 13):
    # load page
    url = 'https://www.puzzle-binairo.com/?size={}'.format(i)
    browser.get(url)

    board = browser.find_element_by_class_name('board-back')
    board_html = board.get_attribute('innerHTML')
    
    size, text = format_board(board_html)
    save_to_file('samples/{0}_{1}x{1}.txt'.format(i, size), text)

browser.quit()
