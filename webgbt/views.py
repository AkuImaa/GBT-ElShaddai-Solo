from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .models import JadwalIbadah, JadwalPelayanan, WartaGereja, Renungan, Komentar, Simpan, Suka, DataPelayanAltar, Baptis, PelayanAltar
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import textwrap
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import cm

# Create your views here.
def home(request):
    context = {
        'renungan': Renungan.objects.all().order_by('-id')[:3],
        'wartagereja': WartaGereja.objects.all().order_by('-id')[:5],
        'jadwalibadah': JadwalIbadah.objects.all().order_by('-id')[:3],
        'jadwalpelayanan': JadwalPelayanan.objects.all().order_by('-id')[:3],
        'suka': Suka.objects.all(),
        'simpan': Simpan.objects.all(),
        'komentar': Komentar.objects.all(),
    }
    return render(request, 'dashboard.html', context)
 
 
 #lihat sejarah greja
@login_required(login_url='login')
def sejarah(request):
    return render(request, 'sejarah.html')
    
#views Renungan
#login_required(login_url='login')
def renungan(request, id):
    data = get_object_or_404(Renungan, id=id)
    content_type = ContentType.objects.get_for_model(Renungan)
    
    komentar = Komentar.objects.filter(
    content_type=content_type,
    object_id=data.id,
    parent__isnull=True
).prefetch_related("balasan").order_by("-dibuat_pada")

    total_like = Suka.objects.filter(
        content_type=content_type,
        object_id=data.id
    ).count()

    user_sudah_like = False

    if request.user.is_authenticated:
        user_sudah_like = Suka.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=data.id
        ).exists()

    context = {
        'data': data,
        'total_like': total_like,
        'user_sudah_like': user_sudah_like,
        'komentar': komentar,
    }

    return render(request, 'renungan.html', context)

@login_required(login_url='login')
def renungan_list(request):
    data_renungan = Renungan.objects.all().order_by('-id')
    
    paginator = Paginator(data_renungan, 5)  # 5 konten per halaman

    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'renungan_list.html', { 'page_obj': page_obj})

#Views JadwalIbadah
#login_required(login_url='login')
def jadwalibadah(request, id):
    data = get_object_or_404(JadwalIbadah, id=id)
    content_type = ContentType.objects.get_for_model(JadwalIbadah)
    
    komentar = Komentar.objects.filter(
    content_type=content_type,
    object_id=data.id,
    parent__isnull=True
).prefetch_related("balasan").order_by("-dibuat_pada")

    total_like = Suka.objects.filter(
        content_type=content_type,
        object_id=data.id
    ).count()

    user_sudah_like = False

    if request.user.is_authenticated:
        user_sudah_like = Suka.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=data.id
        ).exists()

    context = {
        'data': data,
        'total_like': total_like,
        'user_sudah_like': user_sudah_like,
        'komentar': komentar,
    }
    return render(request, 'jadwal_ibadah.html', context)

@login_required(login_url='login')
def jadwal_ibadahlist(request):
    data_jadwalibadah = JadwalIbadah.objects.all().order_by('-id')
    
    paginator = Paginator(data_jadwalibadah, 5)  # 5 konten per halaman

    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'jadwal_ibadahlist.html', { 'page_obj': page_obj})

#Views JadwalPelayanan
#login_required(login_url='login')
def jadwalpelayanan(request, id):
    data = get_object_or_404(JadwalPelayanan, id=id)
    content_type = ContentType.objects.get_for_model(JadwalPelayanan)
    
    komentar = Komentar.objects.filter(
    content_type=content_type,
    object_id=data.id,
    parent__isnull=True
).prefetch_related("balasan").order_by("-dibuat_pada")

    total_like = Suka.objects.filter(
        content_type=content_type,
        object_id=data.id
    ).count()

    user_sudah_like = False

    if request.user.is_authenticated:
        user_sudah_like = Suka.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=data.id
        ).exists()

    context = {
        'data': data,
        'total_like': total_like,
        'user_sudah_like': user_sudah_like,
        'komentar': komentar,
    }
    return render(request, 'jadwal_pelayanan.html', context)
 
