from flask import Flask,render_template,request
import pickle
import numpy as np

merged=pickle.load(open('models/merged_df.pkl', 'rb'))
pt=pickle.load(open('models/pt.pkl', 'rb'))
anime_dt=pickle.load(open('models/anime_dt.pkl', 'rb'))
similarity_scores=pickle.load(open('models/similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           anime_name=list(merged['Name'].values),
                           score=list(merged['score'].values),
                           scored_by=list(merged['scored_by'].values),
                           Genres=list(merged['Genres'].values),
                           Studios=list(merged['Studios'].values),
                           image=list(merged['Image URL'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_animes',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = anime_dt[anime_dt['Name'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Name')['Name'].values))
        item.extend(list(temp_df.drop_duplicates('Name')['Genres'].values))
        item.extend(list(temp_df.drop_duplicates('Name')['Image URL'].values))
        item.extend(list(temp_df.drop_duplicates('Name')['Studios'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)



if __name__ == '__main__':
    app.run(debug=True)