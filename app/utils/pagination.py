def paginate(items, page: int = 1, page_size: int = 10):
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end]