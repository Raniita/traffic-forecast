from enum import unique
from tortoise import fields, models

class Networks(models.Model):
    id = fields.BigIntField(pk=True, unique=True)
    id_network = fields.BigIntField(unique=True)
    name = fields.CharField(max_length=100, null=True)
    description = fields.CharField(max_length=100, null=True)
    ip_network = fields.CharField(max_length=20, null=True)
    influx_net = fields.CharField(max_length=30, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    interfaces: fields.ReverseRelation["Interfaces"]

    def __str__(self):
        return f"<ID {self.id_network}> Network: {self.ip_network}, name: {self.name}"

class Interfaces(models.Model):
    id = fields.BigIntField(pk=True, unique=True)
    id_interface = fields.BigIntField(unique=True)
    name = fields.CharField(max_length=100, null=True)
    description = fields.CharField(max_length=100, null=True)
    influx_rx = fields.CharField(max_length=30, null=False)
    influx_tx = fields.CharField(max_length=30, null=False)
    network = fields.ForeignKeyField('models.Networks', related_name="interfaces")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    

    def __str__(self):
        return f"<ID {self.id_interface}> Interface: {self.name} on network"