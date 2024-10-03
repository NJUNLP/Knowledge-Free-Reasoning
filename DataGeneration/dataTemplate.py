
# -*- coding: utf-8 -*-
chars={}
numbers = {}
lange=['EN','ZH','DE','FR','IT','RU','PL','JA','AR','HE']
Qtemplate={}
TemplateItem={}
ruleEntity = {}
ruleAtt={}
STRLENMIN=3
STRLENMAX=5
SYMBOLICTURN=3
MAXNUM=999
CASENUM=6


ruleEntity = {
    'EN': ["Fae", "Rex", "Sally", "Max", "Alex", "Sam", "Polly", "Stella", "Wren"],
    'ZH': ["费", "雷克斯", "莎莉", "马克斯", "亚历克斯", "山姆", "波莉", "斯特拉", "雷恩"],
    'DE': ["Fae", "Rex", "Sally", "Max", "Alex", "Sam", "Polly", "Stella", "Wren"],
    'FR': ["Fae", "Rex", "Sally", "Max", "Alex", "Sam", "Polly", "Stella", "Wren"],
    'IT': ["Fae", "Rex", "Sally", "Max", "Alex", "Sam", "Polly", "Stella", "Wren"],
    'RU': ["Фэй", "Рекс", "Сэлли", "Макс", "Алекс", "Сэм", "Полли", "Стелла", "Рен"],
    'PL': ["Fae", "Rex", "Sally", "Max", "Alex", "Sam", "Polly", "Stella", "Wren"],
    'JA': ["フェイ", "レックス", "サリー", "マックス", "アレックス", "サム", "ポリー", "ステラ", "レン"],
    'AR': ["فاي", "ريكس", "سالي", "ماكس", "أليكس", "سام", "بولي", "ستيلا", "رين"],
    'HE': ["פיי", "רקס", "סלי", "מקס", "אלכס", "סם", "פולי", "סטלה", "רן"]
}


import json
rulePath="./template/fakeName.json"
for lang in lange:
    tempPath=rulePath
    if lang!="EN":
        tempPath=rulePath.replace("fakeName","fakeName"+lang)
    with open(tempPath, 'r') as f:
        data = json.load(f)
        ruleAtt[lang]=[]
        for key in data.keys():
            ruleAtt[lang]=ruleAtt[lang]+data[key]
    
ruleTypeMapTemplate = {
"anyEN":"Everything that is {} is {}.",
"isEN":"{} is {}.",
"orEN":"{} or {}",
"andEN":"{} and {}",
"notEN":"not {}",
"soEN":"Suppose {0} is {1},then {0} is {2}.",
"anyZH": "任何{}的都是{}。",
"isZH": "{}是{}。",
"orZH": "{}或者{}",
"andZH": "{}和{}",
"notZH": "不是{}",
"soZH": "假设{0}是{1}，那么{0}是{2}。",
"anyDE": "Alles, was {} ist, ist {}.",
"isDE": "{} ist {}.",
"orDE": "{} oder {}",
"andDE": "{} und {}",
"notDE": "nicht {}",
"soDE": "Angenommen, {0} ist {1}, dann ist {0} {2}.",

"anyFR": "Tout ce qui est {} est {}.",
"isFR": "{} est {}.",
"orFR": "{} ou {}",
"andFR": "{} et {}",
"notFR": "pas {}",
"soFR": "Supposons que {0} soit {1}, alors {0} est {2}.",

"anyIT": "Tutto ciò che è {} è {}.",
"isIT": "{} è {}.",
"orIT": "{} o {}",
"andIT": "{} e {}",
"notIT": "non {}",
"soIT": "Supponiamo che {0} sia {1}, allora {0} è {2}.",

"anyRU": "Всё, что является {}, также является {}.",
"isRU": "{} это {}.",
"orRU": "{} или {}",
"andRU": "{} и {}",
"notRU": "не {}",
"soRU": "Предположим, что {0} это {1}, тогда {0} это {2}.",

"anyPL": "Wszystko, co jest {}, jest {}.",
"isPL": "{} jest {}.",
"orPL": "{} lub {}",
"andPL": "{} i {}",
"notPL": "nie {}",
"soPL": "Załóżmy, że {0} jest {1}, wtedy {0} jest {2}.",

"anyJA": "全ての{}は{}です。",
"isJA": "{}は{}です。",
"orJA": "{}または{}",
"andJA": "{}と{}",
"notJA": "{}ではない",
"soJA": "{0}が{1}であると仮定すると、{0}は{2}です。",

"anyAR": "كل ما هو {} هو {}.",
"isAR": "{} هو {}.",
"orAR": "{} أو {}",
"andAR": "{} و{}",
"notAR": "ليس {}",
"soAR": "افترض أن {0} هو {1}، إذًا {0} هو {2}.",

"anyHE": "כל מה שהוא {} הוא {}.",
"isHE": "{} הוא {}.",
"orHE": "{} או {}",
"andHE": "{} ו{}",
"notHE": "לא {}",
"soHE": "נניח ש{0} הוא {1}, אז {0} הוא {2}."
}

