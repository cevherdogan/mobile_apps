
# src/topic_manager.py

Bu dosya, AWS SNS topiklerini ve aboneliklerini yönetmek için gerekli işlevleri sağlar. Topik oluşturma, abonelik ekleme, topikleri listeleme ve boş topikleri kontrol etme gibi işlemleri içerir.

## Dosya ve Kod Açıklaması:

- **create_topic(topic_name, attributes)**: Yeni bir topik oluşturur.
- **delete_topic(topic_arn)**: Belirli bir topiği siler.
- **list_topics()**: Tüm topikleri ve aboneliklerini listeler.
- **add_subscription(topic_arn, subscription_type, endpoint)**: Belirli bir topiğe abonelik ekler.
- **check_empty_topics()**: Tüm topikleri kontrol eder ve boş olanları tespit eder.

## Kullanım:

Aşağıda, `src/topic_manager.py` dosyasını kullanarak çeşitli işlemleri nasıl gerçekleştireceğinizi gösteren örnek kod parçacıkları bulunmaktadır:

### Topik Oluşturma:
```python
topic_manager = TopicManager(config_manager)
topic_manager.create_topic(topic_name="MyNewTopic", attributes={"DisplayName": "My New SNS Topic"})
```
Bu kod, "MyNewTopic" adında yeni bir SNS topiği oluşturur.

### Abonelik Ekleme:
```python
topic_manager.add_subscription(topic_arn="arn:aws:sns:us-east-1:123456789012:MyNewTopic", subscription_type="email", endpoint="example@example.com")
```
Bu kod, belirli bir topiğe email aboneliği ekler.

### Topikleri Listeleme:
```python
topic_manager.list_topics()
```
Bu kod, tüm topikleri ve mevcut aboneliklerini listeler.

### Boş Topikleri Kontrol Etme:
```python
topic_manager.check_empty_topics()
```
Bu kod, boş olan topikleri kontrol eder ve bunları tespit eder.
