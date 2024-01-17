from monitor.database import session
from monitor.database.queries import get_sync_status
from monitor.format import *
from monitor.notifications.notification import Notification
from apprise.Apprise import Apprise

class LostSyncNotification(Notification):

    
    def __init__(self, apobj: Apprise, node_name: str) -> None:
        super().__init__(apobj)
        self.node_name = node_name

    def condition(self) -> bool:
        with session() as db_session:
            sync_status = get_sync_status(db_session)
        return sync_status is not None and not sync_status

    def trigger(self) -> None:
        return self.apobj.notify(
            title='** 🚨 Farmer Lost Sync! 🚨 **',
            body=f"Farmer: {self.node_name}\n" +
            "It seems like your farmer lost its connection to the Chia Network")

    def recover(self) -> None:
        return self.apobj.notify(title='** ✅ Farmer Synced! ✅ **',
                                 body=f"Farmer: {self.node_name}\n" +
                                 "Your farmer is successfully synced to the Chia Network again")
