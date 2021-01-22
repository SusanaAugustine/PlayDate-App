from flask import Flask, request, redirect, render_template
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)

class DataStore():
    data = None
    data1 = None
    data2 = None
    data3 = None

data0 = DataStore()

def play_data(n, v, o, g, a, b, w, c, bo, d, t, l, ap, wh, own, dog, be, y, ad, ow, dw, go):
    import pandas as pd
    import numpy as np
    import itertools # This is a python standard library does not need to be install...is there by default when you install python.
    from sklearn.metrics.pairwise import cosine_similarity
    
    #read the csv file
    df = pd.read_csv(r"C:/Users/User/Desktop/PlayDate/Doggo.csv")
    
    #parameters
    a = float(a)
    w = float(w)
    ow = float(ow)
    dw = int(dw)
    
    #generating Dog_Id
    Dog_Id = 'PD' + str(df.shape[0]+1)
    
    #add all data in a list
    data = [Dog_Id, n, v, o, g, a, b, w, c, bo, d, t, l, ap, wh, own, dog, be, y, ad, ow, dw, go]
    
    #creating a dataframe of the data
    data = pd.DataFrame([data], columns = ['Dog ID', 'Name of your dog', 'Vaccinated', 'Owner Name', 'Gender',
       'Age (in months)', 'Breed', 'Weight (in kg)', 'Character', 'Body type',
       'Diet', 'Temperament with other pets', 'House Location (Area name)',
       'Would you like a PlayDate app for your doggo?',
       'Why would you use a PlayDate app for your doggo?',
       'What traits would you look for in the parents of your date?',
       'What traits would you look for in your dogs  date?',
       'How do you think this will benefit your doggo?',
       'How are you with your doggo?',
       'How comfortable are you with other dogs other than your own?',
       'Owner Age (in Years)', 'Number of doggs you own',
       'How often does your dog like to go out?'])
    df=df.append(data,ignore_index=True)
    
    #preprocessing the data
    similarity_computation_df = pd.DataFrame(pd.concat(
    [
        df[["Dog ID", "Age (in months)", "Weight (in kg)", 'Owner Age (in Years)', 'Number of doggs you own','How comfortable are you with other dogs other than your own?']],
        pd.get_dummies(df[['Vaccinated','Gender', 'Breed', 'Character', 'Body type',
       'Diet', 'Temperament with other pets', 'House Location (Area name)','Why would you use a PlayDate app for your doggo?',
       'What traits would you look for in the parents of your date?',
       'What traits would you look for in your dogs  date?',
       'How do you think this will benefit your doggo?',
       'How are you with your doggo?',
       'How often does your dog like to go out?']], drop_first = True)
    ], 
    axis = 1
    ))
    
    #creates a list of all the unique dog_ids
    dog_ids = df["Dog ID"].unique() 
    
    def generate_combinations(dog_id_list):
        combinations = dict(itertools.combinations(dog_id_list, r=2))
        return combinations

    combinations_dict = generate_combinations(dog_ids)
    
    #finding the similar dogs
    similarity_df = pd.DataFrame()
    for dog_id in dog_ids:
        if dog_id in combinations_dict.keys():
            dog_id_02 = combinations_dict[dog_id]
            row_01 = similarity_computation_df[similarity_computation_df["Dog ID"] == dog_id].iloc[:,1:].values
            row_02 = similarity_computation_df[similarity_computation_df["Dog ID"] == dog_id_02].iloc[:,1:].values
            #print("Currently processing the combination of {} - {}".format(dog_id, dog_id_02))
            similarity_score = cosine_similarity(row_01, row_02)[0]
            temp_df = pd.DataFrame({ "Dog_id_01": dog_id, "Dog_id_02": dog_id_02, "similarity_matrix": similarity_score })
            similarity_df = similarity_df.append(temp_df)
            
    #sorting the dogs accoring to the highest similarity
    Sorted = similarity_df.sort_values(by=['similarity_matrix'], ascending=False)
    
    #for display purpose        
    table = []
    for i in range(10):
        for j in range(len(df)):
            table2 = []
            if(Sorted.iloc[i][0] == df.iloc[j][0]):
                for k in range (8):
                    table2.append(df.iloc[j][k])
                table.append(table2)
    display = pd.DataFrame(table, columns = ['Dog_Id','Name of your dog', 'Vaccinated', 'Owner Name', 'Gender',
       'Age (in months)', 'Breed', 'Weight (in kg)'])
    
    return display
