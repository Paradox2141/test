# Git ve GitHub Kısa Eğitim

## Git Nedir?

Git, kod değişikliklerinizi takip eden bir **versiyon kontrol sistemi**dir. Projenizdeki her değişikliği kaydeder ve gerektiğinde geriye dönmenizi sağlar.

## GitHub Nedir?

GitHub, Git ile yönetilen projeleri bulutta saklamak ve başkalarıyla paylaşmak için kullanılan bir **platformdur**.

---

## Temel Kavramlar

- **Repository (Repo)**: Projenizin saklandığı klasör
- **Commit**: Değişikliklerinizin kaydedilmiş hali (anlık görüntü)
- **Branch**: Projenin farklı bir versiyonu üzerinde çalışmak için dal
- **Merge**: İki branch'i birleştirme
- **Push**: Yerel değişikliklerinizi GitHub'a gönderme
- **Pull**: GitHub'daki değişiklikleri yerel bilgisayarınıza alma
- **Clone**: Bir projeyi GitHub'dan bilgisayarınıza kopyalama
- **Remote**: Uzak sunucudaki repository (örn: GitHub'daki origin veya upstream)
- **Tracking Branch**: Remote branch'lerin bilgisayarınızdaki yerel referansı (örn: origin/master, upstream/master)

---

## 🎯 Tracking Branch (İzleme Dalı) Nedir?

**Tracking branch**, remote (uzak) repository'deki branch'lerin **bilgisayarınızdaki yerel kopyası/referansıdır**.

**Önemli Özellikler:**

- Üzerinde **direkt çalışamazsınız** (checkout edemezsiniz)
- Sadece **referans** olarak kullanılır
- `git fetch` ile **güncellenir**
- `.git/refs/remotes/` klasöründe saklanır

**Branch Türleri:**

```bash
# 1. LOCAL BRANCH (Üzerinde çalıştığınız branch'ler)
master                    # Local master branch
feature-branch            # Local feature branch
# → git checkout ile geçiş yapabilirsiniz
# → Üzerinde commit atabilirsiniz
# → .git/refs/heads/ altında saklanır

# 2. REMOTE TRACKING BRANCH (Referanslar)
origin/master             # Origin'deki master'ın local referansı
upstream/master           # Upstream'deki master'ın local referansı
origin/development        # Origin'deki development'ın local referansı
# → git checkout ile GEÇİŞ YAPAMAZSINIZ (sadece görürsünüz)
# → git fetch ile güncellenir
# → .git/refs/remotes/ altında saklanır
```

**Görsel Açıklama:**

```
GitHub (Remote Sunucu)
┌─────────────────────────────────────┐
│ origin (fork'unuz)                  │
│   - master: A → B → C → D           │
│   - development: A → B → X → Y      │
└─────────────────────────────────────┘
              ↓
              ↓ git fetch origin (indirir)
              ↓
┌─────────────────────────────────────┐
│ Local (.git klasörü)                │
│                                      │
│ TRACKING BRANCHES (referans):       │
│   origin/master: A → B → C → D      │ ← GitHub'daki origin/master'ın kopyası
│   origin/development: A → B → X → Y │ ← GitHub'daki origin/development'ın kopyası
│                                      │
│ LOCAL BRANCHES (çalışma alanı):     │
│   master: A → B → C → D             │ ← Üzerinde çalışabilirsiniz
│   feature: A → B → C → Z            │ ← Üzerinde çalışabilirsiniz
└─────────────────────────────────────┘
```

**Pratik Örnek:**

```bash
# Remote tracking branch'leri görmek:
git branch -r
# origin/master
# origin/development
# upstream/master

# Local branch'leri görmek:
git branch
# * master
#   feature-branch
#   hotfix

# Hepsini görmek:
git branch -a
# * master                    ← Local
#   feature-branch            ← Local
#   hotfix                    ← Local
#   remotes/origin/master     ← Tracking branch
#   remotes/origin/development ← Tracking branch
#   remotes/upstream/master   ← Tracking branch

# Tracking branch'i güncelleme:
git fetch origin
# → origin/master ve origin/development güncellenir

# Tracking branch'ten local branch'e merge:
git checkout master           # Local master'a geç
git merge origin/master       # Tracking branch'i merge et
```

**Neden İki Tür Branch Var?**

```bash
# LOCAL BRANCH: Çalışma alanınız
git checkout master           # Local master'a geç
git commit -m "Yeni özellik"  # Commit atabilirsiniz
# → Sadece bilgisayarınızda değişir

# TRACKING BRANCH: Remote'un aynası
git fetch origin              # origin/master'ı güncelle
# → GitHub'dan indirir, tracking branch güncellenir
# → Local branch DEĞİŞMEZ!

git merge origin/master       # Tracking branch'i local'e merge et
# → Şimdi local branch da güncellenir
```

**Tracking Branch ile Çalışma:**

```bash
# ❌ YANLIŞ: Tracking branch'e checkout yapamazsınız
git checkout origin/master
# Hata: You are in 'detached HEAD' state
# → Çalışamazsınız, sadece görürsünüz

# ✅ DOĞRU: Tracking branch'ten yeni local branch oluştur
git checkout -b my-branch origin/master
# → origin/master'dan yeni local branch oluşturur

# ✅ DOĞRU: Tracking branch'i merge edin
git checkout master
git merge origin/master
# → Tracking branch'i local master'a merge eder
```

**Özet Tablo:**

| Özellik | Local Branch | Tracking Branch |
|---------|-------------|-----------------|
| **Örnekler** | `master`, `feature-branch` | `origin/master`, `upstream/master` |
| **Nerede?** | `.git/refs/heads/` | `.git/refs/remotes/` |
| **Checkout yapılır mı?** | ✅ Evet | ❌ Hayır (detached HEAD) |
| **Commit atılır mı?** | ✅ Evet | ❌ Hayır (sadece referans) |
| **Nasıl güncellenir?** | `git commit` | `git fetch` |
| **Görme** | `git branch` | `git branch -r` |
| **Kullanım** | Üzerinde çalışırsınız | Referans olarak kullanılır |

**Sonuç:** Tracking branch'ler, remote repository'deki branch'lerin bilgisayarınızdaki **yerel aynalarıdır**. Üzerinde direkt çalışamazsınız, sadece `git fetch` ile güncellersiniz ve `git merge` ile local branch'inize aktarırsınız. 🎯

### ⚠️ ÇOK KRİTİK UYARI: Git Otomatik Güncelleme YAPMAZ

**Git, GitHub'ı otomatik olarak kontrol ETMEZ!**

```bash
# ÖNEMLI: fetch/pull yapmazsanız haberiniz olmaz!

# ⚠️ FORK YAPISI İLE ÇALIŞIYORSANIZ:
# Takım arkadaşları UPSTREAM'e (orijinal repo) commit atıyor!
# Kendi fork'unuz (origin) sadece sizin değişikliklerinizi içerir

# ❌ YANLIŞ: Fork'ta origin kendi repomuz
git fetch origin        # → Sadece kendi fork'unuzu günceller (genelde zaten siz çalışıyorsunuz)

# ✅ DOĞRU: Takımın değişiklikleri upstream'de
git fetch upstream      # → Orijinal repo'daki takım değişikliklerini getirir
git merge upstream/master

# ⚠️ NORMAL REPO'DA (FORK DEĞİL):
# Takım arkadaşları origin'e (ana repo) commit atıyor
git fetch origin        # → Takımın değişikliklerini getirir
git merge origin/master
```

**Pratik Örnek - FORK Yapısı:**

```
Pazartesi 09:00 - Projeyi fork'layıp clone'ladınız:
──────────────────────────────────────────────────
GitHub upstream/master: A → B → C → D
GitHub origin/master:   A → B → C → D
Local origin/master:    A → B → C → D  ✅ Güncel

Salı 17:00 - Takım UPSTREAM'e 10 commit attı:
──────────────────────────────────────────────
GitHub upstream/master: A → B → C → D → E → F → G → H → I → J → K → L → M → N
GitHub origin/master:   A → B → C → D  (Fork'unuz eski kaldı)
Local upstream/master:  A → B → C → D  ❌ ESKİ! (Fetch yapmadınız)

Çarşamba 10:00 - Siz merge yapmak istediniz:
────────────────────────────────────────────────
# ❌ YANLIŞ:
git fetch origin              # Sadece fork'unuzu günceller
git merge origin/master       # E-N arası GELİMEZ! (fork'ta yok)

# ✅ DOĞRU:
git fetch upstream            # Orijinal repo'dan güncelle
git log upstream/master -5    # Nelerin geldiğini gör
git merge upstream/master     # Şimdi takımın değişiklikleri gelir
→ E, F, G, H, I, J, K, L, M, N GELİR!

# Fork'unuzu da güncelleyin:
git push origin master        # Fork'unuz da artık güncel
```

**Önerilen Çalışma Akışı:**

**FORK ile çalışıyorsanız:**

```bash
# Her çalışmaya başlamadan ÖNCE:
git fetch upstream            # 1. Orijinal repo'yu kontrol et (TAKIMIN DEĞİŞİKLİKLERİ)
git log upstream/master -10   # 2. Neler değişmiş gör
git merge upstream/master     # 3. Takımın değişikliklerini al
git push origin master        # 4. Fork'unuzu da güncelle

# Şimdi çalışmaya başla
git checkout -b feature-branch
# ... kodlama ...
git commit -m "Yeni özellik"

# Push yapmadan önce TEKRAR kontrol et:
git fetch upstream            # Takım yeni değişiklik yapmış olabilir
git merge upstream/master     # Varsa merge et
git push origin feature-branch
```

**NORMAL REPO ile çalışıyorsanız (fork değil):**

```bash
# Her çalışmaya başlamadan ÖNCE:
git fetch origin              # 1. Ana repo'yu kontrol et
git log origin/master -10     # 2. Neler değişmiş gör
git pull origin master        # 3. Güncellemeleri al

# Şimdi çalışmaya başla
git checkout -b feature-branch
# ... kodlama ...
git commit -m "Yeni özellik"

# Push yapmadan önce TEKRAR kontrol et:
git fetch origin              # Başkaları değişiklik yapmış olabilir
git merge origin/master       # Varsa merge et
git push origin feature-branch
```

**Fark:**

| Yapı | Takım Nerede Çalışıyor? | Hangi Remote'u Fetch Etmeli? |
|------|------------------------|------------------------------|
| **FORK** | `upstream` (orijinal repo) | `git fetch upstream` |
| **NORMAL** | `origin` (ana repo) | `git fetch origin` |

**Özet:** Git otomatik senkronizasyon YAPMAZ! **Fork yapısında takım arkadaşları `upstream`'e commit atıyor**, `origin` sadece sizin fork'unuz. `git fetch upstream` yapmazsanız takımın değişikliklerinden haberiniz olmaz! Normal repo yapısında ise `git fetch origin` yapmalısınız. 🎯

---

## Git Kurulumu ve İlk Ayarlar

### Git'i İndirme

- Windows: <https://git-scm.com/download/win>
- Mac/Linux: Terminal'de `git --version` yazarak kontrol edin

### İlk Yapılandırma

```bash
git config --global user.name "Adınız Soyadınız"
git config --global user.email "email@example.com"
```

---

## Temel Git Komutları

### 1. Yeni Bir Repository Oluşturma

```bash
git init
```

Bu komut, bulunduğunuz klasörü bir Git repository'sine çevirir.

### 2. Dosyaları İzlemeye Alma (Staging)

```bash
git add dosya_adi.txt          # Tek dosya ekleme
git add .                       # Tüm değişiklikleri ekleme
```

### 3. Değişiklikleri Kaydetme (Commit)

```bash
git commit -m "Açıklayıcı mesaj yazın"
```

### 4. Durum Kontrolü

```bash
git status                      # Hangi dosyalar değişti?
git log                         # Commit geçmişi
git log --oneline               # Kısa commit geçmişi
```

### 5. Branch (Dal) İşlemleri

```bash
git branch                      # Tüm branch'leri listele
git branch yeni-branch          # Yeni branch oluştur
git checkout yeni-branch        # Branch'e geç
git checkout -b yeni-branch     # Oluştur ve geç
git merge yeni-branch           # Branch'i birleştir
git branch -d yeni-branch       # Branch'i sil
```

#### Git Merge Detaylı Açıklama

**`git merge master` ne yapar?**

`git merge master` komutu, **master branch'indeki değişiklikleri şu an bulunduğunuz branch'e birleştirir**.

**Örnek Senaryo:**

```bash
# Şu an "feature" branch'indesiniz
git branch
# * feature
#   master

# Master'daki güncellemeleri feature branch'ine çekmek için:
git merge master
```

**Ne Olur?**

1. Master branch'indeki tüm commit'ler feature branch'ine eklenir
2. İki branch'in değişiklikleri birleştirilir
3. Eğer çakışma yoksa, otomatik merge commit oluşturulur
4. Eğer çakışma varsa, manuel düzeltme yapmanız gerekir

**Pratik Kullanım:**

```bash
# Senaryo: Feature branch'inde çalışıyorsunuz, 
# ama master'da yeni güncellemeler var

# 1. Master'ı güncelleyin
git checkout master
git pull origin master

# 2. Kendi branch'inize geri dönün
git checkout feature-branch

# 3. Master'daki değişiklikleri feature branch'inize merge edin
git merge master

# 4. Artık feature-branch hem kendi değişikliklerinizi 
#    hem de master'daki güncellemeleri içerir
```

**Conflict (Çakışma) Durumu:**

Eğer aynı dosyanın aynı satırlarında farklı değişiklikler varsa:

```bash
git merge master
# CONFLICT (content): Merge conflict in dosya.txt
# Automatic merge failed; fix conflicts and then commit the result.

# Çakışan dosyaları düzeltin (VS Code'da çakışmalar gösterilir)
# <<<<<<< HEAD
# Sizin değişiklikleriniz
# =======
# Master'daki değişiklikler
# >>>>>>> master

# Düzeltmeden sonra:
git add .
git commit -m "Merge conflict çözüldü"
```

**Merge vs Rebase:**

| `git merge master` | `git rebase master` |
|-------------------|---------------------|
| Merge commit oluşturur | Commit geçmişini yeniden yazar |
| Geçmiş dallanmış görünür | Geçmiş düz bir çizgi olur |
| Güvenli, değişiklik kaydı net | Daha temiz geçmiş |
| Takım çalışmasında önerilir | Kişisel branch'lerde kullanılır |

**⚠️ ÇOK ÖNEMLİ: Local vs Remote Branch Farkı**

```bash
# ❌ YANLIŞ ANLAMA: git merge master
# Bu komut UPSTREAM (orijinal repo) master'ını ALMAZ!
# YEREL (local) master branch'inizi merge eder

git merge master
# → Kendi bilgisayarınızdaki local master'ı merge eder
# → Origin (kendi fork'unuz) master'ını merge eder

# ✅ DOĞRU: Upstream master'ı merge etmek için
git fetch upstream              # Önce upstream'i çek
git merge upstream/master       # Sonra upstream master'ı merge et
```

**Fork'ta Çalışırken Hangi Master'ı Kullanıyorsunuz?**

```bash
# Remote'larınızı kontrol edin:
git remote -v

# origin    https://github.com/SIZIN_HESAP/repo.git      ← Kendi fork'unuz
# upstream  https://github.com/ORIJINAL_HESAP/repo.git   ← Orijinal repo

# Farklı merge seçenekleri:
git merge master                 # Local master (bilgisayarınızdaki)
git merge origin/master          # Origin master (kendi fork'unuz)
git merge upstream/master        # Upstream master (orijinal repo)
```

**Pratik Örnek:**

```bash
# Durum: Feature branch'indesiniz
git checkout feature-branch

# Seçenek 1: Kendi fork'unuzdaki master'ı merge etmek
git fetch origin
git merge origin/master

# Seçenek 2: Orijinal repo'daki master'ı merge etmek (FORK İÇİN DOĞRU)
git fetch upstream
git merge upstream/master

# Seçenek 3: Local master'ı merge etmek
git merge master
# ⚠️ Dikkat: Local master güncel değilse eski değişiklikleri merge edersiniz!
```

**Önerilen Fork Workflow:**

```bash
# 1. Önce upstream master'ı local master'a çekin
git checkout master
git fetch upstream
git merge upstream/master
git push origin master         # Fork'unuzu da güncelleyin

# 2. Sonra feature branch'inizi güncelleyin
git checkout feature-branch
git merge master               # Artık local master güncel, güvenle merge edebilirsiniz
# VEYA doğrudan:
git merge upstream/master      # Direkt upstream'den de alabilirsiniz
```

**🎯 Fork'ta Remote Tracking Branch Kullanımı:**

```bash
# ⚠️ ÖNEMLİ: git merge HER ZAMAN bilgisayarınızdaki tracking branch'i kullanır!
# Remote'dan otomatik olarak ALMAZ, önce git fetch yapmalısınız!

# origin/master: Bilgisayarınızdaki origin/master tracking branch'i
git merge origin/master
# → LOCAL'deki origin/master tracking branch'ini merge eder
# → Bu tracking branch ancak "git fetch origin" ile güncellenir
# → Fetch yapmadıysanız ESKİ HALİNİ merge eder!

# upstream/master: Bilgisayarınızdaki upstream/master tracking branch'i
git merge upstream/master
# → LOCAL'deki upstream/master tracking branch'ini merge eder
# → Bu tracking branch ancak "git fetch upstream" ile güncellenir
# → Fetch yapmadıysanız ESKİ HALİNİ merge eder!

# master: Bilgisayarınızdaki local master branch'i
git merge master
# → LOCAL'deki master branch'ini merge eder
```

**Pratik Örnek - Fork Senaryosu:**

```bash
# Remote'larınızı görüntüleyin:
git remote -v
# origin    https://github.com/SIZIN_HESAP/repo.git      ← Fork'unuz
# upstream  https://github.com/ORIJINAL_HESAP/repo.git   ← Orijinal repo

# Durum: feature-branch'tesiniz, farklı kaynakları merge etmek istiyorsunuz

# Seçenek 1: Fork'unuzdaki master'ı merge etmek
git fetch origin                  # 1. Fork'tan güncel bilgileri AL (tracking branch'i güncelle)
git merge origin/master           # 2. Güncel tracking branch'i merge et
# → ŞİMDİ fork'unuzdaki değişiklikleri alırsınız (çünkü fetch yaptınız)
# → Fetch yapmadan merge etseydiniz ESKİ HALİ gelirdi!

# Seçenek 2: Orijinal repo'daki master'ı merge etmek (EN YAYGIN)
git fetch upstream                # 1. Orijinal repo'dan güncel bilgileri AL
git merge upstream/master         # 2. Güncel tracking branch'i merge et
# → ŞİMDİ orijinal projedeki güncellemeleri alırsınız (çünkü fetch yaptınız)

# Seçenek 3: Local master'ı merge etmek
git merge master                  # Local master'ı feature-branch'e merge et
# → Bilgisayarınızdaki master'ı alırsınız (güncel olmayabilir!)

# ❌ YANLIŞ: Fetch yapmadan merge etmek
git merge origin/master           # ESKİ tracking branch'i merge eder!
# → GitHub'daki güncel hali GELİMEZ, sadece daha önce fetch edilmiş eski hal gelir!

# ✅ DOĞRU: Önce fetch, sonra merge
git fetch origin                  # Tracking branch'i güncelle
git merge origin/master           # Şimdi güncel hali merge et
```

**Görsel Açıklama:**

```
┌─────────────────────────────────────────────────┐
│ GitHub - Orijinal Repo (upstream)              │
│ https://github.com/ORIJINAL_HESAP/repo.git     │
│                                                  │
│ master: A → B → C → D → E → F                   │
└─────────────────────────────────────────────────┘
              ↓
              ↓ git fetch upstream
              ↓
┌─────────────────────────────────────────────────┐
│ Local (Bilgisayarınız)                          │
│                                                  │
│ upstream/master: A → B → C → D → E → F  (tracking branch) │
│ origin/master: A → B → C → D            (tracking branch) │
│ master: A → B → C → D                    (local branch)    │
│ feature-branch: A → B → X → Y            (local branch)    │
└─────────────────────────────────────────────────┘
              ↓
              ↓ git push origin
              ↓
┌─────────────────────────────────────────────────┐
│ GitHub - Fork (origin)                          │
│ https://github.com/SIZIN_HESAP/repo.git        │
│                                                  │
│ master: A → B → C → D                           │
│ feature-branch: A → B → X → Y                   │
└─────────────────────────────────────────────────┘

# git merge origin/master    → Fork'taki D'ye kadar olan commitleri alır
# git merge upstream/master  → Orijinal'deki F'ye kadar olan commitleri alır
# git merge master           → Local'deki D'ye kadar olan commitleri alır
```

**Ne Zaman Hangisini Kullanmalı?**

| Durum | Komut | Ne Zaman? |
|-------|-------|-----------|
| Orijinal projedeki yeni özellikleri almak | `git merge upstream/master` | En yaygın - orijinal projeden güncelleme |
| Fork'ta başka branch'ten PR merge ettiniz | `git merge origin/master` | Fork'ta yaptığınız değişiklikleri almak |
| Local'de master'a commit attınız | `git merge master` | Nadiren - genellikle tavsiye edilmez |

**⚠️ ÖNEMLİ UYARI: Feature Branch'e Merge Yapınca Local Master Geride Kalır!**

```bash
# DİKKAT: Bu önemli bir detay!

# Durum: feature-branch'tesiniz, origin/master'ı merge ediyorsunuz
git checkout feature-branch
git fetch origin
git merge origin/master
# → origin/master'daki değişiklikler feature-branch'e gelir
# → AMA local master branch'iniz ESKİ HALDE KALIR!
# → Yani feature-branch artık local master'dan ÖNDE olur!

# Sonuç:
# feature-branch = eski durum + origin/master değişiklikleri (GÜNCEL)
# local master = eski durum (GERİDE KALDI)
```

**Görsel Örnek:**

```
Başlangıç:
───────────
origin/master (GitHub):     A → B → C → D → E → F
local master:                A → B → C → D
feature-branch:              A → B → C → D → X → Y

git fetch origin yapınca:
───────────────────────────
origin/master (tracking):    A → B → C → D → E → F  (güncellendi)
local master:                A → B → C → D          (değişmedi)
feature-branch:              A → B → C → D → X → Y  (değişmedi)

git merge origin/master yapınca (feature-branch'teyken):
──────────────────────────────────────────────────────
origin/master:               A → B → C → D → E → F
local master:                A → B → C → D          (HALA ESKİ!)
feature-branch:              A → B → C → D → E → F → X → Y  (ÖNDE!)
                                              ↑
                            origin/master'ı aldı ama local master almadı!
```

**Doğru İş Akışı - Local Master'ı da Güncelleme:**

```bash
# Seçenek 1: Önce local master'ı güncelle, sonra feature-branch'e merge et
git checkout master            # master'a geç
git fetch origin               # origin'den güncelle
git merge origin/master        # master'ı güncelle
git push origin master         # (opsiyonel) fork'a gönder

git checkout feature-branch    # feature'a geri dön
git merge master               # güncel master'ı feature'a merge et
# → Artık hem local master hem feature-branch güncel!

# Seçenek 2: Feature-branch'e direkt merge et (ama sonra master'ı da güncelle)
git checkout feature-branch
git fetch origin
git merge origin/master        # feature güncel
# → ŞİMDİ local master'ı da güncelleyin:
git checkout master
git merge origin/master        # master'ı da güncelle
git checkout feature-branch    # feature'a geri dön

# Seçenek 3: Feature-branch'i doğrudan upstream/master ile güncelle
git checkout feature-branch
git fetch upstream
git merge upstream/master      # Direkt orijinal repo'dan al
# → Local master hala eski kalır, sonra onu da güncelleyin
```

**Pratik Senaryo:**

```bash
# Başlangıç durumu:
git branch
#   master
# * feature-branch

# origin/master'dan güncelleme yap:
git fetch origin
git merge origin/master
# → feature-branch güncellendi
# → local master ESKİ KALDI!

# Şimdi local master'a geçip kontrol edin:
git checkout master
git log --oneline -5
# → origin/master'daki son commit'leri GÖREMEZSİNİZ!
# → Çünkü local master güncel değil!

# Local master'ı güncelleyin:
git merge origin/master
# → Şimdi local master da güncel!

# Veya pull kullanın:
git pull origin master
# → fetch + merge birlikte
```

**Özet - Hangi Branch'ler Güncellenir?**

| Komut | Feature-branch'teyken | Local Master | Origin/Master (GitHub) |
|-------|----------------------|--------------|------------------------|
| `git merge origin/master` | ✅ Güncellenir | ❌ ESKİ KALIR | Değişmez (zaten güncel) |
| `git pull origin master` | ✅ Güncellenir | ❌ ESKİ KALIR | Değişmez (zaten güncel) |
| `git merge master` | ✅ Local master merge edilir | ❌ Değişmez | Değişmez |

**Sonuç:** Feature-branch'teyken `git merge origin/master` yaparsanız, sadece feature-branch güncellenir, local master ESKİ KALIR. Bu yüzden local master'ı da ayrıca güncellemeniz gerekir! 🎯

### 6. Değişiklikleri Geri Alma

```bash
git checkout -- dosya.txt       # Dosyayı son commit'e geri al
git reset HEAD dosya.txt        # Staging'den çıkar
git revert commit-id            # Bir commit'i geri al
```

---

## GitHub ile Çalışma

### 1. GitHub'da Repository Oluşturma

1. GitHub.com'a gidin ve giriş yapın
2. Sağ üstteki **+** butonuna tıklayıp **New repository** seçin
3. Repository adı girin ve **Create repository** tıklayın

### 2. Yerel Projeyi GitHub'a Bağlama

```bash
git remote add origin https://github.com/kullanici_adi/repo_adi.git
git branch -M main
git push -u origin main
```

### 3. GitHub'dan Proje Kopyalama (Clone)

```bash
git clone https://github.com/kullanici_adi/repo_adi.git
```

### 4. Değişiklikleri GitHub'a Gönderme

```bash
git add .
git commit -m "Yeni özellik eklendi"
git push origin main
```

### 5. GitHub'daki Değişiklikleri Alma

```bash
git pull origin main
```

#### Git Pull Detaylı Açıklama

**`git pull` = `git fetch` + `git merge`**

`git pull` komutu iki işlemi birlikte yapar:

1. Remote'dan değişiklikleri indirir (fetch)
2. Otomatik olarak mevcut branch'inize merge eder

**Fork'ta `git pull origin master` vs `git pull upstream master` Farkı:**

```bash
# Remote'larınızı kontrol edin:
git remote -v

# origin    https://github.com/SIZIN_HESAP/repo.git      ← Kendi fork'unuz
# upstream  https://github.com/ORIJINAL_HESAP/repo.git   ← Orijinal repo
```

| Komut | Nereden Çeker? | Ne Zaman Kullanılır? |
|-------|---------------|---------------------|
| `git pull origin master` | **Kendi fork'unuzdan** | Fork'unuzdaki değişiklikleri almak için |
| `git pull upstream master` | **Orijinal repo'dan** | Orijinal projedeki yeni güncellemeleri almak için |

**Pratik Örnekler:**

**Senaryo 1: Orijinal Repo'daki Güncellemeleri Almak (En Yaygın)**

```bash
# Orijinal projeye yeni özellikler eklendi, bunları almak istiyorsunuz
git checkout master
git pull upstream master
# → Orijinal repo'nun master'ındaki değişiklikler local master'a gelir

# Fork'unuzu da güncelleyin
git push origin master
# → Artık hem local hem fork master'ınız güncel
```

**Senaryo 2: Kendi Fork'unuzdaki Değişiklikleri Almak**

```bash
# Başka bir bilgisayardan fork'unuza push yaptınız
# veya GitHub web arayüzünde değişiklik yaptınız
git checkout master
git pull origin master
# → Kendi fork'unuzdaki değişiklikler local'e gelir
```

**Senaryo 3: Takım Arkadaşınız Fork'unuza PR Gönderdi**

```bash
# PR'ı GitHub'da merge ettiniz, şimdi local'e çekmek istiyorsunuz
git checkout master
git pull origin master
# → Fork'unuzdaki merge edilmiş PR local'e gelir
```

**Görsel Karşılaştırma:**

```
Orijinal Repo (upstream)
    ↓ (git pull upstream master)
Local Master (bilgisayarınız)
    ↓ (git push origin master)
Fork (origin)

VEYA

Fork (origin)
    ↓ (git pull origin master)
Local Master (bilgisayarınız)
```

**Fork Workflow - Doğru Sıralama:**

```bash
# 1. Orijinal repo'dan en son değişiklikleri al
git pull upstream master

# 2. Kendi fork'unuzu güncelle
git push origin master

# 3. Feature branch'inizi güncelle
git checkout feature-branch
git merge master
```

**⚠️ Yaygın Hata:**

```bash
# ❌ YANLIŞ: Fork'ta çalışırken sadece origin'den çekmek
git pull origin master
# → Orijinal repo'daki yeni güncellemeleri ALAMAZSINIZ
# → Sadece kendi fork'unuzdaki değişiklikleri alırsınız

# ✅ DOĞRU: Önce upstream'den çek, sonra origin'e push et
git pull upstream master    # Orijinal repo'dan al
git push origin master      # Fork'unuza gönder
```

**Fetch vs Pull Farkı:**

```bash
# git fetch: Sadece indir, merge etme
git fetch upstream
git log upstream/master    # Nelerin geldiğini incele
git merge upstream/master  # Uygunsa merge et

# git pull: İndir ve otomatik merge et
git pull upstream master   # fetch + merge birlikte
```

**🔥 ÇOK ÖNEMLİ: Merge vs Pull Farkı - Neden Pull'da Değişiklik Geldi?**

**Yaşadığınız Durum:**

```bash
# 1. Önce merge denediniz
git merge upstream master
# Çıktı: Already up to date  (Herşey aynı)

# 2. Sonra pull denediniz
git pull upstream master
# Çıktı: Yeni değişiklikler geldi! 🤔
```

**Neden Böyle Oldu?**

#### Sebep 1: Fetch Yapmadınız (EN YAYGIN)

```bash
# git merge upstream/master → LOCAL'deki eski kopyayı merge eder
git merge upstream/master
# → Bilgisayarınızdaki upstream/master (eski olabilir)
# → GitHub'dan yeni değişiklikleri indirmez!
# → "Already up to date" der çünkü eski kopya zaten merge edilmiş

# git pull upstream master → Önce fetch yapar, sonra merge eder
git pull upstream master
# 1. Adım: git fetch upstream (GitHub'dan yeni değişiklikleri indir)
# 2. Adım: git merge upstream/master (şimdi güncel değişiklikleri merge et)
# → Yeni değişiklikler gelir!
```

**Görsel Açıklama:**

```
DURUM 1: git merge upstream/master (fetch yapmadan)
─────────────────────────────────────────────────
GitHub (upstream)
  master: A → B → C → D → E → F    (Yeni commitler var!)
            
Local bilgisayarınız
  upstream/master: A → B → C        (Eski kopya)
  your-branch: A → B → X → Y
  
git merge upstream/master yapınca:
  → C zaten var, yeni bir şey yok
  → "Already up to date" der
  

DURUM 2: git pull upstream master (fetch + merge)
─────────────────────────────────────────────────
GitHub (upstream)
  master: A → B → C → D → E → F
  
git fetch upstream yapılıyor...
Local bilgisayarınız
  upstream/master: A → B → C → D → E → F  (Yeni commitler indirildi!)
  your-branch: A → B → X → Y
  
git merge upstream/master yapılıyor...
  your-branch: A → B → C → D → E → F → X → Y  (Merge edildi!)
  → Yeni değişiklikler geldi! ✅
```

#### Sebep 2: Yanlış Syntax Kullandınız

```bash
# ❌ YANLIŞ: git merge upstream master (slash yok)
git merge upstream master
# → Git bunu "upstream" adında local branch ile "master" branch'ini merge et olarak anlayabilir
# → Veya hata verebilir

# ✅ DOĞRU: git merge upstream/master (slash ile)
git merge upstream/master
# → upstream remote'unun master branch'ini merge et
```

**🔥 ÇOK ÖNEMLİ: `upstream/master` vs `upstream master` Farkı**

Bu iki yazım şekli **AYNI DEĞİLDİR** ve komuta göre farklı anlamlar taşır!

**`upstream/master` (slash ile):**

- Remote tracking branch (uzak dal referansı)
- "upstream remote'unun master branch'i" anlamına gelir
- Git'e "hangi remote'un hangi branch'i" olduğunu söyler

**`upstream master` (boşlukla):**

- İki ayrı parametre
- "upstream adında bir remote" ve "master adında bir branch"
- Sadece bazı komutlarda bu şekilde kullanılır

**Komutlara Göre Kullanım:**

```bash
# ✅ MERGE için: upstream/master (slash ile)
git merge upstream/master      # DOĞRU
git merge upstream master      # YANLIŞ - hata verir veya yanlış anlaşılır

# ✅ PULL için: upstream master (boşlukla)
git pull upstream master       # DOĞRU
git pull upstream/master       # YANLIŞ - çalışmaz

# ✅ FETCH için: sadece remote adı
git fetch upstream             # Tüm branch'leri çeker
git fetch upstream master      # Sadece master branch'ini çeker

# ✅ PUSH için: origin master (boşlukla)
git push origin master         # DOĞRU
git push origin/master         # YANLIŞ

# ✅ LOG, DIFF gibi komutlar için: upstream/master (slash ile)
git log upstream/master
git diff upstream/master
git show upstream/master
```

**Detaylı Karşılaştırma:**

| Komut | Doğru Syntax | Yanlış Syntax | Açıklama |
|-------|-------------|---------------|----------|
| `git merge` | `git merge upstream/master` | ~~`git merge upstream master`~~ | Merge için slash gerekli |
| `git pull` | `git pull upstream master` | ~~`git pull upstream/master`~~ | Pull için boşluk gerekli |
| `git push` | `git push origin master` | ~~`git push origin/master`~~ | Push için boşluk gerekli |
| `git fetch` | `git fetch upstream` | `git fetch upstream master` | İkisi de çalışır |
| `git log` | `git log upstream/master` | - | Log için slash gerekli |
| `git diff` | `git diff upstream/master` | - | Diff için slash gerekli |
| `git rebase` | `git rebase upstream/master` | ~~`git rebase upstream master`~~ | Rebase için slash gerekli |

**Neden Bu Fark Var?**

```bash
# git pull özel bir komuttur ve şu syntax'ı kullanır:
git pull <remote> <branch>
# Örnek: git pull upstream master
# Anlamı: "upstream remote'undan master branch'ini pull et"

# Diğer komutlar remote tracking branch referansı bekler:
git merge <remote>/<branch>
# Örnek: git merge upstream/master
# Anlamı: "upstream/master adlı tracking branch'i merge et"
```

**Pratik Örnekler:**

```bash
# ✅ DOĞRU Kullanımlar:
git fetch upstream                    # Upstream'den tüm branch'leri çek
git merge upstream/master             # Tracking branch'i merge et
git pull upstream master              # Pull ile direkt upstream'den çek
git log upstream/master               # Upstream master'ın logunu gör
git diff master upstream/master       # Farkları karşılaştır

# ❌ YANLIŞ Kullanımlar:
git merge upstream master             # Hata verir veya yanlış yorumlanır
git pull upstream/master              # Çalışmaz
git push origin/master                # Çalışmaz
git log upstream master               # Yanlış yorumlanır
```

**Hafızada Tutma İpucu:**

```
PULL ve PUSH → boşlukla (git pull upstream master)
DİĞER HER ŞEY → slash ile (git merge upstream/master)
```

**Sizin Yaşadığınız Durum:**

```bash
# ❌ git merge upstream master → Muhtemelen "upstream" adında local branch aradı
git merge upstream master
# → "upstream" ve "master" diye iki local branch aradı
# → "Already up to date" dedi çünkü yanlış branch'leri kontrol etti

# ✅ git pull upstream master → Doğru syntax, önce fetch yaptı
git pull upstream master
# 1. git fetch upstream (GitHub'dan indir)
# 2. git merge upstream/master (tracking branch'i merge et)
# → Değişiklikler geldi!
```

**🎯 ÇOK ÖNEMLİ: `git merge upstream master` Git'e Ne Söyledi?**

```bash
# git merge upstream master yazınca Git şunu anladı:
git merge upstream master
# ↓
# "upstream" VE "master" adlı branch'leri MEVCUT BRANCH'e merge et (octopus merge)
# 
# Git iki LOCAL branch aradı:
# 1. "upstream" adında bir branch var mı?
# 2. "master" adında bir branch var mı?
# 
# Eğer "upstream" adlı branch YOKSA:
# → Hata verir veya sadece "master"ı merge etmeye çalışır
# → "Already up to date" diyebilir (master zaten mevcut branch'teyse)
#
# Eğer "upstream" adlı branch VARSA:
# → İkisini de MEVCUT branch'e merge eder

# ✅ DOĞRU: Aslında yapmak istediğiniz:
git merge upstream/master
# ↓
# "upstream" REMOTE'unun "master" BRANCH'ini mevcut branch'e merge et
# Bu, remote tracking branch referansıdır
```

**Git Merge Komutunun Mantığı:**

```bash
# TEK PARAMETRE: Bir branch'i mevcut branch'e merge et
git merge feature-branch           
# → "feature-branch"i MEVCUT branch'e merge eder

git merge upstream/master
# → "upstream/master"ı MEVCUT branch'e merge eder

# ÇOK PARAMETRE: Tüm branch'leri mevcut branch'e merge et (octopus merge)
git merge branch1 branch2          
# → "branch1" VE "branch2"yi MEVCUT branch'e merge eder

git merge upstream master
# → "upstream" VE "master"ı MEVCUT branch'e merge eder (eğer her ikisi de varsa)
# → Eğer "upstream" branch yoksa hata verir veya sadece "master"ı merge eder
```

**Örnek Senaryo:**

```bash
# Durum: feature-branch'tesiniz

# Senaryo 1: Tek parametre
git merge master
# → master'ı feature-branch'e merge eder
# → Sonuç: feature-branch = feature-branch + master

# Senaryo 2: İki parametre (octopus merge)
git merge dev hotfix
# → dev VE hotfix'i feature-branch'e merge eder
# → Sonuç: feature-branch = feature-branch + dev + hotfix

# Senaryo 3: Yanlış syntax (boşluk yerine slash)
git merge upstream master
# → "upstream" adlı local branch VE "master"ı feature-branch'e merge etmeye çalışır
# → Eğer "upstream" adlı local branch yoksa hata verir
```

**Neden "Already up to date" Dedi?**

```bash
# Muhtemelen şu durumlardan biri oldu:

# 1. "upstream" adlı local branch YOK, sadece master'ı kontrol etti
git merge upstream master
# → "upstream" local branch bulunamadı
# → Sadece "master" branch'ini kontrol etti
# → Eğer master zaten güncel veya mevcut branch'teyse "Already up to date" dedi

# 2. Mevcut branch zaten master'dı
git merge upstream master
# → master branch'teyken master'ı merge etmeye çalıştınız
# → "Already up to date" dedi (kendi kendine merge)
```

**Git Merge'in İki Farklı Kullanımı:**

```bash
# 1. LOCAL branch merge (tek isim veya iki isim)
git merge feature-branch           # "feature-branch" adlı local branch'i merge et
git merge branch1 branch2          # İki local branch'i merge et (ender kullanılır)

# 2. REMOTE TRACKING branch merge (slash ile)
git merge origin/master            # origin remote'unun master branch'ini merge et
git merge upstream/master          # upstream remote'unun master branch'ini merge et
```

**🔥 YANLIŞ KULLANIM: `git merge upstream/master feature-branch`**

```bash
# ❌ YANLIŞ ANLAMA: Bununla upstream/master'ı feature-branch'e merge etmiş olmazsınız!
git merge upstream/master feature-branch
# 
# Git bunu şöyle anlar:
# "upstream/master VE feature-branch'i MEVCUT BRANCH'e merge et"
# Yani iki branch'i aynı anda mevcut bulunduğunuz branch'e merge eder (octopus merge)
# 
# Bu genellikle istediğiniz şey DEĞİLDİR!

# ✅ DOĞRU: upstream/master'ı feature-branch'e merge etmek için:
git checkout feature-branch        # 1. Önce feature-branch'e geç
git merge upstream/master          # 2. Sonra upstream/master'ı merge et
```

**Git Merge Komutunun Parametreleri:**

```bash
# Standart kullanım (tek parametre):
git merge <branch-to-merge>
# → Belirtilen branch'i MEVCUT BRANCH'e merge eder

# Örnek:
git checkout feature-branch        # feature-branch'tesiniz
git merge upstream/master          # upstream/master'ı feature-branch'e merge eder

# Çok nadir kullanım (birden fazla parametre - octopus merge):
git merge branch1 branch2 branch3
# → Tüm branch'leri MEVCUT BRANCH'e merge eder
# → İki veya daha fazla branch'i aynı anda merge etmek için
```

**Sizin Sormak İstediğiniz:**

```bash
# SORU: upstream/master'ı feature-branch'e merge etmek istiyorum
# ❌ YANLIŞ:
git merge upstream/master feature-branch
# Bu, iki branch'i MEVCUT branch'e merge eder (neredeyseniz oraya)

# ✅ DOĞRU Yöntem 1: Checkout sonra merge
git checkout feature-branch        # feature-branch'e geç
git merge upstream/master          # upstream/master'ı merge et

# ✅ DOĞRU Yöntem 2: Pull kullanmak (eğer feature-branch'teyseniz)
git checkout feature-branch
git pull upstream master           # Fetch + merge
```

**Pratik Örnek:**

```bash
# Durum: main branch'tesiniz, upstream/master'ı feature-branch'e merge etmek istiyorsunuz

# ❌ YANLIŞ:
git merge upstream/master feature-branch
# → upstream/master VE feature-branch, ikisini de MAIN'e merge eder!
# → İstediğiniz şey bu değil!

# ✅ DOĞRU:
git checkout feature-branch        # feature-branch'e geç
git fetch upstream                 # upstream'i güncelle
git merge upstream/master          # upstream/master'ı feature-branch'e merge et

# Kısa yol:
git checkout feature-branch
git pull upstream master           # fetch + merge birlikte
```

**Octopus Merge (Çok Nadir):**

```bash
# Birden fazla branch'i aynı anda merge etmek:
git checkout main
git merge branch1 branch2 branch3
# → branch1, branch2 ve branch3'ü MAIN'e merge eder
# → Bu özel bir durumdur, normalde kullanılmaz
# → Sadece çok basit, çakışmasız merge'ler için önerilir

# Sizin yazdığınız komut bunu yapar:
git merge upstream/master feature-branch
# → upstream/master VE feature-branch'i MEVCUT branch'e merge eder
# → Bu muhtemelen istediğiniz şey değildir!
```

**Özet:**

| Ne İstiyorsunuz? | Yanlış Komut | Doğru Komut |
|-----------------|--------------|-------------|
| upstream/master'ı feature-branch'e merge et | ~~`git merge upstream/master feature-branch`~~ | `git checkout feature-branch` + `git merge upstream/master` |
| feature-branch'i master'a merge et | - | `git checkout master` + `git merge feature-branch` |
| İki branch'i mevcut branch'e merge et | `git merge branch1 branch2` | Genellikle önerilmez, ayrı ayrı yapın |

**Sonuç:** `git merge upstream/master feature-branch` komutu iki branch'i **MEVCUT** bulunduğunuz branch'e merge eder, upstream/master'ı feature-branch'e değil! Doğru yol: Önce `git checkout feature-branch`, sonra `git merge upstream/master`. 🎯

**Neden "Already up to date" Dedi?**

```bash
# Senaryo 1: "upstream" adında local branch YOK
git merge upstream master
# → Git "upstream" local branch'ini bulamadı
# → Veya sadece "master" branch'ini kendisiyle karşılaştırdı
# → "Already up to date" dedi

# Senaryo 2: "upstream" adında local branch VAR (nadiren)
git merge upstream master
# → Git iki local branch'i merge etmeye çalıştı
# → Eğer zaten güncel idilerse "Already up to date" dedi
```

**En Güvenli Yöntem:**

```bash
# Her zaman açık ve net olun:
git fetch upstream              # 1. Önce fetch
git merge upstream/master       # 2. Sonra slash ile merge

# Veya pull kullanıyorsanız:
git pull upstream master        # Direkt, ama boşlukla
```

**Doğru Kullanım:**

```bash
# Yöntem 1: Fetch sonra Merge (Kontrollü)
git fetch upstream              # 1. Önce indir
git log upstream/master         # 2. Nelerin geldiğini gör
git merge upstream/master       # 3. Uygunsa merge et

# Yöntem 2: Pull (Direkt)
git pull upstream master        # Direkt fetch + merge
```

**Pull Komutunun Arkasında Olan İşlemler:**

```bash
# git pull upstream master şunu yapar:
git fetch upstream              # 1. Remote'dan değişiklikleri indir
git merge upstream/master       # 2. Otomatik merge et

# Yani pull, fetch yapmadan merge etmenizin imkansız olduğunu garantiler!
```

**Pratik Tavsiye:**

```bash
# 🎯 En İyi Pratik: Her zaman fetch ile başlayın

# 1. Önce nelerin geldiğini kontrol edin
git fetch upstream
git log --oneline master..upstream/master
# → Hangi commitler var gösterir

# 2. Farkı görmek isterseniz
git diff master upstream/master

# 3. Uygunsa merge edin
git merge upstream/master

# VEYA hepsini tek seferde:
git pull upstream master        # Fetch + Merge
```

**Debug Komutu:**

```bash
# Remote branch'lerin son fetch tarihini görmek için
git fetch upstream              # Yeni değişiklikleri indir
git log --oneline -5 upstream/master   # Son 5 commit'i gör

# Local ile remote arasındaki farkı görmek için
git fetch upstream
git log --oneline master..upstream/master   # Upstream'de olup local'de olmayan commitler
```

**Özet:**

| Komut | Ne Yapar? | GitHub'dan İndirir mi? |
|-------|-----------|----------------------|
| `git merge upstream/master` | LOCAL'deki eski kopyayı merge eder | ❌ Hayır |
| `git fetch upstream` | Sadece indirir, merge etmez | ✅ Evet |
| `git pull upstream master` | Fetch + Merge (önce indirir, sonra merge eder) | ✅ Evet |

**Sonuç:** `git merge` sadece bilgisayarınızdaki mevcut verilerle çalışır. `git pull` önce GitHub'dan yeni verileri indirir (fetch), sonra merge eder. Bu yüzden pull'da değişiklikler geldi! 🎯

**Önerilen Güvenli Yöntem:**

```bash
# Önce fetch ile kontrol edin
git fetch upstream
git diff master upstream/master    # Farkları görün
git merge upstream/master          # Uygunsa merge edin

# Veya pull ile direkt
git pull upstream master           # Direkt fetch + merge
```

---

## 🔥 MERGE vs PULL: Çok Net Karşılaştırma

**Kafanız karışmasın! İşte net fark:**

### Pull = Fetch + Merge (Remote'dan indirir + birleştirir)

```bash
# git pull upstream master şunları yapar:
git pull upstream master
# ↓
# 1. ADIM: git fetch upstream (GitHub'dan son değişiklikleri İNDİR)
# 2. ADIM: git merge upstream/master (İndirilen değişiklikleri merge et)

# Yani pull MUTLAKA remote'dan indirir!
```

### Merge = Sadece yerel birleştirme (Remote'a bakmaz)

```bash
# git merge upstream/master şunu yapar:
git merge upstream/master
# ↓
# Sadece BİLGİSAYARINIZDAKİ upstream/master tracking branch'ini merge eder
# GitHub'dan HİÇBİR ŞEY indirmez!
# Eğer tracking branch eski ise, ESKİ HALİNİ merge eder!
```

**Görsel Açıklama:**

```
┌─────────────────────────────────────────┐
│ GitHub (Remote)                         │
│ upstream/master: A → B → C → D → E → F │ ← Yeni commitler var!
└─────────────────────────────────────────┘
           ↓
           │  git fetch ile indirilmeli
           │
           ↓ (fetch yapmadıysanız eski)
┌─────────────────────────────────────────┐
│ Local (Bilgisayarınız)                  │
│                                          │
│ upstream/master: A → B → C              │ ← Eski tracking branch
│ your-branch: A → B → X → Y              │
└─────────────────────────────────────────┘

# Senaryo 1: git merge upstream/master (fetch YAPMADAN)
git merge upstream/master
→ Sadece eski C'yi merge eder (D, E, F GELİMEZ!)
→ "Already up to date" der

# Senaryo 2: git pull upstream master
git pull upstream master
→ Önce fetch yapar (D, E, F'yi indirir)
→ Sonra merge eder (D, E, F GELİR!)
→ "Updated" der ve yeni commitler gelir
```

**Pratik Karşılaştırma:**

```bash
# DURUM: GitHub'da upstream master'da yeni commitler var (D, E, F)
# Siz son fetch'i 1 hafta önce yaptınız

# Yöntem 1: MERGE kullanmak (YANLIŞ - eski hali merge eder)
git merge upstream/master
# → Sadece 1 hafta ÖNCEKİ hali merge eder
# → Yeni D, E, F commitleri GELİMEZ!
# → "Already up to date" der (çünkü 1 hafta önceki zaten var)

# Yöntem 2: PULL kullanmak (DOĞRU - yenisini indirir)
git pull upstream master
# → Önce fetch yapar (D, E, F'yi indirir)
# → Sonra merge eder
# → Yeni commitler gelir!

# Yöntem 3: FETCH sonra MERGE (EN KONTROLLÜ)
git fetch upstream              # 1. Önce indir
git log upstream/master         # 2. Nelerin geldiğini gör
git merge upstream/master       # 3. Merge et
# → Kontrollü şekilde yeni commitler gelir
```

**Tablo Karşılaştırma:**

| Özellik | `git merge upstream/master` | `git pull upstream master` |
|---------|----------------------------|---------------------------|
| **Remote'a bakar mı?** | ❌ Hayır | ✅ Evet |
| **GitHub'dan indirir mi?** | ❌ Hayır | ✅ Evet (önce fetch yapar) |
| **Ne merge eder?** | Eski tracking branch'i | Yeni indirilen değişiklikleri |
| **Fetch gerekir mi?** | ✅ Evet (manuel yapmalısınız) | ❌ Hayır (otomatik yapar) |
| **Güvenli mi?** | ⚠️ Dikkat (eski olabilir) | ✅ Evet (her zaman güncel) |

**Ne Zaman Hangisini Kullanmalı?**

```bash
# Seçenek 1: PULL (Hızlı, tek komut)
git pull upstream master
# ✅ Avantaj: Tek komut, mutlaka güncel alır
# ❌ Dezavantaj: Ne geldiğini göremezsiniz, direkt merge edilir

# Seçenek 2: FETCH + MERGE (Kontrollü)
git fetch upstream              # 1. Önce indir
git log upstream/master -5      # 2. Nelerin geldiğini gör
git diff master upstream/master # 3. Farkları incele
git merge upstream/master       # 4. Uygunsa merge et
# ✅ Avantaj: Ne geldiğini görebilirsiniz
# ❌ Dezavantaj: Daha fazla komut

# Seçenek 3: SADECE MERGE (YANLIŞ!)
git merge upstream/master
# ❌ SORUN: Fetch yapmadıysanız eski hali merge eder!
# ❌ GitHub'daki yeni değişiklikler GELİMEZ!
```

**🎯 En Önemli Kural:**

```bash
# ❌ YANLIŞ DÜŞÜNCE:
# "git merge upstream/master yaparım, yeter"
git merge upstream/master
# → Eski tracking branch'i merge eder, yeni değişiklikler gelmez!

# ✅ DOĞRU DÜŞÜNCE:
# "Önce fetch ile güncelle, sonra merge et"
git fetch upstream           # 1. Yenileri indir
git merge upstream/master    # 2. Merge et

# VEYA tek komutla:
git pull upstream master     # Fetch + Merge birlikte
```

**Özet:**

| Amaç | Yanlış Yöntem | Doğru Yöntem |
|------|--------------|-------------|
| GitHub'daki güncellemeleri almak | ~~`git merge upstream/master`~~ | `git pull upstream master` |
| Fetch'ten sonra merge etmek | - | `git fetch` + `git merge upstream/master` |
| Kontrollü güncelleme | - | `git fetch` → incele → `git merge` |

**Sonuç:** Merge, remote'a bakmaz! Pull, remote'dan indirir + merge eder. Remote'dan güncelleme almak için ya `git pull` kullanın, ya da `git fetch` + `git merge` yapın. Sadece `git merge` ile remote'dan güncelleme gelmez! 🎯

---

## Fork ile Çalışma (Fork Workflow)

### Fork Nedir?

Fork, başka birinin projesini kendi GitHub hesabınıza kopyalamaktır. Orijinal projeye zarar vermeden kendi kopyanızda çalışabilirsiniz.

### Fork ile Çalışma Adımları

#### 1. Projeyi Fork'lama

1. GitHub'da fork etmek istediğiniz projeye gidin
2. Sağ üstteki **Fork** butonuna tıklayın
3. Proje sizin hesabınıza kopyalanır

#### 2. Fork'u Bilgisayarınıza Klonlama

```bash
git clone https://github.com/SIZIN_KULLANICI_ADINIZ/repo_adi.git
cd repo_adi
```

#### 3. Upstream (Orijinal Repo) Ekleme

```bash
# Orijinal repository'yi upstream olarak ekle
git remote add upstream https://github.com/ORIJINAL_KULLANICI/repo_adi.git

# Remote'ları kontrol et
git remote -v
# Çıktı:
# origin    https://github.com/SIZIN_KULLANICI_ADINIZ/repo_adi.git (fetch)
# origin    https://github.com/SIZIN_KULLANICI_ADINIZ/repo_adi.git (push)
# upstream  https://github.com/ORIJINAL_KULLANICI/repo_adi.git (fetch)
# upstream  https://github.com/ORIJINAL_KULLANICI/repo_adi.git (push)
```

#### 4. Fork'unuzu Orijinal Repo ile Senkronize Etme

**Önemli:** Fork'unuzdaki bir branch'i upstream'deki master/main ile güncellemek için:

```bash
# 1. Upstream'deki son değişiklikleri al (fetch)
git fetch upstream

# 2. Güncellemek istediğiniz branch'e geç
git checkout main   # veya güncellemek istediğiniz branch adı

# 3. Upstream'deki değişiklikleri kendi branch'inize merge et
git merge upstream/main

# Alternatif: Rebase kullanarak (daha temiz geçmiş)
git rebase upstream/main

# 4. Güncellenmiş branch'i kendi fork'unuza gönder
git push origin main
```

**Başka bir branch'i güncellemek için:**

```bash
# Örneğin "development" branch'ini güncellemek için
git checkout development
git fetch upstream
git merge upstream/main    # veya upstream/development (orijinal branch adına göre)
git push origin development
```

#### 5. Pull Request (PR) Gönderme

Değişikliklerinizi orijinal projeye katkı olarak göndermek için:

```bash
# 1. Yeni bir branch oluştur
git checkout -b yeni-ozellik

# 2. Değişikliklerinizi yapın ve commit edin
git add .
git commit -m "Açıklayıcı commit mesajı"

# 3. Kendi fork'unuza push edin
git push origin yeni-ozellik

# 4. GitHub'da fork'unuza gidin ve "Pull Request" oluşturun
```

### Fork Workflow - Tam Örnek

```bash
# İlk kurulum (bir kez yapılır)
git clone https://github.com/sizin-hesap/tools-abv-fork.git
cd tools-abv-fork
git remote add upstream https://github.com/orijinal-hesap/tools-abv-fork.git

# Her çalışma öncesi fork'u güncelle
git checkout main
git fetch upstream
git merge upstream/main
git push origin main

# Yeni özellik için branch oluştur
git checkout -b fix/bug-duzeltme

# Değişiklik yap
# ... dosyaları düzenle ...

# Commit ve push
git add .
git commit -m "Bug düzeltildi: kullanıcı giriş hatası"
git push origin fix/bug-duzeltme

# GitHub'da Pull Request oluştur
```

### Fork Çalışırken Dikkat Edilecekler

✅ **Upstream'i düzenli güncelleyin**: Çalışmaya başlamadan önce `git fetch upstream` yapın
✅ **Yeni branch kullanın**: Her yeni özellik için ayrı branch açın
✅ **Küçük PR'lar gönderin**: Büyük değişiklikleri küçük parçalara bölün
✅ **Açıklayıcı commit mesajları**: Ne değiştirdiğinizi net açıklayın

❌ **Main branch'te doğrudan çalışmayın**: Upstream ile senkronizasyon zorlaşır
❌ **Çok fazla değişiklik birden**: PR incelemesi zorlaşır

---

## Tipik İş Akışı (Workflow)

### Senaryo 1: Yeni Bir Özellik Ekleme

```bash
# 1. Yeni branch oluştur
git checkout -b yeni-ozellik

# 2. Değişiklik yap ve commit et
git add .
git commit -m "Yeni özellik eklendi"

# 3. Main branch'e geri dön
git checkout main

# 4. Yeni özelliği birleştir
git merge yeni-ozellik

# 5. GitHub'a gönder
git push origin main
```

### Senaryo 2: Takım ile Çalışma

```bash
# 1. Son değişiklikleri al
git pull origin main

# 2. Kendi branch'inde çalış
git checkout -b isim/ozellik-adi

# 3. Değişiklik yap ve commit et
git add .
git commit -m "Açıklayıcı mesaj"

# 4. Kendi branch'ini GitHub'a gönder
git push origin isim/ozellik-adi

# 5. GitHub'da Pull Request (PR) oluştur
```

---

## .gitignore Dosyası

Bazı dosyaların Git tarafından izlenmemesini isteyebilirsiniz (örn. şifreler, geçici dosyalar).

**Örnek `.gitignore` dosyası:**

```
# Node modülleri
node_modules/

# Python
__pycache__/
*.pyc
.env

# IDE
.vscode/
.idea/

# İşletim sistemi dosyaları
.DS_Store
Thumbs.db

# Log dosyaları
*.log
```

---

## Sık Karşılaşılan Sorunlar ve Çözümleri

### Problem 1: "Conflict" (Çakışma)

```bash
# Çakışan dosyaları manuel düzelt
# Sonra:
git add .
git commit -m "Conflict çözüldü"
```

### Problem 2: Yanlış Commit Mesajı

```bash
git commit --amend -m "Düzeltilmiş mesaj"
```

### Problem 3: Son Commit'i Geri Alma

```bash
git reset --soft HEAD~1      # Değişiklikleri koru
git reset --hard HEAD~1      # Değişiklikleri tamamen sil (DİKKAT!)
```

### Problem 4: Remote URL Değiştirme

```bash
git remote set-url origin https://github.com/yeni-kullanici/yeni-repo.git
```

---

## Önemli İpuçları

✅ **Sık commit yapın**: Her mantıklı değişiklikten sonra commit atın
✅ **Açıklayıcı mesajlar yazın**: "fix" yerine "Giriş sayfası hata düzeltildi" yazın
✅ **Branch kullanın**: Main branch'i direkt değiştirmeyin
✅ **Pull yapmayı unutmayın**: Çalışmaya başlamadan önce `git pull` yapın
✅ **.gitignore kullanın**: Hassas bilgileri paylaşmayın

❌ **Büyük dosyalar eklemeyin**: GitHub 100MB üzeri dosyalara izin vermez
❌ **Şifreleri commit etmeyin**: `.env` dosyalarını `.gitignore`'a ekleyin
❌ **Main branch'te deneme yapmayın**: Her zaman yeni branch oluşturun

---

## Hızlı Referans Tablosu

| Komut | Ne Yapar? |
|-------|-----------|
| `git init` | Yeni repository oluştur |
| `git clone [url]` | Repository'yi kopyala |
| `git add .` | Tüm değişiklikleri hazırla |
| `git commit -m "mesaj"` | Değişiklikleri kaydet |
| `git push` | GitHub'a gönder |
| `git pull` | GitHub'dan al |
| `git status` | Durum kontrolü |
| `git log` | Commit geçmişi |
| `git branch` | Branch listesi |
| `git checkout [branch]` | Branch değiştir |
| `git merge [branch]` | Branch birleştir |

---

## Pratik Alıştırma

1. GitHub'da yeni bir repository oluşturun
2. Yerel bilgisayarınızda bir klasör açın ve `git init` yapın
3. Bir `README.md` dosyası oluşturun
4. `git add .` ve `git commit -m "İlk commit"` yapın
5. Repository'yi GitHub'a push edin
6. Yeni bir branch oluşturun ve değişiklik yapın
7. Main branch'e merge edin

---

## Ek Kaynaklar

- **Git Resmi Dökümantasyonu**: <https://git-scm.com/doc>
- **GitHub Guides**: <https://guides.github.com/>
- **Git Görselleştirme**: <https://git-school.github.io/visualizing-git/>
- **Interaktif Git Öğren**: <https://learngitbranching.js.org/>

---

## Sonuç

Git ve GitHub, modern yazılım geliştirmede vazgeçilmez araçlardır. Bu temel komutları öğrendikten sonra:

- Projelerinizi güvenle yönetebilirsiniz
- Takım çalışmasına kolayca adapte olabilirsiniz
- Kod değişikliklerinizi takip edebilirsiniz
- Hata yaptığınızda geriye dönebilirsiniz

**Bol pratik yapın ve hatalardan korkmayın - Git her zaman arkanızda!** 🚀
