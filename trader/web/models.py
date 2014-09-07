from django.db import models
from django.core.urlresolvers import reverse

TRADEORDER_QUALITY_CHOICES = (
    ('normal', 'Normal quality goods'),
    ('premium', 'Premium quality goods'),
    ('experimental', 'Experimantal quality goods'),
)

class TradeOrder(models.Model):
    email = models.EmailField(max_length=255)
    amount = models.IntegerField()
    quality = models.CharField(max_length=20, choices=TRADEORDER_QUALITY_CHOICES, default='normal')
    expired = models.BooleanField(default=False)

    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0} ordered {1} of {2}".format(self.email, self.amount, self.get_quality_display())

    def get_absolute_url(self):
        return reverse('order_view', args=[self.id])