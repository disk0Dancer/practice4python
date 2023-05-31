'''
 Структура данных водителей не должна содержать информации о автобусах кроме ID,
           при выводе истории необходимо выводить данные исходя из связки по ID.
 {
    'Автобусы': 
        [
            {
                'id': value,
                'Гос. номер': value,
                'Маршрут': value,
                'Дата ТО': value, …
            }
        ],
    'Водители':
        [
            {
                'ФИО': value,
                'История':  
                    [
                        {
                            'id' : value,
                            'Дата выезда': datetime value,
                            'Дата сдачи смены': datetime value
                        }, …
                    ]
            }
        ]
    }
}

Реализуйте хранение и необходимые методы обработки 
    (добавление / удаление / редактирование данных, вывод данных по параметру)

{'id': 'value', 'Гос. номер': 'value', 'Маршрут': 'value', 'Дата ТО': 'value'}
{'ФИО': 'value', 'История': [{'id': 'value', 'Дата выезда': 'datetimevalue', 'Дата сдачи смены': 'datetimevalue'}]}
'''
import json
import datetime
from pprint import pprint

today = datetime.date.today()


def menu():
    print('''
    
ГЛАВНОЕ МЕНЮ
1) Автобусы
2) Водители
3) Выход ''')


def bus_menu():
    print('''
    
МЕНЮ Автобусов
1) Показать все Автобусы
2) Показать информацию об  Автобусе по ID
3) Добавить Автобус
4) Изменить информацию об Автобусе
5) Удалить данные об Автобусе по ID
6) Удалить данные об Автобусах
7) Назад
    ''')


def driver_menu():
    print('''
    
МЕНЮ ВОДИТЕЛЕЙ
1) Показать всех Водителей
2) Показать информацию о  Водитиле по ФИО
3) Добавить Водителя
4) Изменить информацию о Водителе
5) Удалить данные о Водителе по ФИО
6) Удалить данные о Водителях
7) Назад
    ''')


def input_int(min, max, message=''):
    '''Считывание целого числа от min до max(включительно)'''
    is_int = False#флаг для остановки цикла

    while 1:
        if is_int:
            break#проверка конвертации
        print(message + "Введите целое число:")

        try:
            num = int(input())#попытка конвертации
            if min <= num <= max:
                is_int = True#флаг
            else:
                print("Число НЕ попадает в допустимый диапазон!")
        except:
            print("\nЧисло введено НЕверно!")
            continue#переход к след итерации
    return num


def get_date(msg):
    while 1:
        print(msg)
        try:
            line = input("Введите дату в формате дд/мм/гггг : ")
            a = [int(x) for x in line.split('/')][::-1]
            Date = datetime.date(a[0], a[1], a[2])
            return Date
        except Exception as e:
            print('Неверный формат даты! (', e, ')')
            continue


def get_str(msg):
    line = ''
    while len(line) < 1:
        #print(msg)
        try:
            line = input(msg)
        except:
            print('Значение введено неверно!')
    return line


def bus_get(file, msg):
    # СЧИТЫВАИЕ ДАННЫХ О АВТОБУСЕ
    id = input_int(0, 1000, "Установите значение ID. ")
    if len(bus_search_id(id)) != 0:
        print(msg)
        return file
    else:
        print('\n')
        file['Автобусы'].append({})
        file['Автобусы'][-1]['id'] = id
        file['Автобусы'][-1]['Гос. номер'] = get_str("Установите значение Гос.Номера:")
        file['Автобусы'][-1]['Маршрут'] = input_int(0, 1000, "Установите значение Маршрута. ")
        file['Автобусы'][-1]['Дата ТО'] = str(get_date('Установите Дату ТО.'))

        pprint(file)
        # сохраниение
        with open('bus_driver.json', 'w') as f:
            json.dump(file, f, ensure_ascii=False, indent=3)
        return file


