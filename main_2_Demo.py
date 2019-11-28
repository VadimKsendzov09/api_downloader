from flickrapi import FlickrAPI
import random
import requests
import os
import time


api_key_2 = 'sjdhfbvsdf78vs8d7f8v7sdf'
secret_key_2 = 'sdfbsdf87b8sd'

api_key = 'ksjdvnbkjsdf8988y9sdf7v8s7dfyb'
secret_key = 'kajfvafd324f'

flickr = FlickrAPI(api_key_2, secret_key_2, format='parsed-json')

dst_folder = '/Volumes/HD710_PRO/folder/set/before_2015_add/'

key_word = 'portrait'
count = 0
check_count = 0
start_year = 2013
link_list = []


def parse_photos(page_count, key_word, min_data, max_data):
    global count
    global dst_folder

    sub_dst_folder = dst_folder + min_data + '_' + max_data + '/'

    if not os.path.isdir(sub_dst_folder):
        os.mkdir(sub_dst_folder)

    for page_number in range(1, page_count):

        photos = flickr.photos.search(text=key_word,
                                      license=4,
                                      sort='relevance',
                                      min_upload_date=min_data,
                                      max_upload_date=max_data,
                                      safe_search=1,
                                      extras='url_o,url_l',
                                      per_page=500,
                                      page=page_number)

        print('Photos on alone page -->', photos['photos']['total'])

        for i in photos['photos']['photo']:
            for key, value in i.items():
                s_t = random.uniform(0.1, 0.4)
                print('deley-', s_t, value)
                time.sleep(s_t)
                if key == 'url_o':
                    link_list.append(value)
                    count += 1
                    r = requests.get(value, stream=True)
                    file_name = str(value).split('/')[-1]

                    file_path = sub_dst_folder + file_name
                    with open(file_path, 'wb') as f:
                        f.write(r.content)
                        print(count, '-url_o--', value, len(link_list))
                        count += 1

                    break

                elif key == 'url_l':
                    link_list.append(value)
                    count += 1
                    r = requests.get(value, stream=True)
                    file_name = str(value).split('/')[-1]
                    file_path = sub_dst_folder + file_name
                    # if file_name not in ready_list:
                    with open(file_path, 'wb') as f:
                        f.write(r.content)
                        print(count, '-url_l--', value, len(link_list))
                        count += 1


for year in range(0, 2):

    for month in range(2, 12):
        min_data = '01-' + str(month) + '-' + str(start_year + year)
        max_data = '01-' + str(month+1) + '-' + str(start_year + year)
        print('min_data---', min_data, max_data)

        req_photo_number = flickr.photos.search(text=key_word,
                                                license=4,
                                                sort='relevance',
                                                min_upload_date=min_data,
                                                max_upload_date=max_data,
                                                safe_search=1,
                                                extras='url_o,url_l')

        count_of_photos = req_photo_number['photos']['total']
        print('count_of_photos====', count_of_photos)
        int_page_count = int(int(count_of_photos)/500)
        float_page_count = int(count_of_photos)/500

        print('page_count====', int_page_count)

        if int(count_of_photos) <= 500:
            parse_photos(2, key_word, min_data, max_data)
        elif int(count_of_photos) > 500:

            int_page_count = int(int(count_of_photos) / 500)
            float_page_count = int(count_of_photos) / 500
            if float_page_count > int_page_count:
                page_count = int_page_count + 2
                parse_photos(page_count, key_word, min_data, max_data)
            else:
                parse_photos(int_page_count, key_word, min_data, max_data)