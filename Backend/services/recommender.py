import pickle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

vector_path = BASE_DIR / "vectors.pkl"
similarity_path = BASE_DIR / "similarity.pkl"

vectors = pickle.load(open(vector_path, "rb"))
similarity = pickle.load(open(similarity_path, "rb"))

def Recommend(movie):
    
    index=vectors[vectors["title"]==movie].index[0]
    distance=similarity[index]
    distance=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])
    top=[]
    recommended_movies=[]
    for i in range(1,6):
        top.append(distance[i][0])
    for i in top:
        recommended_movies.append(vectors["title"].iloc[i])
    print(recommended_movies)
    return recommended_movies