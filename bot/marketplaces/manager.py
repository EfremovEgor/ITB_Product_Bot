from marketplaces.wildberries import WildberriesCabinet


def get_notification_id_by_text(marketplace: str, notification_text: str) -> int | None:
    if marketplace.lower().strip() == "wildberries":
        try:
            ids = list()
            for i, x in enumerate(WildberriesCabinet.available_notifications):
                if x == notification_text.capitalize():
                    ids.append(i)
            return ids[0]
        except ValueError:
            return None
