from flask import request, render_template
import lib.es as es

def get(p):
    host = p['c']['host'] ; index = p['c']['index'] ;

    # get list of mappings
    mapping = es.mapping(host, index, 'post')
    properties = mapping[index]['mappings']['post']['properties']

    # get all field list
    p['field_list'] = []
    for prop in properties.keys():
        field = es.get(host, index, 'field', prop)
        if not field:
            # create field
            field = {
                "type": properties[prop].get('type'),
                "name": prop,
                "order_key": '10000'
            }
            es.create(host, index, 'field', prop, field)
            es.flush(host, index)
            field['id'] = prop

        # add to field list
        p['field_list'].append(field)

    # sort by order key
    p['field_list'] = sorted(p['field_list'],
        key=lambda field: int(field['order_key'] if field['order_key'] else 10000))

    return render_template("post/field/default.html", p=p)
