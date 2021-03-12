from django_filters import rest_framework as filters

from .models import Post


class DateRangeFilter(filters.FilterSet):

    datetime = filters.DateFromToRangeFilter(
            label='Date (Between)', help_text="set date yyyy/mm/dd/")

    class Meta:
        model = Post
        fields = ['datetime']