@login_required(login_url='login') 
def jadwal_pelayananlist(request):
    data_jadwalpelayanan = JadwalPelayanan.objects.all().order_by('-id')
    
    paginator = Paginator(data_jadwalpelayanan, 5)  # 5 konten per halaman

    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'jadwal_pelayananlist.html', { 'page_obj': page_obj})
    
#Views Warta Gereja
#login_required(login_url='login')
def wartagereja(request, id):
    data = get_object_or_404(WartaGereja, id=id)
    content_type = ContentType.objects.get_for_model(WartaGereja)
    
    komentar = Komentar.objects.filter(
    content_type=content_type,
    object_id=data.id,
    parent__isnull=True
).prefetch_related("balasan").order_by("-dibuat_pada")

    total_like = Suka.objects.filter(
        content_type=content_type,
        object_id=data.id
    ).count()

    user_sudah_like = False

    if request.user.is_authenticated:
        user_sudah_like = Suka.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=data.id
        ).exists()

    context = {
        'data': data,
        'total_like': total_like,
        'user_sudah_like': user_sudah_like,
        'komentar': komentar,
    }
    return render(request, 'warta_gereja.html', context)
    
@login_required(login_url='login')    
def warta_gerejalist(request):
    data_wartagereja = WartaGereja.objects.all().order_by('-id')
    
    paginator = Paginator(data_wartagereja, 5)  # 5 konten per halaman

    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'warta_gerejalist.html', { 'page_obj': page_obj})
    
#LoginUsers
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            messages.success(
                request,
                'Selamat datang {user.username}, login berhasil!'
            )
            return redirect('dashboard')
        else:
            messages.error(
                request,
                'Username atau password salah!'
            )
    return render(request, 'login.html')
    
def dashboard(request):
    return render(request, 'dashboard.html')

#LogoutUsers
def logout_user(request):
    logout(request)
    messages.success(
        request,
        'Berhasil logout'
    )
    return redirect('login')

