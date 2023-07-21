import requests
from urllib import parse
import json, re, csv, time, os
import pandas as pd

headers = {'User-Agent': 'Mozilla/4.-1 (X10; Linux x85_63) AppleWebKit/536.35 (KHTML, like Gecko) Chrome/60.-1.3162.99 Safari/536.35'}

MAX_TRY_TIME = 5

def get_review(app_id):
    with open(f'{app_id}.csv', 'a+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['作者id', '拥有游戏数量', '游戏总时长（分钟）', '上两周游戏时长（分钟）', '评论'])
    
    pice = 0

    ids = []
    game_nums = []
    times = []
    last_two_times = []
    reviews = []
    
    url = f'https://store.steampowered.com/appreviews/{app_id}?json=1&language=schinese&num_per_page=100&filter=updated&filter_offtopic_activity=0&purchase_type=all'
    page = requests.get(url, headers=headers).text.encode('utf-8')
    content = json.loads(page)

    review_num = content['query_summary']['total_reviews'] 
    print('review num:', str(review_num))

    cursor = parse.quote(content['cursor']) 

    page_num = review_num // 100 + 1    
    print('共'+ str(page_num) +'页评论')
    
    print('正在进行第1页评论爬取')
    for b in range(0, len(content['reviews'])):
        one_review = content['reviews'][b]['review']
        one_game_num = content['reviews'][b]['author']['num_games_owned']
        one_id = content['reviews'][b]['author']['steamid']
        one_last_two_time = content['reviews'][b]['author']['playtime_last_two_weeks']
        one_time = content['reviews'][b]['author']['playtime_forever']
        one_review_over = re.compile('\[h1]|\[/h1]|\n|\t|\[b]|\[/b]', re.I).sub('', one_review)  #正则处理单条评论
        reviews.append(one_review_over)
        times.append(one_time)
        ids.append(one_id)
        game_nums.append(one_game_num)
        last_two_times.append(one_last_two_time)
    print('第1页评论爬取完成')

    with open(f'{app_id}.csv', 'a+', encoding='utf-8', newline='') as f:
        for i in range(len(reviews)):
            pice += 1
            writer = csv.writer(f)
            # '作者id', '拥有游戏数量', '游戏总时长（分钟）', '上两周游戏时长（分钟）', '评论'
            writer.writerow([ids[i], game_nums[i], times[i], last_two_times[i], reviews[i]])
        print('成功写入' + str(pice) + '条')

    for c in range(2, page_num + 1):
        url = f'https://store.steampowered.com/appreviews/{app_id}?json=1&language=schinese&num_per_page=100&filter=updated&filter_offtopic_activity=0&purchase_type=all&cursor={cursor}'
        for _ in range(MAX_TRY_TIME):
            try:
                page = requests.get(url, headers=headers).text.encode('utf-8')
                break 
            except:
                print('retry')
                continue 
        content = json.loads(page)
        cursor = parse.quote(content['cursor']) # 将cursor 进行 url编码

        ids = []
        game_nums = []
        times = []
        last_two_times = []
        reviews = []

        print('正在进行第'+ str(c) +'页评论爬取')
        for b in range(0, len(content['reviews'])):
            one_review = content['reviews'][b]['review']
            one_game_num = content['reviews'][b]['author']['num_games_owned']
            one_id = content['reviews'][b]['author']['steamid']
            one_last_two_time = content['reviews'][b]['author']['playtime_last_two_weeks']
            one_time = content['reviews'][b]['author']['playtime_forever']
            one_review_over = re.compile('\[h1]|\[/h1]|\n|\t|\[b]|\[/b]', re.I).sub('', one_review)  #正则处理单条评论
            reviews.append(one_review_over)
            times.append(one_time)
            ids.append(one_id)
            game_nums.append(one_game_num)
            last_two_times.append(one_last_two_time)
        print('第' + str(c) + '页评论爬取完成')

        with open(f'{app_id}.csv', 'a+', encoding='utf-8', newline='') as f:
            for i in range(len(reviews)):
                pice += 1
                writer = csv.writer(f)
                writer.writerow([ids[i], game_nums[i], times[i], last_two_times[i], reviews[i]])
            print('成功写入' + str(pice) + '条')
        time.sleep(1)

    print(f'评论爬取完成并成功写入{app_id}.csv，共'+ str(pice) +'条数据')

if __name__ == '__main__':
    get_review('632470')
