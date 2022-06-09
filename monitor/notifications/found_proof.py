from monitor.database import session
from monitor.database.queries import get_proofs_found
from monitor.format import *
from monitor.notifications.notification import Notification
from apprise import Apprise


class FoundProofNotification(Notification):
    last_proofs_found: int = None
    alert_role_id: str = None

    def __init__(self, apobj: Apprise, alert_role_id: str) -> None:
        super().__init__(apobj)
        self.alert_role_id = alert_role_id

    def condition(self) -> bool:
        with session() as db_session:
            proofs_found = get_proofs_found(db_session)
        if proofs_found is not None and self.last_proofs_found is not None and proofs_found > self.last_proofs_found:
            self.last_proofs_found = proofs_found
            return True
        else:
            self.last_proofs_found = proofs_found
            return False

    def trigger(self) -> None:
        if not self.alert_role_id:
            return self.apobj.notify(title='** 🤑 Proof found! 🤑 **',
                                 body="Your farm found a new partial or full proof")
        else:
            return self.apobj.notify(title='** 🤑 Proof found! 🤑 **',
                                 body="<@&"+self.alert_role_id+"> Your farm found a new partial or full proof")
