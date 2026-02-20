import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ColourmanBoard.settings")
django.setup()

from django.db.models import Count, Q

from colourman.models import Colourman


def find_colourmens_and_count_fails(name: str | None = None,
                                    clock_num: int | None = None):
    colourmens = (Colourman
                  .objects.all()
                  .order_by('clock_number')
                  .prefetch_related('unacceptable')
                  .annotate(fails=Count('unacceptable')))
    filters = Q()
    if name is not None:
        filters |= Q(name__icontains=name)
    if clock_num is not None:
        filters |= Q(clock_number__icontains=clock_num)
    if filters:
        colourmens = colourmens.filter(filters)

    return colourmens


employee = (find_colourmens_and_count_fails())
for e in employee:
    print(f"{e.name} ({e.clock_number}) -> fails: {e.fails}")
