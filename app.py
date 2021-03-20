from flask import Flask,jsonify,render_template,request
import json

import tools.ConnectDB as DB

app = Flask(__name__)

# Main index
@app.route('/')
def Index():
    return render_template('index.html')

# all user pages 
@app.route('/users',methods=['GET'])
def users():
    with open('datasets/db_users_details.json') as f:
        data = json.load(f)
    return jsonify(data)

# a user page
@app.route('/users/<string:user_name>',methods=['GET'])
def getUser(user_name):
    with open('datasets/db_users_details.json') as f:
        data = json.load(f)
    user = [user  for user in data if user['UserName']== user_name]
    print(user)
    return jsonify(user)

# add new user pages 
@app.route('/add_user',methods=['POST'])
def add_user():
    if request.method == 'POST':

        PC       = request.form['PC']        
        UserName = request.form['UserName']

        # 0 = good
        # 1 = Bad Post Code 
        # 2 = UserName already exist

        try:
            cod = DB.communications(UserName,PC)
            if cod == 0:
                r = jsonify({'error_code':'0','messaje':'received and save!'})
            elif cod == 1:
                r = jsonify({'error_code':'1','message':'The post code doesn''t exist'})
            elif cod == 2:
                r = jsonify({'error_code':'2','message':'The User already exist'})
        except:
            r = jsonify({'error_code':'3','message':'Unknown Error '})
        return r

if __name__ == '__main__':
    app.run(debug=True,port=4000) 