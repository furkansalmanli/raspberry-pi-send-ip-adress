
from urllib.request import urlopen
import re
import smtplib
#import sm

# Kullanıcı giriş bilgilerini ayarlıyoruz.
from_address = 'mail adresiniz'
to_address = 'mail adresiniz'
subject = 'Pi IP adresimiz'
username = 'mail adresiniz'
password = 'mail şifreniz'

# Ip adresimizi alacağımız siteyi yazıyoruz.
url = 'http://checkip.dyndns.org'
print ("Our chosen IP address service is ", url)

# Url'nin içinden içeriği okuyup ip adresini alıyoruz.
request = urlopen(url).read().decode('utf-8')
# Ip adresini çıkartıyoruz
ourIP = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", request)
ourIP = str(ourIP)
print ("Our IP address is: ", ourIP)

def send_email(ourIP):
# E-posta işlemlerini ayarlıyoruz.
    body_text = ourIP + ' is our PlayPi IP address'
    msg = '\r\n'.join(['To: %s' % to_address, 'From: %s' % from_address, 'Subject: %s' % subject, '', body_text])

    # E-posta'yı gönderme işlemleri yapıyoruz.
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls() # Our security for transmission of credentials
    server.login(username,password)
    server.sendmail(from_address, to_address, msg)
    server.quit()
    print ("Our email has been sent!")

# Eski ip adresimizi last_ip_txt dosyasına yazdırma işlemi yapıyoruz.
with open('/home/pi/Desktop/last_ip.txt', 'rt') as last_ip:
    last_ip = last_ip.read() # Read the text file

# Ip adresinin değişip değişmediğini kontrol ediyoruz ve ona göre çıktı veriyoruz.
if last_ip == ourIP:
    print("Our IP address has not changed.")
else:
    print ("We have a new IP address.")
    with open('/home/pi/Desktop/last_ip.txt', 'wt') as last_ip:
        last_ip.write(ourIP)
    print ("We have written the new IP address to the text file.")
send_email(ourIP)
