from apps.medistore.models.inventorylog_model import InventoryLog
from apps.core.constants.default_values import InventoryAction

def add_log(medicine, quantity_change, performed_by):
    return InventoryLog.objects.create(
        medicine=medicine,
        quantity_change=quantity_change,
        action=InventoryAction.ADDED.value,
        performed_by =performed_by
    )