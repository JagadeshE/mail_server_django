from django.shortcuts import render

# Create your views here.
from mail.models import contact_list
# from mail.models import mail_contact_list

from django.shortcuts import render
from django.db.models import Q

import imaplib
import email
import ssl
import pprint

from csv import reader
import re
import psycopg2
from psycopg2 import Error



def hello_world(request):
    return render(request, 'helloworld.html', {})


def contact_list_page(request):
    return render(request, 'helloworld.html', {})


def contact_index(request):
    contacts = contact_list.objects.all()
    context = {
        'contacts': contacts
    }
    return render(request, 'helloworl.html', context)

def main_page(request):
    return render(request, 'helloworld.html', {})
    
    ##### Original Page Views ######

def home_page(request):
    return render(request, 'base.html', {})

def import_mail(request):
    print("REQUEST :" , request)
    username = ''
    password = ''
    if request.method == 'POST':
        username = request.POST.get('registerUsername')
        password = request.POST.get('registerPass')
    print(username)
    print(password)

    imap_host = 'excus.phytec.de'
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    imap = imaplib.IMAP4(host=imap_host,port=143)
    imap.starttls(context)
    
    ## login to server
    imap.login(username, password)
    print("Please wait Sometime query is running background")
    folder = ['"Inbox"', '"Sent Items"']
    for mail_folder in folder:
        print(mail_folder)
        imap.select(mail_folder)
        tmp, data = imap.search(None, 'ALL')
        print(data)
        for num in data[0].split():
            print(num)
        #     tmp, data = imap.fetch(num, '(RFC822)')
            type, data = imap.fetch(num, '(BODY.PEEK[HEADER] FLAGS)')
            # pprint.pprint(data)
            for response in data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    from_ = msg.get("From")
                    to_ = msg.get("TO")
                    cc_ = msg.get("CC")
                    msg_date = msg.get("Date")
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
                    db_values = (from_user_name,from_user_mail,msg_date)
                    # print("DB VALUES :", db_values)


                    if from_user_mail:
                        mail_exist = contact_list.objects.filter(email=from_user_mail)
                        if not mail_exist:
                            contact_list.objects.create(email=from_user_mail, name=from_user_name,email_date=msg_date)
                            print(from_user_mail)


                    if to_:
                        to_ = to_.strip()
                        to_split = to_.split(",")
                        for id in to_split:
                            to_mail = id.strip('\r\n\t')
                            to_mail = re.sub("\s+", "", to_mail)
                            group_mail = re.search('"(.*)" ?<(.*)>', to_mail)   
                            quote_group_mail = re.search('(.*) ?<(.*)>', to_mail)
                            to_user_name = '' 
                            to_user_mail = ''
                            if quote_group_mail:
                                to_user_name += quote_group_mail.group(1)
                                to_user_mail += quote_group_mail.group(2)
                            elif group_mail:
                                to_user_name = group_mail.group(1) 
                                to_user_mail = group_mail.group(2)
                            else:
                                if '@' in to_mail:
                                    to_user_mail = to_mail
                            re_to_user_name = re.findall(r"\w+",to_user_name)
                            separator = ' '
                            to_user_name = (separator.join(re_to_user_name))
                            to_user_mail = to_user_mail.strip()
                            db_values = (to_user_name,to_user_mail,msg_date)
                            if to_user_mail:
                                to_mail_exist = contact_list.objects.filter(email=to_user_mail)
                                if not to_mail_exist:
                                    contact_list.objects.create(email=to_user_mail, name=to_user_name,email_date=msg_date)
                                    print(to_user_mail)

                    if cc_:
                        cc_ = cc_.strip()
                        cc_split = cc_.split(",")
                        for id in cc_split:
                            cc_mail = id.strip('\r\n\t')
                            cc_mail = re.sub("\s+", "", cc_mail)
                            group_mail = re.search('"(.*)" ?<(.*)>', cc_mail)
                            quote_group_mail = re.search('(.*) ?<(.*)>', cc_mail)
                            cc_user_name = '' 
                            cc_user_mail = ''
                            if quote_group_mail:
                                cc_user_name += quote_group_mail.group(1)
                                cc_user_mail += quote_group_mail.group(2)
                            elif group_mail:                                
                                cc_user_name = group_mail.group(1) 
                                cc_user_mail = group_mail.group(2)
                            else:
                                if '@' in cc_mail:
                                    cc_user_mail = cc_mail
                            re_cc_user_name = re.findall(r"\w+",cc_user_name)
                            separator = ' '
                            cc_user_name = (separator.join(re_cc_user_name))
                            cc_user_mail = cc_user_mail.strip()
                            # cc_user_name = cc_user_name.strip('""')
                            db_values = (cc_user_name,cc_user_mail,msg_date)
                            if cc_user_mail:
                                cc_mail_exist = contact_list.objects.filter(email=cc_user_mail)
                                if not cc_mail_exist:
                                    contact_list.objects.create(email=cc_user_mail, name=cc_user_name,email_date=msg_date)
                                    print(to_user_mail)

    imap.close()
    imap.logout()
    return render(request, 'import.html', {})

def export_mail(request):
    return render(request, 'export.html', {})

def about_us(request):
    return render(request, 'about_us.html', {})

def login(request):
    return render(request, 'login.html', {})

# def mail_list(request):
#     return render(request, 'mail_list.html', {})

def mail_list(request):
    data = contact_list.objects.all()
    
    # Search Bar
    query = request.GET.get("search_box")
    if query:
        print("QUERY :",query)
        data = data.filter(
            Q(email__icontains=query) |
            Q(id__icontains=query) |
            Q(name__icontains=query)
            ).distinct()


    if request.user.is_authenticated:
        return render(request,'mail_list.html', {'obj': data})
    else:
        return render(request, 'login.html')