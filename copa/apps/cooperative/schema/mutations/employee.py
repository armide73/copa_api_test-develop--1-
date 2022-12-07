import graphene
# from graphene_django import DjangoObjectType
from ...models import CooperativeEmployee,Cooperative
from ..types.cooperative import EmployeeType






class CreateEmployee(graphene.Mutation):
    class Arguments:
        cooperative_id=graphene.String(required=True)
        names=graphene.String(required=True)
        employee_id=graphene.String(required=True)
        address=graphene.String(required=True)
        phone_number=graphene.String(required=True)    

    employee=graphene.Field(EmployeeType) 

    @classmethod
    def mutate(cls,root,info,names,employee_id,phone_number,cooperative_id,address):
        
        coperativ= Cooperative(id=cooperative_id)
        employee1=CooperativeEmployee(
            names=names,
            employee_id=employee_id,
            address=address,
            phone_number=phone_number
        )  
        employee1.cooperative=coperativ
        employee1.save()
        return CreateEmployee(employee=employee1)   
  

class UpdateEmployee(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
        cooperative_id=graphene.String()
        names=graphene.String()
        employee_id=graphene.String()
        address=graphene.String()
        phone_number=graphene.String()  

    employee=graphene.Field(EmployeeType) 

    @classmethod
    def mutate(cls,root,info,id,names=None,employee_id=None,phone_number=None,cooperative_id=None,address=None):
        
        emp=CooperativeEmployee.objects.get(id=id)

        emp.names=names or emp.names
        emp.employee_id=employee_id or emp.employee_id
        emp.phone_number=phone_number or emp.phone_number
        emp.address=address or emp.address
        if cooperative_id:
            coperativ= Cooperative(id=cooperative_id)
            emp.cooperative=coperativ
            
        emp.save() 
        return UpdateEmployee(employee=emp) 


class DeleteEmployee(graphene.Mutation):
        class Arguments:
            id = graphene.Int(required=True)
          


        employee=graphene.Field(EmployeeType)
        

        @classmethod
        def mutate(cls, root, info, id):
            emp=CooperativeEmployee.objects.get(id=id)

            emp.cooperative=None
            emp.save
            return DeleteEmployee(employee=emp)





        


     
