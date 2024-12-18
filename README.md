# Kkimpact BOT

https://t.me/KKimpactBot

# kkimpact

### Установка зависимостей
```
pip install -r requirements.txt
```

### Настройка окружения
В корне создать файл `.secrets.toml` со следующим содержанием
```
BOT_TOKEN = "<TOKEN>"
```

### Переместить базу данных
Перемещаем пустую БД `users_info.sqlite` из папки `/setup` в корень проекта
```
cd ~/kkimpact/setup
mv users_info.sqlite ../
```

### Устанавливаем зависимость для OpenCV
```
sudo apt install libgl1 -y
```

### Запуск бота
```
python main.py
```
