from copa.apps.cooperative.models import Cooperative, Member
from copa.apps.stock.models import Productivity, ProductivityMeta, \
    ProductivityField
import graphene
from ..types.stock_types import ProductivityInputType, \
    ProductivityType, ProductivityMetaInputType, ProductivityFieldInputType, \
    ProductivityFieldType
from .....utils.app_utils.database import SaveContextManage, \
    get_model_object
from .....utils.responses.common import SUCCESS_RESPONSES


class AddProductivity(graphene.Mutation):
    """
    Add Productivity

    Args:
        new_production (obj): productivity object data
    """
    success = graphene.String()
    productivity = graphene.Field(ProductivityType)

    class Arguments:
        new_production = graphene.Argument(ProductivityInputType)
        productivity_meta = graphene.List(ProductivityMetaInputType)

    def mutate(self, info, **kwargs):
        # declare variables
        production = kwargs.get('new_production')
        productivity_meta = kwargs.get('productivity_meta')

        # check fields
        cooperative = get_model_object(
            Cooperative, 'id', production['cooperative'])

        member = get_model_object(
            Member, 'id', production['member'])

        # create instance
        production_instance = Productivity(
            cooperative=cooperative,
            member=member,
            quantity=production['quantity'],
            price_per_unity=production['price_per_unity'],
        )

        # save data
        with SaveContextManage(production_instance,
                               model=Productivity) as productivity:
            if productivity_meta and len(productivity_meta) > 0:
                for data in productivity_meta:
                    if data['value'] != '':
                        meta = ProductivityMeta(
                            productivity=productivity,
                            key=data['key'],
                            value=data['value']
                        )
                        meta.save()
            return AddProductivity(
                success='Winjije neza umusaruro',
                productivity=productivity)


class UpdateProductivity(graphene.Mutation):
    """
    Productivity Update Mutation

    Args:
        id ([str]): [productivity key value]
        productivity_data ([obj]): [productivity default attributes]
        productivity_meta ([lst]): [productivity metat data]
    """
    success = graphene.String()
    productivity = graphene.Field(ProductivityType)

    class Arguments:
        id = graphene.String(required=True)
        productivity_data = graphene.Argument(ProductivityInputType)
        productivity_meta = graphene.List(ProductivityMetaInputType)

    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        data = kwargs.get('productivity_data')
        meta = kwargs.get('productivity_meta')

        productivity = get_model_object(Productivity, 'id', id)

        for key in data.keys():
            if key == 'quantity':
                productivity.quantity = data[key] or \
                    productivity.quantity
            elif key == 'unity':
                productivity.unity = data[key] or \
                    productivity.unity
            elif key == 'price_per_unity':
                productivity.price_per_unity = data[key] or \
                    productivity.price_per_unity

        with SaveContextManage(productivity,
                               model=Productivity) as productivity:
            if len(meta) > 0:
                for meta_data in meta:
                    meta = ProductivityMeta.objects.filter(
                        key=meta_data['key'],
                        productivity=productivity).first()
                    if meta:
                        meta.value = meta_data['value'] or meta.value
                        meta.save()
                    else:
                        meta = ProductivityMeta(
                            productivity=productivity,
                            key=meta_data['key'],
                            value=meta_data['value']
                        )
                        meta.save()
        return UpdateProductivity(
            success='Uhinduye neza umusaruro',
            productivity=productivity)


class DeleteProductivity(graphene.Mutation):
    """
    Delete Productivity Mutation

    Args:
        ids ([str]): [productivity primary key]
    """
    success = graphene.String()

    class Arguments:
        id = graphene.List(graphene.String)

    def mutate(self, info, **kwargs):

        ids = kwargs.get('id')
        for id in ids:
            productivity = get_model_object(Productivity, 'id', id)

            productivity.delete()

        return DeleteProductivity(
            success=SUCCESS_RESPONSES['removed'].format('Productivity'))


class AddProductivityField(graphene.Mutation):
    """
    Add Productivity Field

    Args:
        new_productivity_field ([obj]): [new productivity data]
    """
    success = graphene.String()
    productivity_field = graphene.Field(ProductivityFieldType)

    class Arguments:
        new_field = graphene.Argument(ProductivityFieldInputType)

    def mutate(self, info, **kwargs):
        new_field = kwargs.get('new_field')

        cooperative = get_model_object(
            Cooperative, 'id', new_field['cooperative'])

        for key, value in new_field.items():
            if key == 'cooperative':
                new_field[key] = cooperative

        productivity_field = ProductivityField(**new_field)

        with SaveContextManage(productivity_field,
                               model=ProductivityField) as field:
            return AddProductivityField(
                success=SUCCESS_RESPONSES['created'].format('Productivity'),
                productivity_field=field)


class UpdateProductivityField(graphene.Mutation):
    """
    Update Productivity Field

    Args:
        id ([str]): [primary key]
        field_data ([obj]): [productivity object data]
    """
    success = graphene.String()
    productivity_field = graphene.Field(ProductivityFieldType)

    class Arguments:
        id = graphene.String(required=True)
        field_data = graphene.Argument(ProductivityFieldInputType)

    def mutate(self, info, **kwargs):
        field_data = kwargs.get('field_data')

        field_instance = get_model_object(
            ProductivityField, 'id', kwargs.get('id'))

        for key, value in field_data.items():
            if key == 'cooperative':
                setattr(
                    field_instance, key,
                    get_model_object(Cooperative, 'id', value))
            else:
                setattr(field_instance, key, value)

        with SaveContextManage(field_instance,
                               model=ProductivityField) as field:
            return UpdateProductivityField(
                success=SUCCESS_RESPONSES['updated'].format('Productivity'),
                productivity_field=field)


class DeleteProductivityField(graphene.Mutation):
    """
    Delete Productivity Field

    Args:
        id ([str]): [primary key]
    """
    success = graphene.String()

    class Arguments:
        id = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        success = SUCCESS_RESPONSES['deleted'].format('Productivity Field')

        field = get_model_object(ProductivityField, 'id', kwargs.get('id'))

        field.hard_delete()

        return DeleteProductivityField(success=success)
