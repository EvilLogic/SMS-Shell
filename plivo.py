from flask import Flask, request, make_response, Response
import plivo, plivoxml
import subprocess

app = Flask(__name__)

@app.route('/plivo.py',methods=['GET','POST'])
@app.route('/forward_sms/', methods=['GET','POST'])
def inbound_sms():
    # Sender's phone number
    from_number = request.values.get('From')
    # Receiver's phone number - Plivo number
    to_number = request.values.get('To')
    # The text which was received
    text = request.values.get('Text')

    # Print the message
    print('Message received - From: %s, To: %s, Text: %s' % (from_number, to_number, text))

    # Lower text (CASE)
    text = text.lower()

    # Check for links error
    #if 'links' in text:
    #    return

    # Send the message to the system
    p = subprocess.Popen(text, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

    # Wait and construct response
    p_status = p.wait()
    comCode = "Command output : " + output
    comCode = comCode + "Code : " + str(p_status)

    # Generate a Message XML with the details of the reply to be sent
    resp = plivoxml.Response()

    # The phone number to which the SMS has to be forwarded
    # to_forward = 'my phone#redacted'
    body = comCode
    params = {
        'src' : to_number, # Sender's phone number
        'dst' : from_number, # Receiver's phone number
    }

    # Message added
    resp.addMessage(body, **params)

    # Prints the XML
    print(resp.to_xml())
    # Returns the XML
    return Response(str(resp),mimetype='text/xml')

if __name__ == "__main__":
    app.run(host='192.168.2.30', port=80)
