# Nous API Chat Interface

A modern and user-friendly interface for interacting with the Nous Research API models. This application allows those with Nous Research API access to easily test and explore various models using their own API keys.

**🌐 Live Demo**: [https://nousresearch.streamlit.app/](https://nousresearch.streamlit.app/)

> **Ready to use**: The application is already deployed and available online. Simply visit the link above to start using it immediately with your Nous API key. No installation required if you prefer using the hosted version.

![Nous Chat Interface](https://i.imgur.com/example.png)

## 📋 Project Purpose

The primary purpose of this project is to provide Nous Research API users with a convenient testing environment for their API keys and models. It serves as:

- **A Testing Sandbox**: Quickly evaluate different models' responses and capabilities
- **A Development Tool**: Test prompts and system messages before implementing in production applications
- **A Comparison Platform**: Compare different models and parameter settings side by side
- **A User-Friendly Interface**: Access Nous Research's powerful models without writing code

This interface bridges the gap between having API access and effectively exploring what these models can do, making the powerful Nous Research models more accessible for testing and evaluation.

## 🌟 Features

- **Multiple Model Support**: Access various Nous Research models including DeepHermes, Hermes, and more
- **Conversation Management**: Create, rename, and delete conversations
- **Theme Support**: Switch between light and dark themes for comfortable viewing
- **Multilingual Interface**: Available in English and Turkish
- **Export Options**: Save conversations in JSON, PDF, or CSV formats
- **System Message Templates**: Choose from pre-defined system prompts or create custom ones
- **Usage Statistics**: Track token usage and estimated costs

## 🚀 Getting Started

### Online Version

The easiest way to get started is to use the online version:

1. Visit [https://nousresearch.streamlit.app/](https://nousresearch.streamlit.app/)
2. Enter your Nous API key in the sidebar
3. Start chatting with the models immediately

### Local Installation

If you prefer to run the application locally:

#### Prerequisites

- Python 3.8 or higher
- **Nous API key** (obtain from [Nous Research Portal](https://portal.nousresearch.com/))
  - **Note**: This application requires you to have valid Nous Research API access

#### Installation Steps

1. Clone the repository or download the code
<br>git clone https://github.com/bynextex/Nous-Research.git
<br>cd nous-chat


2. Install the required dependencies
<br>pip install -r requirements.txt


3. Run the application
<br>streamlit run nous_chat_appv2.py


4. Open your browser and navigate to `http://localhost:8501`

## 📝 Usage Guide

### Setting Up

1. Enter your Nous API key in the sidebar
2. Select your preferred language (English or Turkish)
3. Choose a model from the dropdown menu

### Creating a Conversation

1. Click on "New Chat" button to start a fresh conversation
2. Previous conversations are listed under "Previous Chats"
3. Click on any conversation name to switch to that conversation

### Configuring Model Parameters

1. Adjust temperature (creativity level) using the slider
- Lower values (0.0-0.3): More consistent, deterministic responses
- Medium values (0.4-0.7): Balanced creativity and consistency
- Higher values (0.8-2.0): More creative and varied responses

2. Set the maximum tokens (response length) according to your needs
- 100 tokens ≈ 75 words
- 1000 tokens ≈ 750 words (about 1.5 pages)

### Using System Messages

1. Select a template from the dropdown menu or create a custom one
- Chains of Thought: For detailed reasoning and explanations
- Expert Advisor: For professional and comprehensive answers
- Simple Helper: For concise and direct responses
- Turkish Assistant: For answers in Turkish
- SEO Expert: For SEO-related advice in bullet points

2. Check "Use Custom System Message" to modify or create your own system prompt

### Chatting

1. Type your message in the text area
2. Click "Send" to get a response
3. The conversation will update automatically

### Managing Conversations

1. Click the "⋮" button next to any conversation to:
- Rename the conversation
- Delete the conversation

2. Use "Clear Chat" to remove all messages from the current conversation

### Exporting Data

1. Select the desired format (JSON, PDF, or CSV)
2. Click "Export" to download the current conversation

## 🛠️ Technical Details

This application is built with:
- Streamlit for the web interface
- ReportLab for PDF generation
- Nous Research API for model interactions

## 🔒 Privacy & Security

- API keys are not stored between sessions
- All data remains local to your browser
- No data is sent to any servers except for the Nous API endpoints

## 🌐 Languages

The interface is available in:
- English
- Turkish

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Developed by [Bynextex](https://x.com/muma_gaga)

---




# TÜRKÇE AÇIKLAMA
# Nous API Sohbet Arayüzü

Nous Research API modelleriyle etkileşim için modern ve kullanıcı dostu bir arayüz. Bu uygulama, Nous Research API erişimi olan kullanıcıların kendi API anahtarlarıyla çeşitli modelleri kolayca test etmelerini ve keşfetmelerini sağlar.

**🌐 Canlı Demo**: [https://nousresearch.streamlit.app/](https://nousresearch.streamlit.app/)

> **Kullanıma Hazır**: Uygulama zaten dağıtılmış ve çevrimiçi olarak kullanılabilir durumdadır. Nous API anahtarınızla hemen kullanmaya başlamak için yukarıdaki bağlantıyı ziyaret edin. Barındırılan sürümü kullanmayı tercih ederseniz kurulum gerekmez.

![Nous Sohbet Arayüzü](https://i.imgur.com/example.png)

## 📋 Proje Amacı

Bu projenin temel amacı, Nous Research API kullanıcılarına API anahtarları ve modelleri için kullanışlı bir test ortamı sağlamaktır. Şu amaçlara hizmet eder:

- **Test Ortamı**: Farklı modellerin yanıtlarını ve yeteneklerini hızlıca değerlendirme
- **Geliştirme Aracı**: Üretim uygulamalarında kullanmadan önce istem ve sistem mesajlarını test etme
- **Karşılaştırma Platformu**: Farklı modelleri ve parametre ayarlarını yan yana karşılaştırma
- **Kullanıcı Dostu Arayüz**: Kod yazmadan Nous Research'ün güçlü modellerine erişim

Bu arayüz, API erişimine sahip olmak ile bu modellerin neler yapabileceğini etkili bir şekilde keşfetmek arasındaki boşluğu doldurarak, Nous Research modellerini test ve değerlendirme için daha erişilebilir hale getirir.

## 🌟 Özellikler

- **Çoklu Model Desteği**: DeepHermes, Hermes ve daha fazlası dahil çeşitli Nous Research modellerine erişim
- **Sohbet Yönetimi**: Sohbet oluşturma, yeniden adlandırma ve silme
- **Tema Desteği**: Rahat görüntüleme için açık ve koyu temalar arasında geçiş
- **Çok Dilli Arayüz**: İngilizce ve Türkçe olarak kullanılabilir
- **Dışa Aktarma Seçenekleri**: Sohbetleri JSON, PDF veya CSV formatlarında kaydetme
- **Sistem Mesajı Şablonları**: Önceden tanımlanmış sistem mesajlarından seçin veya özel mesajlar oluşturun
- **Kullanım İstatistikleri**: Token kullanımı ve tahmini maliyetleri takip edin

## 🚀 Başlarken

### Çevrimiçi Sürüm

Başlamanın en kolay yolu çevrimiçi sürümü kullanmaktır:

1. [https://nousresearch.streamlit.app/](https://nousresearch.streamlit.app/) adresini ziyaret edin
2. Yan menüdeki Nous API anahtarınızı girin
3. Hemen modellerle sohbet etmeye başlayın

### Yerel Kurulum

Uygulamayı yerel olarak çalıştırmayı tercih ederseniz:

#### Gereksinimler

- Python 3.8 veya daha yüksek
- **Nous API anahtarı** ([Nous Research Portal](https://portal.nousresearch.com/) adresinden edinebilirsiniz)
  - **Not**: Bu uygulama, geçerli bir Nous Research API erişiminizin olmasını gerektirir

#### Kurulum Adımları

1. Kodu indirin veya klonlayın
<br>git clone https://github.com/bynextex/Nous-Research.git
<br>cd nous-chat


2. Gerekli eklentileri yükleyin
<br>pip install -r requirements.txt


3. Uygulamayı çalıştırın
<br>streamlit run nous_chat_appv2.py


4. Tarayıcınızı açın ve `http://localhost:8501` adresine gidin

## 📝 Kullanım Kılavuzu

### Kurulum

1. Yan menüdeki Nous API anahtarınızı girin
2. Tercih ettiğiniz dili seçin (İngilizce veya Türkçe)
3. Açılır menüden bir model seçin

### Sohbet Oluşturma

1. Yeni bir sohbet başlatmak için "Yeni Sohbet" düğmesine tıklayın
2. Önceki sohbetler "Önceki Sohbetler" altında listelenir
3. Herhangi bir sohbet adına tıklayarak o sohbete geçiş yapabilirsiniz

### Model Parametrelerini Yapılandırma

1. Sıcaklık (yaratıcılık seviyesi) ayarını kaydırıcı ile ayarlayın
- Düşük değerler (0.0-0.3): Daha tutarlı, belirleyici yanıtlar
- Orta değerler (0.4-0.7): Dengeli yaratıcılık ve tutarlılık
- Yüksek değerler (0.8-2.0): Daha yaratıcı ve çeşitli yanıtlar

2. İhtiyaçlarınıza göre maksimum token (yanıt uzunluğu) ayarlayın
- 100 token ≈ 75 kelime
- 1000 token ≈ 750 kelime (yaklaşık 1.5 sayfa)

### Sistem Mesajlarını Kullanma

1. Açılır menüden bir şablon seçin veya özel bir şablon oluşturun
- Düşünce Zincirleri: Detaylı düşünme ve açıklamalar için
- Uzman Danışman: Profesyonel ve kapsamlı yanıtlar için
- Basit Yardımcı: Kısa ve doğrudan yanıtlar için
- Türkçe Yardımcı: Türkçe yanıtlar için
- SEO Uzmanı: Madde işaretli SEO tavsiyeleri için

2. Kendi sistem mesajınızı oluşturmak veya değiştirmek için "Özel Sistem Mesajı Kullan" seçeneğini işaretleyin

### Sohbet Etme

1. Mesajınızı metin alanına yazın
2. Yanıt almak için "Gönder" düğmesine tıklayın
3. Sohbet otomatik olarak güncellenecektir

### Sohbetleri Yönetme

1. Herhangi bir sohbetin yanındaki "⋮" düğmesine tıklayarak:
- Sohbeti yeniden adlandırabilirsiniz
- Sohbeti silebilirsiniz

2. Mevcut sohbetteki tüm mesajları kaldırmak için "Sohbeti Temizle" seçeneğini kullanın

### Veri Dışa Aktarma

1. İstediğiniz formatı seçin (JSON, PDF veya CSV)
2. Mevcut sohbeti indirmek için "Dışa Aktar" düğmesine tıklayın

## 🛠️ Teknik Detaylar

Bu uygulama şunlarla oluşturulmuştur:
- Web arayüzü için Streamlit
- PDF oluşturma için ReportLab
- Model etkileşimleri için Nous Research API

## 🔒 Gizlilik ve Güvenlik

- API anahtarları oturumlar arasında saklanmaz
- Tüm veriler tarayıcınızda yerel olarak kalır
- Nous API uç noktaları dışında hiçbir sunucuya veri gönderilmez

## 🌐 Diller

Arayüz şu dillerde kullanılabilir:
- İngilizce
- Türkçe

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için LICENSE dosyasına bakın.

## 👨‍💻 Yazar

Geliştiren: [Bynextex](https://x.com/muma_gaga)