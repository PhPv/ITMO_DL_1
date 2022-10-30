## Распознавание номеров автомобилей при проезде через пропускной пункт

### Зачем это нужно?
* Подсчет времени, проведенного владельцем атвомобился на территории предприятия
* Автоматизация работы шлагбаума на кпп
    * автоматически пропускать спецтехнику (скорая/пожарная)
    * автоматически пропускать сотрудников предприятия
    
Установка заивисмостей
```
pip install -r requirements.txt
# yolov5 ставится вручную, но нужна только для дообучения, см. https://github.com/ultralytics/yolov5
```
Запуск на видео (не до конца отдебажено, может поломаться пока, но архитектурно верно):
```
python video_reader.py <path_to_video>
```


Из каких блоков состоит решение:

| Модуль          | Готовые решения                    | Описание модуля | Метрика
| ------------- |------------------| -----|---|
| Object Detection | Yolo/Fast R-CNN/SSD                               | Распознавание автомобиля + распознавание самого номера |mAP
| OCR |  EasyOCR(ResNet+LSTM+CTC)        | Распознавание номера с изображения |Accuracy|
| ReID/classification  | torchreid, mobilenet и друзья | Распознавание спецтехники + мэтчинг в условиях плохой видимости номера ||

### Метрика:
| Model          | Metric                    | Value |
| ------------- |------------------| -----|
| Yolo | mAP 0.5                              |
| OCR |  Accuracy   | |

### Подбор гиперпараметров для Object Detection:
Размер тренировочной выборки: 411 изображение

Размер тестовой выборки 22 изображения (5%)

| Epochs          |Learning Rate|  Image size | Optimizer | Metric value
| ------------- |---|------------------| -----|---|
| 50 | 0.01      |1280|SGD| 0.906|
| 100 |  0.01   |1280|SGD |0.938|
| 50 |  0.01   |640| SGD|0.849|
| 50 |  0.01   |640| Adam|0.66|
| 50 |  0.01   |640| AdamW|0.568|

### Pipeline обработки:

Важное: каждая модель работает с кадром, обертнутым в класс Frame, и дописывает в его свойства свое собственное поле, с которым дальше работает следующая модель. Например, модуль Detection добавляет свойство car_license (массив координат bbox номера), следующий модуль распознавания OCR вырезает номер, работая с этим свойством, и добавляет свое свойство licemse_recognition. Такой метод позволяет легко расширять пайплайн обработки в рамках данной задачи

* Распонаванаие машины + отдельно раcпознанный номер
* bound-box с машиной подается в модуль классификации или реид
* bound-box c номером подается в блок распознавания  цифро-буквенного номера


### Данные:
* [Данные для дообучения Object Detection](https://www.kaggle.com/code/sayamkumar/car-license-plate-detection/data)
* [Данные по номерам](https://nomeroff.net.ua/datasets/autoriaNumberplateOcrRu)


### Описание модуля OCR.

1) https://github.com/PhPv/ITMO_DL_1/blob/detection_recognition/model/ocr.py
Содержит методы распознания номера на базе easyocr c дефолтными настройками для кириллических символов
2) https://github.com/PhPv/ITMO_DL_1/blob/detection_recognition/model/ocr_model.py
Обернутый в класс инференс модели easyocr c постпроцессингом. Возвращает строку с распознанным номером.
3) https://github.com/PhPv/ITMO_DL_1/blob/detection_recognition/model/ocr_research.py
Скрипт исследования точности easyocr на российских номерах.

Также было испробованы best practice в виде проекта https://github.com/ria-com/nomeroff-net
Проект заточен на полный pipeline распознания от фото машины до номера.


### Модуль Object Detection
Модель - [Yolov5](https://github.com/ultralytics/yolov5). Выбираем ее для дообучения на распознавание номера в силу ее возможности работы в рилтайме.
Данные для дообучения переводим в формат, пригодный ждля считывания:
n, x, y, w, h, где

   n — номер класса объекта

   x — относительная координата bounding box’а объекта по оси Ox

   y — относительная координата bounding box’а объекта по оси Oy

   w — относительная ширина bounding box’а объекта

   h — относительная высота bounding box’а объекта

### Возможные модификации решения
* <b>ReID модуль</b> для распознавания спецтехники и метчинга автомобилей, если плохо виден номер (добавить просто, как еще одну ступень в pipeline)
* Масштабирование на больше число камер при неухудшении время обработки: batch-inference, те предусмотреть батчовую обоаботку в методе process у Model
* Качественне дообучение yolo, сейчас работает не очень

### Необходимое оборудование:
RTSP камера (их может быть много) + микрокомпьютер(Raspberry Pi, Khadas), который забирает видео с камер и передает для обработки в облако(обработка на железе не очень рациональна, с учетом, что нужно будет облгечать модели (а значит терять качество) + сложности при масштабировании)

### План работы:

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
