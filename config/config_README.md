
# config README.md

## Yapılandırma Açıklaması:

### Hatırlatma Bildirimleri (reminder):
Hatırlatma iletilerinin kaçıncı günlerde gönderileceğini belirler. Bu örnekte, ilk hatırlatma 2. gün, ikinci hatırlatma 5. gün, üçüncü hatırlatma 7. gün gönderilecektir.

### Topik Silme (deletion):
Bir topiğin kaç gün boyunca boş kalması durumunda otomatik olarak silineceğini belirler. Bu örnekte, topik 9 gün boyunca boş kalırsa silinecektir.

### AWS Konfigürasyonu (aws):
AWS SNS servisleri için gerekli yapılandırmaları içerir. Bu, yerel test ortamında kullanılmak üzere sahte (dummy) değerlerle de ayarlanabilir.

### Admin Email (admin):
Hatırlatma ve silme bildirimlerinin gönderileceği admin email adresini belirler.

### SMTP Konfigürasyonu (smtp):
Yerel bir email sunucusu kullanıyorsanız, bu bölümde SMTP ayarlarını yapılandırabilirsiniz. Bu sayede bildirimler gönderilebilir.

## Kullanım:
Bu `config.yaml` dosyasını yerel ortamda kullanarak tüm işlemleri ve bildirimleri yapılandırabilirsiniz. Eğer AWS gerçek erişim bilgileri kullanıyorsanız, bunları da uygun şekilde dosyada güncelleyebilirsiniz.

Bu yapılandırma dosyası, projeyi yerel ortamda çalıştırmanıza olanak tanır. Herhangi bir ekleme veya değişiklik yapmak isterseniz, lütfen belirtin!
