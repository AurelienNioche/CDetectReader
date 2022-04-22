import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = "CDetectReader.settings"

django.setup()

from read.models import Entry

rsp = input("Are you sure you want to erase everything? (y/n)")
if rsp == "y":
    Entry.objects.all().delete()
    print("erased")
else:
    print("operation cancelled")