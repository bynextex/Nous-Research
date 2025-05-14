import streamlit as st
import requests
import json
import datetime
import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tempfile
import os
import base64
import time

# Temayı kontrol et
if "theme" not in st.session_state:
    st.session_state.theme = "light"  # Varsayılan tema: light

# Tema ayarını yap ve sayfayı yapılandır
theme = st.session_state.theme
st.set_page_config(page_title="Nous Chat", layout="wide", initial_sidebar_state="expanded", page_icon="🧠")

# Input key için benzersiz değer oluştur
if "input_key" not in st.session_state:
    st.session_state.input_key = "initial_input"

# Roboto-Regular ve Roboto-Bold fontlarını roboto_fonts.py dosyasından base64 olarak alacağız.
from roboto_fonts import roboto_regular_b64, roboto_bold_b64

# Fontları base64'ten kaydetme fonksiyonu
def save_font_from_base64(base64_string, filename):
    path = os.path.join(tempfile.gettempdir(), filename)
    with open(path, "wb") as f:
        f.write(base64.b64decode(base64_string))
    return path

# Fontları kaydet ve kontrol et
roboto_regular_path = save_font_from_base64(roboto_regular_b64, "Roboto-Regular.ttf")
roboto_bold_path = save_font_from_base64(roboto_bold_b64, "Roboto-Bold.ttf")

has_unicode_font = True  # Unicode fontları kullandığımıza göre bu değeri True yapıyoruz

# PDF oluşturma fonksiyonu
def create_pdf(chat_history, conversation_name, language):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    if has_unicode_font:
        for style_name in styles.byName:
            styles[style_name].fontName = 'Roboto'  # Font ismi 'Roboto' olarak ayarlandı.

    styles.add(ParagraphStyle(name='Message', fontName='Roboto', fontSize=10, spaceAfter=6))
    styles.add(ParagraphStyle(name='Sender', fontName='Roboto-Bold', fontSize=12, spaceAfter=3))

    flowables = []

    title_text = "Nous API Chat: " if language == "English" else "Nous API Sohbet: "
    title = Paragraph(f"{title_text}{safe_text(conversation_name)}", styles['Title'])
    flowables.append(title)
    flowables.append(Spacer(1, 12))

    for sender, message in chat_history:
        sender_text = Paragraph(f"<b>{safe_text(sender)}:</b>", styles['Sender'])
        flowables.append(sender_text)
        message = message.replace('\n', '<br/>')
        message_text = Paragraph(safe_text(message), styles['Message'])
        flowables.append(message_text)
        flowables.append(Spacer(1, 6))

    doc.build(flowables)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


# Veri saklama için session state başlatma
if 'first_time' not in st.session_state:
    st.session_state.first_time = True

