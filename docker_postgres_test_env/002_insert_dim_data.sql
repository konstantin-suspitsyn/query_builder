/**
*   Вставляем данные
*/

INSERT INTO public.dim_item (sk_item_id, bk_item_id, bk_item_name, bk_combined_map) VALUES
( 1, 'ID_001', 'Atomic Heart', 'Action'),
( 2, 'ID_002', 'Doom X', 'Action'),
( 3, 'ID_003', 'Guardians of G', 'Action'),
( 4, 'ID_004', 'Uncharted', 'Action'),
( 5, 'ID_005', 'Until Dawn', 'Interactive movies'),
( 6, 'ID_006', 'Become Human', 'Interactive movies'),
( 7, 'ID_007', 'Beyond: Two Souls', 'Interactive movies'),
( 8, 'ID_008', 'The Wolf Among Us', 'Interactive movies'),
( 9, 'ID_009', 'Witcher III', 'RPG'),
(10, 'ID_010', 'Pathfinder', 'RPG'),
(11, 'ID_011', 'GTA', 'RPG'),
(12, 'ID_012', 'Dark Souls', 'Horror'),
(13, 'ID_013', 'Silent Hill', 'Horror'),
(14, 'ID_014', 'Alan Wake', 'Horror'),
(15, 'ID_015', 'Resident Evil', 'Horror'),
(16, 'ID_016', 'Dead Stranding', 'Interactive movies'),
(17, 'ID_017', 'System Shock', 'Horror'),
(18, 'ID_018', 'Outlast', 'Horror');

INSERT INTO public.dim_account (sk_account_id, bk_account_id, bk_account_name, bk_combined_map) VALUES
(1, 'ACC_001', 'Sales Action New', 'Action'),
(2, 'ACC_002', 'Sales Interactive movies New', 'Interactive movies'),
(3, 'ACC_003', 'Sales RPG New', 'RPG'),
(4, 'ACC_004', 'Sales Horror New', 'Horror'),
(5, 'ACC_005', 'Sales Action Old', 'Action'),
(6, 'ACC_006', 'Sales Interactive movies Old', 'Interactive movies'),
(7, 'ACC_007', 'Sales RPG Old', 'RPG'),
(8, 'ACC_008', 'Sales Horror Old', 'Horror');


INSERT INTO public.dim_cfo (sk_cfo_id, bk_cfo_id, bk_cfo_name) VALUES
(1, 'MO', 'Москва и МО'),
(2, 'RF_NO_MO', 'РФ без МО');