RULETYPESET= ["ModusPonens", "AndIntro", "AndElim", "OrIntro", "OrElim", "ProofByContra"]

ruleTypeTemplate = {
    "ModusPonensEN": "Implication Elimination",
    "AndIntroEN": "Conjunction Introduction",
    "AndElimEN": "Conjunction Elimination",
    "OrIntroEN": "Disjunction Introduction",
    "OrElimEN": "Disjunction Elimination",
    "ProofByContraEN": "Proof by Contradiction",
    
    "ModusPonensZH": "蕴涵消除",
    "AndIntroZH": "合取引入",
    "AndElimZH": "合取消除",
    "OrIntroZH": "析取引入",
    "OrElimZH": "析取消除",
    "ProofByContraZH": "反证法",

    "ModusPonensDE": "Implikationsbeseitigung",
    "AndIntroDE": "Konjunktionseinführung",
    "AndElimDE": "Konjunktionsbeseitigung",
    "OrIntroDE": "Disjunktionseinführung",
    "OrElimDE": "Disjunktionsbeseitigung",
    "ProofByContraDE": "Beweis durch Widerspruch",

    "ModusPonensFR": "Élimination de l'implication",
    "AndIntroFR": "Introduction de la conjonction",
    "AndElimFR": "Élimination de la conjonction",
    "OrIntroFR": "Introduction de la disjonction",
    "OrElimFR": "Élimination de la disjonction",
    "ProofByContraFR": "Preuve par contradiction",

    "ModusPonensIT": "Eliminazione dell'implicazione",
    "AndIntroIT": "Introduzione della congiunzione",
    "AndElimIT": "Eliminazione della congiunzione",
    "OrIntroIT": "Introduzione della disgiunzione",
    "OrElimIT": "Eliminazione della disgiunzione",
    "ProofByContraIT": "Prova per contraddizione",

    "ModusPonensRU": "Устранение импликации",
    "AndIntroRU": "Введение конъюнкции",
    "AndElimRU": "Устранение конъюнкции",
    "OrIntroRU": "Введение дизъюнкции",
    "OrElimRU": "Устранение дизъюнкции",
    "ProofByContraRU": "Доказательство от противного",

    "ModusPonensPL": "Eliminacja implikacji",
    "AndIntroPL": "Wprowadzenie koniunkcji",
    "AndElimPL": "Eliminacja koniunkcji",
    "OrIntroPL": "Wprowadzenie alternatywy",
    "OrElimPL": "Eliminacja alternatywy",
    "ProofByContraPL": "Dowód przez sprzeczność",

    "ModusPonensJA": "含意の除去",
    "AndIntroJA": "連言の導入",
    "AndElimJA": "連言の除去",
    "OrIntroJA": "選言の導入",
    "OrElimJA": "選言の除去",
    "ProofByContraJA": "矛盾による証明",

    "ModusPonensAR": "إزالة الضمن",
    "AndIntroAR": "مقدمة الربط",
    "AndElimAR": "إزالة الربط",
    "OrIntroAR": "مقدمة التفريق",
    "OrElimAR": "إزالة التفريق",
    "ProofByContraAR": "البرهان بالتناقض",

    "ModusPonensHE": "הסרת ההשלכה",
    "AndIntroHE": "הכנסת הקישור",
    "AndElimHE": "הסרת הקישור",
    "OrIntroHE": "הכנסת האו",
    "OrElimHE": "הסרת האו",
    "ProofByContraHE": "הוכחה בדרך של סתירה"
}



