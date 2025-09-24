import requests
from bs4 import BeautifulSoup
from transliterate import translit
import json




def searching():
    link_parser = input('Введите ключевое слово:\n> ')

    print('Запись начинается...')

    with open('data.json', 'r') as js:
        data = json.load(js)


    text = translit(link_parser, language_code='ru', reversed=True)

    url = f'https://tgsearch.org/search?query={text}'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    username = []


    for article in soup.find_all('div', class_='channel-card__text'):
        for li in article.find_all('li'):
            username.append(li.text)
        if translit(username[1],language_code='ru',reversed=True) != 'privatnyj':
            data['channels'].append(translit(username[1],language_code='ru',reversed=True) + '\n')
        username.clear()


    with open('data.json','w') as text:
        json.dump(data, text, indent=4)
    
    print('Запись закончилась')






