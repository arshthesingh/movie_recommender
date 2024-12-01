import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

movies_df = pd.read_csv('app/filtered_movies_data.csv')

movies_df['overview'] = movies_df['overview'].fillna('')

movies_df['title'] = movies_df['title'].str.lower()

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_df['overview'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(movies_df.index, index=movies_df['title']).drop_duplicates()

def get_recommendations(title):
    
    title = title.lower()
    
    idx = indices.get(title, None)
    
    if idx is None:
        return []  
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # 1: excludes the movie itself
    sim_scores = sim_scores[1:11]
    
    movie_indices = [i[0] for i in sim_scores]
    
    return movies_df['title'].iloc[movie_indices].tolist()
