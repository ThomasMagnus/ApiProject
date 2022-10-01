from django.db import models
from django.db.models import IntegerField, DateField, FloatField


class Delivery(models.Model):

    class Meta:
        __tablename__ = 'delivery'

    id = IntegerField(primary_key=True, auto_created=True, null=False)
    sheet_num = IntegerField(null=False)
    order_num = IntegerField(null=False)
    cost_usd = FloatField(null=False)
    cost_rub = FloatField(null=False)
    delivery_date = DateField()
