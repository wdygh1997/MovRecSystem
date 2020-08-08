import pandas as pd

sim_svd = pd.read_csv("../data/simSVD.csv")
sim_nmf = pd.read_csv("../data/simNMF.csv")
mix_sim = pd.concat([sim_svd, sim_nmf])
print("在线推荐的预测相似电影读入完成...")

mix_sim = mix_sim.sort_values(by=['movieId', 'simDegree'], ascending=[True, False])
mix_sim = mix_sim.loc[~mix_sim.duplicated(subset=['movieId', 'simId']), :]
movieIdList = mix_sim.movieId.unique()
mix_simOL = pd.DataFrame()
for i in movieIdList:
    tmp = mix_sim.loc[mix_sim.movieId == i, :].sort_values(by='simDegree', ascending=False)[:10]
    mix_simOL = pd.concat([mix_simOL, tmp])
print("在线推荐的预测相似电影筛选完成...")

simOL = pd.DataFrame({'movieId': mix_simOL['movieId'], 'simId': mix_simOL['simId']})
simOL.to_csv("../data/simOL.csv", index=False)
print("在线推荐的预测相似电影csv文件存储完成...")

pdt_svd = pd.read_csv("../data/pdtSVD.csv")
pdt_nmf = pd.read_csv("../data/pdtNMF.csv")
mix_pdt = pd.concat([pdt_svd, pdt_nmf])
print("在线推荐的预测高分电影读入完成...")

mix_pdt = mix_pdt.sort_values(by=['userId', 'pdtScore'], ascending=[True, False])
mix_pdt = mix_pdt.loc[~mix_pdt.duplicated(subset=['userId', 'recId']), :]
userIdList = mix_pdt.userId.unique()
mix_pdtOL = pd.DataFrame()
for i in userIdList:
    tmp = mix_pdt.loc[mix_pdt.userId == i, :].sort_values(by='pdtScore', ascending=False)[:10]
    mix_pdtOL = pd.concat([mix_pdtOL, tmp])
print("在线推荐的预测高分电影筛选完成...")

pdtOL = pd.DataFrame({'userId': mix_pdtOL['userId'], 'recId': mix_pdtOL['recId']})
pdtOL.to_csv("../data/pdtOL.csv", index=False)
print("在线推荐的预测高分电影csv文件存储完成...")
