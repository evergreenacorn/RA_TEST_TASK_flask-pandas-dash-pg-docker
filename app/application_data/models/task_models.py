from .base_models import *


class Event(StandartModelMixin, db.Model):
    appsflyer_id = Column(String, nullable=False)  # , unique=True
    revenue = Column(Float)
    revenue_usd = Column(Float)
    install_time = Column(DateTime, default=func.current_timestamp())
    event_time = Column(DateTime, default=func.current_timestamp())
    
    type_id = Column(
        Integer,
        ForeignKey("eventtype.id", ondelete='cascade'),
        nullable=True
    )
    company_id = Column(
        Integer,
        ForeignKey("company.id", ondelete='cascade'),
        nullable=True
    )
    mediasource_id = Column(
        Integer,
        ForeignKey("mediasource.id", ondelete='cascade'),
        nullable=True
    )
    platform_id = Column(
        Integer,
        ForeignKey("platform.id", ondelete='cascade'),
        nullable=True
    )
    

    def __init__(
        self,
        appsflyer_id,
        revenue,
        revenue_usd,
        install_time,
        event_time
    ):
        self.appsflyer_id = appsflyer_id
        self.revenue = revenue
        self.revenue_usd = revenue_usd
        self.install_time = install_time
        self.event_time = event_time


class EventType(StandartModelMixin, db.Model):
    name = Column(String, nullable=False, unique=True)
    events = relationship("Event", backref="event_types")
    
    def __init__(self, name):
        self.name = name
    
    
class Company(StandartModelMixin, db.Model):
    name = Column(String, nullable=False, unique=True)
    events = relationship("Event", backref="company_events")
    
    def __init__(self, name):
        self.name = name


class MediaSource(StandartModelMixin, db.Model):
    name = Column(String, nullable=False, unique=True)
    events = relationship("Event", backref="mediasource_events")
    
    def __init__(self, name):
        self.name = name


class Platform(StandartModelMixin, db.Model):
    name = Column(String, nullable=False, unique=True)
    events = relationship("Event", backref="platform_events")
    
    def __init__(self, name):
        self.name = name