typeMapTemplate = {
    "addZH": "加法",
    "subZH": "减法",
    "mulZH": "乘法",
    "divZH": "除法",
    "eqZH": "等于",
    "isotropicZH": "等差数列",
    "isometricZH": "等比数列",
    "sortZH": "升序排序",
    "addEN": "Addition",
    "subEN": "Subtraction",
    "mulEN": "Multiplication",
    "divEN": "Division",
    "eqEN": "Equality",
    "isotropicEN": "Arithmetic sequence",
    "isometricEN": "Geometric sequence",
    "sortEN": "Ascending Sorting",
    "addDE": "Addition",
    "subDE": "Subtraktion",
    "mulDE": "Multiplikation",
    "divDE": "Division",
    "eqDE": "Gleichheit",
    "isotropicDE": "Arithmetische Folge",
    "isometricDE": "Geometrische Folge",
    "sortDE": "Aufsteigende Sortierung",
    "addFR": "Addition",
    "subFR": "Soustraction",
    "mulFR": "Multiplication",
    "divFR": "Division",
    "eqFR": "Égalité",
    "isotropicFR": "Séquence arithmétique",
    "isometricFR": "Séquence géométrique",
    "sortFR": "Tri ascendant",
    "addIT": "Addizione",
    "subIT": "Sottrazione",
    "mulIT": "Moltiplicazione",
    "divIT": "Divisione",
    "eqIT": "Uguaglianza",
    "isotropicIT": "Sequenza aritmetica",
    "isometricIT": "Sequenza geometrica",
    "sortIT": "Ordinamento ascendente",
    "addRU": "Сложение",
    "subRU": "Вычитание",
    "mulRU": "Умножение",
    "divRU": "Деление",
    "eqRU": "Равенство",
    "isotropicRU": "Арифметическая прогрессия",
    "isometricRU": "Геометрическая прогрессия",
    "sortRU": "Сортировка по возрастанию",
    "addPL": "Dodawanie",
    "subPL": "Odejmowanie",
    "mulPL": "Mnożenie",
    "divPL": "Dzielenie",
    "eqPL": "Równość",
    "isotropicPL": "Ciąg arytmetyczny",
    "isometricPL": "Ciąg geometryczny",
    "sortPL": "Sortowanie rosnące",
    "addJA": "加算",
    "subJA": "減算",
    "mulJA": "乗算",
    "divJA": "除算",
    "eqJA": "等式",
    "isotropicJA": "等差数列",
    "isometricJA": "等比数列",
    "sortJA": "昇順ソート",
    "addAR": "الجمع",
    "subAR": "الطرح",
    "mulAR": "الضرب",
    "divAR": "القسمة",
    "eqAR": "المساواة",
    "isotropicAR": "متتابعة حسابية",
    "isometricAR": "متتابعة هندسية",
    "sortAR": "ترتيب تصاعدي",
    "addHE": "חיבור",
    "subHE": "חיסור",
    "mulHE": "כפל",
    "divHE": "חלוקה",
    "eqHE": "שוויון",
    "isotropicHE": "סדרה חשבונית",
    "isometricHE": "סדרה הנדסית",
    "sortHE": "מיון עולה"
}

