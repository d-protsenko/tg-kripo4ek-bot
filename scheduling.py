import threading
import db_controller
import scheduler_utils
import actions


def create_scheduled_event(interval, action_name, actionargs={}):
    threading.Timer(
        interval,
        create_scheduled_event,
        (interval, action_name, actionargs)
    ).start()
    getattr(actions, action_name)(actionargs)


class Scheduler:

    def __init__(self):
        self.events = {}

    def load_events(self, events):
        self.events = events
        for _ in events:
            create_scheduled_event(_.interval, _.action_name, _.actionargs)

    def add_event(self, id: str, event: scheduler_utils.Event):
        if db_controller.save_event_to_db(id, event):
            threading.Timer(
                event.interval,
                create_scheduled_event,
                (event.interval, event.action_name, event.actionargs)
            ).start()
