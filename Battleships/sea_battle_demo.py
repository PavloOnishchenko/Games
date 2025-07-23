from copy import deepcopy
from enum import Enum
from os import system, name


class Msg(Enum):
    START = ('This is Demo of Sea Battle game.\n'
             'The goal is to show practical example\n'
             'of Matrix and Collections usage.\n\n'
             'You have 5 ships to set on the field.\n'
             'First ship length needs to be set.\n'
             'Length between 2 and 5 field squares.\n'
             'Next Vertical or Horizontal position.\n'
             'And finally ship start coordinate.\n'
             'First part of coordinate between A-J.\n'
             '2-nd part of coordinate between 1-10.\n'
             'Then same way set fire coordinate.\n'
             'You have to shoot your own ships.\n'
             'Fire coordinate will be asked till\n'
             'all ships are destroyed.\n\n'
             'Press Enter to continue.')
    GAME = ('All ships are placed.\n'
            'Try to remember current ships positions.\n'
            'You are going to fire on them now.\n\n'
            'Press Enter to start.')
    END = ('All ships were destroyed.\n'
           'Thank you for testing.\n\n'
           'Press Enter to exit.')


class ShipPosition(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Mk:
    """Markers used on the battlefield"""
    HAZE = ' • '
    '''unknown part of the battlefield'''
    LOCK = ' . '
    '''next square to the boat or ship'''
    BOAT = '[-]'
    '''horizontal location of warships'''
    SHIP = '[|]'
    '''vertical   location of warships'''
    MISS = '( )'
    '''unsuccessful torpedoing attempt'''
    SHOT = '[*]'
    '''a successful torpedoing attempt'''
    KILL = '[X]'
    '''boat or ship has been destroyed'''


def get_length_of_(ship, ships):
    """Takes a user input of new ship length and checks
    if the value is valid and still available in ships.

    Args:
        ship (int): ordinal number of new ship (1-5).
        ships (str): all available ships with length.

    Returns:
        int: length of new ship taken from user input.
    """
    while True:
        length = input('Available ships:\n'
                       f'{ships}'
                       f'Ship #{ship} length (2<->5): ')
        if length == 'exit':
            system('cls' if name == 'nt' else 'clear')
            exit()

        if not length.isdecimal():
            print('Entered value is not a number, '
                  'try again (2<->5) or type exit')
            continue

        length = int(length)

        if length > 5:
            print('Ship length is more than 5, '
                  'try again (2<->5) or type exit')
            continue

        if length < 2:
            print('Ship length is less than 2, '
                  'try again (2<->5) or type exit')
            continue

        # in string all_ships can be one or two 2, thus
        # index() is flaky and hardcoded value 67 is used
        if length == 2:
            if ships[67] == '0':
                print('All ships with length 2 '
                      'already in use, '
                      'try again (2<->5) or type exit')
                continue

        elif ships[ships.index(f'{length}') + 4] == '0':
            print(f'All ships with length {length} '
                  'already in use, '
                  'try again (2<->5) or type exit')
            continue

        return length


def get_position_of_(ship):
    """Takes a user input of new ship position and checks
    if the value is valid and available in ShipPosition.

    Args:
        ship (int): ordinal number of new ship (1-5).

    Returns:
        ShipPosition.VERTICAL | ShipPosition.HORIZONTAL:
        vertical or horizontal position of new ship taken
        from user input.
    """
    while True:
        position = input(f'Ship #{ship} position '
                         '1 (HORIZONTAL) or '
                         '2 (VERTICAL): ')
        if position == 'exit':
            system('cls' if name == 'nt' else 'clear')
            exit()

        if not position.isdecimal():
            print('Entered value is not a number, '
                  'try again (1 or 2) or type exit')
            continue

        position = int(position)

        if position == 1:
            return ShipPosition.HORIZONTAL

        if position == 2:
            return ShipPosition.VERTICAL

        print('Entered number is not 1 or 2, '
              'try again (1 or 2) or type exit')


def get_coordinate_of_(what, rows):
    """Takes a user input of new ship start coordinate and checks
    if the value is valid and available in the dictionary (rows).

    Args:
        what (str): name (Ship|Fire) for what coordinate is needed.
        rows (dict[str, int]): rows names (A-J) with index (1-10).

    Returns:
        dict[str, int]: start coordinate of new ship taken from
        user input as row name (A-J) and item index (1-10): A1.
    """
    while True:
        coordinate = input(f'{what} coordinate (as A1): ')

        if coordinate == 'exit':
            system('cls' if name == 'nt' else 'clear')
            exit()

        if not coordinate:
            print('Nothing entered, '
                  'try again (as A1) or type exit')
            continue

        # first coordinate here expected as letter A-J
        row = coordinate[0].upper()
        item = None

        # second coordinate here expected as number 1-9
        if len(coordinate) == 2:
            item = int(coordinate[1]) \
                if coordinate[1].isdecimal() \
                else coordinate[1]
        # 2nd - 3rd coordinate here expected as number 10
        elif len(coordinate) == 3:
            item = int(coordinate[1:3]) \
                if coordinate[1:3].isdecimal() \
                else coordinate[1:3]

        # if first coordinate is expected letter and
        # second/third coordinate is expected number
        # then coordinates are correct to be returned
        if row in rows and item in rows.values():
            row = rows.get(row)

            return {'row': row, 'item': item}

        print(f'{coordinate} is incorrect, '
              'try again (as A1) or type exit')


def add_ship_to_battlefield(coordinate,
                            position,
                            length,
                            field,
                            rows):
    """Tries to add new ship on the field if provided ship length
    is not out of the field range and if needed space for ship on
    the field is not occupied by another ship coming from ship
    start coordinate and position (vertical or horizontal).

    Args:
        coordinate (dict[str, int]): start coordinate of new ship.
        position (ShipPosition.VERTICAL | ShipPosition.HORIZONTAL):
                  vertical or horizontal position of new ship.
        length (int): length of new ship.
        field (list[list[int | str]]): 2DMatrix with all game data.
        rows (dict[str, int]): rows names (A-J) with index (1-10).

    Returns:
        list[list[int | str]]: copy of 2DMatrix with all game data
        plus new ship if succeeded to be added or None otherwise.
    """
    new_field = deepcopy(field)
    row = coordinate.get('row')
    item = coordinate.get('item')

    ship_horizontal_end = item + length
    ship_vertical_end = row + length

    if position is ShipPosition.HORIZONTAL:
        if ship_horizontal_end > 11:
            print('Ship length is out of '
                  'HORIZONTAL battlefield range '
                  f'{11 - ship_horizontal_end}, '
                  'try again or type exit')
            new_field = None

            return new_field

        while item < ship_horizontal_end:
            if (Mk.BOAT == new_field[row][item] or
                Mk.SHIP == new_field[row][item] or
                Mk.LOCK == new_field[row][item]):
                row = [key for key in rows.keys()
                       if rows[key] == row][0]
                print(f'Coordinate {row}{item} '
                      'is already occupied '
                      'on the way to coordinate '
                      f'{row}{ship_horizontal_end - 1}, '
                      'try again or type exit')
                new_field = None

                return new_field

            new_field[row][item] = Mk.BOAT
            item += 1

    elif position is ShipPosition.VERTICAL:
        if ship_vertical_end > 11:
            print('Ship length is out of '
                  'VERTICAL battlefield range '
                  f'{11 - ship_vertical_end}, '
                  'try again or type exit')
            new_field = None

            return new_field

        while row < ship_vertical_end:
            if (Mk.BOAT == new_field[row][item] or
                Mk.SHIP == new_field[row][item] or
                Mk.LOCK == new_field[row][item]):
                row1 = [key for key in rows.keys()
                        if rows[key] == row][0]
                row = ship_vertical_end - 1
                row2 = [key for key in rows.keys()
                        if rows[key] == row][0]
                print(f'Coordinate {row1}{item} '
                      'is already occupied '
                      'on the way to coordinate '
                      f'{row2}{item}, '
                      'try again or type exit')
                new_field = None

                return new_field

            new_field[row][item] = Mk.SHIP
            row += 1

    return new_field


def margin_around_ship(coordinate,
                       position,
                       length,
                       field,
                       marker):
    """Adds needed margin around ship depending on its position on
    the filed (there are 9 different unique positions for vertical
    and 9 different unique positions for horizontal ship layouts):

    -------Horizontal-------------------Vertical-------

    case 2   case 1  case 3

    [ 2.b ] [ 1.b ] [ 3.b ]_____[ 2.b ] [ 2.a ] [ 2.c ]_____case 2

    [ 2.a ] [ 1.a ] [ 3.a ]_____[ 1.b ] [ 1.a ] [ 1.c ]_____case 1

    [ 2.c ] [ 1.c ] [ 3.c ]_____[ 3.b ] [ 3.a ] [ 3.c ]_____case 3

    Args:
        coordinate (dict[str, int]): start coordinate of the ship.
        position (ShipPosition.VERTICAL | ShipPosition.HORIZONTAL):
                  vertical or horizontal position of the ship.
        length (int): length of the ship.
        field (list[list[int | str]]): 2DMatrix with all game data.
        marker (str): what margin (LOCK|MISS) around ship to draw.

    Returns:
        list[list[int | str]]: 2DMatrix with all game data plus
        needed margin around ship.
    """
    row = coordinate.get('row')
    item = coordinate.get('item')

    ship_horizontal_end = item + length
    ship_vertical_end = row + length

    if position is ShipPosition.HORIZONTAL:

        # start1/end1:
        # in next three cases ship
        # doesn't touch left/right borders
        start1 = item - 1
        end1 = ship_horizontal_end

        # case1.a: ship doesn't touch top/bottom borders
        if (start1 != 0 and end1 != 11 and
               row != 1 and row != 10):

            for i in [start1, end1]:
                field[row][i] = marker

            for ln in [-1, 1]:
                while start1 <= end1:
                    field[row + ln][start1] = marker
                    start1 += 1

                start1 = item - 1
        # case1.b: ship touches top border
        elif (start1 != 0 and end1 != 11 and
                 row == 1):

            for i in [start1, end1]:
                field[row][i] = marker

            while start1 <= end1:
                field[row + 1][start1] = marker
                start1 += 1
        # case1.c: ship touches bottom border
        elif (start1 != 0 and end1 != 11 and
                 row == 10):

            for i in [start1, end1]:
                field[row][i] = marker

            while start1 <= end1:
                field[row - 1][start1] = marker
                start1 += 1

        # start2/end2:
        # in next three cases ship
        # touches left border
        start2 = item
        end2 = ship_horizontal_end

        # case2.a: ship doesn't touch top/bottom borders
        if (start2 == 1 and
               row != 1 and row != 10):

            field[row][end2] = marker

            for ln in [-1, 1]:
                while start2 <= end2:
                    field[row + ln][start2] = marker
                    start2 += 1

                start2 = item
        # case2.b: ship touches top border
        elif (start2 == 1 and
                 row == 1):

            field[row][end2] = marker

            while start2 <= end2:
                field[row + 1][start2] = marker
                start2 += 1
        # case2.c: ship touches bottom border
        elif (start2 == 1 and
                 row == 10):

            field[row][end2] = marker

            while start2 <= end2:
                field[row - 1][start2] = marker
                start2 += 1

        # start3/end3:
        # in next three cases ship
        # touches right border
        start3 = item - 1
        end3 = ship_horizontal_end - 1

        # case3.a: ship doesn't touch top/bottom borders
        if (end3 == 10 and
             row != 1 and row != 10):

            field[row][start3] = marker

            for ln in [-1, 1]:
                while start3 <= end3:
                    field[row + ln][start3] = marker
                    start3 += 1

                start3 = item - 1
        # case3.b: ship touches top border
        elif (end3 == 10 and
               row == 1):

            field[row][start3] = marker

            while start3 <= end3:
                field[row + 1][start3] = marker
                start3 += 1
        # case3.c: ship touches bottom border
        elif (end3 == 10 and
               row == 10):

            field[row][start3] = marker

            while start3 <= end3:
                field[row - 1][start3] = marker
                start3 += 1

    elif position is ShipPosition.VERTICAL:

        # start1/end1:
        # in next three cases ship
        # doesn't touch top/bottom borders
        start1 = row - 1
        end1 = ship_vertical_end

        # case1.a: ship doesn't touch left/right borders
        if (start1 != 0 and end1 != 11 and
              item != 1 and item != 10):

            for ln in [start1, end1]:
                field[ln][item] = marker

            for i in [-1, 1]:
                while start1 <= end1:
                    field[start1][item + i] = marker
                    start1 += 1

                start1 = row - 1
        # case1.b: ship touches left border
        elif (start1 != 0 and end1 != 11 and
                item == 1):

            for ln in [start1, end1]:
                field[ln][item] = marker

            while start1 <= end1:
                field[start1][item + 1] = marker
                start1 += 1
        # case1.c: ship touches right border
        elif (start1 != 0 and end1 != 11 and
                item == 10):

            for ln in [start1, end1]:
                field[ln][item] = marker

            while start1 <= end1:
                field[start1][item - 1] = marker
                start1 += 1

        # start2/end2:
        # in next three cases ship
        # touches top border
        start2 = row
        end2 = ship_vertical_end

        # case2.a: ship doesn't touch left/right borders
        if (start2 == 1 and
              item != 1 and item != 10):

            field[end2][item] = marker

            for i in [-1, 1]:
                while start2 <= end2:
                    field[start2][item + i] = marker
                    start2 += 1

                start2 = row
        # case2.b: ship touches left border
        elif (start2 == 1 and
                item == 1):

            field[end2][item] = marker

            while start2 <= end2:
                field[start2][item + 1] = marker
                start2 += 1
        # case2.c: ship touches right border
        elif (start2 == 1 and
                item == 10):

            field[end2][item] = marker

            while start2 <= end2:
                field[start2][item - 1] = marker
                start2 += 1

        # start3/end3:
        # in next three cases ship
        # touches bottom border
        start3 = row - 1
        end3 = ship_vertical_end - 1

        # case3.a: ship doesn't touch left/right borders
        if (end3 == 10 and
            item != 1 and item != 10):

            field[start3][item] = marker

            for i in [-1, 1]:
                while start3 <= end3:
                    field[start3][item + i] = marker
                    start3 += 1

                start3 = row - 1
        # case3.b: ship touches left border
        elif (end3 == 10 and
              item == 1):

            field[start3][item] = marker

            while start3 <= end3:
                field[start3][item + 1] = marker
                start3 += 1
        # case3.c: ship touches right border
        elif (end3 == 10 and
              item == 10):

            field[start3][item] = marker

            while start3 <= end3:
                field[start3][item - 1] = marker
                start3 += 1

    return field


def available_ships(length, ships):
    """Reduces amount of available ships after new one with
    given length has been placed on the field.

    Args:
        length (int): length of the ship.
        ships (str): all available ships with length.

    Returns:
        str: amount of all ships which are still available
        after new one with given length has been placed on
        the field.
    """
    # max amount of ships with same length on the field is
    # two, thus amount of ships reduces from two to one and
    # from one to zero if its length provided to this func.
    ships = ships.replace(f'{length}:  1',
                          f'{length}:  0')
    ships = ships.replace(f'{length}:  2',
                          f'{length}:  1')

    return ships


def replace_marker_with_item_index(field, marker):
    """Replaces marker which was used while adding ships on the
    field and not needed anymore with index of the item instead
    of it which will be used further in the program as others
    not occupied items on the field.

    Args:
        field (list[list[int | str]]): 2DMatrix with all game data.
        marker (str): what will be replaced with item index.

    Returns:
        list[list[int | str]]: 2DMatrix with all game data plus
        needed marker replaced with item index.
    """
    for row in field:
        for item in row:
            if item == marker:
                r = field.index(row)
                i = row.index(item)
                field[r][i] = i

    return field


def fire(coordinate, hit, destroyed, field):
    """Fires on provided coordinate on the battlefield and in case
    of succeed checks if ship was destroyed following next patterns
    similar for vertical and horizontal ship position on the field:

    Horizontal case 1

    [-][*][*] : [*][*][*] --> [X][*][*] --> [X][X][*] --> [X][X][X]

    Horizontal case 2

    [*][*][-] : [*][*][*] --> [*][*][X] --> [*][X][X] --> [X][X][X]

    Horizontal case 3

    [*][-][*] : [*][*][*] --> [*][X][*] --> [*][X][X] --> [X][X][X]

    Vertical case 1

    [|] : -------> [*] ---------> [X] ---------> [X] ---------> [X]

    [*] : -------> [*] ---------> [*] ---------> [X] ---------> [X]

    [*] : -------> [*] ---------> [*] ---------> [*] ---------> [X]

    Vertical case 2

    [*] : -------> [*] ---------> [*] ---------> [*] ---------> [X]

    [*] : -------> [*] ---------> [*] ---------> [X] ---------> [X]

    [|] : -------> [*] ---------> [X] ---------> [X] ---------> [X]

    Vertical case 3

    [*] : -------> [*] ---------> [*] ---------> [*] ---------> [X]

    [|] : -------> [*] ---------> [X] ---------> [X] ---------> [X]

    [*] : -------> [*] ---------> [*] ---------> [X] ---------> [X]

    Args:
        coordinate (dict[str, int]): coordinate of the fire.
        hit (set[tuple[int, int]]): unique coord of all hit ships.
        destroyed (dict[str, dict[str, int] | ShipPosition | int]):
                   saves ship coord, layout & length if destroyed.
        field (list[list[int | str]]): 2DMatrix with all game data.

    Returns:
        list[list[int | str]]: 2DMatrix with all game data plus hit
        ship or hit water on the battlefield. Or -copy- of 2DMatrix
        with all game data plus destroyed ship on the battlefield.
    """
    row: int = coordinate.get('row')
    item: int = coordinate.get('item')

    # in this case stop scrolling, function returns field
    if item == field[row][item]:
        field[row][item] = Mk.MISS

    # Horizontal cases
    elif Mk.BOAT == field[row][item]:
        field[row][item] = Mk.SHOT

        # just a counter to check if all ships destroyed
        hit.add((row, item))

        # start checking if ship already destroyed

        # copying field in case if ship still not destroyed
        # thus old version of field will be returned not to
        # mess results with failed attempts to mark ship as
        # destroyed
        new_field = deepcopy(field)
        start = item
        ship_touches_border = False

        # case 1
        if item == 1:
            while new_field[row][item] == Mk.SHOT:
                if new_field[row][item + 1] == Mk.BOAT:

                    return field

                new_field[row][item] = Mk.KILL
                item += 1

            # everywhere below in this point ship destroyed
            # before field copy will be returned lets save:
            # ship coordinate, position and length
            # this data will be used by another function to
            # draw margin around destroyed ship
            length = item - start

            destroyed['coordinate'] = {'row': row,
                                       'item': start}
            destroyed['position'] = ShipPosition.HORIZONTAL
            destroyed['length'] = length

            return new_field

        elif (Mk.BOAT != new_field[row][item - 1] and
              Mk.SHOT != new_field[row][item - 1]):
            while new_field[row][item] == Mk.SHOT:
                if (item != 10 and
                    new_field[row][item + 1] == Mk.BOAT):

                    return field

                new_field[row][item] = Mk.KILL

                if item != 10:
                   item += 1
                else:
                   ship_touches_border = True

            if ship_touches_border:
               item += 1

            length = item - start

            destroyed['coordinate'] = {'row': row,
                                       'item': start}
            destroyed['position'] = ShipPosition.HORIZONTAL
            destroyed['length'] = length

            return new_field

        # case 2
        if item == 10:
            while new_field[row][item] == Mk.SHOT:
                if new_field[row][item - 1] == Mk.BOAT:

                    return field

                new_field[row][item] = Mk.KILL
                item -= 1

            length = start - item
            start = item + 1

            destroyed['coordinate'] = {'row': row,
                                       'item': start}
            destroyed['position'] = ShipPosition.HORIZONTAL
            destroyed['length'] = length

            return new_field

        elif (Mk.BOAT != new_field[row][item + 1] and
              Mk.SHOT != new_field[row][item + 1]):
            while new_field[row][item] == Mk.SHOT:
                if (item != 1 and
                    new_field[row][item - 1] == Mk.BOAT):

                    return field

                new_field[row][item] = Mk.KILL

                if item != 1:
                   item -= 1
                else:
                   ship_touches_border = True

            if ship_touches_border:
               item -= 1

            length = start - item
            start = item + 1

            destroyed['coordinate'] = {'row': row,
                                       'item': start}
            destroyed['position'] = ShipPosition.HORIZONTAL
            destroyed['length'] = length

            return new_field

        # case 3
        if (Mk.SHOT == new_field[row][item - 1] and
            Mk.SHOT == new_field[row][item + 1]):

            new_item = item

            while new_field[row][new_item] == Mk.SHOT:
                if (new_item != 10 and
                    new_field[row][new_item + 1] == Mk.BOAT):

                    return field

                new_field[row][new_item] = Mk.KILL

                if new_item != 10:
                   new_item += 1
                else:
                   ship_touches_border = True

            if ship_touches_border:
               new_item += 1
               ship_touches_border = False

            item -= 1

            while new_field[row][item] == Mk.SHOT:
                if (item != 1 and
                    new_field[row][item - 1] == Mk.BOAT):

                    return field

                new_field[row][item] = Mk.KILL

                if item != 1:
                   item -= 1
                else:
                   ship_touches_border = True

            if ship_touches_border:
               item -= 1

            length = new_item - (item + 1)
            start = item + 1

            destroyed['coordinate'] = {'row': row,
                                       'item': start}
            destroyed['position'] = ShipPosition.HORIZONTAL
            destroyed['length'] = length

            return new_field

    # Vertical cases
    elif Mk.SHIP == field[row][item]:
        field[row][item] = Mk.SHOT

        hit.add((row, item))

        new_field = deepcopy(field)
        start = row
        ship_touches_border = False

        # case 1
        if row == 1:
            while new_field[row][item] == Mk.SHOT:
                if new_field[row + 1][item] == Mk.SHIP:

                    return field

                new_field[row][item] = Mk.KILL
                row += 1

            length = row - start

            destroyed['coordinate'] = {'row': start,
                                       'item': item}
            destroyed['position'] = ShipPosition.VERTICAL
            destroyed['length'] = length

            return new_field

        elif (Mk.SHIP != new_field[row - 1][item] and
              Mk.SHOT != new_field[row - 1][item]):
            while new_field[row][item] == Mk.SHOT:
                if (row != 10 and
                    new_field[row + 1][item] == Mk.SHIP):

                    return field

                new_field[row][item] = Mk.KILL

                if row != 10:
                   row += 1
                else:
                   ship_touches_border = True

            if ship_touches_border:
               row += 1

            length = row - start

            destroyed['coordinate'] = {'row': start,
                                       'item': item}
            destroyed['position'] = ShipPosition.VERTICAL
            destroyed['length'] = length

            return new_field

        # case 2
        if row == 10:
            while new_field[row][item] == Mk.SHOT:
                if new_field[row - 1][item] == Mk.SHIP:

                    return field

                new_field[row][item] = Mk.KILL
                row -= 1

            length = start - row
            start = row + 1

            destroyed['coordinate'] = {'row': start,
                                       'item': item}
            destroyed['position'] = ShipPosition.VERTICAL
            destroyed['length'] = length

            return new_field

        elif (Mk.SHIP != new_field[row + 1][item] and
              Mk.SHOT != new_field[row + 1][item]):
            while new_field[row][item] == Mk.SHOT:
                if (row != 1 and
                    new_field[row - 1][item] == Mk.SHIP):

                    return field

                new_field[row][item] = Mk.KILL

                if row != 1:
                   row -= 1
                else:
                   ship_touches_border = True

            if ship_touches_border:
               row -= 1

            length = start - row
            start = row + 1

            destroyed['coordinate'] = {'row': start,
                                       'item': item}
            destroyed['position'] = ShipPosition.VERTICAL
            destroyed['length'] = length

            return new_field

        # case 3
        if (Mk.SHOT == new_field[row - 1][item] and
            Mk.SHOT == new_field[row + 1][item]):

            new_row = row

            while new_field[new_row][item] == Mk.SHOT:
                if (new_row != 10 and
                    new_field[new_row + 1][item] == Mk.SHIP):

                    return field

                new_field[new_row][item] = Mk.KILL

                if new_row != 10:
                   new_row += 1
                else:
                   ship_touches_border = True

            if ship_touches_border:
               new_row += 1
               ship_touches_border = False

            row -= 1

            while new_field[row][item] == Mk.SHOT:
                if (row != 1 and
                    new_field[row - 1][item] == Mk.SHIP):

                    return field

                new_field[row][item] = Mk.KILL

                if row != 1:
                   row -= 1
                else:
                   ship_touches_border = True

            if ship_touches_border:
               row -= 1

            length = new_row - (row + 1)
            start = row + 1

            destroyed['coordinate'] = {'row': start,
                                       'item': item}
            destroyed['position'] = ShipPosition.VERTICAL
            destroyed['length'] = length

            return new_field

    return field


def print_(message):
    """Inserts a message in dynamically changeable frame and prints
    it.

    Args:
        message (Msg.START | Msg.GAME | Msg.END): gives info before
                 loop which places ships on the battlefield START,
                 then info before the main game loop GAME and final
                 info in the end of the game END.
    """
    message = message.value

    if 'Press Enter to continue' in message:
        system('cls' if name == 'nt' else 'clear')
        print('\n')

    lines = message.split('\n')
    edit_message = ''
    max_length = 0

    for line in lines:
        length = len(line)

        if length > max_length:
            max_length = length

    for line in lines:
        length = len(line)
        spaces = max_length - length
        edit_message += f'| {line}' + ' ' * spaces + ' |\n'

    frame = max_length + 4
    input(f'{'=' * frame}\n'
          f'{edit_message}'
          f'{'=' * frame}\n')

    system('cls' if name == 'nt' else 'clear')

    if 'Press Enter to exit' in message:
        exit()


def print_ships_on_(field, show_ships):
    """Prints 2DMatrix with all game data and shows or hides ships
    on it depends on the provided show ships condition. Also hides
    all numbers from one to ten which fills 2DMatrix where its item
    is not occupied (except first row which is used as coordinate).

    Args:
        field (list[list[int | str]]): 2DMatrix with all game data.
        show_ships (bool): if True then ships will be shown on the
                    battlefield, otherwise ships will be hidden.
    """

    system('cls' if name == 'nt' else 'clear')

    for row in field:
        for item in row:
            if (type(item) is int and
                field.index(row) != 0 or
                item == Mk.BOAT and not show_ships or
                item == Mk.SHIP and not show_ships):
                print(Mk.HAZE, end='\t')
            else:
                print(item, end='\t')
        print('\n')


def play_game():
    all_ships = (f'5:  1 x {'[-]' * 5}\n'
                 f'4:  1 x {'[-]' * 4}\n'
                 f'3:  2 x {'[-]' * 3}\n'
                 f'2:  1 x {'[-]' * 2}\n')

    battlefield = [
        ['  '] + list(range(1, 11)),
        ['A:'] + list(range(1, 11)),
        ['B:'] + list(range(1, 11)),
        ['C:'] + list(range(1, 11)),
        ['D:'] + list(range(1, 11)),
        ['E:'] + list(range(1, 11)),
        ['F:'] + list(range(1, 11)),
        ['G:'] + list(range(1, 11)),
        ['H:'] + list(range(1, 11)),
        ['I:'] + list(range(1, 11)),
        ['J:'] + list(range(1, 11)),
    ]

    row_name_as_index = {
        'A': 1,
        'B': 2,
        'C': 3,
        'D': 4,
        'E': 5,
        'F': 6,
        'G': 7,
        'H': 8,
        'I': 9,
        'J': 10,
    }

    print_(Msg.START)

    all_ships_length = 0

    # loop which places ships on the battlefield
    for new_ship in range(1, 6):
        ship_length = get_length_of_(new_ship, all_ships)
        all_ships_length += ship_length
        ship_position = get_position_of_(new_ship)
        ship_coordinate = None
        ship_on_battlefield = None

        while ship_on_battlefield is None:
            ship_coordinate = get_coordinate_of_(
                                         'Ship '
                                         f'#{new_ship}',
                                         row_name_as_index)
            ship_on_battlefield = add_ship_to_battlefield(
                                         ship_coordinate,
                                         ship_position,
                                         ship_length,
                                         battlefield,
                                         row_name_as_index)
        battlefield = ship_on_battlefield
        battlefield = margin_around_ship(ship_coordinate,
                                         ship_position,
                                         ship_length,
                                         battlefield,
                                         Mk.LOCK)
        print_ships_on_(battlefield, True)
        all_ships = available_ships(ship_length, all_ships)

    battlefield = replace_marker_with_item_index(battlefield,
                                                 Mk.LOCK)
    print_(Msg.GAME)

    hit_coordinates = set()

    # the main game loop
    while len(hit_coordinates) < all_ships_length:
        ship_destroyed = {}
        fire_coordinate = get_coordinate_of_('Fire',
                                             row_name_as_index)
        battlefield = fire(fire_coordinate,
                           hit_coordinates,
                           ship_destroyed,
                           battlefield)
        if ship_destroyed:
            ship_coordinate = ship_destroyed.get('coordinate')
            ship_position = ship_destroyed.get('position')
            ship_length = ship_destroyed.get('length')
            battlefield = margin_around_ship(ship_coordinate,
                                             ship_position,
                                             ship_length,
                                             battlefield,
                                             Mk.MISS)
        print_ships_on_(battlefield, False)

    print_(Msg.END)


if __name__ == '__main__':
    play_game()


# ToDo: finish writing the game by providing computer as an
#  opponent with random placement of ships and random fire
#  with different levels of difficulties (F / SF / S / SS):
#  1. Fire (if ship is hit ignores it continue random fire)
#  2. Smart Fire (if ship is hit continue to search for it)
#  3. Search (is ship with max length which fits the space)
#  4. Smart Search (takes centre of found space which fits)
