Python programlama dili ile RSA Asimetrik şifreleme kullanılarak kullanıcılara eposta gönderen bir program tasarlanmıştır. Şifreleme ve şifre çözme işlemleri için Python PyCryptodome kütüphanesi kullanılmıştır.

Şifreli bir iletişim iki tarafı içerir: bilgiyi şifreleyen gönderen ve şifreyi çözen alıcı. Asimetrik şifreleme, adından da anlaşılacağı gibi gönderen ve alıcı için iki ayrı anahtar kullanır. Asimetrik şifrelemede, genel anahtar şifrelemesi olarak da adlandırılan bir genel anahtar-özel anahtar eşleşmesi kullanılır, böylece genel anahtarla şifrelenen veriler yalnızca özel anahtarla çözülebilir. 

Programa giriş yapan kullanıcılar ilk olarak RSA ile kendi public ve private anahtalarını oluşturmak zorundadır (Public.pem ve private.pem). Mesaj atacağımız kişilerin de aynı yöntemle kendi public ve private anahtarlarını oluşturmuş olmaları ve public anahtalarını bizim erişebileceğimiz bir web sayfasında paylaşmaları gerekmektedir. Benim kişilerimin public anahtarları apimera.xyz web adresinde paylaşıldı ve “e-posta.pem” şeklinde Contacts klasörüne kaydedildi.

Mesaj göndermek istediğimiz kişilerin Public anahtarlarını Contacts klasörüne kopyaladıktan sonra mesaj gönder seçeneğini seçip alıcı e-posta adreslerini yazıyoruz. Konu ve mesaj kısımlarını yazdıktan sonra gönderdiğimiz kişilerin public anahtarları ile şifrelenip mesajlarımız iletilir.

Gönderdiğimiz mesajlar şifrelenmiş olarak iletilir.

Mesajlar farklı public anahtarlarla şifrelendiği için farklı görünmektedir. Her kullanıcı kendi private anahtarı ile mesajın şifresini çözüp görüntüleyebilir. Programımızdan Inbox menusunu seçip okumak istediğimiz mesajı seçiyoruz.

Asimetrik şifreleme kullanarak ve PyCryptodome kütüphanesi kullanarak Python ile yaptığımız mesajlaşma programı ile şifreli mesajlarımızı kullanıcılara başarılı bir şekilde ilettik ve kullanıcılar kendi private şifreleri ile çözüp başarılı bir şekilde mesajı okuyabilmişlerdir.
