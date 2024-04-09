import pymunk


def add_walls(space, screen_width, screen_height, wall_thickness, elasticity,
              friction):
    """
    Добавляет стены на игровое поле.

    :param space: Объект пространства, в котором будут размещены стены.
    :param screen_width: Ширина экрана.
    :param screen_height: Высота экрана.
    :param wall_thickness: Толщина стен.
    :param elasticity: Упругость стен.
    :param friction: Трение стен.
    """
    # Создаем стены как объекты Segment
    walls = [
        pymunk.Segment(space.static_body, (0, 0), (screen_width, 0),
                       wall_thickness),
        pymunk.Segment(space.static_body, (0, 0), (0, screen_height),
                       wall_thickness),
        pymunk.Segment(space.static_body, (screen_width, 0),
                       (screen_width, screen_height), wall_thickness),
        pymunk.Segment(space.static_body, (0, screen_height),
                       (screen_width, screen_height), wall_thickness)
    ]

    # Назначаем каждой стене упругость и трение
    for wall in walls:
        wall.elasticity = elasticity
        wall.friction = friction

    # Добавляем стены в пространство
    space.add(*walls)
