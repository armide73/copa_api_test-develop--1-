from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from ...utils.app_utils.file_helpers import get_data_as_array, \
    check_header, save_productivity
from django.utils.translation import gettext as _
from rest_framework import status
from ...apps.stock.models import ProductivityField


class UploadProductivity(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated, )
    """
    Upload Productivity data

    Args:
        APIView ([obj]): [Object]
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
            message = {
                "error": _(error)}
            return Response(message, status.HTTP_400_BAD_REQUEST)

        # check productivity file header
        allowed_header = [
            'member_id',
            'names',
            'mobile',
            'quantity',
            'price_per_unity'
        ]

        meta_header = ProductivityField.objects.filter(
            cooperative=id).values_list('key', flat=True)

        for attribute in meta_header:
            allowed_header.append(attribute)

        # check the header of the data received
        header = check_header(data[0], allowed_header)

        if header is None:
            if data[1][0] not in allowed_header:
                message = {"error": _(
                        'Please check productivity example file')}
                return Response(message, status.HTTP_400_BAD_REQUEST)
        # save all productivity data
        data_response = save_productivity(data, id=id)

        return Response({'success': 'Uploaded productivity successfully',
                         'data': {
                             'errors': data_response['errors'],
                             'productivity': data_response['productivity'],
                             'duplicates': data_response['duplicates']
                         }})