def bus_change(file, msg):
    # СЧИТЫВАИЕ ДАННЫХ О АВТОБУСЕ
    id = input_int(0, 1000, "Установите значение ID. ")
    if len(bus_search_id(id)) == 0:
        print(msg)
        return file
    else:
        for i in range(len(file['Автобусы'])):
            if file['Автобусы'][i]['id'] == id:
                ind = i
        print('\n')
        #file['Автобусы'].append({})
        file['Автобусы'][ind]['id'] = id#                                    ! запрет изменения id  для автобуса
        file['Автобусы'][ind]['Гос. номер'] = get_str("Установите значение Гос.Номера:")
        file['Автобусы'][ind]['Маршрут'] = input_int(0, 1000, "Установите значение Маршрута. ")
        file['Автобусы'][ind]['Дата ТО'] = str(get_date('Установите Дату ТО.'))
        # когда делаи то?
        #pprint(file)
        # сохраниение
        print(f'Данные об Автобусе {id} обновлены.')
        with open('bus_driver.json', 'w') as f:
            json.dump(file, f, ensure_ascii=False, indent=3)
        return file


def driver_get(file):
    # СЧИТЫВАИЕ ДАННЫХ О Водиле БЕЗ ПРОВЕРОК
    fio = get_str('Введите ФИО Водителя:')
    if len(driver_search_id(fio)) != 0:
        print("Данные об этом Водителе уже есть!")
        return file
    else:
        print('\n')
        file['Водители'].append({})
        file['Водители'][-1]['ФИО'] = fio

        while 1:
            option = input_int(1, 2, f'Добавить поездку?\n1. Да\n2. Нет\n')
            if option == 2:
                break
            else:
                file = driver_add_ride(file['Водители'][-1]['ФИО'], -1)

        with open('bus_driver.json', 'w') as f:
            json.dump(file, f, ensure_ascii=False, indent=3)
        return file
        # добавить водителя -> добавить опр водителю поездку ( для автобусов о которых есть данные )


def driver_change(file):
    # СЧИТЫВАИЕ ДАННЫХ О Водиле БЕЗ ПРОВЕРОК
    fio = get_str('Введите ФИО Водителя:')
    i = 0
    if len(driver_search_id(fio)) == 0:
        print("Данных об этом Водителе еще нет!")
        return file
    else:
        print('\n')

        while file['Водители'][i]['ФИО'].lower() != fio.lower():
            i += 1

        while 1:
            match input_int(1, 4, f'Редактирование Истории поездок:\n1. Добавить поездку\n2. Удалить поездку\n3. Изменить поездку\n4. Далее\n'):
                case 1:
                    file = driver_add_ride(file['Водители'][i]['ФИО'], i)
                case 2:
                    file = driver_del_ride(file['Водители'][i]['ФИО'], i)
                case 3:
                    file = driver_change_ride(file['Водители'][i]['ФИО'], i)
                case 4:
                    print('История поездок обновлена.')
                    break

        with open('bus_driver.json', 'w') as f:
            json.dump(file, f, ensure_ascii=False, indent=3)
        return file


#
#

def driver_add_ride(fio, ind):
    #добавление

    driver_ride_history(ind)

    if 'История' not in file['Водители'][ind].keys():
        file['Водители'][ind]['История'] = []
    file['Водители'][ind]['История'].append({})
    while 1:
        id = input_int(0, 1000, 'Введите id автобуса. ')
        if len(bus_search_id(id)) == 0:
            print(f"Нет данных об Автобусе с id = {id}!")
            continue
        file['Водители'][ind]['История'][-1]['id'] = id

        start_date = get_date('Установите Дату Выезда: ')
        print()
        end_date = get_date('Установите Дату Сдачи Смены: ')
        print()
        if start_date <= end_date:
            file['Водители'][ind]['История'][-1]['Дата выезда'] = str(start_date)
            file['Водители'][ind]['История'][-1]['Дата сдачи смены'] = str(end_date)
            print('Поездка добавлена.\n')
            break
        else:
            print('\nДата сдачи смены < Даты начала смены!')
            continue
    return file