# İlk kez çalıştığında varsayılan değerleri ayarla
if st.session_state.first_time:
    # Oturum durumu kontrolleri
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "conversations" not in st.session_state:
        st.session_state.conversations = {"Main Chat": []}
        st.session_state.current_conversation = "Main Chat"

    if "token_usage" not in st.session_state:
        st.session_state.token_usage = {"total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0}

    if "total_cost" not in st.session_state:
        st.session_state.total_cost = 0.0

    if "language" not in st.session_state:
        st.session_state.language = "English"  # Varsayılan dil İngilizce
        
    # Bu değişkeni oluşturduk, tekrar çalıştırmamak için
    st.session_state.first_time = False

# Sohbet düzenleme modu için state
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = None
    st.session_state.rename_input = ""

# CSS Stiller - sadece sağ taraf sohbet paneli için koyu/açık tema
def local_css():
    if theme == "dark":
        main_bg = "#282c34"
        text_color = "#E0E0E0"
        chat_bg_user = "#36404a"
        chat_bg_ai = "#2d3748"
    else:  # light tema
        main_bg = "#FFFFFF"
        text_color = "#333333"
        chat_bg_user = "#E6F7FF"
        chat_bg_ai = "#F0F0F0"
    
    # Genel CSS
    st.markdown(f"""
    <style>
        /* Sadece ana içerik alanı - sohbet paneli */
        .main .block-container {{
            background-color: {main_bg};
            color: {text_color};
            padding: 2rem;
        }}
        
        /* Mesaj baloncukları */
        .user-message {{
            background-color: {chat_bg_user}; 
            padding: 10px; 
            border-radius: 5px; 
            margin-bottom: 10px;
            color: {text_color};
        }}
        
        .ai-message {{
            background-color: {chat_bg_ai}; 
            padding: 10px; 
            border-radius: 5px; 
            margin-bottom: 10px;
            color: {text_color};
        }}
        
        /* Tema butonları için stiller */
        .theme-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 8px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            width: 40px;
            height: 40px;
            margin: 0 10px;
            font-size: 20px;
        }}
        
        /* Light tema butonu */
        .light-theme-btn {{
            background-color: #FFFFFF;
            color: #FFB612;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        /* Dark tema butonu */
        .dark-theme-btn {{
            background-color: #1E293B;
            color: #C0C0FF;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }}
        
        /* Ana içerik alanındaki bağlantılar */
        .main .block-container a {{
            color: {"#4da1ff" if text_color == "#E0E0E0" else "#0366d6"} !important;
        }}
        
        /* Ana içerik alanındaki başlıklar */
        .main .block-container h1, 
        .main .block-container h2, 
        .main .block-container h3 {{
            color: {text_color};
        }}
        
        /* Bildirim sesi için gizli audio elementi */
        .audio-element {{
            display: none;
        }}
        
        /* Mesaj kutusunu aşağıda sabitleme */
        .chat-input-area {{
            position: sticky;
            bottom: 0;
            background-color: {main_bg};
            padding: 1rem 0;
            margin-top: 1rem;
            border-top: 1px solid {"#3e4451" if theme == "dark" else "#e1e4e8"};
        }}
    </style>
    """, unsafe_allow_html=True)
    
# CSS ekle
local_css()

# Sesli bildirim için audio bileşeni
def get_audio_html():
    return """
    <audio id="notification-sound" class="audio-element">
        <source src="data:audio/mpeg;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjM1LjEwNAAAAAAAAAAAAAAA//tQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAAAgAAAWAAIDBAUGBwgJCgsMDQ4PEBESExQVFhcYGRobHBwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/wAAAA5MYXZmNTguMzUuMTAwAAAAAAAAAAAAAAD/80DEAAAAA0gAAAAATEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQsRbAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQsS3AAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQsT/AK8UgBmMYAQ0wAAjjQAAAVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVX/80LERAEO1AApmGAGeAAGNAAAARVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVU=" type="audio/mpeg">
    </audio>
    
    <script>
        function playNotificationSound() {
            document.getElementById('notification-sound').play();
        }
    </script>
    """

# Bildirim sesi çalma fonksiyonu
def play_notification_sound():
    js_code = "playNotificationSound()"
    html = f"""
        <script>
            {js_code}
        </script>
    """
    st.components.v1.html(html, height=0)

# Dil verilerini içeren sözlük
ui_text = {
    "Türkçe": {
        "title": "🧠 Nous API ile Sohbet",
        "subtitle": "Nous modellerini test etmek için basit ve güçlü bir arayüz.",
        "active_chat": "Aktif Sohbet",
        "settings": "Ayarlar",
        "appearance": "Görünüm",
        "light_mode": "Açık Mod",
        "dark_mode": "Koyu Mod",
        "api_key": "Nous API Anahtarınız",
        "model_selection": "Model Seçimi",
        "model_settings": "Model Ayarları",
        "temperature": "Sıcaklık (Temperature)",
        "max_tokens": "Maksimum Token",
        "system_msg": "Sistem Mesajı",
        "template": "Şablon",
        "use_custom": "Özel Sistem Mesajı Kullan",
        "custom_msg": "Özel Sistem Mesajı",
        "write_msg": "Mesajınızı yazın:",
        "send": "Gönder",
        "warning_api": "API anahtarınızı girin.",
        "warning_prompt": "Lütfen bir mesaj yazın.",
        "waiting": "Yanıt bekleniyor...",
        "api_error": "API Hatası",
        "chat": "Sohbet",
        "you": "Siz",
        "footer": "Geliştiren: [Bynextex](https://x.com/muma_gaga) - Bu arayüz tamamen kişisel test amaçlıdır.",
        "conversations": "Sohbetler",
        "new_chat": "🆕 Yeni Sohbet",
        "previous": "Önceki Sohbetler",
        "stats": "Kullanım İstatistikleri",
        "total_token": "Toplam Token",
        "prompt_token": "Prompt Token",
        "response_token": "Yanıt Token",
        "cost": "Tahmini Maliyet",
        "export": "Dışa Aktar",
        "format": "Format",
        "export_btn": "Dışa Aktar",
        "no_chat": "Dışa aktarılacak sohbet bulunamadı!",
        "pdf_error": "PDF oluşturma hatası",
        "pdf_error_detail": "Hata ayrıntıları: Sohbetinizde PDF formatıyla uyumsuz karakterler olabilir.",
        "clear": "🗑️ Sohbeti Temizle",
        "delete": "Sil",
        "rename": "Yeniden Adlandır",
        "cancel": "İptal",
        "save": "Kaydet",
        "new_name": "Yeni isim",
        "delete_confirm": "Bu sohbeti silmek istediğinizden emin misiniz?",
        "more_options": "Daha fazla"
    },
    "English": {
        "title": "🧠 Chat with Nous API",
        "subtitle": "A simple and powerful interface for testing Nous models.",
        "active_chat": "Active Chat",
        "settings": "Settings",
        "appearance": "Appearance",
        "light_mode": "Light Mode",
        "dark_mode": "Dark Mode",
        "api_key": "Your Nous API Key",
        "model_selection": "Model Selection",
        "model_settings": "Model Settings",
        "temperature": "Temperature",
        "max_tokens": "Maximum Tokens",
        "system_msg": "System Message",
        "template": "Template",
        "use_custom": "Use Custom System Message",
        "custom_msg": "Custom System Message",
        "write_msg": "Write your message:",
        "send": "Send",
        "warning_api": "Please enter your API key.",
        "warning_prompt": "Please write a message.",
        "waiting": "Waiting for response...",
        "api_error": "API Error",
        "chat": "Chat",
        "you": "You",
        "footer": "Developed by: [Bynextex](https://x.com/muma_gaga) - This interface is for personal testing purposes only.",
        "conversations": "Conversations",
        "new_chat": "🆕 New Chat",
        "previous": "Previous Chats",
        "stats": "Usage Statistics",
        "total_token": "Total Tokens",
        "prompt_token": "Prompt Tokens",
        "response_token": "Response Tokens",
        "cost": "Estimated Cost",
        "export": "Export",
        "format": "Format",
        "export_btn": "Export",
        "no_chat": "No chat to export!",
        "pdf_error": "PDF creation error",
        "pdf_error_detail": "Error details: Your chat may contain characters incompatible with PDF format.",
        "clear": "🗑️ Clear Chat",
        "delete": "Delete",
        "rename": "Rename",
        "cancel": "Cancel",
        "save": "Save",
        "new_name": "New name",
        "delete_confirm": "Are you sure you want to delete this chat?",
        "more_options": "More options"
    }
}


# Sistem mesajı şablonları (dil bazlı)
system_messages = {
    "Türkçe": {
        "Düşünce Zincirleri": "You are a deep thinking AI, you may use extremely long chains of thought to deeply consider the problem and deliberate with yourself via systematic reasoning processes to help come to a correct solution prior to answering. You should enclose your thoughts and internal monologue inside <deepthought> tags, and then provide your solution or response to the problem. Always respond in Turkish.",
        "Uzman Danışman": "You are an expert advisor, knowledgeable in a wide range of fields. Provide direct, comprehensive answers with professional insight and up-to-date information. Always respond in Turkish.",
        "Basit Yardımcı": "You are a helpful, concise assistant. Provide simple, direct answers. Always respond in Turkish.",
        "Türkçe Yardımcı": "Sen yardımcı bir Türkçe asistansın. Sorulara açık, anlaşılır ve doğru yanıtlar ver. Türkçe dilbilgisi ve yazım kurallarına dikkat et.",
        "SEO Uzmanı": "Sen SEO konusunda uzmanlaşmış bir danışmansın. Yanıtlarını daima güncel SEO pratiklerine uygun şekilde ver ve önerilerini maddeler halinde, uygulanabilir şekilde sırala. Her zaman Türkçe yanıt ver."
    },
    "English": {
        "Chains of Thought": "You are a deep thinking AI, you may use extremely long chains of thought to deeply consider the problem and deliberate with yourself via systematic reasoning processes to help come to a correct solution prior to answering. You should enclose your thoughts and internal monologue inside <deepthought> tags, and then provide your solution or response to the problem.",
        "Expert Advisor": "You are an expert advisor, knowledgeable in a wide range of fields. Provide direct, comprehensive answers with professional insight and up-to-date information.",
        "Simple Helper": "You are a helpful, concise assistant. Provide simple, direct answers.",
        "Turkish Assistant": "You are a helpful Turkish assistant. Provide clear, understandable, and accurate answers to questions. Pay attention to Turkish grammar and spelling rules. Always respond in Turkish.",
        "SEO Expert": "You are an SEO consultant specialized in search engine optimization. Always provide your answers according to current SEO practices and list your suggestions in bullet points in an applicable way."
    }
}

# Yardım metinleri
SYSTEM_MESSAGE_HELP = {
    "Türkçe": """
### Sistem Mesajı Nedir?

Sistem mesajı, AI modelinin nasıl davranacağını ve yanıt vereceğini belirleyen talimatları içerir.

#### Faydaları:

1. **Modelin Kişiliğini Ayarlama**: 
   - Farklı sistem mesajları, modelin farklı şekillerde davranmasını sağlar.
   - "Türkçe Yardımcı" seçtiğinizde, model otomatik olarak Türkçe yanıt verir.

2. **Düşünce Derinliğini Kontrol Etme**:
   - "Düşünce Zincirleri" seçeneği, modelin düşünce sürecini adım adım gösterir.
   - "Basit Yardımcı" ise kısa ve özlü yanıtlar verir.

3. **Uzmanlık Seviyesini Ayarlama**:
   - "Uzman Danışman" seçildiğinde, model daha kapsamlı ve profesyonel yanıtlar verir.

#### Kullanım Örnekleri:

- Programlama yardımı için "Uzman Danışman"
- Basit sorular için "Basit Yardımcı"
- Karmaşık problemler için "Düşünce Zincirleri"
- Türkçe içerik için "Türkçe Yardımcı"

#### Özel Sistem Mesajı Örneği:
Sen SEO konusunda uzmanlaşmış bir danışmansın. Yanıtlarını daima
güncel SEO pratiklerine uygun şekilde ver ve önerilerini maddeler
halinde, uygulanabilir şekilde sırala.


Bu şekilde modele özel talimatlar verebilir, belirli bir konuda uzmanlaşmış yanıtlar alabilirsiniz.
""",
    "English": """
### What is a System Message?

A system message contains instructions that determine how the AI model will behave and respond.

#### Benefits:

1. **Adjusting the Model's Personality**: 
   - Different system messages cause the model to behave in different ways.
   - When you select "Turkish Assistant," the model automatically responds in Turkish.

2. **Controlling Depth of Thought**:
   - The "Chains of Thought" option shows the model's thought process step by step.
   - "Simple Helper" provides short and concise answers.

3. **Setting Expertise Level**:
   - When "Expert Advisor" is selected, the model provides more comprehensive and professional answers.

#### Usage Examples:

- "Expert Advisor" for programming help
- "Simple Helper" for basic questions
- "Chains of Thought" for complex problems
- "Turkish Assistant" for Turkish content

#### Custom System Message Example:
You are an SEO consultant specialized in search engine optimization.
Always provide your answers according to current SEO practices and
list your suggestions in bullet points in an applicable way.



This way you can give special instructions to the model and get specialized answers on a specific topic.
"""
}

TEMPERATURE_HELP = {
    "Türkçe": """
### Sıcaklık (Temperature) Nedir?

Sıcaklık, AI'nın yanıtlarındaki yaratıcılık ve rastgelelik seviyesini kontrol eder.

- **0.0 - 0.3**: Daha tutarlı, belirleyici ve odaklanmış yanıtlar
- **0.4 - 0.7**: Dengeli yaratıcılık ve tutarlılık
- **0.8 - 1.0**: Daha yaratıcı, çeşitli ve sürpriz yanıtlar
- **1.0+**: Yüksek yaratıcılık ve bazen beklenmedik çıktılar

#### Ne Zaman Ne Kullanmalı:

- **Düşük sıcaklık (0.2)**: Faktüel sorgular, kod yazımı, mantıksal problemler
- **Orta sıcaklık (0.7)**: Genel sohbet, açıklamalar, beyin fırtınası
- **Yüksek sıcaklık (1.0+)**: Hikaye yazımı, şiir, yaratıcı içerik
""",
    "English": """
### What is Temperature?

Temperature controls the level of creativity and randomness in the AI's responses.

- **0.0 - 0.3**: More consistent, deterministic, and focused responses
- **0.4 - 0.7**: Balanced creativity and consistency
- **0.8 - 1.0**: More creative, diverse, and surprising responses
- **1.0+**: High creativity and sometimes unexpected outputs

#### When to Use What:

- **Low temperature (0.2)**: Factual queries, code writing, logical problems
- **Medium temperature (0.7)**: General conversation, explanations, brainstorming
- **High temperature (1.0+)**: Story writing, poetry, creative content
"""
}

MAX_TOKENS_HELP = {
    "Türkçe": """
### Maksimum Token Nedir?

Maksimum token, AI'nın yanıtının alabileceği maksimum uzunluğu belirler.

- 1 token ≈ 4 karakter veya ¾ kelime
- 100 token ≈ 75 kelime
- 1000 token ≈ 750 kelime (yaklaşık 1.5 sayfa)
- 4000 token ≈ 3000 kelime (yaklaşık 6 sayfa)

#### Dikkat Edilmesi Gerekenler:

- Daha yüksek token limiti = Daha uzun yanıtlar = Daha yüksek maliyet
- Çok düşük token limiti, yanıtın aniden kesilebilmesine neden olabilir
- API'nin toplam token limiti (prompt + yanıt) modele göre değişir

Kullanım senaryonuza göre uygun değeri seçin. Uzun açıklamalar için 1000+, kısa yanıtlar için 100-300 token yeterlidir.
""",
    "English": """
### What is Maximum Token?

Maximum token determines the maximum length that the AI's response can have.

- 1 token ≈ 4 characters or ¾ word
- 100 tokens ≈ 75 words
- 1000 tokens ≈ 750 words (approximately 1.5 pages)
- 4000 tokens ≈ 3000 words (approximately 6 pages)

#### Things to Consider:

- Higher token limit = Longer responses = Higher cost
- Too low token limit can cause the response to be cut off abruptly
- The API's total token limit (prompt + response) varies by model

Choose an appropriate value for your use case. 1000+ tokens for long explanations, 100-300 tokens for short answers is sufficient.
"""
}

# Metin güvenlik kontrolü ve temizleme - HTML güvenliği eklenmiş
def safe_text(text):
    if text is None:
        return ""
    # Güvenli string dönüşümü
    text = str(text)
    # HTML özel karakterlerini kaçış karakteriyle değiştir
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#39;')
    return text

# CSV dışa aktarma için encode fonksiyonu
def generate_csv(chat_history, current_lang):
    conversation_data = []
    for sender, message in chat_history:
        # Sohbet içeriği için dil kontrolü ve çeviri
        if current_lang == "English" and sender == "Siz":
            sender = "You"
        conversation_data.append({"Sender": safe_text(sender), "Message": safe_text(message)})
    
    df = pd.DataFrame(conversation_data)
    return df.to_csv(index=False, encoding='utf-8-sig')  # UTF-8 BOM ile kaydedilir

# PDF oluşturma fonksiyonu - Türkçe karakter desteği iyileştirildi
def create_pdf(chat_history, conversation_name, language):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Türkçe karakterler için font
    if has_unicode_font:
        for style_name in styles.byName:
            styles[style_name].fontName = 'Roboto'
    
    styles.add(ParagraphStyle(name='Message', fontName='Roboto', fontSize=10, spaceAfter=6))
    styles.add(ParagraphStyle(name='Sender', fontName='Roboto-Bold', fontSize=12, spaceAfter=3))

    flowables = []

    # Başlık
    title_text = "Nous API Chat: " if language == "English" else "Nous API Sohbet: "
    title = Paragraph(f"{title_text}{safe_text(conversation_name)}", styles['Title'])
    flowables.append(title)
    flowables.append(Spacer(1, 12))

    # Sohbet içeriği
    for sender, message in chat_history:
        # Sohbet içeriği için dil kontrolü ve çeviri
        if language == "English" and sender == "Siz":
            sender = "You"
            
        sender_text = Paragraph(f"<b>{safe_text(sender)}:</b>", styles['Sender'])
        flowables.append(sender_text)
        
        # Unicode karakterlerde sorun olmaması için
        # Paragraf içindeki satır sonlarını düzelt
        message = message.replace('\n', '<br/>')
        message_text = Paragraph(safe_text(message), styles['Message'])
        flowables.append(message_text)
        flowables.append(Spacer(1, 6))

    # PDF oluştur
    doc.build(flowables)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data

# Temayı değiştirme fonksiyonu
def toggle_theme(new_theme):
    st.session_state.theme = new_theme
    st.rerun()  # experimental_rerun yerine rerun kullanın

# Geçerli dili alma
current_lang = st.session_state.language
texts = ui_text[current_lang]

# Ses bildirimi için HTML bileşeni ekle
st.markdown(get_audio_html(), unsafe_allow_html=True)

# İki sütunlu düzen
col1, col2 = st.columns([1, 3])

with col1:
    st.header(texts["conversations"])
    
    # Yeni sohbet butonu
    if st.button(texts["new_chat"]):
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        new_conv_name = f"Sohbet {timestamp}" if current_lang == "Türkçe" else f"Chat {timestamp}"
        st.session_state.conversations[new_conv_name] = []
        st.session_state.current_conversation = new_conv_name
        st.session_state.chat_history = []
        # Yeni mesaj gönderimi için input key'i güncelle
        st.session_state.input_key = f"input_{time.time()}"
        st.rerun()
    
    # Sohbet listesi ve seçimi
    st.subheader(texts["previous"])
    
    # Edit mode ayarlama fonksiyonu
    def set_edit_mode(mode):
        st.session_state.edit_mode = mode
    
    # Sohbet listesi düzenlenmesi
    for conv_name in st.session_state.conversations.keys():
        # Eğer bu sohbet yeniden adlandırma modundaysa
        if st.session_state.edit_mode == f"rename_{conv_name}":
            # Yeniden adlandırma formu
            with st.form(key=f"rename_form_{conv_name}"):
                new_name = st.text_input(texts["new_name"], value=conv_name, key=f"new_name_{conv_name}")
                col1_r, col2_r = st.columns(2)
                with col1_r:
                    cancel = st.form_submit_button(texts["cancel"])
                with col2_r:
                    save = st.form_submit_button(texts["save"])
                
                if save and new_name and new_name != conv_name:
                    # Sohbeti yeniden adlandır
                    st.session_state.conversations[new_name] = st.session_state.conversations[conv_name]
                    del st.session_state.conversations[conv_name]
                    if st.session_state.current_conversation == conv_name:
                        st.session_state.current_conversation = new_name
                    st.session_state.edit_mode = None
                    st.rerun()
                elif cancel:
                    st.session_state.edit_mode = None
                    st.rerun()
        
        # Eğer bu sohbet silme modundaysa
        elif st.session_state.edit_mode == f"delete_{conv_name}":
            st.warning(texts["delete_confirm"])
            col1_d, col2_d = st.columns(2)
            with col1_d:
                if st.button(texts["cancel"], key=f"cancel_delete_{conv_name}"):
                    st.session_state.edit_mode = None
                    st.rerun()
            with col2_d:
                if st.button(texts["delete"], key=f"confirm_delete_{conv_name}"):
                    # Sohbeti sil
                    del st.session_state.conversations[conv_name]
                    if st.session_state.current_conversation == conv_name:
                        if len(st.session_state.conversations) > 0:
                            st.session_state.current_conversation = list(st.session_state.conversations.keys())[0]
                            st.session_state.chat_history = st.session_state.conversations[st.session_state.current_conversation]
                        else:
                            st.session_state.current_conversation = "Main Chat"
                            st.session_state.conversations["Main Chat"] = []
                            st.session_state.chat_history = []
                    st.session_state.edit_mode = None
                    st.rerun()
        
        else:
            # Normal sohbet listesi görünümü
            col1_c, col2_c = st.columns([4, 1])
            with col1_c:
                if st.button(conv_name, key=f"conv_{conv_name}"):
                    st.session_state.current_conversation = conv_name
                    st.session_state.chat_history = st.session_state.conversations[conv_name]
                    # Sohbet değişimi için input key'i güncelle
                    st.session_state.input_key = f"input_{time.time()}"
                    st.rerun()
            with col2_c:
                # Üç nokta menüsü
                if st.button("⋮", key=f"options_{conv_name}"):
                    st.session_state.edit_mode = f"options_{conv_name}"
                    st.rerun()
            
            # Eğer seçenekler menüsü açıksa
            if st.session_state.edit_mode == f"options_{conv_name}":
                st.button(texts["rename"], key=f"rename_option_{conv_name}", on_click=lambda name=conv_name: set_edit_mode(f"rename_{name}"))
                st.button(texts["delete"], key=f"delete_option_{conv_name}", on_click=lambda name=conv_name: set_edit_mode(f"delete_{name}"))
                st.button(texts["cancel"], key=f"cancel_options_{conv_name}", on_click=lambda: set_edit_mode(None))
    
    # Kullanım bilgileri
    st.subheader(texts["stats"])
    st.write(f"{texts['total_token']}: {st.session_state.token_usage['total_tokens']}")
    st.write(f"{texts['prompt_token']}: {st.session_state.token_usage['prompt_tokens']}")
    st.write(f"{texts['response_token']}: {st.session_state.token_usage['completion_tokens']}")
    st.write(f"{texts['cost']}: ${st.session_state.total_cost:.6f}")
    
    # Dışa Aktarma
    st.subheader(texts["export"])
    export_format = st.selectbox(texts["format"], ["JSON", "PDF", "CSV"])
    if st.button(texts["export_btn"]):
        if len(st.session_state.chat_history) == 0:
            st.error(texts["no_chat"])
        else:
            if export_format == "JSON":
                conversation_data = []
                for sender, message in st.session_state.chat_history:
                    # Sohbet içeriği için dil kontrolü ve çeviri
                    if current_lang == "English" and sender == "Siz":
                        sender = "You"
                    conversation_data.append({"sender": safe_text(sender), "message": safe_text(message)})
                
                json_string = json.dumps(conversation_data, indent=2, ensure_ascii=False)
                
                # UTF-8 BOM ile kaydedilir
                buffer = io.StringIO()
                buffer.write(json_string)
                buffer.seek(0)
                
                # Dosya adını doğrudan sohbet adından al
                filename = f"{st.session_state.current_conversation}.json"
                st.download_button(
                    label="JSON" if current_lang == "English" else "JSON İndir",
                    data=buffer.getvalue(),
                    file_name=filename,
                    mime="application/json;charset=utf-8"
                )
            
            elif export_format == "PDF":
                try:
                    pdf_data = create_pdf(st.session_state.chat_history, st.session_state.current_conversation, current_lang)
                    # Dosya adını doğrudan sohbet adından al
                    filename = f"{st.session_state.current_conversation}.pdf"
                    st.download_button(
                        label="PDF" if current_lang == "English" else "PDF İndir",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"{texts['pdf_error']}: {str(e)}")
                    st.info(texts["pdf_error_detail"])
                
            elif export_format == "CSV":
                try:
                    csv_data = generate_csv(st.session_state.chat_history, current_lang)
                    # Dosya adını doğrudan sohbet adından al
                    filename = f"{st.session_state.current_conversation}.csv"
                    st.download_button(
                        label="CSV" if current_lang == "English" else "CSV İndir",
                        data=csv_data.encode('utf-8-sig'),  # UTF-8 BOM ile kaydedilir
                        file_name=filename,
                        mime="text/csv;charset=utf-8-sig"
                    )
                except Exception as e:
                    st.error(f"CSV oluşturma hatası: {str(e)}")
    
    # Temizle butonu
    if st.button(texts["clear"]):
        st.session_state.chat_history = []
        st.session_state.conversations[st.session_state.current_conversation] = []
        # Sohbeti temizlediğimizde input key'i güncelle
        st.session_state.input_key = f"input_{time.time()}"
        st.rerun()

with col2:
    # Ana uygulama
    st.title(texts["title"])
    st.markdown(f"**{texts['active_chat']}:** {st.session_state.current_conversation}")
    st.markdown(texts["subtitle"])
    
    # Sidebar - API Key ve Ayarlar
    st.sidebar.header(texts["settings"])
    
    # Tema seçimi (aydınlık/karanlık)
    st.sidebar.subheader(texts["appearance"])
    theme_cols = st.sidebar.columns(2)
    with theme_cols[0]:
        if st.button("☀️", help=texts["light_mode"]):
            toggle_theme("light")
        st.caption(texts["light_mode"])
    with theme_cols[1]:
        if st.button("🌙", help=texts["dark_mode"]):
            toggle_theme("dark")
        st.caption(texts["dark_mode"])
    
    st.sidebar.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
    
    # Dil seçimi (bayraklı)
    st.sidebar.subheader("Dil / Language")
    lang_cols = st.sidebar.columns([1, 3])
    with lang_cols[0]:
        if current_lang == "Türkçe":
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Flag_of_Turkey.svg/125px-Flag_of_Turkey.svg.png", width=30)
        else:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Flag_of_the_United_States.svg/125px-Flag_of_the_United_States.svg.png", width=30)
    
    with lang_cols[1]:
        selected_lang = st.selectbox(
            "", 
            ["Türkçe", "English"],
            index=0 if current_lang == "Türkçe" else 1,
            label_visibility="collapsed"
        )
    
    # Dil değiştirilmişse güncelle
    if selected_lang != current_lang:
        st.session_state.language = selected_lang
        st.rerun()
    
    st.sidebar.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
    
    # API anahtar bölümü
    st.sidebar.subheader(texts["api_key"])
    api_key = st.sidebar.text_input("", type="password", label_visibility="collapsed")
    
    st.sidebar.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
    
    # Model seçimi bölümü
    st.sidebar.subheader(texts["model_selection"])
    model = st.sidebar.selectbox("", [
        "Hermes-3-Llama-3.1-405B",  # Eksik olan model eklendi
        "DeepHermes-3-Mistral-24B-Preview",
        "Hermes-3-Llama-3.1-70B",
        "DeepHermes-3-Llama-3-8B-Preview"
    ], label_visibility="collapsed")

    
    st.sidebar.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
    
    # Model ayarları bölümü
    st.sidebar.header(texts["model_settings"])
    
    # Sıcaklık ayarı ve yardım butonu
    temp_col1, temp_col2 = st.sidebar.columns([5, 1])
    with temp_col1:
        st.text(texts["temperature"])
    with temp_col2:
        if st.button("?", key="temp_help"):
            st.session_state.show_temp_help = not st.session_state.get('show_temp_help', False)
    
    if st.session_state.get('show_temp_help', False):
        st.sidebar.info(TEMPERATURE_HELP[current_lang])
    
    temperature = st.sidebar.slider("", min_value=0.0, max_value=2.0, value=0.7, step=0.1, key="temperature_slider", label_visibility="collapsed")
    
    st.sidebar.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
    
    # Maksimum token ayarı ve yardım butonu
    token_col1, token_col2 = st.sidebar.columns([5, 1])
    with token_col1:
        st.text(texts["max_tokens"])
    with token_col2:
        if st.button("?", key="token_help"):
            st.session_state.show_token_help = not st.session_state.get('show_token_help', False)
    
    if st.session_state.get('show_token_help', False):
        st.sidebar.info(MAX_TOKENS_HELP[current_lang])
    
    max_tokens = st.sidebar.slider("", min_value=100, max_value=4000, value=1000, step=100, key="max_tokens_slider", label_visibility="collapsed")
    
    st.sidebar.markdown("<hr class='section-separator'>", unsafe_allow_html=True)
    
    # Sistem mesajı bölümü
    st.sidebar.header(texts["system_msg"])
    
    # Sistem mesajı başlığı ve yardım butonu yan yana
    col_sys_1, col_sys_2 = st.sidebar.columns([5, 1])
    with col_sys_1:
        st.text(texts["template"])
    with col_sys_2:
        if st.button("?", key="help_system"):
            st.session_state.show_help = not st.session_state.get('show_help', False)
    
    if st.session_state.get('show_help', False):
        st.sidebar.info(SYSTEM_MESSAGE_HELP[current_lang])
        
    # Dile göre sistem mesajı şablonlarını getir
    current_templates = list(system_messages[current_lang].keys())
    selected_system = st.sidebar.selectbox("", current_templates, label_visibility="collapsed")
    system_message = system_messages[current_lang][selected_system]
    
    # Özel sistem mesajı
    use_custom_system = st.sidebar.checkbox(texts["use_custom"])
    if use_custom_system:
        system_message = st.sidebar.text_area(texts["custom_msg"], value=system_message, height=150)
    
    # Sohbet geçmişi - Önce bu gösterilecek
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history:
            st.subheader(texts["chat"])
            for sender, message in st.session_state.chat_history:
                display_sender = sender
                if current_lang == "English" and sender == "Siz":
                    display_sender = "You"
                
                if display_sender == "You" or display_sender == "Siz":
                    st.markdown(f"<div class='user-message'><strong>{safe_text(display_sender)}:</strong> {safe_text(message)}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='ai-message'><strong>{safe_text(display_sender)}:</strong> {safe_text(message)}</div>", unsafe_allow_html=True)
    
    # Kullanıcı mesajı alanı - En aşağıda sabit
    input_container = st.container()
    
    with input_container:
        st.markdown("<div class='chat-input-area'>", unsafe_allow_html=True)
        # Kullanıcı mesajı - key değerini dinamik olarak ayarla
        user_prompt = st.text_area(
            texts["write_msg"], 
            key=st.session_state.input_key,
            height=100
        )
        
        # Gönder butonu
        if st.button(texts["send"]):
            if not api_key:
                st.warning(texts["warning_api"])
            elif not user_prompt.strip():
                st.warning(texts["warning_prompt"])
            else:
                with st.spinner(texts["waiting"]):
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
        
                    data = {
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
        
                    response = requests.post(
                        "https://inference-api.nousresearch.com/v1/chat/completions", 
                        headers=headers,
                        json=data
                    )
        
                    if response.status_code == 200:
                        response_json = response.json()
                        reply = response_json["choices"][0]["message"]["content"]
        
                        # Token kullanımını güncelle (API dönüşünde varsa)
                        if "usage" in response_json:
                            usage = response_json["usage"]
                            st.session_state.token_usage["prompt_tokens"] += usage.get("prompt_tokens", 0)
                            st.session_state.token_usage["completion_tokens"] += usage.get("completion_tokens", 0)
                            st.session_state.token_usage["total_tokens"] += usage.get("total_tokens", 0)
                            
                            # Maliyet tahmini (tahmini fiyat modele göre değişebilir)
                            prompt_cost = usage.get("prompt_tokens", 0) * 0.000001  # Örnek fiyat
                            completion_cost = usage.get("completion_tokens", 0) * 0.000002  # Örnek fiyat
                            total_cost = prompt_cost + completion_cost
                            st.session_state.total_cost += total_cost
        
                        # Sohbet geçmişine ekle
                        user_label = texts["you"] if current_lang == "English" else "Siz"
                        st.session_state.chat_history.append((user_label, user_prompt))
                        st.session_state.chat_history.append(("Nous", reply))
                        
                        # Mevcut konuşmayı güncelle
                        st.session_state.conversations[st.session_state.current_conversation] = st.session_state.chat_history
                        
                        # Input kutusunu temizlemek için key değişimi
                        st.session_state.input_key = f"input_{time.time()}"
                        
                        # Bildirim sesi çal
                        play_notification_sound()
                        
                        st.rerun()
                    else:
                        st.error(f"{texts['api_error']}: {response.status_code}")
                        st.code(response.text)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(texts["footer"], unsafe_allow_html=True)