import numpy as np
import pandas as pd
import pickle
import algorithm.readrating

ratings_matrix = algorithm.readrating.read_ratings()
print("评分数据ratings读入完成...")


def nmf_factorization(x, k, e, max_step):
    w = np.random.rand(x.shape[0], k)
    h = np.random.rand(k, x.shape[1])
    for step in range(max_step):
        pre_x = np.dot(w, h)
        err = x - pre_x
        cost = np.sum(err * err)
        print("已迭代{}次，损失函数值为{}...".format(step+1, cost))
        if cost < e:
            break
        top_w = np.dot(x, h.T)
        bottom_w = np.dot(w, np.dot(h, h.T))
        w[bottom_w != 0] = (w * top_w / bottom_w)[bottom_w != 0]
        top_h = np.dot(w.T, x)
        bottom_h = np.dot(w.T, np.dot(w, h))
        h[bottom_h != 0] = (h * top_h / bottom_h)[bottom_h != 0]
    return w, h


p, q = nmf_factorization(ratings_matrix.values, 305, 125000, 1000)
print("评分数据矩阵nmf分解完成...")
print("基于用户评分的电影特征提取完成...")

q_std = ((q.T - q.mean(axis=1))/q.std(axis=1)).T
print("电影特征矩阵z-score标准化完成...")

top = q_std.T.dot(q_std)
bottom = (np.linalg.norm(q_std, axis=0).reshape(-1, 1)).dot(np.linalg.norm(q_std, axis=0).reshape(1, -1))
similarity = top/bottom
print("电影特征向量的余弦相似度计算完成...")

with open("../data/similarityNMF", "wb") as file:
    pickle.dump(similarity, file)
print("电影相似度pickle序列化完成...")

simMod = similarity
for i in range(simMod.shape[0]):
    simMod[i][i] = 0
movieIdList = ratings_matrix.columns
simNMF = pd.DataFrame()
for i in range(ratings_matrix.shape[1]):
    movieId = movieIdList[i]
    simIdList = movieIdList[simMod[i, :] >= 0]
    simDegreeList = simMod[i, simMod[i, :] >= 0]
    if len(simDegreeList) > 10:
        index = np.argsort(simDegreeList)[::-1]
        index = index[:10]
        simIdList = simIdList[index]
        simDegreeList = simDegreeList[index]
    simNMF = pd.concat([simNMF, pd.DataFrame({'movieId': movieId, 'simId': simIdList, 'simDegree': simDegreeList})])
print("相似电影的DataFrame构建完成...")

simNMF.to_csv("../data/simNMF.csv", index=False)
print("相似电影的csv文件存储完成...")

simMod = (similarity+1)/2
userIdList = ratings_matrix.index
movieIdList = ratings_matrix.columns
pdtNMF = pd.DataFrame()
for i in range(ratings_matrix.shape[0]):
    userId = userIdList[i]
    unrated = ratings_matrix.values[i, :] == 0
    rated = ~unrated
    recIdList = movieIdList[unrated]
    top = (simMod[unrated, :][:, rated]).dot(ratings_matrix.values[i, rated])
    bottom = np.sum(simMod[unrated, :][:, rated], axis=1)
    pdtScoreList = top/bottom
    if len(pdtScoreList) > 10:
        index = np.argsort(pdtScoreList)[::-1]
        index = index[:10]
        recIdList = recIdList[index]
        pdtScoreList = pdtScoreList[index]
    pdtNMF = pd.concat([pdtNMF, pd.DataFrame({'userId': userId, 'recId': recIdList, 'pdtScore': pdtScoreList})])
    print("已计算完成{}位用户的预测电影...".format(i+1))
print("预测电影的DataFrame构建完成...")

pdtNMF.to_csv("../data/pdtNMF.csv", index=False)
print("预测电影的csv文件存储完成...")
