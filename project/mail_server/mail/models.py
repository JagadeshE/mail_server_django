from django.db import models
import imaplib
import email
import ssl
import pprint

import email
from email.header import decode_header
import webbrowser
from csv import reader
import re
import psycopg2
from psycopg2 import Error



# Create your models here.
class contact_list(models.Model):
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email_date = models.CharField(max_length=200)

    def mail_list_database(self, **kwargs):

        username = "jagadeshkumar108@gmail.com"
        password = "Jaga@1893"

        imap = imaplib.IMAP4_SSL("imap.gmail.com")

        # authenticate
        imap.login(username, password)
        print(imap.list())
        status, messages = imap.select('Inbox')

        print(messages)
        # total number of emails
        messages = int(messages[0])
        for i in range(1, messages, 1):
            print(i)
            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")
            print(msg)
            for response in msg:
                if isinstance(response, tuple):
                    print(response)
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode()
                    # email sender
                    from_ = msg.get("From")
                    to_ = msg.get("TO")
                    cc_ = msg.get("CC")
                    msg_date = msg.get("Date")

                    print(from_)

                    from_ = from_.strip()
                    from_mail = from_.strip('\r\n\t')
                    from_mail = re.sub("\s+", "", from_mail)
                    group_mail = re.search('"(.*)" ?<(.*)>', from_mail)
                    quote_group_mail = re.search('(.*) ?<(.*)>', from_mail)
                    from_user_name = '' 
                    from_user_mail = ''
                    if quote_group_mail:
                        from_user_name += quote_group_mail.group(1)
                        from_user_mail += quote_group_mail.group(2)
                    elif group_mail:
                        from_user_name = group_mail.group(1) 
                        from_user_mail = group_mail.group(2)
                    else:
                        if '@' in from_mail:
                            from_user_mail = from_mail
                    re_from_user_name = re.findall(r"\w+",from_user_name)
                    separator = ' '
                    from_user_name = (separator.join(re_from_user_name))
                    from_user_mail = from_user_mail.strip()
                    db_values = (from_user_name,from_user_mail,msg_date,)
                    if self.email != from_user_mail:
                        self.email = from_user_mail
                        self.name = from_user_name
                        self.date = msg_date
                        print("YES")
                    else:
                        print("NO")
                    super(contact_list, self).save(**kwargs)
                    # if not check_mail:
                    #     insert_mail = contact_list( email = from_user_mail, name = from_user_name, email_date = msg_date)       
                    #     insert_mail.save()

        imap.close()
        imap.logout()

        # imap_host = 'excus.phytec.d'
        # imap_user = 'jagadesh.e@phytec.in'
        # imap_pass = 'zIXQp6gGqcwAY9'
        # context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        # imap = imaplib.IMAP4(host=imap_host,port=143)
        # imap.starttls(context)

        # ## login to server
        # imap.login(imap_user, imap_pass)
        # print("Please wait Sometime query is running background")
        # folder = ['"Inbox"', '"Sent Items"']
        # for mail_folder in folder:
        #     print(mail_folder)
        #     imap.select(mail_folder)
        #     tmp, data = imap.search(None, 'ALL')
        #     print(data)
        #     for num in data[0].split():
        #         print(num)
        #         # tmp, data = imap.fetch(num, '(RFC822)')
        #         type, data = imap.fetch(num, '(BODY.PEEK[HEADER] FLAGS)')
        #         # pprint.pprint(data)
        #         for response in data:
        #             if isinstance(response, tuple):
        #                 msg = email.message_from_bytes(response[1])
        #                 from_ = msg.get("From")
        #                 to_ = msg.get("TO")
        #                 cc_ = msg.get("CC")
        #                 msg_date = msg.get("Date")
        #                 from_ = from_.strip
        #                 # from_split = from_.split(",")
        #                 # for from_id in from_split:

        #                 from_mail = from_.strip('\r\n\t')
        #                 from_mail = re.sub("\s+", "", from_mail)
        #                 group_mail = re.search('"(.*)" ?<(.*)>', from_mail)
        #                 quote_group_mail = re.search('(.*) ?<(.*)>', from_mail)
        #                 from_user_name = '' 
        #                 from_user_mail = ''
        #                 if quote_group_mail:
        #                     from_user_name += quote_group_mail.group(1)
        #                     from_user_mail += quote_group_mail.group(2)
        #                 elif group_mail:
        #                     from_user_name = group_mail.group(1) 
        #                     from_user_mail = group_mail.group(2)
        #                 else:
        #                     if '@' in from_mail:
        #                         from_user_mail = from_mail
        #                 re_from_user_name = re.findall(r"\w+",from_user_name)
        #                 separator = ' '
        #                 from_user_name = (separator.join(re_from_user_name))
        #                 from_user_mail = from_user_mail.strip()
        #                 db_values = (from_user_name,from_user_mail,msg_date,)

        #                 check_mail = contact_list.objects.filter(email='from_user_mail')
        #                 if not check_mail:
        #                     insert_mail = contact_list( email = from_user_mail, name = from_user_name, email_date = msg_date)       
        # imap.close()
        # imap.logout() 
    # mail_list_database()


# class new_contact_list(models.Model):
#     new_email = models.CharField(max_length=200)
#     new_name = models.CharField(max_length=200)
#     new_email_date = models.CharField(max_length=200)