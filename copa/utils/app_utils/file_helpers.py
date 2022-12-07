from pyexcel_xlsx import get_data as xlsx_get_data
from pyexcel_ods3 import get_data as ods_get_data
from ...apps.cooperative.models import Member, \
    MemberMeta, Cooperative, MemberField
from ...apps.stock.models import Productivity, \
    ProductivityMeta, ProductivityField

from ...utils.app_utils.database import get_model_object


def get_data_as_array(file_obj):
    if file_obj.name.endswith('.xlsx'):
        for i in xlsx_get_data(file_obj, fill=True):
            if i:
                return xlsx_get_data(file_obj)[i]
            else:
                return None
    elif file_obj.name.endswith('.ods'):
        for i in ods_get_data(file_obj):
            if i:
                return ods_get_data(file_obj)[i]
            else:
                return None
    else:
        return None


def check_header(data, allowed_header):
    for header in data:
        if header in allowed_header:
            continue
        else:
            return None
    return data


def save_members(data, id=None):
    # loop through the data
    errors = []
    members = []
    duplicates = []
    cooperative = get_model_object(Cooperative, 'id', id)
    member_field_keys = MemberField.objects.values_list('key', flat=True)

    allowed_header = [
        'first_name',
        'last_name',
        'mobile',
        'identity_card',
        'gender'
    ]
    titleIndex = 0

    for row_id, row in enumerate(data):
        if row_id == 0:
            continue

        if row and row[0] != '' and row[0] in allowed_header:
            titleIndex = 1
            continue

        check_row = check_member_row(row)

        if check_row is None:
            continue

        member_exist = Member.objects.filter(
            cooperative=cooperative,
            identity_card=str(row[data[titleIndex].index('identity_card')]).split('.')[0]).first() # noqa

        if member_exist:
            duplicates.append(row)
            continue
        else:
            gender = str(row[data[titleIndex].index('gender')]).capitalize() if len(row) == len(data[titleIndex]) else None # noqa
            member_instance = Member.objects.create(
                first_name=row[data[titleIndex].index('first_name')] or None,
                last_name=row[data[titleIndex].index('last_name')] or None,
                mobile=str(row[data[titleIndex].index('mobile')]).split('.')[0] or None, # noqa
                identity_card=str(row[data[titleIndex].index('identity_card')]).split('.')[0] or None, # noqa
                gender=gender,
                cooperative=cooperative
            )

            if member_instance:
                for attribute in data[titleIndex]:
                    if attribute in member_field_keys:
                        meta_instance = MemberMeta.objects.filter(
                            member=member_instance, key=attribute).first()

                        if meta_instance:
                            meta_instance.value = row[data[titleIndex].index(
                                attribute)] or meta_instance.value
                            meta_instance.save()
                        else:
                            meta = {
                                'key': attribute,
                                'value': row[data[titleIndex].index(attribute)]
                            }
                            meta_instance = MemberMeta(**meta)
                            meta_instance.member = member_instance
                            meta_instance.save()
                members.append(row)

    return {'errors': errors,
            'members': members,
            'duplicates': duplicates}


def check_member_row(row):
    if len(row) == 0:
        return None
    return row


def save_productivity(data, id=None):
    # loop through the data
    errors = []
    productivity = []
    duplicates = []
    cooperative = get_model_object(Cooperative, 'id', id)
    productivity_field_keys = \
        ProductivityField.objects.values_list('key', flat=True)
    allowed_header = [
        'member_id',
        'names', 'mobile',
        'quantity', 'price_per_unity']
    titleIndex = 0

    for row_id, row in enumerate(data):
        if row_id == 0:
            continue

        if row and row[0] != '' and row[0] in allowed_header:
            titleIndex = 1
            continue

        member_instance = None

        if len(row) >= data[titleIndex].index('mobile'):
            member_instance = Member.objects.filter(
                mobile__contains=row[data[titleIndex].index('mobile')]).first() if row[data[titleIndex].index('mobile')] else None # noqa

        if member_instance is None:
            continue

        productivity_instance = Productivity.objects.create(
            member=member_instance,
            quantity=row[data[titleIndex].index('quantity')],
            price_per_unity=row[data[titleIndex].index('price_per_unity')],
            cooperative=cooperative
        )

        if productivity_instance:
            for attribute in data[titleIndex]:
                if attribute in productivity_field_keys:
                    meta_instance = ProductivityMeta.objects.filter(
                        productivity=productivity_instance,
                        key=attribute).first()

                    if meta_instance:
                        value = row[data[titleIndex].index(attribute)]
                        meta_instance.value = value \
                            or meta_instance.value
                        meta_instance.save()
                    else:
                        meta = {
                            'key': attribute,
                            'value': row[data[titleIndex].index(attribute)]
                        }
                        meta_instance = ProductivityMeta(**meta)
                        meta_instance.productivity = productivity_instance
                        meta_instance.save()
            productivity.append(row)

    return {'errors': errors,
            'productivity': productivity,
            'duplicates': duplicates}
