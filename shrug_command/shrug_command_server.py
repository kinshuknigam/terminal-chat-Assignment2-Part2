from flask import Flask, request, jsonify
import json

import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)



@app.route('/execute', methods = ['POST'])
def quote_post():
    # data = request.get_json()
    data = json.loads(request.data)
    command = data['data']['command']
    main_msg = data['data']['message']

    # print(command,main_msg)
    if command == "shrug":
        # main_msg2 = f"{main_msg}¯\_(ツ)_/¯"
        main_msg2 = main_msg+ "¯\_(ツ)_/¯"
    
    
    # print(main_msg2)
    response = {"data":{"command": command, "message": main_msg2}}
    # print("response",response)
    # print("response jsonify",jsonify(response))
    response_code = 200
    return jsonify(response) , response_code


if __name__ == '__main__':
    app.run(port=5051, host='0.0.0.0',debug=True )
