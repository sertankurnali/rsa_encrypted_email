import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import email
import imaplib
from email.header import decode_header
from email import message
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

print("---epostaya Giris Yapiniz---")
#em = input("Kullanici Adi:")
#passwd =  getpass.getpass("Sifre:")
em = "sertan@apimera.xyz"
passwd =  "Xy$sAXDL9m-OaF3"

## sunucu smtp ayarlari
session = smtplib.SMTP('smtp.hostinger.com', 587)
session.starttls()

try:
	session.login(em,passwd)
except smtplib.SMTPAuthenticationError:
	print("Yanlis Kullanici Adi veya Sifre")
	exit()

print("Giris Basarili!")

while(True):

	menu='''\n\n\n
	Menu:
	1. Eposta Gonder
	2. Posta Kutusu
	3. Anahtar ciftleri uret (RSA)
	4. Cikis
	'''

	print(menu)

	choice = input("\n Bir Secenek Giriniz: ")

	if choice=='4':
		exit()

	####### Public ve Private Anahtarlarin olusturulmasi (RSA)
	if choice=='3':
		### Private Key uret ve kaydet
		key = RSA.generate(2048)
		private_key = key.export_key()
		f = open("Keys/private.pem","wb")
		f.write(private_key)
		f.close()
		print("Private key uretildi")


		###  Public Key uret ve kaydet
		public_key = key.publickey().export_key()
		f = open("Keys/public.pem","wb")
		f.write(public_key)
		f.close()
		print("Public key Uretildi")


	#### 2. Secenek Posta Kutusu
	if choice == '2':
		M = imaplib.IMAP4_SSL("imap.hostinger.com")
		M.login(em, passwd)

		M.select("INBOX")
		typ, data = M.search(None, 'ALL')
		print("="*100)
		for num in data[0].split():
			print("SNo. "+num.decode())
			typ, data = M.fetch(num, '(RFC822)')
			msg = email.message_from_bytes(data[0][1])
			#print(msg)
			subject, encoding = decode_header(msg["Subject"])[0]
			From, encoding = decode_header(msg.get("From"))[0]
			print("Subect: "+subject)
			print("From: "+From)
			print("-"*100)
		print("="*100)

		selectEmail = input("Eposta numarasini giriniz(cikis icin q):")
		if selectEmail == "q": continue
		typ, data = M.fetch(selectEmail, '(RFC822)')
		msg = email.message_from_bytes(data[0][1])
		subject, encoding = decode_header(msg["Subject"])[0]
		print(subject)
		From, encoding = decode_header(msg.get("From"))[0]
		print(From)

		# eposta parcalari uzerinde itersayon
		for part in msg.walk():
			content_type = part.get_content_type()
			content_disposition = str(part.get("Content-Disposition"))
			try:
				body = part.get_payload(decode=True)
			except:
				pass
			if content_type == "text/plain" and "attachment" not in content_disposition:
				#print(body)
				################## DECRYPTION #################################################
				private_key = RSA.import_key(open("Keys/private.pem").read())
				ciphertext = body	
				#### RSA decrypt
				cipher_rsa = PKCS1_OAEP.new(private_key)
				data = cipher_rsa.decrypt(ciphertext)
				print("\nDecrypted Message:\n")
				print(data.decode("utf-8"))
				print("\n\n\n")

	### Secenek 1 Eposta Gonder
	if choice == '1':
		email_adresleri = input("Virgülle ayrılmış e-posta adreslerini girin: ")
		email_listesi = email_adresleri.split(",")
		subject = input("Enter Subject:")
		msg = input("Enter Message:").encode("utf-8")
		for rec_email in email_listesi:
		## Alicilarin Public keylerinin olup olmadigini kontrol et
			try:
				recipient_key= RSA.import_key(open("Contacts/"+rec_email+".pem").read())
			except FileNotFoundError:
				yn = print("Girilen eposta alicilarina ait Public keyleri kontrol edin!")
				continue
			#### Epostayı gezin
			message = MIMEMultipart()
			message['From'] = em
			message['To'] = rec_email
			message['Subject'] = subject

			########### ENCRYPTION #############################
			#RSA
			cipher_rsa = PKCS1_OAEP.new(recipient_key)
			ciphertext= cipher_rsa.encrypt(msg)
			body = ciphertext

			message.attach(MIMEText(body, 'plain','utf-8'))
			print("Sending message to: ",rec_email)
			### Send Email
			text = message.as_string()
			print("Sending message to: ",rec_email)
			print("\n\n"+text)
			session.sendmail(em,rec_email, text)
			print("Encrypted Email Sent!")
			print("to  ",rec_email)
			time.sleep(3)


session.quit()