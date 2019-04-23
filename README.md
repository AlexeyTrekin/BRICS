# BRICS
BRICS project data preparation

1. Выбрать изображение, для которого нужна разметка.
Узнать его bbox, выполнив питоновский скрипт bbox.py:
python3 bbox.py <filepath>
где filepath - путь к файлу изображения.

2. Сделать запрос (скопировать из файла с соответствующим типом), заменить границы YMIN, XMIN, YMAX, XMAX на вывод скрипта из п.1

3. Нажать "RUN", затем "EXPORT" и выбрать опцию "download as geojson"

4. Выполнить скрипт rasterize_markup.py, исправив там пути к файлам.
