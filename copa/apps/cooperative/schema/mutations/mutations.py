import graphene

from .cooperative import AddCooperative
from .member import AddMember, UpdateMember, \
    DeleteMember, AddMemberField, DeleteMemberField, UpdateMemberField, VerifyMembership
from .employee import CreateEmployee,UpdateEmployee,DeleteEmployee

class Mutation(graphene.ObjectType):
    add_cooperative = AddCooperative.Field()
    add_member = AddMember.Field()
    update_member = UpdateMember.Field()
    delete_member = DeleteMember.Field()
    add_member_field = AddMemberField.Field()
    delete_member_field = DeleteMemberField.Field()
    update_member_field = UpdateMemberField.Field()
    verify_membership = VerifyMembership.Field()
    create_cooperativeEmployee= CreateEmployee.Field() 
    update_cooperativeEmployee= UpdateEmployee.Field()
    delete_cooperativeEmployee= DeleteEmployee.Field()