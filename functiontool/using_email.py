from email.mime.text import MIMEText
from email.header import Header
import smtplib

def send(content,subject,*args):
    '''
    content：邮件正文
    subject: 邮件主题
    之后的任意参数都会被解读为收件人，请传入邮箱字符串
    '''
    print(content)
    print(subject)
    print(args[0])
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = 'm18309560115@163.com'
    msg['To'] = ','.join(list(args))
    smtp = smtplib.SMTP_SSL('smtp.163.com')
    smtp.ehlo('smtp.163.com')
    smtp.login("m18309560115@163.com", "1qaz2wsx")
    smtp.sendmail("m18309560115@163.com",list(args), msg.as_string())
    smtp.quit()






if __name__=='__main__':
    send('你好，这是一份邮件，用于测试。\n不知道为什么不通过要求','爬虫错误测试','2486296941@qq.com')