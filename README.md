# game_cosmo
Проект представляет из себя космическую 2D игру (на начальной стадии разработки) с видом сверху, сделанную на Pygame. На данный момент реализовано полноценное динамическое меню с возможностью игровых настроек (смена разрешению, регулирование звука) и сброса, вывод игровой статистики, при старте новой игры реализован ввод имени и выбор сложности. Сама игра на данный момент представляет из себя:
1. Космический корабль, с возможностью движения под разным уголом (движение реализовано одновременно как и по экрану, так и по карте, так же имеется эффект постепенного ускорения и торможения);
2. Стрельбу под разным углом с рандомным отклонением выстрела и взрывом по таймеру;
3. Логика перемещения объектов относительно корабля ГГ при его движении, динамический пересчёт смены спрайтов и скорости движения объектов относительно FPS и разрешения экрана.

Проекту требуется рефакторинг и некоторые способы реализации знающим людям покажутся странными, так как это мой первый проект на Pygame.

Для запуска необходимо:
- Создать виртуальное окружение(не обязательно, но тогда будет грустить один маленький venv);
- Установить все зависимости из файла requirements.txt;
- Запустить файл ya_cosmo.py
