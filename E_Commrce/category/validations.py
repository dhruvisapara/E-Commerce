from rest_framework import serializers
from pdb import set_trace as pdb


def validate_user(value):

    if value != 1:
        raise serializers.ValidationError("Only super admin can add category.")
