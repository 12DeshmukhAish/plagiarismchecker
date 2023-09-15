


import os
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# List of pre-existing dataset files
dataset_files = [
     "C:/Users/deshm/OneDrive/Desktop/report1.docx",
    "C:/Users/deshm/OneDrive/Desktop/report2.docx"
]

def calculate_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix[0, 1]

def compare_text(uploaded_text):
    for dataset_file in dataset_files:
        if os.path.exists(dataset_file):
            try:
                with open(dataset_file, "rb") as file:
                    dataset_text = file.read().decode("utf-8", errors="ignore")
                    similarity = calculate_cosine_similarity(uploaded_text, dataset_text)
                    if similarity >= 0.5:
                        return f"The uploaded text is at least 30% similar to the dataset in {dataset_file}."
            except Exception as e:
                continue
    return "The uploaded text is different from all the pre-existing datasets."

# Create the Flask app with an explicit template_folder
# path = "templates"
app = Flask(__name__, template_folder = "E:\\reactjs\\final\\templates")

# Route for the home page
@app.route("/")
def home():
    return render_template('up.html', result=' ')

# Route for handling file upload and comparison
@app.route('/compare', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        uploaded_text = file.read().decode("utf-8", errors="ignore")
        result = compare_text(uploaded_text)  # Call the compare_text function
        return render_template('up.html', result=result)

    return "Error handling file upload"  # Handle unexpected error
if __name__ == "__main__":
    app.run(debug=True)