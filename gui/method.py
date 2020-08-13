import numpy as np
import pandas as pd
import io
import re
import requests
import PIL.Image
import PIL.ImageTk
import lxml.etree
import pickle
import dbcon.mysqlcon


def get_url(movie_id):
    con, cur = dbcon.mysqlcon.mysql_connect()
    cur.execute("select imdbId from movrecsystem.links where movieId = {}".format(movie_id))
    imdb_id = str(cur.fetchall()[0][0])
    dbcon.mysqlcon.mysql_close(con, cur)
    imdb_id = "0" * (7 - len(imdb_id)) + imdb_id
    url = "http://www.imdb.com/title/tt{}/".format(imdb_id)
    return url


def get_src(url, movie_id):
    html = requests.get(url)
    bs = lxml.etree.HTML(html.text)
    img_url = bs.xpath('//link[@rel="image_src"]/@href')[0]
    con, cur = dbcon.mysqlcon.mysql_connect()
    sql = "select title, genres from movrecsystem.movies where movieId = {}".format(movie_id)
    cur.execute(sql)
    data = cur.fetchall()
    title = re.findall('(.*)\(', data[0][0])[0].strip(' ')
    date = re.findall('\((\d*)\)', data[0][0])[0].strip(' ')
    genres_list = data[0][1].strip('\r').split('|')
    genres = "\n".join(genres_list)
    dbcon.mysqlcon.mysql_close(con, cur)
    return img_url, title, date, genres


def get_image(img_url, w_box=80, h_box=120):
    html = requests.get(img_url).content
    data_stream = io.BytesIO(html)
    image = PIL.Image.open(data_stream)
    w, h = image.size
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    image_resized = image.resize((width, height), PIL.Image.ANTIALIAS)
    photo_image = PIL.ImageTk.PhotoImage(image_resized)
    return photo_image


# page值：old表示当前是老用户，new表示当前是新用户
def get_online_svd(user_id, movie_id, page):
    con, cur = dbcon.mysqlcon.mysql_connect()
    if page == "old":
        cur.execute("select recId from movrecsystem.pdtol where userId = {}".format(user_id))
        pdt_list = cur.fetchall()
        cur.execute("select simId from movrecsystem.simol where movieId = {}".format(movie_id))
        sim_list = cur.fetchall()
        mix_list = set(pdt_list) | set(sim_list)
        mix_list = np.array([mix[0] for mix in mix_list])
    else:
        cur.execute("select movieId, count(1) from movrecsystem.ratings group by movieId order by count(1) desc limit 50;")
        mix_list = cur.fetchall()
        mix_list = np.array([mix[0] for mix in mix_list])
    cur.execute("select * from movrecsystem.ratings where userId = {}".format(user_id))
    rated_list = cur.fetchall()
    rated_list = np.array(rated_list)
    dbcon.mysqlcon.mysql_close(con, cur)
    mix_list = np.array(list(set(mix_list) - set(rated_list[:, 1])))

    mov_id_list = pickle.load(open("../data/movieidlist", "rb"))
    similarity = pickle.load(open("../data/similaritySVD", "rb"))
    similarity = pd.DataFrame(similarity, columns=mov_id_list, index=mov_id_list, copy=True)

    recent_mov_list = rated_list[np.argsort(rated_list[:, -1])[::-1][:5], :]

    value = similarity.loc[mix_list, recent_mov_list[:, 1]].values.dot(recent_mov_list[:, 2]) / np.sum(similarity.loc[mix_list, recent_mov_list[:, 1]].values, axis=1)

    rec_list = mix_list[np.argsort(value)[::-1][:5]]
    return rec_list


# page值：old表示当前是老用户，new表示当前是新用户
def get_online_nmf(user_id, movie_id, page):
    con, cur = dbcon.mysqlcon.mysql_connect()
    if page == "old":
        cur.execute("select recId from movrecsystem.pdtol where userId = {}".format(user_id))
        pdt_list = cur.fetchall()
        cur.execute("select simId from movrecsystem.simol where movieId = {}".format(movie_id))
        sim_list = cur.fetchall()
        mix_list = set(pdt_list) | set(sim_list)
        mix_list = np.array([mix[0] for mix in mix_list])
    else:
        cur.execute("select movieId, count(1) from movrecsystem.ratings group by movieId order by count(1) desc limit 50;")
        mix_list = cur.fetchall()
        mix_list = np.array([mix[0] for mix in mix_list])
    cur.execute("select * from movrecsystem.ratings where userId = {}".format(user_id))
    rated_list = cur.fetchall()
    rated_list = np.array(rated_list)
    dbcon.mysqlcon.mysql_close(con, cur)
    mix_list = np.array(list(set(mix_list) - set(rated_list[:, 1])))

    mov_id_list = pickle.load(open("../data/movieidlist", "rb"))
    similarity = pickle.load(open("../data/similarityNMF", "rb"))
    similarity = pd.DataFrame(similarity, columns=mov_id_list, index=mov_id_list, copy=True)

    recent_mov_list = rated_list[np.argsort(rated_list[:, -1])[::-1][:5], :]

    value = similarity.loc[mix_list, recent_mov_list[:, 1]].values.dot(recent_mov_list[:, 2]) / np.sum(similarity.loc[mix_list, recent_mov_list[:, 1]].values, axis=1)

    rec_list = mix_list[np.argsort(value)[::-1][:5]]
    return rec_list