#Komentar
@login_required(login_url='login')
def komentar(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":

        isi = request.POST.get("isi")
        parent_id = request.POST.get("parent_id")
        object_id = request.POST.get("object_id")
        model = request.POST.get("model")

        model_map = {
            "renungan": Renungan,
            "warta": WartaGereja,
            "ibadah": JadwalIbadah,
            "pelayanan": JadwalPelayanan,
        }

        if model not in model_map:
            return redirect("/")

        model_class = model_map[model]

        objek = get_object_or_404(
            model_class,
            id=object_id
        )

        parent = None

        if parent_id:
            parent = get_object_or_404(
                Komentar,
                id=parent_id
            )

        Komentar.objects.create(
            user=request.user,
            isi=isi,
            parent=parent,
            content_type=ContentType.objects.get_for_model(model_class),
            object_id=objek.id
        )

    return redirect(request.META.get("HTTP_REFERER"))
#Suka
@login_required(login_url='login')
def toggle_like(request, model_name, id):

    if not request.user.is_authenticated:
        return redirect('login')

    # Ambil model secara dinamis
    model = apps.get_model('webgbt', model_name)

    obj = get_object_or_404(model, id=id)

    content_type = ContentType.objects.get_for_model(model)

    like = Suka.objects.filter(
        user=request.user,
        content_type=content_type,
        object_id=obj.id
    ).first()

    # Toggle Like
    if like:
        like.delete()
    else:
        Suka.objects.create(
            user=request.user,
            content_type=content_type,
            object_id=obj.id
        )

    return redirect(request.META.get('HTTP_REFERER'))

#baptis
@login_required(login_url='login')
def baptis(request):

    if request.method == 'POST':

        Baptis.objects.create(
            nama=request.POST['nama'],
            tempat_lahir=request.POST['tempat_lahir'],
            tanggal_lahir=request.POST['tanggal_lahir'],
            jenis_kelamin=request.POST['jenis_kelamin'],
            alamat=request.POST['alamat'],
            no_hp=request.POST['no_hp'],
            status=request.POST['status_baptis'],
        )

        return redirect('jadwal_baptis')

    data = Baptis.objects.order_by('-id')

    return render(
        request,
        'baptis.html',
        {
            'data': data
        }
    )

@login_required(login_url='login')
def download_baptis(request, id):
    data = get_object_or_404(Baptis, id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Form_Baptis.pdf"'

    p = canvas.Canvas(response)
    width, height = 595, 842  # ukuran A4

    # ====================================================
    # BORDER HALAMAN
    # ====================================================
    p.setStrokeColor(HexColor("#1E3A8A"))
    p.setLineWidth(2)
    p.rect(20, 20, width-40, height-40)

    # ====================================================
    # HEADER
    # ====================================================
    p.setFillColor(HexColor("#1E3A8A"))
    p.rect(20, height-90, width-40, 70, fill=1)

    p.setFillColor(white)
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width/2, height-50, "FORM PENDAFTARAN BAPTIS")

    p.setFont("Helvetica", 11)
    p.drawCentredString(width/2, height-70, "Gereja Bethel Elshaddai Solo")

    # ====================================================
    # GARIS PEMBATAS
    # ====================================================
    p.setStrokeColor(HexColor("#D1D5DB"))
    p.line(40, height-110, width-40, height-110)

    # ====================================================
    # IDENTITAS
    # ====================================================
    y = height - 150

    p.setFillColor(black)
    p.setFont("Helvetica-Bold", 13)
    p.drawString(50, y, "DATA PESERTA BAPTIS")

    y -= 30

    p.setFont("Helvetica", 11)

    data_form = [
        ("Nama", data.nama),
        ("Tempat Lahir", data.tempat_lahir),
        ("Tanggal Lahir", str(data.tanggal_lahir)),
        ("Jenis Kelamin", data.jenis_kelamin),
        ("Alamat", data.alamat),
        ("Nomor HP", data.no_hp),
    ]

    for label, value in data_form:

        # kotak label
        p.setFillColor(HexColor("#F3F4F6"))
        p.rect(50, y-5, 140, 22, fill=1, stroke=0)

        p.setFillColor(black)
        p.setFont("Helvetica-Bold", 11)
        p.drawString(55, y+2, label)

        p.setFont("Helvetica", 11)
        p.drawString(205, y+2, f": {value}")

        y -= 35

    # ====================================================
    # KETERANGAN
    # ====================================================
    y -= 15

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Keterangan")

    y -= 20

    p.setFont("Helvetica", 10)
    p.drawString(55, y, "Formulir ini merupakan bukti pendaftaran baptis.")

    # ====================================================
    # TANDA TANGAN
    # ====================================================
    y -= 80

    p.line(70, y, 200, y)
    p.line(360, y, 490, y)

    p.setFont("Helvetica", 10)
    p.drawCentredString(135, y-15, "Peserta Baptis")
    p.drawCentredString(425, y-15, "Petugas Gereja")

    # ====================================================
    # AYAT ALKITAB
    # ====================================================
    footer = (
        "Matius 28:19-20\n"
        "Karena itu pergilah, jadikanlah semua bangsa murid-Ku "
        "dan baptislah mereka dalam nama Bapa dan Anak dan Roh Kudus, "
        "dan ajarlah mereka melakukan segala sesuatu yang telah "
        "Kuperintahkan kepadamu. Dan ketahuilah, Aku menyertai kamu "
        "senantiasa sampai kepada akhir zaman."
    )

    p.setStrokeColor(HexColor("#1E3A8A"))
    p.rect(40, 40, width-80, 90)

    text = p.beginText(50, 110)
    text.setFont("Helvetica-Oblique", 9)
    text.setLeading(12)

    for line in textwrap.wrap(footer, width=90):
        text.textLine(line)

    p.drawText(text)

    p.save()
    return response
    
#Jadwal Baptis
def jadwal_baptis(request):
    data = Baptis.objects.exclude(
        status='draft'
    ).order_by('-id')

    return render(request, 'jadwal_baptis.html', {
        'data': data
    })
def lihat_baptis(request):

    total = Baptis.objects.count()

    belum_baptis = Baptis.objects.filter(
        status="Belum Pernah Baptis"
    ).count()

    pindahan = Baptis.objects.filter(
        status="Pindahan Gereja"
    ).count()

    peserta_jadwal = Baptis.objects.exclude(
        jadwal_baptis__isnull=True
    ).order_by('-id')   # atau -created_at

    context = {
        'total': total,
        'belum_baptis': belum_baptis,
        'pindahan': pindahan,
        'peserta_jadwal': peserta_jadwal,
    }

    return render(request, 'lihatbaptis.html', context)
#daftar pelayan altar
#login_required(login_url='login')
def pelayan_altar(request):

    if request.method == 'POST':

        data = PelayanAltar.objects.create(
            nama=request.POST['nama'],
            tempat_lahir=request.POST['tempat_lahir'],
            tanggal_lahir=request.POST['tanggal_lahir'],
            jenis_kelamin=request.POST['jenis_kelamin'],
            alamat=request.POST['alamat'],
            no_hp=request.POST['no_hp'],
            bidang_pelayanan=request.POST['bidang_pelayanan'],
            pengalaman=request.POST.get('pengalaman'),
        )

        return redirect('download_pelayan', data.id)

    return render(request, 'joinpelayanan.html')

@login_required(login_url='login')
def download_pelayan(request, id):

    data = get_object_or_404(PelayanAltar, id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Form_pelayanaltar.pdf"'

    p = canvas.Canvas(response)
    width, height = 595, 842  # ukuran A4

    # ====================================================
    # BORDER HALAMAN
    # ====================================================
    p.setStrokeColor(HexColor("#1E3A8A"))
    p.setLineWidth(2)
    p.rect(20, 20, width-40, height-40)

    # ====================================================
    # HEADER
    # ====================================================
    p.setFillColor(HexColor("#1E3A8A"))
    p.rect(20, height-90, width-40, 70, fill=1)

    p.setFillColor(white)
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width/2, height-50, "FORM DAFTAR PELAYAN ALTAR")

    p.setFont("Helvetica", 11)
    p.drawCentredString(width/2, height-70, "Gereja Bethel Elshaddai Solo")

    # ====================================================
    # GARIS PEMBATAS
    # ====================================================
    p.setStrokeColor(HexColor("#D1D5DB"))
    p.line(40, height-110, width-40, height-110)

    # ====================================================
    # IDENTITAS
    # ====================================================
    y = height - 150

    p.setFillColor(black)
    p.setFont("Helvetica-Bold", 13)
    p.drawString(50, y, "DATA CALON PELAYAN ALTAR")

    y -= 30

    p.setFont("Helvetica", 11)

    data_form = [
        ("Nama", data.nama),
        ("Tempat Lahir", data.tempat_lahir),
        ("Tanggal Lahir", str(data.tanggal_lahir)),
        ("Jenis Kelamin", data.jenis_kelamin),
        ("Alamat", data.alamat),
        ("Nomor HP", data.no_hp),
        ("Bidang Pelayanan", data.bidang_pelayanan),
        ("Pengalaman Pelayanan", data.pengalaman),
    ]

    for label, value in data_form:

        # kotak label
        p.setFillColor(HexColor("#F3F4F6"))
        p.rect(50, y-5, 140, 22, fill=1, stroke=0)

        p.setFillColor(black)
        p.setFont("Helvetica-Bold", 11)
        p.drawString(55, y+2, label)

        p.setFont("Helvetica", 11)
        p.drawString(205, y+2, f": {value}")

        y -= 35

    # ====================================================
    # KETERANGAN
    # ====================================================
    y -= 15

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Keterangan")

    y -= 20

    p.setFont("Helvetica", 10)
    p.drawString(55, y, "Formulir ini merupakan bukti pendaftaran pelayan altar.")

    # ====================================================
    # TANDA TANGAN
    # ====================================================
    y -= 80

    p.line(70, y, 200, y)
    p.line(360, y, 490, y)

    p.setFont("Helvetica", 10)
    p.drawCentredString(135, y-15, "Calon Pelayan")
    p.drawCentredString(425, y-15, "Petugas Gereja")

    # ====================================================
    # AYAT ALKITAB
    # ====================================================
    footer = (
        "Matius 28:19-20\n"
        "Karena itu pergilah, jadikanlah semua bangsa murid-Ku "
        "dan baptislah mereka dalam nama Bapa dan Anak dan Roh Kudus, "
        "dan ajarlah mereka melakukan segala sesuatu yang telah "
        "Kuperintahkan kepadamu. Dan ketahuilah, Aku menyertai kamu "
        "senantiasa sampai kepada akhir zaman."
    )

    p.setStrokeColor(HexColor("#1E3A8A"))
    p.rect(40, 40, width-80, 90)

    text = p.beginText(50, 110)
    text.setFont("Helvetica-Oblique", 9)
    text.setLeading(12)

    for line in textwrap.wrap(footer, width=90):
        text.textLine(line)

    p.drawText(text)

    p.save()
    return response
    
#Daftar akun 
def daftar(request):

    if request.method == 'POST':

        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:

            messages.error(request, 'Password tidak sama!')
            return redirect('daftar')

        if User.objects.filter(username=username).exists():

            messages.error(request, 'Username sudah digunakan!')
            return redirect('daftar')

        User.objects.create_user(
            username=username,
            password=password1
        )

        messages.success(request, 'Akun berhasil dibuat!')
        return redirect('login')

    return render(request, 'daftar.html')

#Lupa Password
def lupa_password(request):

    if request.method == "POST":

        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # cek username
        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            messages.error(request, "Username tidak ditemukan")
            return redirect('lupa_password')

        # cek password sama
        if password1 != password2:
            messages.error(request, "Konfirmasi password tidak cocok")
            return redirect('lupa_password')

        # ganti password
        user.set_password(password1)
        user.save()

        messages.success(request, "Password berhasil diganti")
        return redirect('login')

    return render(request, 'lupa.html')

#Data Pelayan Altar
def data_pelayan(request):

    pelayanan = {}

    bidang_list = [
        'Worship Leader',
        'Pembawa Firman',
        'Singer',
        'Music',
        'Multimedia',
        'Usher',
        'Tamborin',
        'Sekolah Minggu'
    ]

    for bidang in bidang_list:

        pelayanan[bidang] = DataPelayanAltar.objects.filter(
            bidang_pelayanan=bidang
        )

    context = {
        'pelayanan': pelayanan
    }

    return render(request, 'data_pelayan.html', context)

#simpan kontern
@login_required
def simpan(request):
    if request.method == "POST":

        content_type_name = request.POST.get("content_type")
        object_id = request.POST.get("object_id")

        model_map = {
            "renungan": Renungan,
            "wartagereja": WartaGereja,
            "jadwalibadah": JadwalIbadah,
            "jadwalpelayanan": JadwalPelayanan,
        }

        model = model_map.get(content_type_name)

        if model is None:
            return redirect(request.META.get("HTTP_REFERER", "/"))

        obj = model.objects.get(id=object_id)

        content_type = ContentType.objects.get_for_model(model)

        Simpan.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj.id
        )

    return redirect(request.META.get("HTTP_REFERER", "/"))

#simpan kontern
@login_required   
def daftar_simpanan(request):
    simpanan = Simpan.objects.filter(
        user=request.user
    ).select_related('content_type').order_by('-disimpan_pada')

    return render(request, 'daftar_simpanan.html', {
        'simpanan': simpanan
    })
    
def hapus_simpanan(request, id):
    simpan = get_object_or_404(
        Simpan,
        id=id,
        user=request.user
    )

    simpan.delete()

    return redirect('simpanan')