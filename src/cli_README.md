
# src/cli.py

Bu dosya, AWS SNS konularını ve abonelikleri yönetmek için temel bir komut satırı arayüzü (CLI) sağlar.

## Dosya ve Kod Açıklaması:

- **argparse**: Komut satırı argümanlarını işlemek için kullanılır.
- **TopicManager, ConfigManager, NotificationManager**: Daha önce belirlediğimiz işlevselliklere uygun olarak yönetim sınıflarıdır.
- **command**: Kullanıcının çalıştırmak istediği komutu alır (`create_topic`, `add_subscription`, `list_topics`, `check_empty_topics`, `configure_notifications`).

## Kullanım:

Aşağıda, `src/cli.py` dosyasını kullanarak çeşitli işlemleri nasıl gerçekleştireceğinizi gösteren örnek komutlar bulunmaktadır:

```bash
python src/cli.py create_topic --topic_name "MyNewTopic"
```
Bu komut, "MyNewTopic" adında yeni bir SNS topiği oluşturur.

```bash
python src/cli.py add_subscription --topic_name "MyNewTopic" --subscription_type "email" --endpoint "example@example.com"
```
Bu komut, "MyNewTopic" topiğine bir email aboneliği ekler.

```bash
python src/cli.py list_topics
```
Bu komut, tüm topikleri ve mevcut aboneliklerini listeler.

```bash
python src/cli.py check_empty_topics
```
Bu komut, boş olan topikleri kontrol eder.

```bash
python src/cli.py configure_notifications --reminder_days 2 5 7 --deletion_days 9
```
Bu komut, hatırlatma ve silme işlemleri için zamanlamayı yapılandırır. İlk hatırlatma 2. gün, ikinci hatırlatma 5. gün, üçüncü hatırlatma 7. gün yapılır. Topik, 9 gün boyunca boş kalırsa silinir.

Bu yapılandırma ile projenizi yerel ortamda çalıştırabilir ve AWS SNS üzerindeki işlemlerinizi yönetebilirsiniz.
