from django.utils import timezone
import graphene
from graphql_jwt.decorators import login_required

from copa.apps.pricing.models import Pricing, Subscription

from ..types.cooperative import MemberInputType, \
    MemberType, MemberMetaInputType, MemberFieldType, MemberFieldInputType
from ...models import Member, Cooperative, MemberMeta, MemberField
from .....services.kudibooks.vendor import KudiVendor
from .....utils.app_utils.database import SaveContextManage, \
    get_model_object
from .....utils.responses.common import SUCCESS_RESPONSES


class AddMember(graphene.Mutation):
    """
    Add Member Mutation

    Args:
        new_member ([obj]): [member object data]
    """
    success = graphene.String()
    member = graphene.Field(MemberType)

    class Arguments:
        new_member = graphene.Argument(MemberInputType)
        meta_data = graphene.List(MemberMetaInputType)

    @login_required
    def mutate(self, info, **kwargs):
        success = 'Member created successfully'

        new_member = kwargs.get('new_member')
        meta_data = kwargs.get('meta_data')

        for key, value in new_member.items():
            if key == 'cooperative' and value:
                new_member[key] = get_model_object(Cooperative, 'id', value)

        member_instance = Member(**new_member)

        with SaveContextManage(member_instance, model=Member) as member:
            if meta_data and len(meta_data) > 0:
                for data in meta_data:
                    meta_instance = MemberMeta.objects.filter(
                        member=member, key=data['key']).first()

                    if meta_instance:
                        meta_instance.value = data['value'] or \
                            meta_instance.value
                        meta_instance.save()
                    else:
                        for key, value in data.items():
                            if key == 'member':
                                member = get_model_object(
                                    Member, 'id', value)
                                data[key] = member
                        meta_instance = MemberMeta(**data)
                        meta_instance.member = member
                        meta_instance.save()

            cooperative = member.cooperative
            if member:
                member.send_verification_link_sms()
            kudibooks = cooperative.get_service("KUDIBOOKS")
            if kudibooks and kudibooks.is_enabled:
                KudiVendor(
                    company_id=cooperative.kudibooks_company_id,
                    name=member.first_name + ' ' + member.last_name,
                    tin="",
                    first_name=member.first_name,
                    last_name=member.last_name,
                    email="",
                    phone=member.mobile,
                ).create()

            return AddMember(success=success, member=member)


class UpdateMember(graphene.Mutation):
    """
    Update Member Mutation

    Args:
        id ([str]): [Member primary key]
        member_data ([obj]): [Member data object]

    Returns:
        [success]: [Success Message]
    """
    success = graphene.String()
    member = graphene.Field(MemberType)

    class Arguments:
        id = graphene.String(required=True)
        member_data = graphene.Argument(MemberInputType)
        meta_data = graphene.List(MemberMetaInputType)
        subscriptions = graphene.List(graphene.String)

    @login_required
    def mutate(self, info, **kwargs):
        success = SUCCESS_RESPONSES['updated'].format('Member')

        member_data = kwargs.get('member_data')
        meta_data = kwargs.get('meta_data')
        subscriptions = kwargs.get('subscriptions')

        member_instance = get_model_object(
            Member, 'id', kwargs.get('id'))

        for key, value in member_data.items():
            if key == 'cooperative' and value:
                coop = get_model_object(Cooperative, 'id', value)
                setattr(member_instance, key, coop)
            else:
                setattr(member_instance, key, value)

        with SaveContextManage(member_instance, model=Member) as member:
            if meta_data and len(meta_data) > 0:
                for meta in meta_data:
                    meta_instance = MemberMeta.objects.filter(
                        member=member, key=meta['key']).first()

                    if meta_instance:
                        meta_instance.value = meta['value'] or \
                            meta_instance.value
                        meta_instance.save()
                    else:
                        meta_instance = MemberMeta(**meta)
                        meta_instance.member = member
                        meta_instance.save()
            
            if subscriptions:
                for pricing_id in subscriptions:
                    pricing = Pricing.objects.filter(id=pricing_id).first()
                    if not member or not pricing:
                        continue
                        
                    Subscription.objects.create(
                        cooperative=member.cooperative,
                        pricing=pricing,
                        subscription_date=timezone.now(),
                        expiry_date=Subscription.get_expiry_date(pricing.period, timezone.now()),
                        member=member,
                    )
            

            return UpdateMember(success=success, member=member)


class DeleteMember(graphene.Mutation):
    """
    Delete Member

    Args:
        id (str): member id
    """
    success = graphene.String()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, **kwargs):
        check_member = get_model_object(
            Member, 'id', kwargs.get('id'))

        check_member.hard_delete()

        return DeleteMember(
            success=SUCCESS_RESPONSES['suspended'].format('Member'))


class AddMemberField(graphene.Mutation):
    """
    Add Member Field Mutation

    Args:
        new_field ([type]): [description]
    """
    success = graphene.String()
    member_field = graphene.Field(MemberFieldType)

    class Arguments:
        new_field = graphene.Argument(MemberFieldInputType)

    @login_required
    def mutate(self, info, **kwargs):

        success = SUCCESS_RESPONSES['created'].format('Member Field')

        field = kwargs.get('new_field')

        for key, value in field.items():
            if key == 'cooperative':
                field[key] = get_model_object(
                    Cooperative, 'id', value)

        field_instance = MemberField(**field)

        with SaveContextManage(field_instance, model=MemberField) as field:
            return AddMemberField(
                success=success, member_field=field)


class UpdateMemberField(graphene.Mutation):
    """
    Update Member Field Mutation

    Args:
        id ([str]): [primary key]
        field_data ([obj]): [object data]
    """
    success = graphene.String()
    member_field = graphene.Field(MemberFieldType)

    class Arguments:
        id = graphene.String(required=True)
        field_data = graphene.Argument(MemberFieldInputType)

    @login_required
    def mutate(self, info, **kwargs):
        success = SUCCESS_RESPONSES['updated'].format('Member Field')

        field_data = kwargs.get('field_data')

        field_instance = get_model_object(
            MemberField, 'id', kwargs.get('id'))

        for key, value in field_data.items():
            if key == 'cooperative':
                setattr(
                    field_instance, key,
                    get_model_object(Cooperative, 'id', value))
            else:
                setattr(field_instance, key, value)

        with SaveContextManage(field_instance, model=MemberField) as field:
            return UpdateMemberField(
                success=success, member_field=field)


class DeleteMemberField(graphene.Mutation):
    """
    Delete Member Field Mutation

    Args:
        id ([str]): [field primary key]
    """
    success = graphene.String()

    class Arguments:
        id = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        success = SUCCESS_RESPONSES['deleted'].format('Member Field')

        field = get_model_object(
            MemberField, 'id', kwargs.get('id'))

        field.hard_delete()

        return DeleteMemberField(success=success)

class VerifyMembership(graphene.Mutation):
    """
    Verify Membership

    Args:
        member_id (str): member id
        token (str): verification token
    """
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    member = graphene.Field(MemberType)

    class Arguments:
        member_id = graphene.String(required=True)
        token = graphene.String(required=True)

    def mutate(self, info, member_id=None, token=None):
        member = get_model_object(Member, 'id', member_id)

        try:
            member.verify_membership(token)
        except Exception as exception:
            return VerifyMembership(success=False, errors=[str(exception)], member=member)

        return VerifyMembership(
            success=SUCCESS_RESPONSES['verified'].format('Membership'), member=member)
