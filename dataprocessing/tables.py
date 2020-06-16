from .models import channel
from table import Table
from table.columns import Column

class channelTable(Table):
    id = Column(field = 'Channel_id')
    name = Column(field='channel_name')

    class Meta:
        model = channel