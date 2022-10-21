from tortoise import fields, models

class Networks(models.Model):
    id_net = fields.IntField(pk=True, unique=True)
    name = fields.CharField(max_length=100, null=True)
    description = fields.CharField(max_length=100, null=True)
    ip_net = fields.CharField(max_length=20, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    interfaces: fields.ReverseRelation["Interfaces"]

    def __str__(self):
        return f"<ID {self.id_net}> Network: {self.ip_net}, name: {self.name}"

class Interfaces(models.Model):
    id_if = fields.IntField(pk=True, unique=True)
    #id_net_if = fields.ForeignKeyField('models.Networks', related_name="id_net")
    #id_net = fields.IntField()
    net = fields.ForeignKeyField('models.Networks', related_name="interfaces")
    name = fields.CharField(max_length=100, null=True)
    description = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"<ID {self.id_if}> Interface: {self.name} on network ID {self.net}"