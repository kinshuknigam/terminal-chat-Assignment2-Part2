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

   
    if command == "email":   # REPLACE - Put in separate file
        all_words = main_msg.split()
        from_email = "rishabhmthakur2@gmail.com"
        # from_email = "kinshuk_nigam@berkeley.edu"
        to_email= all_words[0]
        subject = all_words[1]
        body= ' '.join([str(elem) for elem in all_words[2:]])
        print(to_email," + ",subject," + ",body)
        main_msg2 = "Testingggggg"

        if not to_email or not from_email or not subject or not body:
            main_msg2=  "Please fill out all fields to send an email"
            response_code = 400  
        else:
            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                html_content=body)
            try:
                # print("*********DONE************")  # REPLACE
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                sg.send(message)
                # response = {"message": "Email was sent"}
                main_msg2 = "Email was sent"
                response_code = 200
            except Exception as e:
                logging.error(e)
        
        


    # print(main_msg2)
    response = {"data":{"command": command, "message": main_msg2}}
    # print("response",response)
    # print("response jsonify",jsonify(response))
    response_code = 200
    return jsonify(response) , response_code


if __name__ == '__main__':
    app.run(port=5052, host='0.0.0.0',debug=True )
