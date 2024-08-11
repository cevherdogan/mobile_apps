# templates

Bu klasör, Jinja2 şablonlarını içerir. Bu şablonlar, hatırlatma ve silme bildirimleri için e-posta içeriği oluşturmak üzere kullanılır.

## Dosya ve Şablon Açıklaması:

- **reminder_template.md**: Boş kalan topikler için hatırlatma iletisi şablonu.
- **deletion_template.md**: Boş kalan ve silinmiş topikler için silme bildirimi şablonu.

## Şablonların Kullanımı:

### Hatırlatma İletisi Şablonu (reminder_template.md):
Bu şablon, boş kalan topikler için hatırlatma e-postaları oluşturmak için kullanılır.

#### Şablon İçeriği:
```jinja
# {{ topic_name }} Hakkında Hatırlatma

Merhaba,

{{ days_passed }} gün önce {{ topic_name }} topiği oluşturuldu. Ancak bu topik hala boş durumda.

Lütfen topiği kullanmak istiyorsanız abonelik ekleyin, aksi takdirde {{ delete_in_days }} gün sonra otomatik olarak silinecektir.

Bu topik {{ scheduled_deletion_date }} tarihinde silinecektir.

İyi günler dileriz.

- Sistem Yöneticisi
```

### Silme İletisi Şablonu (deletion_template.md):
Bu şablon, boş kalan ve belirtilen süre sonunda silinen topikler için bildirim e-postaları oluşturmak için kullanılır.

#### Şablon İçeriği:
```jinja
# {{ topic_name }} Topiği Silindi

Merhaba,

{{ topic_name }} topiği {{ total_days }} gün boyunca boş kaldığı için otomatik olarak silinmiştir.

Eğer bu bir hata ise, lütfen sistem yöneticinizle iletişime geçin.

İyi günler dileriz.

- Sistem Yöneticisi
```

Bu şablonlar, `NotificationManager` sınıfı tarafından kullanılarak e-posta içerikleri oluşturulur. Şablonlar, `Jinja2` motoru tarafından dinamik olarak doldurulur ve e-posta olarak gönderilir.
