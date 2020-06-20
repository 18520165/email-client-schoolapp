from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import smtplib, email, base64, os

import crypta


def display_send_mail(username, password, list_reciever=None):
    GUI_send_mail = Tk()
    GUI_send_mail.title("Gửi Mail")
    GUI_send_mail.geometry("700x625")
    GUI_send_mail.resizable(0, 0)

    def event_pressed_back():
        GUI_send_mail.destroy()
        import navigation

        navigation.display_navigation(username, password)

    def event_pressed_send():
        send_mail_func(
            username,
            password,
            entry_to.get(),
            entry_subject.get(),
            entry_message.get(0.0, END),
            filepaths.get().split(", "),
            combobox_select_crypto.get(),
        )

    #### Nhóm "Mail người nhận"
    # Label "To"
    label_to = Label(GUI_send_mail, text="To:")
    label_to.place(x=20, y=20)

    # Label "Subject"
    label_subject = Label(GUI_send_mail, text="Subject:")
    label_subject.place(x=20, y=60)

    # Label "message"
    label_message = Label(GUI_send_mail, text="Message:")
    label_message.place(x=20, y=100)

    # Option Encryption
    label_attachments = Label(GUI_send_mail, text="Attachments:", width=100)
    label_attachments.place(x=20, y=350)

    # Option Encryption
    label_encryption = Label(GUI_send_mail, text="Encryption:", width=100)
    label_encryption.place(x=20, y=380)

    label_key = Label(GUI_send_mail, text=f"Key:")
    label_key.place(x=20, y=410)

    label_iv = Label(GUI_send_mail, text=f"IV:")
    label_iv.place(x=340, y=410)

    label_recipient_key = Label(GUI_send_mail, text=f"Recipient public key:")
    label_recipient_key.place(x=20, y=520)

    label_rsa_key = Label(GUI_send_mail, text=f"RSA keys:")
    label_rsa_key.place(x=20, y=460)

    # Text "Message"
    entry_message = Text(GUI_send_mail, wrap="word",)
    entry_message.place(x=100, y=100, width=500, height=230)

    # Entry "To"
    entry_to = Entry(GUI_send_mail)
    entry_to.place(x=100, y=20, width=230)

    # Entry "Subject"
    entry_subject = Entry(GUI_send_mail)
    entry_subject.place(x=100, y=60, width=230)

    combobox_select_crypto = Combobox(
        GUI_send_mail,
        values=["None", "Caesar", "Vigenere", "AES", "DES"],
        width=17,
        state="readonly",
    )
    combobox_select_crypto.current(0)
    combobox_select_crypto.place(x=100, y=380)

    entry_key = Entry(GUI_send_mail, width=35)
    entry_key.place(x=100, y=410)

    entry_iv = Entry(GUI_send_mail, width=35)
    entry_iv.place(x=385, y=410)

    entry_recipient_key = Entry(GUI_send_mail, width=35)
    entry_recipient_key.place(x=150, y=520)

    entry_rsa_pub = Entry(GUI_send_mail, width=35, state=DISABLED)
    entry_rsa_pub.place(x=150, y=460)

    entry_rsa_priv = Entry(GUI_send_mail, width=35, state=DISABLED)
    entry_rsa_priv.place(x=150, y=490)

    ###nhóm "chọn file"
    ###event_pressed_send "chọn file"
    def event_select_file():
        file_path = filedialog.askopenfilenames(
            parent=GUI_send_mail, title="Choose a file"
        )
        filepaths.configure(state=NORMAL)
        filepaths.insert(0, ", ".join(file_path))
        filepaths.configure(state=DISABLED)

    def event_pressed_generate_keys():
        rsa_keys = 

    # button "chọn file"
    button_file = Button(GUI_send_mail, text="Select file", command=event_select_file)
    button_file.place(x=525, y=350)

    filepaths = Entry(GUI_send_mail, width=55, state=DISABLED)
    filepaths.place(x=100, y=350)

    # Button send
    button_send = Button(GUI_send_mail, text="Generate RSA keys", command=event_pressed_generate_keys, width=20)
    button_send.place(x=470, y=460)

    # Button send
    button_send = Button(GUI_send_mail, text="Send", command=event_pressed_send)
    button_send.place(x=600, y=570)

    ### button để quay lại tab navigation
    button_back = Button(GUI_send_mail, text="Back", command=event_pressed_back)
    button_back.place(x=20, y=570)

    rsa_key = None

    def encrypt_for_exchanging(data, recipientPub, userPrivate):
        private_encrypted = crypta.RSA_Encrypt(data, userPrivate)
        public_encrypted = crypta.RSA_Encrypt(private_encrypted, recipientPub)

        return public_encrypted

    def send_mail_func(
        username,
        password,
        receiver_email="",
        Subject="",
        message="",
        list_file=[],
        crypto_type=None,
    ):
        port = 587
        smtp_server = "smtp.gmail.com"

        # Neu khong co nguoi nhan
        if receiver_email != "":

            # Neu message khong rong hoac co file dinh kem
            if message != "" or list_file[0] != "":
                bbc = receiver_email
                msg = MIMEMultipart()

                # msg = MIMEMultipart("alternative"); #Dùng khi gửi theo dạng html

                # Thông tin về From, To, Subject, Bcc của mail.
                msg["From"] = username
                msg["To"] = receiver_email
                msg["Subject"] = Subject
                msg["Bcc"] = bbc

                print("send mail")

                key = ""
                iv = ""

                # Neu message khong rong
                if message != "":
                    # Message của người gửi muốn người nhận nhận được
                    body_mail = message

                    if crypto_type:

                        if entry_key:
                            # encrypted_key = encrypt_for_exchanging(entry_key.get(), )
                            msg.add_header("CryptKey", entry_key.get())

                        if entry_iv:
                            msg.add_header("CryptInitial", entry_iv.get())

                        if crypto_type == "AES":
                            body_mail = crypta.AES_Encrypt(
                                body_mail, "0123456789abcdef", "0123456789abcdef"
                            )
                        elif crypto_type == "Caesar":
                            body_mail = crypta.Caesar_Encrypt(
                                body_mail, int(entry_key.get())
                            )[: len(body_mail) - 1]

                        elif crypto_type == "DES":
                            body_mail = crypta.DES_Encrypt(
                                body_mail, "12346578", "13245678"
                            )

                        elif crypto_type == "Vigenere":
                            body_mail = crypta.Vigenere_Encrypt(
                                body_mail, int(entry_key.get())
                            )

                    # Định dạng message của mail theo kiểu plain text và lưu vào message_mail
                    message_mail = MIMEText(body_mail, "html", "utf-8")
                    # part2 = MIMEText(html, "html")

                    # Đính kèm nội dung mail đang được lưu trong par1 vào msg
                    msg.attach(message_mail)

                # Neu co file dinh kem
                if list_file[0] != "":
                    attachments = list_file  # In same directory as script
                    # sau khi print ra thì filepath bị split mỗi kí tự thành 1 phần tử của list => sai
                    # cần fix lỗi chỗ này.

                    for i in range(0, len(attachments)):
                        file = attachments[i]
                        file_basename = os.path.basename(file)
                        # Open PDF file in binary mode
                        with open(file, "rb") as attachment:
                            # Add file as application/octet-stream
                            # Email client can usually download this automatically as attachment
                            file_mail = MIMEBase("application", "octet-stream")
                            file_mail.set_payload(attachment.read())

                        # Encode file in ASCII characters to send by email
                        encoders.encode_base64(file_mail)

                        # Add header as key/value pair to attachment part
                        file_mail.add_header(
                            "Content-Disposition",
                            "attachment",
                            filename=("utf-8", "", file_basename),
                        )
                        msg.attach(file_mail)

                all_message = msg.as_string()

                try:
                    # Tạo một đối tượng SMTP, cho phép kết nối tới server của SMTP và cho phép sử dụng các phương thức của SMTP
                    server = smtplib.SMTP(smtp_server, port)

                    # Tạo kết nối SMTP không bảo mật và mã hóa nó với starttls()
                    server.starttls()

                    # Đăng nhập tài khoản gmail của người gửi
                    server.login(username, password)

                    # Tiến hành gửi mail từ người gửi tới người nhận, message được định dang theo string.
                    server.sendmail(username, receiver_email, all_message)

                    # Trong trường hợp có lỗi khi kết nối tới server của SMTP hoặc xảy ra bất kì lỗi gì trong quá trình xử lí
                    # Sẽ xuất thông báo lỗi
                except Exception as e:

                    print(e)

                finally:
                    messagebox.showinfo("Success", "Sent!")
                    server.quit()

            # Khong co message va file
            else:
                messagebox.showerror("Error", "The content is empty!")

        # Khong co nguoi nhan
        else:
            messagebox.showerror("Error", "Please specify at least one recipient.!")

    GUI_send_mail.mainloop()


display_send_mail("18520165@gm.uit.edu.vn", "1634608674")