charTypeMapTemplate = {
    "repeatZH": "不进行任何变化",
    "addZH": "在第{loc}个词之前插入'{char}'",
    "subZH": "删除第{loc}个词",
    "replaceZH": "交换第{loc1}个词和第{loc2}个词的位置",
    "repeatEN": "Do not make any changes",
    "addEN": "Insert '{char}' before the {loc}th word",
    "subEN": "Delete the {loc}th word",
    "replaceEN": "Swap the positions of the {loc1}th and {loc2}th words",
    "repeatDE": "Keine Änderungen vornehmen",
    "addDE": "Fügen Sie '{char}' vor dem {loc}. Wort ein",
    "subDE": "Löschen Sie das {loc}. Wort",
    "replaceDE": "Tauschen Sie die Positionen des {loc1}. und des {loc2}. Wortes",
    "repeatFR": "Ne faites aucun changement",
    "addFR": "Insérez '{char}' avant le {loc}e mot",
    "subFR": "Supprimez le {loc}e mot",
    "replaceFR": "Échangez les positions des mots {loc1} et {loc2}",
    "repeatIT": "Non apportare modifiche",
    "addIT": "Inserisci '{char}' prima della {loc}a parola",
    "subIT": "Elimina la {loc}a parola",
    "replaceIT": "Scambia le posizioni della {loc1}a e della {loc2}a parola",
    "repeatRU": "Не вносите изменений",
    "addRU": "Вставьте '{char}' перед {loc}-м словом",
    "subRU": "Удалите {loc}-е слово",
    "replaceRU": "Поменяйте местами {loc1}-е и {loc2}-е слова",
    "repeatPL": "Nie dokonuj żadnych zmian",
    "addPL": "Wstaw '{char}' przed {loc}-ym słowem",
    "subPL": "Usuń {loc}-e słowo",
    "replacePL": "Zamień miejscami {loc1}-e i {loc2}-e słowo",
    "repeatJA": "変更を加えない",
    "addJA": "{loc}番目の単語の前に'{char}'を挿入する",
    "subJA": "{loc}番目の単語を削除する",
    "replaceJA": "{loc1}番目と{loc2}番目の単語の位置を入れ替える",
    "repeatAR": "لا تجري أي تغييرات",
    "addAR": "أدخل '{char}' قبل الكلمة ال{loc}ة",
    "subAR": "احذف الكلمة ال{loc}ة",
    "replaceAR": "قم بتبديل مواقع الكلمة {loc1} والكلمة {loc2}",
    "repeatHE": "אל תבצע שינויים",
    "addHE": "הוסף '{char}' לפני המילה ה-{loc}",
    "subHE": "מחק את המילה ה-{loc}",
    "replaceHE": "החלף את מיקומי המילים {loc1} ו-{loc2}"
}

with open('./template/Q.json', 'r') as f:
    Q = json.load(f)
with open('./template/INPUT.json', 'r') as f:
    INPUT = json.load(f)

chars['IT'] = [
    "gioco", "azienda", "mercato", "livello", "tecnologia", "linea", "affari", "presidente", "viso", "insegnante",
    "fatto", "casa", "nome", "veicolo", "donna", "anno", "mese", "libro", "caso", "modo",
    "storia", "scuola", "paese", "idea", "sviluppo", "educazione", "ragazzo", "ufficio", "mano",
    "risultato", "ricerca", "ragazza", "scienza", "cosa", "cibo", "società", "musica", "vita", "minuto",
    "arte", "forza", "legge", "porta", "problema", "squadra", "uomo", "numero", "momento", "genitore", "occhio",
    "tempo", "notte", "auto", "corpo", "bambino", "servizio", "padre", "membro", "settimana", "città", "film",
    "domanda", "persona", "governo", "lato", "aria", "lavoro", "ora", "altri", "fine", "cambiamento",
    "festa", "testa", "giorno", "ambiente", "informazione", "gruppo", "denaro", "studente", "guerra",
    "storia", "schiena", "parte", "ragione", "posto", "lingua", "mattina", "problema", "conoscenza",
    "stato", "comunità", "mondo", "famiglia", "natura", "area", "tipo", "bambino", "amore", "amico", "salute"
]
chars['FR'] = [
    "jeu", "entreprise", "marché", "niveau", "technologie", "ligne", "affaires", "président", "visage", "enseignant",
    "fait", "maison", "nom", "véhicule", "femme", "année", "mois", "livre", "cas", "chemin",
    "histoire", "école", "pays", "idée", "développement", "éducation", "gars", "bureau", "main",
    "résultat", "recherche", "fille", "science", "chose", "nourriture", "société", "musique", "vie", "minute",
    "art", "force", "loi", "porte", "problème", "équipe", "homme", "nombre", "moment", "parent", "œil",
    "temps", "nuit", "voiture", "corps", "enfant", "service", "père", "membre", "semaine", "ville", "film",
    "question", "personne", "gouvernement", "côté", "air", "emploi", "heure", "autres", "fin", "changement",
    "fête", "tête", "jour", "environnement", "information", "groupe", "argent", "étudiant", "guerre",
    "histoire", "dos", "partie", "raison", "lieu", "langue", "matin", "problème", "connaissance",
    "état", "communauté", "monde", "famille", "nature", "zone", "type", "enfant", "amour", "ami", "santé"
]

