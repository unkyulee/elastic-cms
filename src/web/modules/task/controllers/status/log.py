import json
import lib.es as es
import web.util.tools as tools
import web.util.jinja as jinja

def get(p):
    # load instance
    instance_id = p['nav'][-1]
    p['instance'] = es.get(p['host'], 'core_task', 'instance', instance_id)
    if not p['instance']:
        return tools.alert('invalid instance id - {}'.format(instance_id))

    # Search Keyword
    search_keyword = tools.get("search[value]") + "*"

    # Length of the result
    length = tools.get("length")
    if not length: length = 10

    # Offset of the result
    start = tools.get("start")
    if not start: start = 0

    # draw
    draw = tools.get("draw")
    if not draw: draw = 0

    # Apply Search Keyword
    query = "instance_id:{} AND {}".format(instance_id, search_keyword)

    option = 'from={}&size={}&sort=created:desc'.format(start, length)
    # search results
    search_result = es.list(p['host'], 'core_task', 'log', query, option)

    # Get Total number of records
    total = es.count(p['host'], 'core_task', 'log')
    filter_total = es.count(p['host'], 'core_task', 'log', query)

    # Form header
    DataTableJson = {}
    DataTableJson = {
        # draw - this is handshake id which maps the request - response async maps from JS
        "draw": int(draw),
        "recordsTotal": total,
        "recordsFiltered": filter_total,
        "data":[
            [
                log['action'],
                log['message'],
                log['status'],
                log['created']
            ] for log in search_result
        ]
    }

    # Return in JSON format
    return json.dumps(DataTableJson)
