from bs4 import BeautifulSoup


def get_bs_object(obj):
    return BeautifulSoup(str(obj), 'html.parser')