chars['DE'] = [
    "Spiel", "Unternehmen", "Markt", "Ebene", "Technologie", "Linie", "Geschäft", "Präsident", "Gesicht", "Lehrer",
    "Fakt", "Haus", "Name", "Fahrzeug", "Frau", "Jahr", "Monat", "Buch", "Fall", "Weg",
    "Geschichte", "Schule", "Land", "Idee", "Entwicklung", "Bildung", "Typ", "Büro", "Hand",
    "Ergebnis", "Forschung", "Mädchen", "Wissenschaft", "Ding", "Essen", "Gesellschaft", "Musik", "Leben", "Minute",
    "Kunst", "Kraft", "Gesetz", "Tür", "Problem", "Team", "Mann", "Nummer", "Moment", "Elternteil", "Auge",
    "Zeit", "Nacht", "Auto", "Körper", "Kind", "Dienst", "Vater", "Mitglied", "Woche", "Stadt", "Film",
    "Frage", "Person", "Regierung", "Seite", "Luft", "Arbeit", "Stunde", "Andere", "Ende", "Veränderung",
    "Partei", "Kopf", "Tag", "Umwelt", "Information", "Gruppe", "Geld", "Student", "Krieg",
    "Geschichte", "Rücken", "Teil", "Grund", "Ort", "Sprache", "Morgen", "Problem", "Wissen",
    "Staat", "Gemeinschaft", "Welt", "Familie", "Natur", "Gebiet", "Art", "Kind", "Liebe", "Freund", "Gesundheit"
]


chars['RU'] = [
    "игра", "компания", "рынок", "уровень", "технология", "линия", "бизнес", "президент", "лицо",
    "учитель", "факт", "дом", "имя", "транспортное средство", "женщина", "год", "месяц", "книга", "дело", "путь",
    "история", "школа", "страна", "идея", "развитие", "образование", "парень", "офис", "рука",
    "результат", "исследование", "девушка", "наука", "вещь", "еда", "общество", "музыка", "жизнь", "минута",
    "искусство", "сила", "закон", "дверь", "вопрос", "команда", "мужчина", "число", "момент", "родитель", "глаз",
    "время", "ночь", "автомобиль", "тело", "ребенок", "услуга", "отец", "член", "неделя", "город", "фильм",
    "вопрос", "человек", "правительство", "сторона", "воздух", "работа", "час", "другие", "конец", "изменение",
    "вечеринка", "голова", "день", "окружающая среда", "информация", "группа", "деньги", "студент", "война",
    "история", "спина", "часть", "причина", "место", "язык", "утро", "проблема", "знания",
    "государство", "община", "мир", "семья", "природа", "область", "вид", "ребенок", "любовь", "друг", "здоровье"
]


chars['EN']=['game', 'company', 'market', 'level', 'technology', 'line', 'business', 'president', 'face', 'teacher', 'fact', 'house', 'name', 'vehicle', 'woman', 'year', 'month', 'book', 'case', 'way', 'history', 'school', 'country', 'idea', 'development', 'education', 'guy', 'office', 'hand', 'result', 'research', 'girl', 'science', 'thing', 'food', 'society', 'music', 'life', 'minute', 'art', 'force', 'law', 'door', 'issue', 'team', 'man', 'number', 'moment', 'parent', 'eye', 'time', 'night', 'car', 'body', 'kid', 'service', 'father', 'member', 'week', 'city', 'movie', 'question', 'person', 'government', 'side', 'air', 'job', 'hour', 'others', 'end', 'change', 'party', 'head', 'day', 'environment', 'information', 'group', 'money', 'student', 'war', 'story', 'back', 'part', 'reason', 'place', 'language', 'morning', 'problem', 'knowledge', 'state', 'community', 'world', 'family', 'nature', 'area', 'kind', 'child', 'love', 'friend', 'health']

