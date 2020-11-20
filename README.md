# Naver News Crawling
Python을 이용한 네이버 뉴스 검색 결과 크롤링 프로그램

## 설치
git 명령을 사용해 적당한 위치에 repo를 다운로드 합니다.
```
$ cd <YOUR_DIRECTORY>
$ git clone https://github.com/yskim041/naver_news_crawling.git
```

프로그램에서 사용하는 라이브러리들을 설치해줍니다.

#### pip 을 사용하는 경우
```
$ pip install -r requirements.txt
```

#### conda 를 사용하는 경우
```
$ conda install --file requirements.txt
```

## 사용방법
다운받은 repo가 저장된 폴더로 이동 후, `naver_news_crawling.py` 스크립트를 실행합니다.
```
$ cd <YOUR_DIRECTORY>
$ cd naver_news_crawling
$ python naver_news_crawling.py
```

스크립트가 실행되면, 화면에 출력되는 안내에 따라 검색어, 페이지 수, 검색 방식, 검색 일자를 설정해줍니다. 기본 설정 값은 `configs.json` 에서 설정할 수 있습니다. 반복적으로 같은 방식의 검색을 수행할 경우, 아래 **기본 설정 변경** 파트를 참고하여 `configs.json` 파일을 적절하게 설정한 후 사용하시기 바랍니다.

#### 결과 확인
검색 결과는 스크립트가 실행된 경로 아래 `results` 라는 폴더 내에 저장됩니다. 또는, `configs.json` 내에 지정한 `output_directory` 안에 저장하도록 설정할 수 있습니다.

#### 기본 설정 변경
repo가 저장된 폴더 안에 있는 `configs.json` 파일을 수정하여 기본 설정을 변경할 수 있습니다. 변경 가능한 옵션은 다음과 같습니다.

| Option                | Description                                                     |
|-----------------------|-----------------------------------------------------------------|
| `default_query`       | 기본 검색 키워드                                                |
| `max_pages`           | 수집할 최대 페이지 수 (한 페이지당 10개의 기사가 포함됨)        |
| `sort_type`           | 기사 검색 방식 (관련도순=0, 최신순=1, 오래된순=2)               |
| `date_range`          | 검색 일자 범위 (오늘로부터 며칠 전 기사부터 검색할 것인지 설정) |
| `output_directory`    | 검색 결과 파일을 저장할 경로                                    |
