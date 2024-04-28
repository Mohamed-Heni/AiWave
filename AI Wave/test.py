import vertexai
import os
from vertexai.preview.generative_models import GenerativeModel, Image
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase app

cred = credentials.Certificate("C:\\Users\\Lenovo\\Desktop\\AI Wave\\ai-wave-421620-firebase-adminsdk-9pjnl-d82ffffc15.json")


firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ai-wave-421620-default-rtdb.firebaseio.com/'
})
# Get a reference to the database
ref = db.reference()
peoples_ref = ref.child("peoples")
PROJECT_ID = "ai-wave-421620"
REGION = "us-central1"
vertexai.init(project=PROJECT_ID, location=REGION)

generative_multimodal_model = GenerativeModel("gemini-pro")

def create_object_from_string(s):
    keys = ['name', 'gender', 'socialSkill','domain','Score']  # Assuming these are the keys you want
    values = s.split('|')
    return {key: value for key, value in zip(keys, values)}
folder_path = "C:\\Users\\Lenovo\\Desktop\\AI Wave\\Cv"
def list_files(folder_path):
    # Iterate over all the files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "rb") as f: 
                pdf_content = f.read()
            response = generative_multimodal_model.generate_content(f"giving this : {pdf_content}  give me an output exactly like this no word less no word more no comments nothig just this and don't usne any talble or any to indicate the colum (it will be use for a database so don't add any thing): Name|Gender|social Skill on scale of 10 (just write a number from 1 to 10) | speciality(computer scence , medicine....)| over all score(just a number on scale of 1000)")
            content_text = response.candidates[0].content.parts[0].text
            content_text=create_object_from_string(content_text)
            new_people=peoples_ref.push(content_text)
            print(content_text)

def sort_by_score(arr):
    # Convert the 'Score' attribute to integers for proper sorting
    for item in arr:
        item['Score'] = int(item['Score'])

    # Sort the array of objects based on the 'Score' attribute
    sorted_arr = sorted(arr, key=lambda x: x['Score'], reverse=True)

    return sorted_arr
def creat_tri_file():
    poeples_snapshot = peoples_ref.get()
    data=poeples_snapshot.items()
    T=[]
    for _, values in data:
        T.append(values)
    T=sort_by_score(T)
    with open("C:\\Users\\Lenovo\\Desktop\\AI Wave\\top_poeples.txt","w") as file:
        for item in T:
            # Construct the formatted string for each object
            formatted_string = f"Name: {item['name']}   Gender: {item['gender']}   Social Skill: {item['socialSkill']}   Speciality: {item['domain']}   Score: {item['Score']}\n"
            # Write the formatted string to the text file
            file.write(formatted_string)
list_files(folder_path)
creat_tri_file()
        

        