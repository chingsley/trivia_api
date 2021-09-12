def paginate_data(request, query_result):
    page = request.args.get('page', 0, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    start = page * page_size
    end = start + page_size
    plants = [plant.format() for plant in query_result]
    return plants[start:end]


def format_query_result(query_result):
    return [record.format() for record in query_result]
