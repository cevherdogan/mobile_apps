
# src/config_manager.py

Bu dosya, AWS SNS konfigürasyon dosyalarını yönetmek için gerekli işlevleri sağlar. Konfigürasyon dosyaları, proje boyunca çeşitli yapılandırmaları yüklemek, kaydetmek ve güncellemek için kullanılır.

## Dosya ve Kod Açıklaması:

- **load_config(file_path)**: Belirtilen dosya yolundan konfigürasyon dosyasını yükler.
- **save_config(config, file_path)**: Konfigürasyon verilerini belirtilen dosya yoluna kaydeder.
- **update_config(params)**: Mevcut konfigürasyonu verilen parametrelerle günceller.

## Kullanım:

Aşağıda, `src/config_manager.py` dosyasını kullanarak çeşitli işlemleri nasıl gerçekleştireceğinizi gösteren örnek kod parçacıkları bulunmaktadır:

### Konfigürasyon Dosyasını Yüklemek:
```python
config_manager = ConfigManager("config/config.yaml")
config = config_manager.load_config()
```
Bu kod, `config/config.yaml` dosyasını yükler ve konfigürasyon verilerini alır.

### Konfigürasyon Dosyasını Kaydetmek:
```python
config_manager.save_config(config, "config/config.yaml")
```
Bu kod, mevcut konfigürasyon verilerini `config/config.yaml` dosyasına kaydeder.

### Konfigürasyonu Güncellemek:
```python
config_manager.update_config({"reminder_days": [2, 5, 7], "deletion_days": 9})
```
Bu kod, konfigürasyonu verilen parametrelerle günceller ve değişiklikleri kaydeder.
