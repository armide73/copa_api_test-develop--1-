import graphene
from graphene_django_extras import DjangoListObjectField
from ..types.cooperative import CooperativeListType, \
    MemberListType, MemberFieldListType, MemberMetaListType,EmployeeType
from graphql_jwt.decorators import login_required
from graphene_django import DjangoListField
from ...models import Cooperative, CooperativeEmployee



class Query(graphene.AbstractType):
    cooperatives = DjangoListObjectField(
        CooperativeListType, description='All Cooperatives query')
    
    # members = DjangoFilterPaginateListField(
    #     MemberListType, pagination=LimitOffsetGraphqlPagination())
    # employee= DjangoListObjectField(EmployeeType,description='All employees query')
    
    employees= graphene.List(EmployeeType,description='All employees query green')
    employe=graphene.Field(EmployeeType, id=graphene.ID())

    members = DjangoListObjectField(
        MemberListType, description='All Members query')
    member_fields = DjangoListObjectField(
        MemberFieldListType,
        description='All Cooperative Member Fields query')
    member_meta = DjangoListObjectField(
        MemberMetaListType,
        description='All Cooperative Member Meta query')

    is_service_enabled = graphene.Boolean(service=graphene.String())

    @login_required
    def resolve_is_service_enabled(self, info, service=None):
        user = info.context.user
        cooperative = user.cooperatives
        if not cooperative:
            return False
        return cooperative.is_service_enabled(service)
  
    def resolve_employees(root,info):
        return CooperativeEmployee.objects.all() 

    def resolve_employe(root, info, id):
        return CooperativeEmployee.objects.get(id=id)    
# class QueryEmp(graphene.ObjectType):
#     employees= graphene.List(EmployeeType,description='All employees query green')

#     def resolve_employees(root,info):
#         return CooperativeEmployee.objects.all()        