def driver_del_ride(fio, ind):
    #удаление поездки из истории водилы по фио + индекс поездки в истории
    if 'История' in file['Водители'][ind].keys() and len(file['Водители'][ind]['История'])>0:
        driver_ride_history(ind)
        ride_ind = input_int(1, len(file['Водители'][ind]['История']), 'Введите номер поездки которую желаете удалить. ')-1
        file['Водители'][ind]['История'].pop(ride_ind-1)
        print('Поездка удалена.\n')
    else:
        print('Пустая история поездок!')
    return file


def driver_change_ride(fio, ind):
    # изменение

    driver_ride_history(ind)

    if 'История' not in file['Водители'][ind].keys() or len(file['Водители'][ind]['История'])<1:
        print('Пустая история поездок!')
        return file
    while 1:
        ride_ind = input_int(1, len(file['Водители'][ind]['История']),
                             'Введите номер поездки которую желаете Изменить. ')-1
        id = input_int(0, 1000, 'Введите id автобуса. ')
        if len(bus_search_id(id)) == 0:
            print(f"Нет данных об Автобусе с id = {id}!")
            continue
        file['Водители'][ind]['История'][ride_ind]['id'] = id

        start_date = get_date('Установите Дату Выезда: ')
        print()
        end_date = get_date('Установите Дату Сдачи Смены: ')
        print()
        if start_date <= end_date:
            file['Водители'][ind]['История'][ride_ind]['Дата выезда'] = str(start_date)
            file['Водители'][ind]['История'][ride_ind]['Дата сдачи смены'] = str(end_date)
            print('Поездка добавлена.\n')
            break
        else:
            print('\nДата сдачи смены < Даты начала смены!')
            continue
    return file


def driver_ride_history(ind):
    # история поездок водителя
    if 'История' in file['Водители'][-1].keys():
        print('\nТекущая История поездок:')
        for i in range(len(file['Водители'][ind]['История'])):
            print(i+1, '-'*9)
            for data in ['id', 'Дата выезда', 'Дата сдачи смены']:
                print(f"{data} : {file['Водители'][ind]['История'][i][data]}")
        print()


def bus_search_id(id):
    # поиск автобуса по ид, возврат данных автобуса
    for i in file["Автобусы"]:
        if i['id'] == id:
            return i
    return {}


def driver_search_id(fio):
    # поиск водилы по фио, возврат данных водилы
    for i in file["Водители"]:
        if i['ФИО'].lower() == fio.lower():
            return i
    return {}


def driver_print(driver):
    # красивая печать данных о водителе

    print('-'*10, f"\nФИО : {driver['ФИО']}")
    if 'История' in driver.keys():
        for ride in driver['История']:
            print('='*10)
            for data in ['id', 'Дата выезда', 'Дата сдачи смены']:
                print(f"{data} : {ride[data]}")
    else:
        print('Пустая история поездок!')


def bus_print(bus):
    # красивая печать данных об Автобусе
    print('-'*20)
    for data in ['id', 'Гос. номер', 'Маршрут', 'Дата ТО']:
        print(f"{data} : {bus[data]}")

# дефолт бд
#file = {"Автобусы": [], "Водители": []}
#with open('bus_driver.json', 'w') as f:
#    json.dump(file, f, ensure_ascii=False)
#    pprint(file)


try:
    with open('bus_driver.json', 'r') as f:
        file = json.load(f)
        pprint(file)
except IOError:
    print('Файл не существует в каталоге! Он будет создан ситемой.')
    file = {"Автобусы": [], "Водители": []}
    with open('bus_driver.json', 'w') as f:
        json.dump(file, f, ensure_ascii=False)
        pprint(file)
except:
    print("Ошибка в стуртуре файла! Файл будет перезаписан.")
    file = {"Автобусы": [], "Водители": []}
    with open('bus_driver.json', 'w') as f:
        json.dump(file, f, ensure_ascii=False)
        pprint(file)


