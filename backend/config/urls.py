from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.companies.views import CompanyViewSet
from apps.einvoicing.views import InvoiceSubmissionViewSet, MockGovernmentAPIView
from apps.invoicing.views import InvoiceViewSet

router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"invoices", InvoiceViewSet, basename="invoice")
router.register(r"submissions", InvoiceSubmissionViewSet, basename="submission")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/mock-government/receive/", MockGovernmentAPIView.as_view(), name="mock-government"),
    path("api/", include(router.urls)),
]
