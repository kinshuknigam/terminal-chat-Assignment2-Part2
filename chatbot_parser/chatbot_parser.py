from flask import Flask, request, jsonify
import json, requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/chatbot"
db = SQLAlchemy(app)

class commands(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # print("********** 3 *******************")
    command = db.Column(db.String(20),primary_key=True)
    # print("********** 4 *******************")
    server_url = db.Column(db.String(200))
    # print("********** 5 *******************")
    # breed = db.Column(db.String(80))

    def to_dict(self):
        # print("********** 6 *******************")
        return {
            # 'id': self.id,
            'command': self.command,
            'server_url': self.server_url
            # 'breed': self.breed
        }

@app.route('/message', methods = ['POST'])
def quote_post():
    data = request.get_json()
    # print(data)
    # main_msg = data.get("data")
    main_msg = data['data']['message']
    substring = ' '
    index = main_msg.find(substring)

    if main_msg[0] == "/" and main_msg.find(' ') != -1:
        command = main_msg[0:index]
        message = main_msg[index+1:]
    elif main_msg[0] == "/" and main_msg.find(' ') == -1:
        command = main_msg
        message = ""
    else:
        command = ""
        message = main_msg
    
    

    # print(command[1:],message)
    # new_data={"data": {"command": "shrug", "message": "This is a test" }}
    if command[1:]=="shrug" or command[1:]=="email":
        print("**********************",command,message)
        
        
        cats = commands.query.all() 

        print(("**********************",222222222222))
        cat_dict = {}
        for cat in cats:
            cat_dict[cat.command] = cat.server_url
        
        
        # with open('./serverMapping.json', 'r') as f:
            # json_data = json.load(f)
    
        url_prep = cat_dict[command[1:]]+"/execute"
        new_data = {"data": {"command": command[1:], "message": message}}
        new_data = json.dumps(new_data)
        print(url_prep," + ",new_data)

        response = requests.post(url=url_prep, data=new_data)
        response_code = 200
    # print("R1",response.json())
        return jsonify(response.json()), response_code
        
        
    # elif command[1:]=="email":
    #     new_data = {"data": {"command": command[1:], "message": message}}
    #     new_data = json.dumps(new_data)
    #     response = requests.post(url="", data=new_data)
    #     response_code = 200

    else:
        response = {"data":{"command": command[1:], "message": message}}
        response_code = 200
        # print("R2",response)
    
    # print(response, "jiiii")
        return jsonify(response), response_code


@app.route('/register', methods = ['POST'])
def quote_register():
    input_data = request.get_json()
    print(("**********************",input_data))
    # print(data)
    # main_msg = data.get("data")
    command = input_data['data']['command']
    server_url = input_data['data']['server_url']

    print(("**********************",1111111111111))

    new_Quote = commands(command=command, server_url=server_url)
    db.session.add(new_Quote) # Allows us to add/post new rows to the table

    print(("**********************",222222222222))
    try:
        print(("**********************",33333333333))
        db.session.commit() # Ensures that the data is actually written to the table - ACID properties anyone?
        return jsonify(new_Quote.to_dict())
    except IntegrityError as e:
        db.session.rollback()
        existing_quote = commands.query.filter_by(command=command).first()
        existing_quote.server_url = server_url
        db.session.commit()
        return jsonify(existing_quote.to_dict())
    
    # with open('serverMapping.json', 'r') as f:
    #     json_data = json.load(f)

    #     json_data[command]=server_url
    
    #     with open('serverMapping.json', 'w') as f:
    #         json.dump(json_data, f)

    
    response = {"data": {"command": command, "message": "saved"}}

    response_code = 200
    return jsonify(response), response_code



if __name__ == '__main__':
    app.run(port=5050, host='0.0.0.0',debug=True )