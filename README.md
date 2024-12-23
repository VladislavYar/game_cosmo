# game_cosmo
Проект представляет из себя космическую 2D игру (на начальной стадии разработки) с видом сверху, сделанную на Pygame. На данный момент реализовано полноценное динамическое меню с возможностью игровых настроек (смена разрешению, регулирование звука) и сброса, вывод игровой статистики, при старте новой игры реализован ввод имени и выбор сложности. Сама игра на данный момент представляет из себя:
1. Космический корабль, с возможностью движения под разным уголом (движение реализовано одновременно как и по экрану, так и по карте, так же имеется эффект постепенного ускорения и торможения);
2. Стрельбу под разным углом с рандомным отклонением выстрела и взрывом по таймеру;
3. Логика перемещения объектов относительно корабля ГГ при его движении, динамический пересчёт смены спрайтов и скорости движения объектов относительно FPS и разрешения экрана.

## Как запустить проект:

В терминале, перейдите в каталог, в который будет загружаться приложение:
```
cd 
```
Клонируйте репозиторий:
```
git clone git@github.com:VladislavYar/game_cosmo.git
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запуск проект:
```
python ya_cosmo.py
```

## Cтек проекта
Python v3.11, Pygame

