from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings

from users import views as user_views





urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('owner_register/', user_views.owner_register, name='owner_register'),
    path('searcher_main/', user_views.searcher_main, name='searcher_main'),
    path('owner_main/', user_views.owner_main, name='owner_main'),
    path('technician_main/', user_views.technician_main, name='technician_main'),
    path('tenant_main/', user_views.tenant_main, name='tenant_main'),
    path('contract/', user_views.house_unit_list, name='contract'),
    path('house_units/<int:house_unit_id>/', user_views.house_unit_detail, name='house_unit_detail'),
    path('reports/submit/', user_views.submit_report, name='submit_report' ),
    path('users/', user_views.users_list, name='users_list' ),
    path('notifications/', user_views.notifications, name='notifications'),
    path('profile/', user_views.view_user_profile, name='view_profile'),
    path('edit-profile/', user_views.edit_profile, name='edit_profile'),
    path('post_unit/', user_views.post_unit, name='post_unit'),
    path('make_payment/<int:house_unit_id>/', user_views.make_payment, name='make_payment'),
    path('login/', user_views.login, name='login'),
    path('make-payment/<int:house_unit_id>/', user_views.make_payment, name='make_payment'),
    path('search/contracts/', user_views.search_with_contracts, name='search_with_contracts'),
    path('add_to_favorites/<int:house_unit_id>/', user_views.add_to_favorites, name='add_to_favorites'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('transactions/manage/', user_views.manage_transactions, name='manage_transactions'),
    path('transactions/verify/<int:transaction_id>/', user_views.verify_transaction, name='verify_transaction'),
    path('transactions/not-verify/<int:transaction_id>/', user_views.not_verify_transaction, name='not_verify_transaction'),
    path('owner/transactions/', user_views.view_transactions_for_owner, name='view_transactions_for_owner'),
    path('tenant/transactions/', user_views.tenant_transactions, name='tenant_transactions'),
    path('tenant/rented-houses/', user_views.tenant_rented_houses, name='tenant_rented_houses'),
    path('tenant/make_payment/<int:house_unit_id>/', user_views.make_payment_for_tenant, name='tenant_make_payment'),
    path('favorites/', user_views.favorites_view, name='favorites'),
    path('', include('Cohome.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



