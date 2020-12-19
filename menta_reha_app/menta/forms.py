from django import forms
from django.core.mail import EmailMessage
from .models import Menta


# forms.Formクラスを継承したInquiryFormを作成する
class InquiryForm(forms.Form):
    # formsにあるメソッドを使用し、クラス変数を作る
    name = forms.CharField(label="お名前", max_length=45)
    email = forms.EmailField(label="メールアドレス")
    url = forms.URLField(label="あなたのWebサイト", required=False)
    title = forms.CharField(label="タイトル", max_length=45)
    message = forms.CharField(label="メッセージ", widget=forms.Textarea)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.fields["name"].widget.attrs["class"] = "form-control col-12"
        self.fields["name"].widget.attrs["placeholder"] = "お名前をここに入力してください。"

        self.fields["email"].widget.attrs["class"] = "form-control col-12"
        self.fields["email"].widget.attrs["placeholder"] = "メールアドレスをここに入力してください。"

        self.fields["url"].widget.attrs["class"] = "form-control col-12"
        self.fields["url"].widget.attrs["placeholder"] = "あなたのWebサイトのURLをここに入力してください。"

        self.fields["title"].widget.attrs["class"] = "form-control col-12"
        self.fields["title"].widget.attrs["placeholder"] = "タイトルをここに入力してください。"

        self.fields["message"].widget.attrs["class"] = "form-control col-12"
        self.fields["message"].widget.attrs["placeholder"] = "メッセージをここに入力してください。"

    # フォームバリデーションを通ったユーザー入力値をclean_dataで値を取得できる（辞書型で格納されている）
    def send_email(self):
        name = self.cleaned_data["name"]
        email = self.cleaned_data["email"]
        url = self.cleaned_data["url"]
        title = self.cleaned_data["title"]
        message = self.cleaned_data["message"]

        subject = f"お問い合わせ {title}"
        message = f"送信者：{name}, メールアドレス:{email}, メッセージ：{message}、webサイト：{url}"
        from_email = "admin@example.com"
        to_list = ["test@example.com"]
        cc_list = [email]

        email_message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        email_message.send()
        

# モデルフォームクラスを使用(model.pyのMentaと、新規作成のformが類似しているため、MentaModelを活用してformを作る方が効率的)
class MentaCreateForm(forms.ModelForm):
    class Meta:
        model = Menta
        fields = ('title', 'content', 'photo1','photo2', 'photo3',)
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'