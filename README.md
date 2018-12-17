# Pentix
Вариация компьютерной игры [Тетрис](https://ru.wikipedia.org/wiki/%D0%A2%D0%B5%D1%82%D1%80%D0%B8%D1%81).

*Необходим интерпретатор Python версии не ниже, чем 3.6*
## Правила:
Случайные фигурки пентамино падают сверху в прямоугольное поле шириной 10 и высотой 20 клеток.
В полёте игрок может поворачивать фигурку на 90° и двигать её по горизонтали и вниз.
Также можно «сбрасывать» фигурку, то есть ускорять её падение, когда уже решено, куда фигурка должна упасть.<br />
Фигурка летит до тех пор, пока не наткнётся на другую фигурку либо на дно поля.
Если при этом заполнился горизонтальный ряд из 10 клеток, он пропадает и всё, что выше него, опускается на одну клетку.<br />
Игра заканчивается, когда новая фигурка не может поместиться на поле.<br />
Игрок получает очки за каждый заполненный ряд, поэтому его задача — заполнять ряды, не заполняя само поле (по вертикали) как можно дольше, чтобы таким образом получить как можно больше очков.
## Управление
`Space` - фигурка сбрасывается вниз поля.<br />
`P` - игра ставится на паузу или снимается с паузы (Pause).<br />
`R` - осущетвляется перезапуск игры (Restart).<br />
`UP`, `DOWN`, `RIGHT`, `LEFT` - перемещение фигурки в соответствущие стороны.
## Установка программы
Сохраните папку со сборкой в произвольном каталоге.<br />
В консоли с помощью команды `pip` установите библиотеку PyQt5:
> C:\\>pip install pyqt5

## Автор
Чернущенко Денис, Ноябрь 2017
## Контакты
E-mail   : Denis1.618@yandex.ru