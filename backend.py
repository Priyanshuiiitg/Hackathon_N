import os
import openai
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load your OpenAI API key from the .env file
openai.api_key = os.getenv("API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]
    
    # Send user input to OpenAI GPT-3 model
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="You are  an Educational Chatbot for Juniors: Empowering Students to Navigate Academic and Non-Academic Challenges .I want you to serve as a dependable and accessible resource for junior students and try to give answers as much interactive as possible  and now  the next few lines will user input process them: `"+   user_input+"`",
        max_tokens=50  # Adjust this based on your needs
    )
    
    bot_response = response.choices[0].text.strip()
    from bardapi import Bard

    bard = Bard(token='bQgxCfPTL1GwyoIr0s7tme5TDIaKrFwFVPY2pby6H6Sg1vnto5CbPmaau7Q06nFs6SI3fg.')
    audio = bard.speech(bot_response)
    with open("speech.mp3", "wb") as f:
        f.write(bytes(audio['audio']))
    return jsonify({"bot_response": bot_response})


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files['image']
        

        if 'image' not in request.files or not uploaded_file:
            return jsonify({'error': 'No file selected'})

        if uploaded_file and allowed_file(uploaded_file.filename):
            # Save the uploaded file to the UPLOAD_FOLDER
            filename = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(filename)

            # You can perform further processing here if needed
            # print(uploaded_file.filename)
            from bardapi import Bard
            bard=Bard(token='bQgxCfPTL1GwyoIr0s7tme5TDIaKrFwFVPY2pby6H6Sg1vnto5CbPmaau7Q06nFs6SI3fg.')
            image=open(uploaded_file.filename,'rb').read()
            answer=bard.ask_about_image("what is in image or what is solution of this image and give answers in 4-5 lines",image)
            print(answer['content'])
            return jsonify({'message': answer['content']})
        else:
            return jsonify({'error': 'Invalid file format. Allowed formats: jpg, jpeg, png, gif'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
