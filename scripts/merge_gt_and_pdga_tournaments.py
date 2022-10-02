from django.db.models import Q

from dgf.models import Tournament

gt_pdga = {(1100, 34914),
           (1103, 37071),
           (1104, 35145),
           (1105, 34913),
           (1108, 37482),
           (1111, 36277),
           (1116, 35125),
           (1117, 35032),
           (1120, 37371),
           (1124, 35707),
           (1133, 36704),
           (1142, 37545),
           (1144, 35252),
           (1157, 36365),
           (1186, 37970),
           (1190, 37533),
           (1195, 37352),
           (1202, 38106),
           (1221, 39314),
           (1229, 39440),
           (1233, 39286),
           (1234, 41424),
           (1238, 41146),
           (1241, 39849),
           (1249, 40332),
           (1251, 38925),
           (1252, 42021),
           (1254, 41878),
           (1256, 42741),
           (1257, 39130),
           (1274, 42757),
           (1276, 39233),
           (1279, 41459),
           (1283, 42041),
           (1288, 41921),
           (1289, 41766),
           (1300, 42733),
           (1311, 41282),
           (1348, 43523),
           (1354, 44489),
           (1360, 47145),
           (1362, 46743),
           (1366, 44084),
           (1367, 47159),
           (1368, 46270),
           (1369, 46394),
           (1372, 47568),
           (1383, 44230),
           (1384, 45427),
           (1385, 45425),
           (1395, 43892),
           (1396, 44490),
           (1397, 47545),
           (1399, 47008),
           (1414, 46531),
           (1415, 44741),
           (1416, 47099),
           (1422, 47768),
           (1444, 45664),
           (1445, 47152),
           (1446, 44691),
           (1464, 46897),
           (1496, 46772),
           (1601, 51529),
           (1603, 53078),
           (1604, 54378),
           (1605, 48334),
           (1610, 48463),
           (1611, 52629),
           (1614, 48370),
           (1615, 47967),
           (1622, 54931),
           (1625, 54019),
           (1628, 50319),
           (1629, 49268),
           (1630, 54059),
           (1632, 53671),
           (1638, 53727),
           (1645, 53165),
           (1646, 53166),
           (1648, 53247),
           (1651, 52677),
           (1657, 51665),
           (1662, 53831),
           (1668, 52703),
           (1673, 52611),
           (1678, 52995),
           (1680, 53605),
           (1692, 54108),
           (1699, 54209),
           (1701, 54715),
           (1714, 57779),
           (1718, 60772),
           (1719, 55503),
           (1724, 57777),
           (1725, 57778),
           (1730, 59515),
           (1731, 59516),
           (1736, 55329),
           (1737, 58215),
           (1745, 59907),
           (1749, 57295),
           (1751, 58306),
           (1754, 59906),
           (1757, 61069),
           (1760, 56582),
           (1762, 57852),
           (1769, 57019),
           (1778, 57760),
           (1780, 60051),
           (1781, 61309),
           (1782, 61311),
           (1810, 59947),
           (1824, 62678),
           (1825, 62723),
           (1828, 61358)
           }


def get_tournament(query):
    try:
        return Tournament.objects.get(query)
    except Tournament.DoesNotExist:
        return None


def fix_gt_pdga_ids(gt_pdga_relations):
    gt_pdga_1 = set()
    gt_pdga_2 = set()
    gt_non_pdga = set()
    non_gt_pdga = set()
    non_gt_non_pdga = set()

    for gt_id, pdga_id in gt_pdga_relations:

        gt_tournament = get_tournament(Q(gt_id=gt_id))
        pdga_tournament = get_tournament(Q(pdga_id=pdga_id))

        if gt_tournament:
            if pdga_tournament:
                if gt_tournament.id == pdga_tournament.id:
                    print('GT 1, PDGA 1 --> nothing to do!')
                    gt_pdga_1.add((gt_id, pdga_id))
                else:
                    print('GT 1, PDGA 1 --> delete PDGA tournament + update PDGA ID')
                    gt_pdga_2.add((gt_id, pdga_id))
                    pdga_tournament.delete()
                    gt_tournament.pdga_id = pdga_id
                    gt_tournament.save()
            else:
                print('GT 1, PDGA 0 --> update PDGA ID')
                gt_non_pdga.add((gt_id, pdga_id))
                gt_tournament.pdga_id = pdga_id
                gt_tournament.save()
        else:
            if pdga_tournament:
                print('GT 0, PDGA 1 --> update GT ID')
                non_gt_pdga.add((gt_id, pdga_id))
                pdga_tournament.gt_id = gt_id
                pdga_tournament.save()
            else:
                print('GT 0, PDGA 0 --> it\'s ok')
                non_gt_non_pdga.add((gt_id, pdga_id))

    print(f'GT-PDGA_1 ({len(gt_pdga_1)}): {gt_pdga_1}')
    print(f'GT-PDGA_2 ({len(gt_pdga_2)}): {gt_pdga_2}')
    print(f'GT-NON_PDGA ({len(gt_non_pdga)}): {gt_non_pdga}')
    print(f'NON_GT-PDGA ({len(non_gt_pdga)}): {non_gt_pdga}')
    print(f'NON_GT-NON_PDGA ({len(non_gt_non_pdga)}): {non_gt_non_pdga}')


if __name__ == '__main__':
    fix_gt_pdga_ids(gt_pdga)
