from django.conf.urls import patterns, include, url
from django.contrib import admin

from anno.views import hello
from anno.views import current_datetime
from anno.views import train
from anno.views import search
from anno.views import validate
from anno.views import login
from anno.views import log
from anno.views import tasks
from anno.views import annolist
from anno.views import annotation
from anno.views import log_annotation
from anno.views import log_session_annotation
from anno.views import log_questionnaire
from anno.views import questionnaire
from anno.views import log_query_satisfaction
from anno.views import description
from anno.views import list_all_queries
from anno.views import show_page
from anno.views import debug_log
from anno.views import recordannolist
from anno.views import recordanno
from anno.views import log_record_annotation
from anno.views import init_query_list
from anno.views import rel_annotation
from anno.views import log_rel_annotation

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sessionanno.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    (r'^hello/$',hello),
    (r'^debugLogService/$', debug_log),
    (r'^time/',current_datetime),
    (r'^search/(\d{1,2})/(.*?)/(\d{1,2})/$',search),
    (r'^train/(\d{1,2})/$',train),
    (r'^validate/(\d{1,2})/$',validate),
    (r'^login/$',login),
    (r'^tasks/(\d{10})/$',tasks),
    (r'^annolist/(\d{1,2})/$',annolist),
    (r'^annotation/(\d{1,2})/(.*?)/$', annotation),
    (r'^questionnaire/(\d{1,2})/$', questionnaire),
    (r'^description/(\d{1,2})/(.*?)/$', description),
    (r'^LogService/$', log),
    (r'^AnnoService/$', log_annotation),
    (r'^SessionAnnoService/$', log_session_annotation),
    (r'^QuestionnaireService/$', log_questionnaire),
    (r'^QuerySatisfactionService/$', log_query_satisfaction),
    (r'^admin/allQueries/$', list_all_queries),
    (r'^SERP/(\d{1,2})/(.*?)/(\d{1,2})/$', show_page),
    (r'^recordannolist/(\d{10})/$', recordannolist),
    (r'^recordanno/(\d{1,2})/$', recordanno),
    (r'^RecordAnnoService/$', log_record_annotation),

    (r'^relevanceannolist/(\d{10})/$', init_query_list),
    (r'^relevanceanno/(\d{1,2})/(.*?)/$', rel_annotation),
    (r'^relAnnoService/$', log_rel_annotation),
)
