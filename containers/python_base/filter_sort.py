from sqlalchemy import ARRAY, func
from sqlalchemy.orm import Session


def get_filter_by_args(model, dict_args: dict):
    filters = []
    for key, value in dict_args.items():  # type: str, any
        if key.endswith("__lte"):
            key = key.replace("__lte", "")
            filters.append(getattr(model, key) <= value)
        elif key.endswith("__lt"):
            key = key.replace("__lt", "")
            filters.append(getattr(model, key) < value)
        elif key.endswith("__gte"):
            key = key.replace("__gte", "")
            filters.append(getattr(model, key) >= value)
        elif key.endswith("__gt"):
            key = key.replace("__gt", "")
            filters.append(getattr(model, key) > value)
        elif key.endswith("__ne"):
            key = key.replace("__ne", "")
            filters.append(getattr(model, key) != value)
        elif key.endswith("__eq"):
            key = key.replace("__eq", "")
            filters.append(getattr(model, key) == value)
        else:
            if isinstance(getattr(model, key).type, ARRAY):
                filters.append(
                    func.array_to_string(getattr(model, key), ",").ilike(
                        "%{}%".format(value)
                    )
                )
            else:
                filters.append(getattr(model, key).ilike("%{}%".format(value)))
    return filters


def get_sorter_by_args(model, args: list):
    sorters = []
    for key in args:
        if key[0] == "-":
            sorters.append(getattr(model, key[1:]).desc())
        else:
            sorters.append(getattr(model, key))
    return sorters


def get_results(model, db: Session, filter_args: dict = {}, sort_args: list = []):
    filters = get_filter_by_args(model, filter_args)
    sorters = get_sorter_by_args(model, sort_args)
    return db.query(model).filter(*filters).order_by(*sorters).all()
