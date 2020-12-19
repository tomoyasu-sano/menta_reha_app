import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from .forms import InquiryForm, MentaCreateForm
from .models import Menta

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('menta:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

# LoginRequiredMixin → generic.ListViewの順番でないとerror
class MentaListView(LoginRequiredMixin, generic.ListView):
    model = Menta
    template_name = 'menta_list.html'
    paginate_by = 2
    #context_object_name = "menta_lists"  # 左記を指定するとobjectが入る。指定しない場合、menta_listにobjectが入る

    # 全データを表示するだけなら、get_querysetメソッドをオーバーライドする必要はない
    def get_queryset(self):
        mentas = Menta.objects.filter(user=self.request.user).order_by('-created_at')
        return mentas

## モデルの主キー(pk)以外のフィールドを使用したい場合(記事のタイトルなど)、Viewに「slug_field」と「slug_url_kwarg」を指定して、urls.pyを修正すれば実現できる
"""
class DetailView(generic.DetailView):
    model = Post
    slug_field = "title"  # モデルのフィールドの名前
    slug_url_kwarg = "title"  # urls.pyでのキーワードの名前
"""

class MentaDetailView(LoginRequiredMixin, generic.DetailView):
    model = Menta
    template_name = 'menta_detail.html'


class MentaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Menta
    template_name = "menta_create.html"
    # From クラスを継承したMentaCreateForm
    form_class = MentaCreateForm
    success_url = reverse_lazy('menta:menta_list')

    def form_valid(self, form):
        menta = form.save(commit=False)
        # userは必須。form側では持たせない場合、サーバー側にセットする必要がある
        # form_valid メソッドで、request.userを呼び出すことで、ログインしているユーザーのモデルオブジェクトをセット
        menta.user = self.request.user
        menta.save()
        messages.success(self.request, '日記を作成しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '日記の作成に失敗しました。')
        return super().form_invalid(form)

class MentaUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Menta
    template_name = "menta_update.html"
    form_class = MentaCreateForm

    def get_success_url(self):
        return reverse_lazy('menta:menta_detail', kwargs={'pk': self.kwargs['pk']})
        
    def form_valid(self, form):
        messages.success(self.request, "更新しました。")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "更新に失敗しました。" )
        return super().form_invalid(form)

class MentaDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Menta
    template_name = "menta_delete.html"
    success_url = reverse_lazy('menta:menta_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '日記を削除しました')
        return super().delete(request, *args, *kwargs)