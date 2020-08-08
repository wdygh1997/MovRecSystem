import pandas as pd
import pickle


# 从ratings.csv中读入<用户-电影>评分矩阵
def read_ratings():
    ratings = pd.read_csv("../data/ratings.csv")
    ratings_dict = {}
    for i in range(ratings.shape[0]):
        line = ratings.loc[i]
        if line.movieId in ratings_dict:
            ratings_dict[line.movieId][line.userId] = line.rating
        else:
            ratings_dict[line.movieId] = {line.userId: line.rating}
    ratings_matrix = pd.DataFrame(ratings_dict)
    # 缺省值填充为0
    ratings_matrix = ratings_matrix.fillna(0)
    return ratings_matrix


# 将电影id的列表序列化存储起来，在gui.method中需要使用
ratings_mtx = read_ratings()
mov_id_list = ratings_mtx.columns
mov_id_list = list(map(int, mov_id_list))
with open("../data/movieidlist", "wb") as file:
    pickle.dump(mov_id_list, file)
