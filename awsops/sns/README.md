# AWS SNS Operations

Bu dizin, AWS SNS aboneliklerini ve topic'lerini yönetmek için kullanılan betikleri içerir. Aşağıdaki betikler, SNS üzerinde topic ekleme, silme ve listeleme işlemleri için kullanılır.

## Kullanım

### Topic Ekleme, Listeleme, Silme

```bash
./add_topic.sh <topic_name> [profile_name]
./list_topics.sh [profile_name]
./delete_topic.sh <topic_arn> [profile_name]
```

- <topic_name>: Oluşturmak istediğiniz SNS topic'in adını belirtin.
- <topic_arn>: Silmek istediğiniz SNS topic'in ARN'sini belirtin.
- [profile_name]: Kullanmak istediğiniz AWS profilinin adını belirtin. Profil adı verilmezse, default profili kullanılır.


- **Ornek Kullanim**
  ```bash
  ./add_topic.sh MyNewTopic [profile_name]
  ./list_topics.sh [profile_name]
  ./delete_topic.sh arn:aws:sns:us-east-1:123456789012:MyNewTopic [profile_name]
```


## Unit Testing and Validation

Bu projede, AWS SNS konularını ve aboneliklerini test etmek ve doğrulamak için bir dizi betik bulunmaktadır. Bu betikler, test abonelikleri eklemek, test mesajları göndermek ve SNS yapılandırmalarını doğrulamak için kullanılır.

### Simple Test Validation
`simple_test_validation.sh` betiği, SNS topic'lerinizi ve aboneliklerinizi test etmek için kullanabileceğiniz otomatik bir test aracıdır. Bu betik, topic'leri listelemenize, yeni abonelikler eklemenize ve test mesajları göndermenize olanak tanır.

Daha fazla bilgi için [Simple SNS Test Validation Script README](SIMPLE_TEST_VALIDATION_README.md) dosyasına göz atın.

### SNS Entegrasyon Testi
`sns_integration_test.sh` betiği, SNS topic'lerinizi ve aboneliklerinizi kapsamlı bir şekilde test etmek için kullanılır. Bu betik, entegrasyon testleri yaparak SNS yapılandırmalarınızın düzgün çalışıp çalışmadığını kontrol eder.

## Dosya ve Klasör Yapısı

- **add_topic.sh**: SNS topic eklemek için kullanılır.
- **list_topics.sh**: Mevcut SNS topic'leri listelemek için kullanılır.
- **delete_topic.sh**: Belirtilen SNS topic'ini silmek için kullanılır.
- **simple_test_validation.sh**: SNS topic'lerinizi ve aboneliklerinizi test etmek için otomatik bir test betiğidir.
- **sns_integration_test.sh**: SNS yapılandırmalarınızı kapsamlı bir şekilde test etmek için entegrasyon testi betiğidir.
- **sns_config.json**: SNS yapılandırmaları için kullanılan JSON dosyasıdır.
- **topic_arns.txt**: SNS topic ARN'lerini saklamak için kullanılan geçici dosyadır.
- **sns_integration.log**: Entegrasyon testleri sırasında oluşturulan log dosyasıdır.
- **soft_switch/**: Proje dosyalarını içeren dizin.
- **SIMPLE_TEST_VALIDATION_README.md**: `simple_test_validation.sh` betiği için detaylı kullanım kılavuzu.


