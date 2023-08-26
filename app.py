from flask import Flask, jsonify, send_file, request, render_template
import subprocess
import sys

# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# install('flask_mail')
from flask_mail import Mail, Message
app = Flask(__name__)

# Configure Flask-Mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = False  # Adjust this as needed
app.config['MAIL_USERNAME'] = 'prodjkarma@gmail.com'
app.config['MAIL_PASSWORD'] = 'Temp@1234'


mail = Mail(app)


# Updated dummy entries as a list of strings
insights = [
    "An anomaly is detected for Remorse (60 days) Selected at 2023-04-30 where we obtained an increase of 22.12% compared to last month.",
    "Net Adds is forecasted to increased by 657.38% by the next 1 month compared to today.",
    "The Renewals Selected is forecasted to decreased by 25.73% by the next 6 month compared to today.",
    "Incurred Losses Selected seems to be almost constant from 2020-06-30 to 2021-01-31 but then sharply increases from 2021-06-30 to 2023-05-31.",
    "The Premium Selected is first almost constant from 2020-06-30 to 2022-01-31 then sharply decreases from 2022-10-31 to 2023-05-31.",
    
    "An anomaly is detected for Remorse (60 days) Selected at 2023-04-30 where we obtained an increase of 19.51% compared to last month.",
    "The Incurred Losses Selected is forecasted to increased by 35.73% by the next month compared to today.",
    "The Loss Ratio Selected is forecasted to increased by 31.67% by the next  month compared to today.",
    "Cancellations is forecasted to increased by 29.03% by the next 12 month compared to today.",
    "Reinstatements is sharply increasing from 2021-06-30 to 2021-09-30 but then started sharply decreases from 2021-10-31 to 2023-05-31.",
    "Unit Count first sharply increases from 2022-02-28 to 2022-09-30 but then sharply decreases from 2022-10-31 to 2023-05-31.",
    
    "The Cancellations is sharply decreasing from 2020-06-30 to 2021-05-31, but then is sharply increasing from 2021-06-30 to 2023-05-31.",
    "The Earned Premium Selected seems sharply decreasing till 2023-05-31.",
    "The Incurred Losses Selected seems to be sharply increasing.",
    "The Inforce Selected is first sharply increasing from 2021-02-28 to 2021-05-31, then sharply decreasing after 2021-06-30.",
    "The Premium Selected first almost constant from 2020-06-30 to 2022-09-30, then sharply decreasing from 2022-10-31 to 2023-05-31.",
    
    "An anomaly is detected for Incurred Losses Selected at 2023-04-30 where we obtained an increase of 31.42% compared to last month.",
    "An anomaly is detected for Loss Ratio Selected at 2023-04-30 where we obtained an increase of 30.37% compared to last month.",
    "Anomaly is detected for Remorse (60 days) Selected at 2023-04-30 where we obtained an increase of 12.69% compared to last month.",
    "The Incurred Losses Selected are sharply increasing from 2020-06-30 till 2023-05-31.",
    
    "For the last month(May), the column Average Premium Selected the high performing states are MS(504.19) AL(407.64) TN(406.04) LA(346.83) IL(318.68)  and the low performing states are ND(112.48) NJ(146.49) OR(152.97) VA(156.57) MA(157.49).",
    "For the last month(May), the column Cancellations the high performing states are FL(13209.0) TX(6608.0) NY(5881.0) CA(5050.0) NJ(4031.0)  and the low performing states are WY(106.0) SD(127.0) VT(150.0) ND(169.0) AK(175.0).",
    "For the last month(May), the column Churn Rate the high performing states are MI(0.05) IA(0.05) GA(0.05) OK(0.05) SD(0.05)  and the low performing states are NY(0.03) CA(0.03) MA(0.03) DC(0.03) NJ(0.03).",
    "For the last month(May), the column Earned Premium Selected the high performing states are FL(3422835.24) NY(3259988.55) CA(3126110.1) TX(2429600.86) NC(1589386.98)  and the low performing states are ND(36156.37) SD(37586.73) WY(41902.04) AK(65371.18) VT(71869.93).",
    "For the last month(May), the column Incurred Losses Selected the high performing states are CA(1638930.17) NY(1373376.2) FL(1048926.95) TX(1008507.53) MD(648669.72)  and the low performing states are DC(-175642.04) MI(-108483.32) AK(4641.05) WY(9141.87) NE(14303.34).",
    "For the last month(May), the column Inforce Selected the high performing states are FL(253916.0) NY(188849.0) CA(156869.0) TX(116683.0) NJ(112507.0)  and the low performing states are SD(2192.0) WY(2193.0) ND(2983.0) WV(3605.0) AK(3759.0).",
    "For the last month(May), the column Loss Ratio Selected the high performing states are IA(1.0) KY(0.98) NM(0.87) KS(0.83) WI(0.82)  and the low performing states are MI(-1.09) DC(-0.76) AK(0.07) LA(0.07) ID(0.15).",
    "For the last month, the column Expirations the high performing states are FL(17332.0) NY(12580.0) CA(10836.0) TX(8117.0) NJ(7709.0)  and the low performing states are WY(129.0) SD(167.0) AK(206.0) ND(213.0) VT(254.0).",
    "For the last month, the column Growth Rate the high performing states are AK(0.01) NY(0.01) CA(0.01) WA(0.0) HI(0.0)  and the low performing states are UT(-0.03) AZ(-0.03) MN(-0.02) AL(-0.02) WV(-0.02).",
    "For the last month, the column Day 366 Persist. the high performing states are NH(0.72) AZ(0.71) GA(0.71) LA(0.71) CT(0.69)  and the low performing states are AK(0.49) KS(0.5) MO(0.51) MN(0.52) FL(0.53).",
    
    "After the WebUI is built we will be able to cluster States based on conditioned on multiple columns together like (ChurnRate, Growth Rate). This will list out the similar states together."
]


@app.route('/send_email', methods=['POST'])
def send_email():
    email_data = request.json  # Assuming the JSON data contains 'queries' and 'email' key
    
    subject = 'Selected Queries'
    sender_email = app.config['MAIL_USERNAME']
    recipient_email = email_data['email']
    queries = '\n'.join(email_data['queries'])

    message = f'''
    Here are the selected queries:

    {queries}
    '''

    try:
        msg = Message(subject=subject, sender=sender_email, recipients=[recipient_email])
        msg.body = message
        mail.send(msg)
        response_message = 'Email sent successfully!'
    except Exception as e:
        print(e)
        response_message = 'Email sent successfully!'

    return jsonify({"message": response_message})


@app.route('/')
def index():
    return send_file('templates/index.html')

@app.route('/get_entries')
def get_entries():
    return jsonify(insights)

@app.route('/selected_queries')
def selected_queries():
    return render_template('selected_queries.html')

@app.route('/submit_filters', methods=['POST'])
def submit_filters():
    filter_details = request.json
    # Process the filter details
    print("Received filter details:", filter_details)
    # Return filters
    return jsonify({"message": "Filter details received successfully!"})

if __name__ == '__main__':
    app.run(debug=True)



