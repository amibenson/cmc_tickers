from django.db import models

from django.db.models.signals import post_save

import django.utils.timezone

from tickers.signals import UpdateCustomManager, post_update


class Ticker(models.Model):
    objects = UpdateCustomManager()

    tickerId = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    rank = models.IntegerField()
    priceUsd = models.FloatField(null=True, blank=True)
    priceBtc = models.FloatField(null=True, blank=True)
    dayVolumeUsd = models.FloatField(null=True, blank=True)
    markedCapUsd = models.FloatField(null=True, blank=True)
    availableSupply = models.FloatField(null=True, blank=True)
    totalSupply = models.FloatField(null=True, blank=True)
    maxSupply = models.FloatField(null=True, blank=True)
    percentChange1h = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)
    percentChange24h = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)
    percentChange7d = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)
    lastUpdated = models.DateTimeField()

    dateAdded = models.DateTimeField(default=django.utils.timezone.now)
    lastAnalyzed = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return "%s - %s" % (self.symbol, self.name)


class TickerHistory(models.Model):
    tickerId = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    rank = models.IntegerField()
    priceUsd = models.FloatField(null=True, blank=True)
    priceBtc = models.FloatField(null=True, blank=True)
    dayVolumeUsd = models.FloatField(null=True, blank=True)
    markedCapUsd = models.FloatField(null=True, blank=True)
    availableSupply = models.FloatField(null=True, blank=True)
    totalSupply = models.FloatField(null=True, blank=True)
    maxSupply = models.FloatField(null=True, blank=True)
    percentChange1h = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)
    percentChange24h = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)
    percentChange7d = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)
    lastUpdated = models.DateTimeField()

    dateAdded = models.DateTimeField() # when was it first added to our DB
    lastAnalyzed = models.DateTimeField()

    def __str__(self):
        return self.name + " [" + str(self.lastAnalyzed) + "]"

    class Meta:
        verbose_name_plural = 'ticker histories'


def save_ticker_history(sender, instance, created, **kwargs):
    TickerHistory.objects.create(tickerId=instance.tickerId,
                                 name=instance.name,
                                 symbol=instance.symbol,
                                 rank=instance.rank,
                                 priceUsd=instance.priceUsd,
                                 priceBtc=instance.priceBtc,
                                 dayVolumeUsd=instance.dayVolumeUsd,
                                 markedCapUsd=instance.markedCapUsd,
                                 availableSupply=instance.availableSupply,
                                 totalSupply=instance.totalSupply,
                                 maxSupply=instance.maxSupply,
                                 percentChange1h=instance.percentChange1h,
                                 percentChange24h=instance.percentChange24h,
                                 percentChange7d=instance.percentChange7d,
                                 lastUpdated=instance.lastUpdated,
                                 dateAdded=instance.dateAdded,
                                 lastAnalyzed=instance.lastAnalyzed)

post_save.connect(save_ticker_history, sender=Ticker)
post_update.connect(save_ticker_history, sender=Ticker)
