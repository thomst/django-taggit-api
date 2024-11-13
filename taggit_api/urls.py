
from django.urls import path
from .views import RemoveTagApi
from .views import AddTagApi


urlpatterns = [
    path('remove-tag/<int:tag_id>/from/<slug:app_label>/<slug:model_name>/', RemoveTagApi.as_view(), name='remove-tag-from-all-by-id'),
    path('remove-tag/<slug:tag_slug>/from/<slug:app_label>/<slug:model_name>/', RemoveTagApi.as_view(), name='remove-tag-from-all'),
    path('remove-tag/<int:tag_id>/from/<slug:app_label>/<slug:model_name>/<int:obj_id>/', RemoveTagApi.as_view(), name='remove-tag-by-id'),
    path('remove-tag/<slug:tag_slug>/from/<slug:app_label>/<slug:model_name>/<int:obj_id>/', RemoveTagApi.as_view(), name='remove-tag'),
    path('add-tag/<int:tag_id>/to/<slug:app_label>/<slug:model_name>/<int:obj_id>/', AddTagApi.as_view(), name='add-tag-by-id'),
    path('add-tag/<slug:tag_slug>/to/<slug:app_label>/<slug:model_name>/<int:obj_id>/', AddTagApi.as_view(), name='add-tag'),
]
