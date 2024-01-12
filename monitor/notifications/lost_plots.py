from apprise.Apprise import Apprise
from monitor.database import session
from monitor.database.queries import get_plot_count
from monitor.format import *
from monitor.notifications.notification import Notification


class LostPlotsNotification(Notification):
    last_plot_count: int
    highest_plot_count: int
    alert_threshold: int

    def __init__(self, apobj: Apprise, node_name: str, alert_threshold: int) -> None:
        super().__init__(apobj)
        self.last_plot_count = None
        self.node_name = node_name
        self.highest_plot_count = None
        self.alert_threshold = alert_threshold

    def condition(self) -> bool:
        with session() as db_session:
            self.last_plot_count = get_plot_count(db_session)

        if self.last_plot_count is not None and self.highest_plot_count is not None and self.last_plot_count < self.highest_plot_count - self.alert_threshold:
            return True
        else:
            self.highest_plot_count = self.last_plot_count
            return False

    def trigger(self) -> None:
        return self.apobj.notify(title='** 🚨 Farmer Lost Plots! 🚨 **',
                                 body="It seems like your farmer lost some plots\n" +
                                 f"Farmer: {self.node_name}\n" +
                                 f"Expected: {self.highest_plot_count}, Found: {self.last_plot_count}\n")

    def recover(self) -> None:
        return self.apobj.notify(title='** ✅ Farmer Plots recoverd! ✅ **',
                                 body=f"Farmer: {self.node_name}\n" +
                                 "Your farmer's plot count has recovered to its previous value")