def collabrative(input1,display):
    import pandas as pd
    df = pd.read_csv(r"C:/Users/User/Desktop/PlayDate/Doggo.csv")
    df1 = pd.read_csv(r"C:/Users/User/Desktop/PlayDate/Userssearch.csv")
    input1 = pd.DataFrame(input1, columns = ['Input'])
    input1 = pd.concat([display, input1], axis=1, sort=False)
    insert = []
    for i in range (len(input1)):
        if (input1.iloc[i][8] == 'Like'):
            insert.append(input1.iloc[i][0])
    cf = []
    for i in range (len(insert)):
        for j in range (len(df1)):
            for k in range (1,5):
                if (insert[i] == df1.iloc[j][k]):
                    cf.append(df1.iloc[j][0])
    
    table1 = []
    for i in range (len(cf)):
        for j in range (len(df)):
            table3 = []
            if (df.iloc[j][0] == cf[i]):
                for k in range (8):
                    table3.append(df.iloc[j][k])
                table1.append(table3)
    display2 = pd.DataFrame(table1, columns = ['Dog_Id','Name of your dog', 'Vaccinated', 'Owner Name', 'Gender',
               'Age (in months)', 'Breed', 'Weight (in kg)'])
    return(display2)

@app.route('/')
def playdate():
    return render_template('PlayDate.html')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
	name = request.form['dogname']
	gender = request.form['Gender']
	age = request.form['age']
	vaccinated = request.form['vaccinated']
	breed = request.form['breed']
	weight = request.form['weight']
	character = request.form['character']
	bodytype = request.form['bodytype']
	diet = request.form['diet']
	temprament = request.form['temprament']
	ownername = request.form['ownername']
	locname = request.form['locname']
	app1 = request.form['app1']
	whyapp = request.form['whyapp']
	ownertra = request.form['ownertra']
	dogtra = request.form['dogtra']
	benefit = request.form['benefit']
	yourdog = request.form['yourdog']
	app2 = request.form['app2']
	ownerage = request.form['ownerage']
	dogno = request.form['dogno']
	goout = request.form['goout']

	data = play_data(n=name, v=vaccinated, o=ownername, g=gender, a=age, b=breed, w=weight, c=character, bo=bodytype, d=diet, t=temprament, l=locname, ap=app1, wh=whyapp, own=ownertra, dog=dogtra, be=benefit, y=yourdog, ad=app2, ow=ownerage, dw=dogno, go=goout)
	data0.data = data
	return render_template("display.html", data=data)
  #return render_template('display.html',  tables=[classes='data', header="true"])

@app.route('/search2', methods=['GET', 'POST'])
def search2():
  inp1 = request.form
  input1 = list()
  for k,v in inp1.items():
    input1.append(v)
  data1 = collabrative(input1, data0.data)
  data0.data1 = data1
  return render_template("collabrative.html",len=len(data1), data=data1)

@app.route('/search3', methods=['GET', 'POST'])
def search3():
  inp2 = request.form
  input2 = list()
  for k,v in inp2.items():
    input2.append(v)
  data2 = collabrative(input2, data0.data1)
  data0.data2 = data2
  return render_template("collabrative2.html",len=len(data2), data=data2)

@app.route('/search4', methods=['GET', 'POST'])
def search4():
  inp3 = request.form
  input3 = list()
  for k,v in inp3.items():
    input3.append(v)
  data3 = collabrative(input3, data0.data2)
  
  return render_template("collabrative3.html",len=len(data3), data=data3)
if __name__ == '__main__':
	app.run(debug=True)