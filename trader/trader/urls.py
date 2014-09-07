from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Main application views
    url(r'^$', 'web.views.index', name='index'),
    url(r'^add/$', 'web.views.order_add', name='order_add'),
    url(r'^order/(?P<order_id>\d+)/$', 'web.views.order_view', name='order_view'),

    # So we can simulate external API
    url(r'^price_api/$', 'web.views.api_price', name='api_price'),

    url(r'^admin/', include(admin.site.urls)),
)
