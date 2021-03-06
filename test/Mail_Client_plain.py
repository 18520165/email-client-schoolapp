from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

def get_customer_information(filename):
	customer = []

	with open(filename, mode = 'r', encoding = 'utf-8') as line:
		for info in line.read().splitlines():
			temp_info = info.split('|')
			customer.append({'name': temp_info[0], 'email': temp_info[1]})

	return customer

def get_template(filename):
	with open(filename, mode = 'r', encoding = 'utf-8') as template_content:
		temp_content = template_content.read()

		return Template(temp_content)

if __name__ == "__main__":
	customers = get_customer_information('listmails.txt')
	message_template = get_template('templatemail.txt')
	smtp_info = {
	'SMTP_ENCRYPT': 'tls',
	'SMTP_ADDRESS': 'smtp.gmail.com',
	'SMTP_PORT': 587,
	'MAIL_LOGIN': 'nhanth240500@gmail.com',
	'MAIL_PASSWORD': '0977177687Nhan',
	}

try:
		if smtp_info.get('SMTP_ENCRYPT', "tls"):
			s = smtplib.SMTP(host = smtp_info.get('SMTP_ADDRESS'), port = smtp_info.get('SMTP_PORT'))
			s.starttls()
		else:
			s = smtplib.SMTP_SSL(host = smtp_info.get('SMTP_ADDRESS'), port = smtp_info.get('SMTP_PORT'))
			s.ehlo()

		s.login(smtp_info.get('MAIL_LOGIN'), smtp_info.get('MAIL_PASSWORD'))

		for customer in customers:
			customer_name = customer.get('name').lower().title()
            
			msg = MIMEMultipart()
			message = message_template.substitute(CUSTOMER_NAME = customer_name)
            
			msg['From'] = smtp_info.get('MAIL_LOGIN')
			msg['To'] = "{0} <{1}>".format(customer_name, customer.get('email'))
			msg['Subject'] = "Chào {0}. Bạn nhận được một mail từ Hoàng Nhân".format(customer_name)
			msg.attach(MIMEText(message, 'plain'))
			s.send_message(msg)
			del msg
			logging.info("Gửi mail cho {0} thành công".format(customer.get('email')))

		s.quit()
except smtplib.SMTPException as e:
	logging.error("Không thể gửi mail. Chi tiết: {0}".format(e))

smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login('nhanth240500@gmail.com', '0977177687Nhan')
