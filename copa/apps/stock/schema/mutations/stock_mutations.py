import graphene
from .productivity import AddProductivity, \
    UpdateProductivity, DeleteProductivity, AddProductivityField, \
    DeleteProductivityField, UpdateProductivityField
from .send_message import SendMessage


class Mutation(graphene.ObjectType):
    add_productivity = AddProductivity.Field()
    update_productivity = UpdateProductivity.Field()
    delete_productivity = DeleteProductivity.Field()
    send_productivity_message = SendMessage.Field()
    add_productivity_field = AddProductivityField.Field()
    update_productivity_field = UpdateProductivityField.Field()
    delete_productivity_field = DeleteProductivityField.Field()
