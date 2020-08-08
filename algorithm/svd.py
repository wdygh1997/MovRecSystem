import numpy as np
import pandas as pd
import pickle
import algorithm.readrating

ratings_matrix = algorithm.readrating.read_ratings()
print("评分数据ratings读入完成...")

u, s, vt = np.linalg.svd(ratings_matrix)
print("评分数据矩阵svd分解完成...")

truncated_s = np.diag(s[:305])
truncated_vt = vt[:305, :]
s_vt = truncated_s.dot(truncated_vt)
print("基于用户评分的电影特征提取完成...")

s_vt_std = ((s_vt.T - s_vt.mean(axis=1))/s_vt.std(axis=1)).T
print("电影特征矩阵z-score标准化完成...")

top = s_vt_std.T.dot(s_vt_std)
bottom = (np.linalg.norm(s_vt_std, axis=0).reshape(-1, 1)).dot(np.linalg.norm(s_vt_std, axis=0).reshape(1, -1))
similarity = top/bottom
print("电影特征向量的余弦相似度计算完成...")

with open("../data/similaritySVD", "wb") as file:
    pickle.dump(similarity, file)
print("电影相似度pickle序列化完成...")

simMod = similarity
for i in range(simMod.shape[0]):
    simMod[i][i] = 0
movieIdList = ratings_matrix.columns
simSVD = pd.DataFrame()
for i in range(ratings_matrix.shape[1]):
    movieId = movieIdList[i]
    simIdList = movieIdList[simMod[i, :] >= 0]
    simDegreeList = simMod[i, simMod[i, :] >= 0]
    if len(simDegreeList) > 10:
        index = np.argsort(simDegreeList)[::-1]
        index = index[:10]
        simIdList = simIdList[index]
        simDegreeList = simDegreeList[index]
    simSVD = pd.concat([simSVD, pd.DataFrame({'movieId': movieId, 'simId': simIdList, 'simDegree': simDegreeList})])
print("相似电影的DataFrame构建完成...")

simSVD.to_csv("../data/simSVD.csv", index=False)
print("相似电影的csv文件存储完成...")

simMod = (similarity+1)/2
userIdList = ratings_matrix.index
movieIdList = ratings_matrix.columns
pdtSVD = pd.DataFrame()
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
    pdtSVD = pd.concat([pdtSVD, pd.DataFrame({'userId': userId, 'recId': recIdList, 'pdtScore': pdtScoreList})])
    print("已计算完成{}位用户的预测电影...".format(i+1))
print("预测电影的DataFrame构建完成...")

pdtSVD.to_csv("../data/pdtSVD.csv", index=False)
print("预测电影的csv文件存储完成...")
