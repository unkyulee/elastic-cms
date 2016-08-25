from flask import render_template, request
import lib.es as es
import web.util.tools as tools


def get(p):
    # load schedule
    schedule_id = p['nav'][-1]
    schedule = es.get(p['host'], 'core_task', 'schedule', schedule_id)
    if not schedule:
        return tools.alert('schedule not found - {}'.format(schedule_id))

    es.delete(p['host'], 'core_task', 'schedule', schedule_id)
    es.flush(p['host'], 'core_task')

    return tools.redirect(request.referrer)
