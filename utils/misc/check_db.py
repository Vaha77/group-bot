import schedule
from django.forms import model_to_dict

from database.models import *

# ADMINS = []
# ADMINS_NAME = []

def check_db_for_admin(FreeList=None):
    adm = Admins.select()
    aaa = [model_to_dict(item) for item in adm]
    for i in aaa:
        FreeList.append({"id":i["admin_id"]})
        FreeList.append({"name":i["admin_name"]})
    print("55")

schedule.every(5).seconds.do(check_db_for_admin)

while True:
    schedule.run_pending()