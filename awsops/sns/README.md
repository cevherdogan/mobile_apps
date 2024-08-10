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