while 1:
    menu()
    option = input_int(1, 3, "Ввыберите пункт меню. ")
    match option:

        case 1:# автобусы
            while 1:
                # перезагрузка данных
                with open('bus_driver.json', 'r') as f:
                    file = json.load(f)
                bus_menu()
                option = input_int(1, 7, "Ввыберите пункт меню. ")
                match option:

                    case 1:# показать всех
                        if len(file['Автобусы']) > 0:
                            for bus in file['Автобусы']:
                                bus_print(bus)
                        else:
                            print('\nНет данных об автобусах!')

                    case 2:# показать 1 по ключу
                        id = input_int(0, 1000, "Установите значение ID. ")
                        if len(bus_search_id(id)) > 0:
                            bus_print(bus_search_id(id))# печать найденного автобуса
                        else:
                            print('Данных об этом Автобусе нет!')

                    case 3:# добавить
                        file = bus_get(file, "Данные об Автобусе с таким ID уже добавлены!")

                    case 4:# изменить
                        file = bus_change(file, "Данные об Автобусе с таким ID еще НЕ добавлены!")
                        # изменить ид в историях, если он был изменен


                    case 5:# удалить
                        id = input_int(0, 1000, "Установите значение ID. ")
                        if len(bus_search_id(id)) > 0:
                            for i in range(len(file['Автобусы'])-1):
                                if file['Автобусы'][i]['id'] == id:
                                    file['Автобусы'].pop(i)
                            print("Данные об Автобусе удалены!")

                            # удаление данных об этом автобусе из истории поездок водителей
                            for driver in file['Водители']:
                                if 'История' in driver.keys():
                                    for ride in range(len(driver['История'])):
                                        if driver['История'][ride]['id'] == id:
                                            driver['История'].pop(ride)

                            with open('bus_driver.json', 'w') as f:
                                json.dump(file, f, ensure_ascii=False, indent=3)
                        else:
                            print('Данных об этом Автобусе нет!')


                    case 6:# очистить
                        file['Автобусы'] = []
                        with open('bus_driver.json', 'w') as f:
                            json.dump(file, f, ensure_ascii=False, indent=3)
                        print('\nДанные об Автобусах удалены.')

                    case 7:# назад
                        print('\nНазад.')
                        break

        case 2:# водители

            while 1:
                # перезагрузка данных
                with open('bus_driver.json', 'r') as f:
                    file = json.load(f)
                driver_menu()
                option = input_int(1, 7, "Ввыберите пункт меню. ")
                match option:
                    case 1:# показать всех
                        if len(file['Водители']) > 0:
                            for d in file['Водители']:
                                driver_print(d)
                        else:
                            print('\nНет данных о водителях!')

                    case 2:# показать 1 по фио
                        fio = get_str('\nВведите ФИО Водителя:')
                        if len(driver_search_id(fio)) > 0:
                            driver_print(driver_search_id(fio))# печать данных найденного водителя
                        else:
                            print('Данных об этом Водителе нет!')

                    case 3:# добавить
                        file = driver_get(file)

                    case 4:# изменить
                        file = driver_change(file)

                    case 5:# удалить
                        fio = get_str('\nВведите ФИО Водителя:')
                        if len(driver_search_id(fio)) > 0:
                            for i in range(len(file['Водители'])):
                                if file['Водители'][i]['ФИО'].lower() == fio.lower():
                                    file['Водители'].pop(i)
                            with open('bus_driver.json', 'w') as f:
                                json.dump(file, f, ensure_ascii=False, indent=3)
                            print("Данные о Водителе удалены!")
                        else:
                            print('Данных об этом Водителе нет!')

                    case 6:# очистить
                        file['Водители'] = []
                        with open('bus_driver.json', 'w') as f:
                            json.dump(file, f, ensure_ascii=False, indent=3)
                        print('\nДанные о Водителях удалены.')

                    case 7:# назад
                        print('\nНазад.')
                        break

        case 3:# выход

            print('\nКонец.')
            break

#существование файла
#   проверка коректности структуры ( перезаписать + сообщение )
#   *   проверить изменение автобуса ( дублирование )
#изменение поездки

# какого хрена все работает как часы???