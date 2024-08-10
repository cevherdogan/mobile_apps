
# src/notification_manager.py

Bu dosya, boş olan AWS SNS topikleri için hatırlatma bildirimleri ve otomatik silme işlemleri ile ilgili fonksiyonları içerir. Bu işlemler, belirli günlerde admin'e e-posta gönderme ve gerekli koşullarda topikleri silme işlemlerini yönetir.

## Dosya ve Kod Açıklaması:

- **send_reminder(topic_arn, days_passed)**: Belirtilen günler geçmişse, boş topik için admin'e hatırlatma iletisi gönderir.
- **send_deletion_notice(topic_arn)**: Topik silindiğinde admin'e bilgi verir.
- **configure_notification_schedule(days)**: Hatırlatma ve silme işlemleri için zamanlama yapılandırmasını yönetir.

## Kullanım:

Aşağıda, `src/notification_manager.py` dosyasını kullanarak çeşitli işlemleri nasıl gerçekleştireceğinizi gösteren örnek kod parçacıkları bulunmaktadır:

### Hatırlatma İletisi Gönderme:
```python
notification_manager = NotificationManager(config_manager)
notification_manager.send_reminder(topic_arn="arn:aws:sns:us-east-1:123456789012:MyTopic", days_passed=2)
```
Bu kod, belirli bir topik için admin'e 2 gün sonra hatırlatma iletisi gönderir.

### Silme Bildirimi Gönderme:
```python
notification_manager.send_deletion_notice(topic_arn="arn:aws:sns:us-east-1:123456789012:MyTopic")
```
Bu kod, belirli bir topik silindiğinde admin'e bildirim gönderir.

### Bildirim Zamanlamasını Yapılandırma:
```python
notification_manager.configure_notification_schedule(days=[2, 5, 7])
```
Bu kod, hatırlatma iletilerinin 2., 5. ve 7. günlerde gönderilmesini sağlar.

Bu işlevlerle, proje boyunca admin'e hatırlatma ve silme bildirimleri gönderebilir, işlemleri otomatikleştirebilirsiniz.
