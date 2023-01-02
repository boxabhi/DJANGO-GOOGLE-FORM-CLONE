from rest_framework import permissions
from .models import Form


class IsFormOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        
        # main_url = (request.build_absolute_uri())
        # form_code = main_url.split('/')
        # form_obj = Form.objects.filter(code = form_code[5] )

        # if form_obj.exists():
        #     return form_obj[0].creator == request.user

        return True

    
    def has_object_permission(self, request, view, obj):

        return obj.creator == request.user


        #return super().has_object_permission(request, view, obj)