-- İçerik Özet Agent — taslaklar tablosu
-- Her pipeline turunda yeni satırlar. Gelecekte feedback loop için genişletilebilir.

CREATE TABLE IF NOT EXISTS taslaklar (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    tarih              TEXT NOT NULL,                   -- YYYY-MM-DD
    baslik             TEXT NOT NULL,
    link               TEXT NOT NULL,
    kaynak             TEXT NOT NULL,
    ozet               TEXT NOT NULL,                   -- Claude çıktısı
    teknik_dogruluk    INTEGER NOT NULL,                -- 0-10
    turkce_kalitesi    INTEGER NOT NULL,                -- 0-10
    ozet_netligi       INTEGER NOT NULL,                -- 0-10
    ortalama           REAL NOT NULL,                   -- üç puanın ortalaması
    model              TEXT NOT NULL,                   -- örn. claude-sonnet-4-5
    input_tokens       INTEGER DEFAULT 0,
    output_tokens      INTEGER DEFAULT 0,
    yayinlandi         INTEGER DEFAULT 0,               -- 0/1 — eşik geçti mi
    olusturulma        TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Sorgu performansı için basit index'ler
CREATE INDEX IF NOT EXISTS idx_tarih ON taslaklar(tarih);
CREATE INDEX IF NOT EXISTS idx_yayin ON taslaklar(yayinlandi);
CREATE INDEX IF NOT EXISTS idx_ort ON taslaklar(ortalama);

-- Gelecekteki feedback loop için — şu an boş, ilerde okuyucu tepkileri ile doldurulur
CREATE TABLE IF NOT EXISTS geri_bildirim (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    taslak_id    INTEGER NOT NULL,
    tepki        TEXT NOT NULL,              -- 'begen', 'gec', 'bozuk', 'fazla-teknik' vb.
    ek_not       TEXT,
    tarih        TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (taslak_id) REFERENCES taslaklar(id)
);
