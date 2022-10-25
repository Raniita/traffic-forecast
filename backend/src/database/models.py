from enum import unique
from tortoise import fields, models

class Networks(models.Model):
    id = fields.BigIntField(pk=True, unique=True)
    id_network = fields.BigIntField(unique=True)
    name = fields.CharField(max_length=100, null=True)
    description = fields.CharField(max_length=100, null=True)
    ip_network = fields.CharField(max_length=20, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    interfaces: fields.ReverseRelation["Interfaces"]

    def __str__(self):
        return f"<ID {self.id_network}> Network: {self.ip_network}, name: {self.name}"

class Interfaces(models.Model):
    id = fields.BigIntField(pk=True, unique=True)
    id_interface = fields.BigIntField(unique=True)
    #id_net_if = fields.ForeignKeyField('models.Networks', related_name="id_net")
    #id_net = fields.IntField()
    network = fields.ForeignKeyField('models.Networks', related_name="interfaces")
    name = fields.CharField(max_length=100, null=True)
    description = fields.CharField(max_length=100, null=True)
    #created_at = fields.DatetimeField(auto_now_add=True)
    #modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"<ID {self.id_interface}> Interface: {self.name} on network"