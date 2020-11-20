#!/usr/bin/env python3
"""
Naver에서 뉴스를 검색 후, 결과 리스트의 주요 내용을 엑셀로 저장하는 프로그램
"""

import os
import sys
import json
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def validate_date_text(date_txt):
    try:
        datetime.strptime(date_txt, '%Y.%m.%d.')
        return date_txt
    except:
        if date_txt.endswith(' 전'):
            date_obj = None
            if date_txt.endswith('분 전'):
                date_obj = datetime.now() - timedelta(minutes=int(date_txt[:-3]))
            elif date_txt.endswith('시간 전'):
                date_obj = datetime.now() - timedelta(hours=int(date_txt[:-4]))
            elif date_txt.endswith('일 전'):
                date_obj = datetime.now() - timedelta(days=int(date_txt[:-3]))

            if date_obj:
                return date_obj.strftime('%Y.%m.%d.')
        return None


def contents_cleansing(contents):
    # 컨텐츠 앞뒤의 불필요한 부분 제거
    clean_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '',
                            str(contents)).strip()
    clean_contents = re.sub('<ul class="relation_lst">.*?</dd>', '',
                            clean_contents).strip()
    clean_contents = re.sub('<.+?>', '', clean_contents).strip()
    return clean_contents


def crawler(max_pages, query, sort_type, start_date, end_date, output_dir):
    title_text = []
    link_text = []
    source_text = []
    date_text = []
    contents_text = []
    result = {}

    s_from = start_date.replace(".", "")
    e_to = end_date.replace(".", "")
    page = 1
    max_pages_t = (int(max_pages) - 1) * 10 + 1  # 11=2페이지, 21=3페이지, ...
    data_frame = None

    for page in range(1, max_pages_t + 1, 10):
        url = "https://search.naver.com/search.naver?where=news&query=\"" + query + "\"&sort=" + sort_type \
                + "&ds=" + start_date + "&de=" + end_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to \
                + "%2Ca%3A&start=" + str(page)
        print(f'검색결과 수집 중... page {page // 10 + 1}')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 제목과 링크주소 추출
        atags = soup.find_all('a', class_='news_tit')
        for atag in atags:
            title_text.append(atag.text)    # 제목
            link_text.append(atag['href'])  # 링크주소

        # 매체명 추출
        source_lists = soup.find_all('a', class_='info press')
        for source_list in source_lists:
            source_text.append(source_list.text)  # 매체명

        # 날짜 추출
        date_lists = soup.find_all('span', class_='info')
        for date_list in date_lists:
            valid_date = validate_date_text(date_list.text)
            if valid_date is not None:
                date_text.append(valid_date)

        # 본문요약본
        contents_lists = soup.find_all('a', class_='api_txt_lines')
        for contents_list in contents_lists:
            contents_text.append(contents_cleansing(contents_list))

        # 다음 페이지가 존재하지 않을 경우 반복문 종료
        if len(contents_lists) < 10:
            break

    # 결과를 DataFrame으로 변환
    result = {"date": date_text, "title": title_text, "source": source_text, "contents": contents_text, "link": link_text}
    data_frame = pd.DataFrame(result)

    # 결과 저장
    output_filepath = os.path.join(output_dir, '{}.xlsx'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
    data_frame.to_excel(output_filepath, sheet_name='검색결과')
    print(f'\n검색 완료: {output_filepath}')


def main():
    print('=' * 80 + '\n입력 형식에 맞게 입력해주세요. 아무 것도 입력하지 않으시면 기본 값이 적용됩니다.\n' + '=' * 80)

    # Load default values from configs.json
    with open('./configs.json', 'r', encoding='utf8') as f_in:
        configs = json.load(f_in)
        default_query = configs['default_query']
        default_max_pages = configs['max_pages']
        default_sort_type = configs['sort_type']

        date_range = configs['date_range'] or 30
        time_format = '%Y.%m.%d'
        default_start_date = (datetime.now() - timedelta(days=int(date_range))).strftime(time_format)
        default_end_date = datetime.now().strftime(time_format)

        output_dir = configs['output_directory']
        if output_dir is None:
            output_dir = './results'
        os.makedirs(output_dir, exist_ok=True)

    # Get command line inputs
    max_pages = input(f'최대 크롤링할 페이지 수 입력하시오 [Default={default_max_pages}]: ') or default_max_pages
    query = input(f'검색어 입력 [Default={default_query}]: ') or default_query
    sort_type = input(f'뉴스 검색 방식 입력 (관련도순=0, 최신순=1, 오래된순=2) [Default={default_sort_type}]: ') or default_sort_type
    start_date = input(f'시작날짜 입력 [Default={default_start_date}]: ') or default_start_date
    end_date = input(f'끝날짜 입력 [Default={default_end_date}]: ') or default_end_date

    # Run crawler
    crawler(max_pages, query, sort_type, start_date, end_date, output_dir)


if __name__ == '__main__':
    sys.exit(main())
