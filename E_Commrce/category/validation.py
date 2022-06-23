from rest_framework import serializers


def validate_user(value):
    import pdb;pdb.set_trace()
    if value != 1:
        raise serializers.ValidationError("Only super admin can add category.")
