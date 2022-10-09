## Распознавание номеров автомобилей при проезде через пропускной пункт

### Зачем это нужно?
* Подсчет времени, проведенного владельцем атвомобился на территории предприятия
* Автоматизация работы шлагбаума на кпп
    * автоматически пропускать спецтехнику (скорая/пожарная)
    * автоматически пропускать сотрудников предприятия
    

Из каких блоков состоит решение:

| Модуль          | Готовые решения                    | Описание модуля | 

| Object Detection | Yolo                               | Распознавание автомобиля + распознавание самого номера |
| OCR |  EasyOCR(ResNet+LSTM+CTC        | Распознавание номера с изображения |
| ReID/classification  | torchreid, mobilenet и друзья | Распознавание спецтехники + мэтчинг в условиях плохой видимости номера |



Pipeline обработки:

* Распонаванаие машины + отдельно раcпознанный номер
* bound-box с машиной подается в модуль классификации или реид
* bound-box c номером подается в блок распознавания  цифро-буквенного номера


Данные:
* Машины спереди/сзади
* +спецтехника
* Данные по номерам
https://nomeroff.net.ua/datasets/autoriaNumberplateOcrRu


#### План работы:

teammate

[alexandraroots](https://github.com/alexandraroots) :
1. Обоснование выбора модели (object detcetion).
2. Обернуть модель в модуль 
3. Дообучение модели (object detcetion) 
4. Обернуть в пайплайн 

[PhPv](https://github.com/PhPv) :
1. Сбор данных
2. Проверка p2p

[Nikolai Pavlychev](https://github.com/NikolayPavlychev)  :
1. Выбор модели распознавания номера(OCR)
2. Обернуть модель в модуль 

Описание модуля OCR.

1) https://github.com/PhPv/ITMO_DL_1/blob/detection_recognition/model/ocr.py
Содержит методы распознания номера на базе easyocr c дефолтными настройками для кириллических символов
2) https://github.com/PhPv/ITMO_DL_1/blob/detection_recognition/model/ocr_model.py
Обернутый в класс инференс модели easyocr c постпроцессингом. Возвращает строку с распознанным номером.
3) https://github.com/PhPv/ITMO_DL_1/blob/detection_recognition/model/ocr_research.py
Скрипт исследования точности easyocr на российских номерах.

Также было испробованы best practice в виде проекта https://github.com/ria-com/nomeroff-net
Проект заточен на полный pipeline распознания от фото машины до номера.
