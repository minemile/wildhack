## Autocompleter
Проект по дополнению поисковых подсказок (autocompleter) на основе trie и inverted index

### Train
Подготовка исходного csv в нужный формат. Создание индексов.

```bash
python train.py --dataset_path data/search_hist_sample_10mil.csv --save_to cache_10m/
```
```dataset_path``` - путь на подготовленные данные с леммами

```save_to``` - путь на папку куда будут сохранятся индексы 

### Inferece
Создание модели и прогнозирование по запросу автодополнения
```bash
python inferece.py --cache_dir cache --speller_bin cache/jamspell_ru_model_subtitles.bin --endless True
```
```cache_dir``` -  путь на папку куда сохранены артефакты первого этапа

```speller_bin``` - путь на модель spell checker'а

```endless``` - режим приложения при котором бесконечно вычитывается user input для автодополнений

```query``` - предсказание дополнения для одного запроса и выход из приложения
