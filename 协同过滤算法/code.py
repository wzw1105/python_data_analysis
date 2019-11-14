xiex#coding=utf-8
'''
基于用户的推荐算法
'''
import pandas as pd

# 向给定用户推荐（返回：pd.Series）
def recommend(user_id):
    # 找到距离最近的用户id
    nearest_user_id = computeNearestNeighbor(user_id, metric='cosine').index[0]
    print('最近邻用户id：' + str(nearest_user_id))
    # 找出邻居评价过、但自己未曾评价的乐队（或商品）
    # 结果：index是商品名称，values是评分
    #就是推荐原用户没有看过的但是在相似用户看过的电影集合里面
    recommendList = df.loc[nearest_user_id, df.loc[user_id].isnull() & df.loc[nearest_user_id].notnull()].sort_values()
    return recommendList

# 计算最近的邻居
def computeNearestNeighbor(user_id, metric='cosine', k=5):
    """
    metric: 度量函数
    k:      返回k个邻居
    返回：pd.Series，其中index是邻居名称，values是距离
    """
    return df.drop(user_id).index.to_series().apply(cosine, args=(user_id,)).nlargest(k)

# 余弦相似度
def cosine(user_id1, user_id2):
    x, y = build_xy(user_id1, user_id2)
    # 分母
    denominator = (sum(x*x)*sum(y*y))**0.5
    try:
        value = sum(x*y)/denominator
    except ZeroDivisionError:
        value = 0
    return value

# 构建共同的评分向量
def build_xy(user_id1, user_id2):
        bool_array = df.loc[user_id1].notnull() & df.loc[user_id2].notnull()
        return df.loc[user_id1, bool_array], df.loc[user_id2, bool_array]

def main():
    rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_table('ml_1m/ratings.dat', sep='::', header=None, names=rnames,
                            usecols = [0,1,2],engine='python')
    mnames = ['movie_id', 'title', 'genres']
    movies = pd.read_table('ml_1m/movies.dat', sep='::', header=None, names=mnames,
                            usecols = [0,1],engine='python')
    data = pd.merge(ratings, movies)
    global df
    # 转换成User-Item矩阵
    df = ratings.pivot(index='user_id', columns='movie_id', values='rating')
    #print(df)
    print('The avaliable id list of the option')
    print('q: quit the process')
    print('1: show the rating of the movie both for usera and userb')
    print('2: show the similarity degree of the two users')
    print('3: show the 5 most similarest users of the given user')
    print('4: recommend the movies according to the given users')
    while(True):
    	opt=input('Please input the id of your option: ')
    	if(opt=='q'):
    		break
    	elif(opt=='1'):
    		usera,userb=map(int,input('Please input the name_id of two users: ').split())
    		result=build_xy(usera,userb)
    		print('movie-id rating-usera rating-userb')
    		for i,v in result[0].items():
    			print(i,'       ',v,'        ',result[1][i])
    	elif(opt=='2'):
    		usera,userb=map(int,input('Please input the name_id of two users: ').split())
    		print('-> The similarity degree of two users is: ',cosine(usera,userb))
    	elif(opt=='3'):
    		user=int(input('Please input the name_id of the user:'))
    		result=computeNearestNeighbor(user)
    		print('-> The top 5 most-similarest users are: ',end='')
    		print(result.index.tolist())
    	elif(opt=='4'):
    		user=int(input('Please input the name_id of the user:'))
    		result=recommend(user)
    		print('The movies recommend to user ',user,' are: ',end='')
    		print(result.index.tolist())

if __name__ == '__main__':
    main()