chars['ZH']=['游戏', '公司', '市场', '水平', '技术', '线', '商业', '总统', '脸', '教师', '事实', '房子', '名字', '交通工具', '女人', '年', '月', '书', '案例', '方式', '历史', '学校', '国家', '想法', '发展', '教育', '男孩', '办公室', '手', '结果', '研究', '女孩', '科学', '事物', '食物', '社会', '音乐', '生活', '分钟', '艺术', '力量', '法律', '门', '问题', '团队', '男人', '数字', '时刻', '父母', '眼睛', '时间', '夜晚', '汽车', '身体', '孩子', '服务', '父亲', '成员', '周', '城市', '电影', '问题', '人', '政府', '侧面', '空气', '工作', '小时', '其他人', '结束', '变化', '党派', '头', '日子', '环境', '信息', '群体', '金钱', '学生', '战争', '故事', '背部', '部分', '原因', '地方', '语言', '早晨', '问题', '知识', '状态', '社区', '世界', '家庭', '自然', '区域', '类型', '孩子', '爱', '朋友', '健康']

chars['PL'] = [
    "gra", "firma", "rynek", "poziom", "technologia", "linia", "biznes", "prezydent", "twarz",
    "nauczyciel", "fakt", "dom", "nazwa", "pojazd", "kobieta", "rok", "miesiąc", "książka", "przypadek", "droga",
    "historia", "szkoła", "kraj", "pomysł", "rozwój", "edukacja", "facet", "biuro", "ręka",
    "wynik", "badanie", "dziewczyna", "nauka", "rzecz", "jedzenie", "społeczeństwo", "muzyka", "życie", "minuta",
    "sztuka", "siła", "prawo", "drzwi", "kwestia", "zespół", "mężczyzna", "numer", "chwila", "rodzic", "oko",
    "czas", "noc", "samochód", "ciało", "dziecko", "usługa", "ojciec", "członek", "tydzień", "miasto", "film",
    "pytanie", "osoba", "rząd", "strona", "powietrze", "praca", "godzina", "inni", "koniec", "zmiana",
    "impreza", "głowa", "dzień", "środowisko", "informacja", "grupa", "pieniądze", "student", "wojna",
    "historia", "plecy", "część", "powód", "miejsce", "język", "ranek", "problem", "wiedza",
    "stan", "społeczność", "świat", "rodzina", "natura", "obszar", "typ", "dziecko", "miłość", "przyjaciel", "zdrowie"
]


chars['JA'] = [
    "ゲーム", "会社", "市場", "レベル", "技術", "ライン", "ビジネス", "大統領", "顔",
    "教師", "事実", "家", "名前", "車両", "女性", "年", "月", "本", "事件", "方法",
    "歴史", "学校", "国", "アイデア", "開発", "教育", "男", "オフィス", "手",
    "結果", "研究", "女の子", "科学", "物", "食べ物", "社会", "音楽", "人生", "分",
    "芸術", "力", "法", "ドア", "問題", "チーム", "男性", "数字", "瞬間", "親", "目",
    "時間", "夜", "車", "体", "子供", "サービス", "父", "メンバー", "週", "市", "映画",
    "質問", "人", "政府", "側面", "空気", "仕事", "時間", "他人", "終わり", "変化",
    "パーティー", "頭", "日", "環境", "情報", "グループ", "お金", "学生", "戦争",
    "物語", "背中", "部分", "理由", "場所", "言語", "朝", "問題", "知識",
    "状態", "コミュニティ", "世界", "家族", "自然", "地域", "種類", "子供", "愛", "友達", "健康"
]


