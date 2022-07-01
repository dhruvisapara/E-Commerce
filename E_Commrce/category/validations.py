from rest_framework import serializers
from pdb import set_trace as pdb


def validate_user(value):
    print(value)
    import pdb;
    pdb.set_trace()
    # if value != 1:

        # raise serializers.ValidationError("Only super admin can add category.")
