from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from ...utils.app_utils.file_helpers import get_data_as_array, \
    check_header, save_members
from django.utils.translation import gettext as _
from rest_framework import status
# from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
# from copa.utils.app_utils.database import get_model_object
from copa.apps.cooperative.models import Member, MemberField


DEFAULT_TAG = "copa-profiles"


class UploadMembers(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated, )
    """
    Upload cooperative members

    Args:
        APIView (obj): include header requests
    """
    def post(self, request, id=None, data=None, data_type=None, format=None):
        file_obj = None
        try:
            file_obj = request.data['file']
        except Exception:
            file_obj = request.data['filepond']

        data = get_data_as_array(file_obj)

        if data is None:
            error = 'Uploaded file is not valid, please use one (.xlsx)'
            message = {"error": _(error)}
            return Response(message, status.HTTP_400_BAD_REQUEST)

        allowed_header = [
            'first_name',
            'last_name',
            'mobile',
            'identity_card',
            'gender'
        ]

        meta_header = MemberField.objects.filter(
            cooperative=id).values_list('key', flat=True)

        for attribute in meta_header:
            allowed_header.append(attribute)

        # check the header of the data received
        header = check_header(data[0], allowed_header)

        if header is None:
            if data[1][0] not in allowed_header:
                message = {"error": _(
                        'Please check member example file')}
                return Response(message, status.HTTP_400_BAD_REQUEST)

        # save into the database all members
        data_response = save_members(data, id=id)
        return Response({'success': 'Uploaded members successfully',
                         'data': {
                             'errors': data_response['errors'],
                             'members': data_response['members'],
                             'duplicates': data_response['duplicates']
                         }})


def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))


class UploadMemberImage(APIView):
    """
    Upoad member image

    Args:
        APIView (obj): include header requests
    """
    def post(self, request, id=None):
        image = request.data['file']

        # validate image

        # check member id
        member_instance = Member.objects.filter(id=id).first()

        if not member_instance:
            return Response({'error': 'Umunyamuryango ntabwo yabonetse'})

        response = upload(
            image,
            tags=DEFAULT_TAG,
            public_id=id,
            eager=dict(
                width=250,
                height=250,
                crop="scale"
            ))

        dump_response(response)

        url, options = cloudinary_url(
            response['public_id'],
            format=response['format'],
            width=250,
            height=250,
            crop="scale",
        )

        if url:
            member_instance.image = url

        member_instance.save()

        return Response({
            'success': 'Ifoto yabitswe neza',
            'data': response,
            'options': options})
