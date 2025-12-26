USE gudianmusic;
SET SESSION sql_mode = '';

-- 1. 示范音乐 3 首
INSERT INTO music (title, artist, dynasty, genre, cover, description) VALUES
('高山流水', '管', '唐', 'guqin', 'image/gsls.jfif', '古琴名曲'),
('十面埋伏', '刘', '明', 'pipa', 'image/smmf.jfif', '琵琶武曲'),
('春江花月夜', '王', '清', 'pipa', 'image/cjhyy.jfif', '琵琶文曲');

-- 2. 示范弹幕 1 条（非用户）
INSERT INTO danmus (text, position, speed, is_user) VALUES
('礼乐之邦，华夏正音', 3, 30.0, 0);