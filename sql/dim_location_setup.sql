
INSERT INTO public.dim_location (
    location_code,
    location_name,
    administrative_level,
    province_name,
    latitude,
    longitude,
    timezone
)
VALUES
    ('ID-BKY', 'Bengkayang', 'Kabupaten', 'Kalimantan Barat',  0.8200, 109.4770, 'Asia/Jakarta'),
    ('ID-KHU', 'Kapuas Hulu', 'Kabupaten', 'Kalimantan Barat',  0.8470, 112.9320, 'Asia/Jakarta'),
    ('ID-KKU', 'Kayong Utara', 'Kabupaten', 'Kalimantan Barat', -1.2500, 109.9500, 'Asia/Jakarta'),
    ('ID-KTP', 'Ketapang', 'Kabupaten', 'Kalimantan Barat', -1.8500, 109.9830, 'Asia/Jakarta'),
    ('ID-KKR', 'Kubu Raya', 'Kabupaten', 'Kalimantan Barat', -0.0700, 109.3500, 'Asia/Jakarta'),
    ('ID-LDK', 'Landak', 'Kabupaten', 'Kalimantan Barat',  0.3900, 109.9500, 'Asia/Jakarta'),
    ('ID-MLW', 'Melawi', 'Kabupaten', 'Kalimantan Barat', -0.3500, 111.7500, 'Asia/Jakarta'),
    ('ID-MPW', 'Mempawah', 'Kabupaten', 'Kalimantan Barat',  0.3500, 108.9600, 'Asia/Jakarta'),
    ('ID-SBS', 'Sambas', 'Kabupaten', 'Kalimantan Barat',  1.3600, 109.3000, 'Asia/Jakarta'),
    ('ID-SGU', 'Sanggau', 'Kabupaten', 'Kalimantan Barat',  0.1200, 110.6000, 'Asia/Jakarta'),
    ('ID-SKD', 'Sekadau', 'Kabupaten', 'Kalimantan Barat', -0.0300, 110.9500, 'Asia/Jakarta'),
    ('ID-STG', 'Sintang', 'Kabupaten', 'Kalimantan Barat',  0.0700, 111.5000, 'Asia/Jakarta'),
    ('ID-PNK', 'Pontianak', 'Kota', 'Kalimantan Barat', -0.0263, 109.3425, 'Asia/Jakarta'),
    ('ID-SKW', 'Singkawang', 'Kota', 'Kalimantan Barat',  0.9060, 108.9870, 'Asia/Jakarta')
ON CONFLICT (location_code) DO NOTHING;