chars['AR'] = [
    "لعبة", "شركة", "سوق", "مستوى", "تكنولوجيا", "خط", "أعمال", "رئيس", "وجه",
    "معلم", "حقيقة", "منزل", "اسم", "مركبة", "امرأة", "سنة", "شهر", "كتاب", "قضية", "طريقة",
    "تاريخ", "مدرسة", "بلد", "فكرة", "تطوير", "تعليم", "شاب", "مكتب", "يد",
    "نتيجة", "بحث", "فتاة", "علم", "شيء", "طعام", "مجتمع", "موسيقى", "حياة", "دقيقة",
    "فن", "قوة", "قانون", "باب", "مشكلة", "فريق", "رجل", "عدد", "لحظة", "والد", "عين",
    "زمن", "ليل", "سيارة", "جسم", "طفل", "خدمة", "أب", "عضو", "أسبوع", "مدينة", "فيلم",
    "سؤال", "شخص", "حكومة", "جانب", "هواء", "عمل", "ساعة", "آخرون", "نهاية", "تغيير",
    "حفلة", "رأس", "يوم", "بيئة", "معلومات", "مجموعة", "مال", "طالب", "حرب",
    "قصة", "ظهر", "جزء", "سبب", "مكان", "لغة", "صباح", "مشكلة", "معرفة",
    "حالة", "مجتمع", "عالم", "عائلة", "طبيعة", "منطقة", "نوع", "طفل", "حب", "صديق", "صحة"
]

chars['HE'] = [
    "משחק", "חברה", "שוק", "רמה", "טכנולוגיה", "קו", "עסקים", "נשיא", "פנים",
    "מורה", "עובדה", "בית", "שם", "רכב", "אישה", "שנה", "חודש", "ספר", "מקרה", "דרך",
    "היסטוריה", "בית ספר", "מדינה", "רעיון", "פיתוח", "חינוך", "בחור", "משרד", "יד",
    "תוצאה", "מחקר", "ילדה", "מדע", "דבר", "אוכל", "חברה", "מוזיקה", "חיים", "דקה",
    "אמנות", "כוח", "חוק", "דלת", "בעיה", "קבוצה", "גבר", "מספר", "רגע", "הורה", "עין",
    "זמן", "לילה", "מכונית", "גוף", "ילד", "שירות", "אב", "חבר", "שבוע", "עיר", "סרט",
    "שאלה", "אדם", "ממשלה", "צד", "אוויר", "עבודה", "שעה", "אחרים", "סוף", "שינוי",
    "מסיבה", "ראש", "יום", "סביבה", "מידע", "קבוצה", "כסף", "סטודנט", "מלחמה",
    "סיפור", "גב", "חלק", "סיבה", "מקום", "שפה", "בוקר", "בעיה", "ידע",
    "מדינה", "קהילה", "עולם", "משפחה", "טבע", "אזור", "סוג", "ילד", "אהבה", "חבר", "בריאות"
]

from num2words import num2words
for lang in lange:
    numbers[lang] = []
    for i in range(MAXNUM+1):
        if lang!='ZH':
            numbers[lang].append(num2words(i, lang=lang.lower()))


digits = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
units = ['', '十', '百', '千', '万']

def convert_to_chinese_num(num):
    if num == 0:
        return '零'
    
    num_str = str(num)
    length = len(num_str)
    
    if length > 4:
        return "数字超出范围"
    
    chinese_num = ''
    for i in range(length):
        digit = int(num_str[i])
        if digit == 0:
            if chinese_num and chinese_num[-1] != '零':
                chinese_num += digits[digit]
        else:
            chinese_num += digits[digit] + units[length - 1 - i]
    
    chinese_num = chinese_num.replace('零十', '零')
    chinese_num = chinese_num.replace('零百', '零')
    chinese_num = chinese_num.replace('零千', '零')
    chinese_num = chinese_num.rstrip('零')
    
    if chinese_num.startswith('一十'):
        chinese_num = chinese_num[1:]
    
    return chinese_num
numbers['ZH'] = []
for i in range(MAXNUM+1):
    numbers['ZH'].append(convert_to_chinese_num(i))


for lang in lange:
    numbers[lang] = []
    for i in range(MAXNUM+1):
        numbers[lang].append(str(i))