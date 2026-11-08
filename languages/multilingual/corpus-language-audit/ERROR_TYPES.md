# Типы ошибок в определении языков

Этот файл дополняет [README](README.md). В нём собраны все типы ошибок, найденные в полях «Written in» (язык, на котором написан документ) и «Described language» (язык, который документ описывает). Для каждого типа дана таблица перепутанных языков, а к таблицам приложены CSV с предлагаемыми исправлениями.

> Таблицы 1–4 собирает скрипт [`scripts/build_error_types.py`](scripts/build_error_types.py) из [`data/proposed_corrections_by_code.csv`](data/proposed_corrections_by_code.csv). В них только коды с уверенностью «проверено вручную», «высокая» или «средняя». Коды с низкой уверенностью есть в CSV, но не в таблицах.

## Сводка

| # | Тип ошибки | Поле | Масштаб |
|---|---|---|---|
| 1 | Код угадан по буквам названия языка | Written in, Described | 155 кодов в таблице; ~2,7 тыс. документов с предложенной заменой |
| 2 | В документе другой язык | Written in | 125 кодов; ~1,7 тыс. документов |
| 3 | Перепутаны родственные или соседние языки | Written in | 3 кода; ~0,9 тыс. документов (в основном дари ↔ пушту) |
| 4 | Не та историческая стадия языка | Written in | 4 кода; ~0,2 тыс. документов по автоматике + `goh` целиком |
| 5 | Выдуманное название языка | Described | найдено 5 «языков» на одном источнике |
| 6 | Название и код описываемого языка расходятся | Described | десятки кодов в списке описываемых языков |
| 7 | Несколько языков слиты в одно название | Described | 50 из первой тысячи описываемых языков |
| 8 | Второстепенный язык засчитан как язык документа | Written in | ~36% пар «документ — язык» |
| 9 | Коды не нормализованы | Written in, Described | 57 кодов вне ISO 639-3 + макроязыки |
| 10 | Язык приписан не-тексту или битому тексту | Written in | `und` 33 тыс., GIF, битые кодировки |
| 11 | Доли языков — округлённые прикидки | Written in | почти все многоязычные документы |

---

## 1. Код угадан по буквам названия языка

Модель правильно называет язык, но ISO-код не берёт из справочника, а составляет из букв названия: Puyuma → `puy`, Kavalan → `kav`, Kotava → `kot`, Dholuo → `dho`. Почти всегда такой код существует и принадлежит другому, нередко вымершему языку. Поэтому все документы этого языка уходят под чужую метку целиком.

Признак: буквы метки идут по порядку в названии реального языка и начинаются с той же буквы (колонка `error_type = code_from_name`). Особый случай — `bar`: так модель сократила название источника *Bartangi Corpus*, а `bar` — это код баварского.

| Метка в корпусе | Документов | На самом деле | Доля в проверке | Уверенность | Пример документа |
|---|---:|---|---:|---|---|
| `chc` Catawba | 479 | `cic` Chickasaw | 99% | проверено вручную | 2932840: Webster's Chickasaw-English Thesaurus Dictionary |
| `bar` Bavarian | 460 | `sgh` Shughni (Bartangi) | 96% | проверено вручную | 1006645: Unknown (Fragment from Bartangi Corpus) |
| `mbu` Mbula-Bwazza | 92 | `mqb` Mbuko | 97% | проверено вручную | 831390: français — mbuko |
| `koo` Konzo | 54 | `ozm` Koonzime | 98% | проверено вручную | 7599: français — koonzime |
| `mer` Meru | 53 | `mqb` Mbuko | — | проверено вручную | 7597: français — mbuko |
| `prk` South Wa | 48 | `pra` Prakrit | 81% | проверено вручную | 782435: Nammaya Sundari Kaha |
| `dho` Dhodia-Kukna | 48 | `luo` Dholuo | 46% | проверено вручную | 1017852: 7AM Dala FM News |
| `kot` Lagwan | 46 | `avk` Kotava | 83% | проверено вручную | 2932970: Dictionary Portuguese - Kotava |
| `puy` Purisimeño | 42 | `pyu` Puyuma | 100% | проверено вручную | 833484: 知本卑南語學習手冊 第8階 (Katratripul Puyuma Language Level 8. Students) |
| `kai` Karekare | 40 | `cak` Kaqchikel | 60% | проверено вручную | 2120384: Retamaxik ri Kaqchikel Ch'ab'al: Nab'ey Wuj (Aprendiendo el idioma Kaqchikel, Lib |
| `mbk` Malol | 21 | `mqb` Mbuko | 100% | проверено вручную | 831395: Mbuko Lexicon |
| `par` Panamint | 19 | `xpr` Parthian | 84% | проверено вручную | 897462: Inscriptional Parthian Script (250 B.C.E.) 2 |
| `kav` Katukína | 17 | `ckv` Kavalan | 82% | проверено вручную | 920656: Kavalan Dictionary |
| `bnu` Bentong | 16 | `bnn` Bunun | 94% | проверено вручную | 817736: 郡群布農語學習手冊 第２階 Isbukun Bunun Language Level 2. Students book |
| `gar` Galeya | 12 | `grt` Garo | 50% | проверено вручную | 104752: A dream to have in heaven |
| `bun` Sherbro | 11 | `bnn` Bunun | 64% | проверено вручную | 817717: 郡群布農語學習手冊 第６階 Isbukun Bunun Language Level 6. Students book |
| `sak` Sake | 10 | `szy` Sakizaya | 100% | проверено вручную | 822482: 撒奇萊雅語學習手冊 第３階 Sakizaya Language Level 3. Students book |
| `nam` Nangikurrunggurr | 7 | `nmy` Namuyi | 86% | проверено вручную | 104792: Can You See My Yak? |
| `laz` Aribwatsa | 5 | `lzz` Laz | 80% | проверено вручную | 110733: Hz. Muhammedişi Skidala |
| `tim` Timbe | 5 | `tms` Tima | — | проверено вручную | 2931354: A Tima-English Dictionary: An illustrated lexicon of a Niger-Congo language spoke |
| `car` Galibi Carib | 4 | `cbc` Carapana | 25% | проверено вручную | 2122150: Marí Yaye Mena Carapana, Yaia Yaye Mena Español Macarica Tuti (Carapana Grammar / |
| `rot`  | 4 | `roo` Rotokas | — | проверено вручную | 110192: Vocabulary of Rotokas--Pidgin--English |
| `han` Hangaza | 4 | `hnn` Hanunoo | — | проверено вручную | 896048: Hanunoo-English Vocabulary |
| `aci` Akacari | 4 | `acr` Achi | 100% | проверено вручную | 110323: Qatzu uwach wuj: Achi 5º primaria |
| `tzl` Talossan | 4 | `tzh` Tzeltal | — | проверено вручную | 104864: El Tzeltal Hablado (Spoken Tzeltal) |
| `pur` Puruborá | 3 | `puy` Purisimeño | — | проверено вручную | 19529: Purisimeño-English, English-Purisimeño Lexicon |
| `ser` Serrano | 3 | `sei` Seri | 100% | проверено вручную | 2122668: Seri Dictionary: People and Kinship Terms |
| `sum`  | 3 | `sux` Sumerian | — | проверено вручную | 103992: The Babylonian Expedition of the University of Pennsylvania. Series A: Cuneiform t |
| `sen` Nanerigé Sénoufo | 3 | `see` Seneca | 100% | проверено вручную | 848922: An Act Passed May 8, 1845 For the protection and improvement of the Seneca Indians |
| `fan` Fang (Equatorial Guinea) | 3 | `fng` Fanagalo | 100% | проверено вручную | 2122367: Fanagalo Phrase-Book, Grammar, Dictionary |
| `kos` Kosraean | 3 | `cku` Koasati | 100% | проверено вручную | 2933030: Koasati Traditional Narratives: Kowassá:ti Incokfa:ihilká |
| `bem` Bemba (Zambia) | 3 | `beq` Bembe | — | проверено вручную | 14904: Dictionnaire Beembe-Français Mukaanda |
| `tar` Central Tarahumara | 3 | `tae` Tariana | 33% | проверено вручную | 2110979: Dicionário tariana-português e português-tariana |
| `ram` Central-Southern Timbira | 3 | `rma` Rama | 67% | проверено вручную | 816431: Diccionario Elemental Rama: Rama - Inglés - Español; Inglés - Rama; Español - Rama |
| `csw` Swampy Cree | 63 | `cic` Chickasaw | 100% | высокая | 2932825: A Grammar of Chickasaw (Excerpt) |
| `ngb` Northern Ngbandi | 25 | `nnh` Ngiemboon | 92% | высокая | 7692: Dictionnaire Ngiemboon-Français |
| `qan`  | 24 | `kjb` Q'anjob'al | 92% | высокая | 110716: No' noq' b'ay kotx'otx'al: Los animales de nuestra tierra |
| `tzu` Tzotzil, Huixtán | 23 | `tzj` Tz'utujil | 87% | высокая | 109411: Najb’ey taq nusik’ineem: Tz'utujil (Mis primeras lecturas, 1o primaria) |
| `rom`  | 23 | `rmy` Vlax Romani | 87% | высокая | 1166901: Blicke in das Leben der Zigeuner |
| `roh` Romansh | 22 | `rhg` Rohingya | 73% | высокая | 2097822: Rohingya to English Dictionary (2000plus words) |
| `sam`  | 21 | `smp` Samaritan Hebrew | 90% | высокая | 854024: A grammar of the Samaritan language, with extracts and vocabulary |
| `aym`  | 21 | `ayc` Southern Aymara | 90% | высокая | 2122135: Arte y grammatica muy copiosa dela lengua aymara |
| `aue`  | 15 | `auv` Auvergnat | 100% | высокая | 850153: Les Perdrix |
| `lim` Limburgan | 14 | `lif` Limbu | 79% | высокая | 2121993: vfDaf]ªaf n'ªaf]ªaf ;fxf /]Þ n]ÞDhfªaf dftª\d] |
| `paw` Pawnee | 10 | `pwn` Paiwan | 70% | высокая | 816905: Eastern Paiwan Language Beginner Teaching Material of Alpha: Teacher's Manual |
| `bur`  | 9 | `bsk` Burushaski | 78% | высокая | 103894: A Burushaski-English Dictionary |
| `sgd` Surigaonon | 9 | `sog` Sogdian | 89% | высокая | 2112820: Sogdian Dictionary (Sogdian-Persian-English) |
| `mrt` Marghi Central | 9 | `vma` Martuthunira | 89% | высокая | 829450: Dedication |
| `ksi` I'saka | 8 | `kas` Kashmiri | 75% | высокая | 998008: زُون چُھہ اَکھ نازدار کانۍ (Zoon chhe ek naazdaar kaani) |
| `chj` Ojitlán Chinantec | 8 | `cac` Chuj | 100% | высокая | 110916: Winskolmalno nok' |
| `pow` San Felipe Otlaltepec Popoloca | 8 | `pwr` Powari | 100% | высокая | 909327: Powari Bal Bachak Chalval (January 2023) |
| `ahm` Mobumrin Aizi | 7 | `aho` Ahom | 100% | высокая | 848887: Ahom Beginner Tai |
| `cle` Lealao Chinantec | 6 | `dri` C'lela | 83% | высокая | 73327: Future Time Reference in C'lela: A Kainji Language of Nigeria (Appendix C - C'lela  |
| `ane` Xârâcùù | 6 | `aty` Aneityum | 100% | высокая | 898394: Nitasvitai uhup |
| `shu` Chadian Arabic | 6 | `jiv` Shuar | 83% | высокая | 78087: SHUAR CHICHAM NEKATAI: Guía de Aprendizaje del Idioma Shuar, Total y Funcional para |
| `nic`  | 5 | `ncb` Central Nicobarese | 80% | высокая | 851545: Dictionary of the Car-Nicobarese Language |
| `kiw` Northeast Kiwai | 5 | `kio` Kiowa | 100% | высокая | 2932063: Kavy-dawhhyah: Kiowa Christian Songs |
| `cfn`  | 5 | `con` Cofán | 80% | высокая | 108679: La creación y el diluvio / The Creation and the Flood |
| `rui` Rufiji | 5 | `dru` Rukai | 100% | высокая | 820820: 東魯凱語學習手冊 第６階 Taromak Rukai Language Level 6. Students book |
| `roa`  | 5 | `ron` Romanian | 100% | высокая | 944160: Fragmente din Evanghelie (variantă arhaică/OCR) |
| `bga` Gwamhi-Wuri | 5 | `bng` Benga | 100% | высокая | 845734: Malango ma Bolenaka ma Tyâtyi Jisu Kraist |
| `hmn`  | 5 | `mww` Hmong Daw | 100% | высокая | 855661: English-Hmong Phrasebook with Useful Wordlist (for Hmong Speakers) |
| `bis` Bislama | 36 | `bzi` Bisu | 44% | средняя | 89712: Basaa-French Finderlist |
| `chm`  | 25 | `ccc` Chamicuro | 32% | средняя | 2113693: Vocabulario y textos chamicuro |
| `nub`  | 21 | `onw` Old Nubian | 48% | средняя | 2939903: The Old Nubian Miracle of Saint Menas |
| `sai`  | 17 | `xsy` Saisiyat | 53% | средняя | 2108214: 賽夏語學習手冊 第１階 Saisiyat Language Level 1. Students book |
| `nah`  | 17 | `nhe` Eastern Huasteca Nahuatl | 53% | средняя | 2122136: Libro de la miseria y brevedad de la vida del hombre: y de sus quatro postrimeria |
| `kar`  | 15 | `kdr` Karaim | 47% | средняя | 2933008: A Crimean Karaim-English Dictionary: 10 000 entries |
| `aka` Akan | 15 | `knj` Akateko | 33% | средняя | 106216: Sb'i K'ultajb'al yet Qichmam Akateko: Toponimias Maya Akateka |
| `kaq` Capanahua | 12 | `cak` Kaqchikel | 58% | средняя | 2120383: Cuestionario Lingüístico para la investigación de las variaciones dialectales del |
| `nob`  | 9 | `fia` Nobiin | 33% | средняя | 2930751: Нубийский язык (The Nubian Language) |
| `ard` Arabana | 9 | `pmh` Ardha-Magadhi | 56% | средняя | 772061: An Illustrated Ardha-Magadhi Dictionary, Vol.1 |
| `mot` Barí | 8 | `meu` Motu | 62% | средняя | 896423: A Dictionary of Police Motu |
| `nip`  | 8 | `alq` Algonquin | 38% | средняя | 1092381: Nipicwasoskikw |
| `mun`  | 7 | `unr` Mundari | 57% | средняя | 851841: Mundari Hymns |
| `den`  | 7 | `anv` Denya | 43% | средняя | 52625: Manjóge Denya Ngwá 3 (Denya Primer 3) |
| `kui` Kuikúro-Kalapálo | 7 | `kxv` Kuvi | 43% | средняя | 897614: Odia-Kuvi Sabdakosh |
| `nan` Min Nan Chinese | 6 | `gld` Nanai | 33% | средняя | 70327: Nanai Folk Tales and Legends 7 |
| `sra` Saruga | 6 | `srm` Saramaccan | 33% | средняя | 2117381: Saramaccan for Beginners: A Pedagogical Grammar of the Saramaccan Language |
| `dgo` Dogri | 6 | `dig` Digo | 33% | средняя | 844287: Digo-English-Swahili Dictionary |
| `srd`  | 6 | `sro` Campidanese Sardinian | 50% | средняя | 79477: Su chistionu de s'allega: Osservatziones, ideas e propostas a pitzu de sa limba sar |
| `ach` Acoli | 6 | `acr` Achi | 67% | средняя | 110311: Uk’ux qak’aslemal: Achi 6º primaria |
| `kon`  | 6 | `kwy` Kikongo | 33% | средняя | 296396: Gramática da língua do Congo (kikongo); dialecto kisolongo |
| `see` Seneca | 6 | `trv` Seediq | 67% | средняя | 917275: 原住民族語基礎教材─字母篇 (Teacher's Manual: Seediq) |
| `shb` Ninam | 5 | `bun` Sherbro | 40% | средняя | 2544: Sherbro Dictionary |
| `sal`  | 5 | `slr` Salar | 60% | средняя | 2931023: Salar Language Materials |
| `tem` Timne | 5 | `kri` Krio | 40% | средняя | 2112821: Basic Krio and Temne Vocabulary |
| `srs` Sarsi | 4 | `sgz` Sursurunga | 50% | средняя | 896877: Sursurunga Dictionary |
| `mey` Hassaniyya | 4 | `mej` Meyah | 50% | средняя | 896729: Mahteyi Itur Warn gonu Ekergud: Ancient tale about Itur Warn and Ekergud |
| `ngm` Ngatik Men's Creole | 4 | `nmc` Ngam | 50% | средняя | 45432: Vernacular-English Dictionary (Ngam) |
| `kng` South-Central Koongo | 4 | `xnr` Kangri | 100% | средняя | 944205: Kangri UD Corpus Sample |
| `nkn` Nkangala | 4 | `nak` Nakanai | 100% | средняя | 853306: A Grammar of Nakanai (Part 4) |
| `alb`  | 4 | `akz` Alabama | 75% | средняя | 2933036: Dictionary of the Alabama Language: English-Alabama |
| `bat`  | 4 | `bbc` Batak Toba | 50% | средняя | 895874: Bataksch-Nederduitsch woordenboek |
| `mct`  | 4 | `ncl` Mictlan | 50% | средняя | 1092235: Micta emikwan (Fragment) |
| `muy` Muyang | 4 | `myw` Muyuw | 75% | средняя | 896538: Muyuw-English Dictionary |
| `tao` Yami | 4 | `ssf` Thao | 75% | средняя | 839272: 邵語學習手冊 第7階 (Thao Language Learning Handbook Level 7) |
| `krg` North Korowai | 4 | `coe` Koreguaje | 75% | средняя | 2933060: Diccionario bilingüe Koreguaje-Español Español-Koreguaje |
| `wao` Wappo | 4 | `auc` Waorani | 50% | средняя | 111323: Waorani Clause Formulas |
| `agu` Aguacateco | 4 | `agr` Aguaruna | 75% | средняя | 1006664: Aguaruna news report on government aid and health measures (Lambayeque/Huánuco) |
| `apa`  | 4 | `xap` Apalachee | 50% | средняя | 2930613: An Apalachee Vocabulary |
| `mpu` Makuráp | 4 | `akc` Mpur | 50% | средняя | 110830: Op ti wa: Masses of water washed things away |
| `onn` Onobasulu | 4 | `ono` Onondaga | 100% | средняя | 849074: Essay of an Onondaga Grammar, or a Short Introduction to Learn the Onondaga Al Maq |
| `gan` Gan Chinese | 4 | `gnb` Gangte | 50% | средняя | 840632: Gangte Literature Society Publication (2016 Edition) |
| `jua` Júma | 4 | `jun` Juang | 50% | средняя | 851189: Juanga Part 1 Curve |
| `pon` Pohnpeian | 4 | `lnm` Pondi | 50% | средняя | 849487: A Sketch Grammar of Pondi |
| `ata` Pele-Ata | 4 | `aqp` Atakapa | 50% | средняя | 109913: A dictionary of the Atakapa language accompanied by text material |
| `jaq` Yaqay | 4 | `jqr` Jaqaru | 100% | средняя | 48743: Vocabulario Jaqaru-Español Español-Jaqaru |
| `maw` Mampruli | 4 | `mph` Mawng | 50% | средняя | 2930618: Mawng Dictionary |
| `gur` Farefare | 4 | `gvr` Gurung | 50% | средняя | 107230: Khuyi Talokye (Gurung Language) Volume III (Class-III) |
| `boe` Mundabli-Mufu | 4 | `bol` Bole | 100% | средняя | 38811: Bole-English-Hausa Dictionary (Second Edition) |
| `tkt` Kathoriya Tharu | 4 | `ttc` Tektiteko | 100% | средняя | 2121992: Diccionario Especializado en Educación en el Idioma Maya Tektiteko |
| `tan` Tangale | 3 | `txg` Tangut | 33% | средняя | 103378: Измененный и заново утвержденный кодекс девиза царствования Небесное процветание ( |
| `ren` Rengao | 3 | `rel` Rendille | 33% | средняя | 851505: Rendille Genesis Translation |
| `srt` Sauri | 3 | `smp` Samaritan Hebrew | 67% | средняя | 854022: Samaritan (13th Century C.E.) with West-Syriac Reading (In Arabic) |
| `atg` Ivbie North-Okpela-Arhe | 3 | `ato` Atong | 100% | средняя | 37701: Atong – English Dictionary Second Edition |
| `alg`  | 3 | `alq` Algonquin | 100% | средняя | 2122897: Ka titc Jezos tebeniminang ondaje aking enansinaikatek masinaigan ki ojitogoban k |
| `luw` Luo (Cameroon) | 3 | `hlu` Luwian | 100% | средняя | 2098846: Corpus of Hieroglyphic Luwian Inscriptions: Volume III: Inscriptions of the Hitti |
| `kwa` Dâw | 3 | `kwd` Kwaio | 67% | средняя | 898089: Kwaio Dictionary |
| `tak` Tala | 3 | `tkm` Takelma | 67% | средняя | 108755: Takelma Texts |
| `phl` Palula | 3 | `ypa` Phala | 67% | средняя | 109837: A Grammar of Phala |
| `kum` Kumyk | 3 | `kdi` Kumam | 33% | средняя | 2139287: Kumam Vocabulary with Grammatical Notes |
| `yug` Yugh | 3 | `ybe` Yugur | 33% | средняя | 389303: The Western Yugur (Yellow Uygur) Language: Grammar, Texts, Vocabulary |
| `dar` North-Central Dargwa | 3 | `dry` Darai | 33% | средняя | 2108099: A Darai-English, English-Darai Glossary |
| `vai` Vai | 3 | `vap` Vaiphei | 100% | средняя | 840441: Vaiphei Pau Matdan Leh Thuphuak (Vaiphei Grammar & Composition) Part II |
| `pru` Iwaro | 3 | `prg` Prussian | 100% | средняя | 2113237: Old Prussian Elbing Vocabulary |
| `guy`  | 3 | `guf` Gupapuyngu | 33% | средняя | 793659: Gupapuyŋu-English Dictionary |
| `pao` Northern Paiute | 3 | `pac` Pacoh | 33% | средняя | 53531: Pacoh – Vietnamese – English Dictionary |
| `nso` Pedi | 3 | `nas` Naasioi | 33% | средняя | 896205: Nasioi Language Course |
| `koi` Komi-Permyak | 3 | `kpx` Mountain Koiali | 67% | средняя | 54980: Mountain Koiali – English Dictionary / English – Mountain Koiali Dictionary |
| `dhv` Dehu | 3 | `div` Dhivehi | 100% | средняя | 2108198: English - Dhivehi Dictionary / Dhivehi - English Dictionary: A guide to the langu |
| `hot` Hote | 3 | `yau` Hoti | 67% | средняя | 103882: Hoti Qomoon Ki Tameer Fikar Say Hoti He Hangamon Se Nahi By G A Parwez Publish By |
| `bou` Bondei | 3 | `pcc` Bouyei | 67% | средняя | 46679: Survey of the Guizhou Bouyei Language |
| `kuk` Kepo' | 3 | `gvn` Kuku-Yalanji | 100% | средняя | 839377: Kuku-Yalanji Dictionary |
| `tum` Tumbuka | 3 | `kho` Khotanese | 33% | средняя | 2107743: The Tumshugese Karmavācanā Text |
| `hry`  | 3 | `bgc` Haryanvi | 100% | средняя | 942418: Haryanvi Magazine Nohra |
| `bng` Benga | 3 | `gcc` Baining | 33% | средняя | 2932854: Mali (Baining) dictionary: Mali-Baining amēthamon angētha thēvaik |
| `rov`  | 3 | `rug` Roviana | 100% | средняя | 896058: Buka Hope: The Holy Bible in the Roviana language of the Solomon Islands |
| `hai`  | 3 | `tli` Tlingit | 33% | средняя | 2930715: Practical Grammar of Northern Haida: Level I |
| `bad`  | 3 | `bfq` Badaga | 33% | средняя | 896847: The Gospel of Mark in Badaga = Marka bareda lokaratcaagana kade |
| `cab` Garifuna | 3 | `cjp` Cabécar | 67% | средняя | 71930: Diccionario Cabécar-Español Español-Cabécar |
| `tek` Kwa South | 3 | `eme` Teko | 67% | средняя | 943884: Unknown (UD_Teko-TuDeT test set) |
| `aln` Gheg Albanian | 3 | `alq` Algonquin | 67% | средняя | 2122889: L'histoire sainte en algonquin |
| `iwj`  | 3 | `ibd` Iwaidja | 100% | средняя | 2120549: Text Specimen (Iwaidja) |
| `mrs` Maragus | 3 | `zrs` Mairasi | 67% | средняя | 2139325: FARIR MAIRAS NA'ATUEI: Perbendaharaan Kata Bahasa Mairasi / Mairasi Vocabulary |
| `mga`  | 3 | `mem` Mangala | 33% | средняя | 108742: Mangala Gauranga Lilamritam |
| `dah` Gwahatike | 3 | `dal` Dahalo | 100% | средняя | 296216: A Grammatical Sketch of Dahalo including texts and a glossary |
| `tlo` Tasomi-Tata | 3 | `tlr` Tolo | 100% | средняя | 895720: Tolo Dictionary |
| `nch` Central Huasteca Nahuatl | 3 | `ncz` Natchez | 67% | средняя | 389919: Natchez |
| `kay` Kamayurá | 3 | `txu` Kayapó | 33% | средняя | 389829: Gramática Pedagógica Kayapó |
| `dja`  | 3 | `dji` Djinang | 100% | средняя | 2125108: An Interim Djinang Dictionary |
| `krr`  | 3 | `kai` Karekare | 33% | средняя | 9342: Karekare-English-Hausa Dictionary, Second Edition |
| `inu`  | 3 | `moe` Innu (Montagnais) | 67% | средняя | 1090435: Essipit |
| `kht` Khamti | 3 | `kho` Khotanese | 100% | средняя | 2108243: The Khotanese Sudhanāvadāna |
| `sgo` Songa | 3 | `sag` Sango | 67% | средняя | 67896: A Grammar of Sango |

## 2. В документе другой язык

Метка указывает на язык, которого в документе нет, а сходства в названиях не видно. Обычно это та же беда с кодами, только неочевидная: например, `esg` (ахери-гонди) у староиспанской поэзии или `slb` (салуан) у старых словенских текстов. Бывают и прямые ошибки определения языка:

- **776437, «Saat Geet»** — сборник стихов Дхармавира Бхарати 1964 года на хинди, а метка `san:1`, только санскрит. Это так даже по аннотации самой модели. Около 2% «санскритских» документов выглядят так же.
- **694296, «TNLA-DB-05-1972…»** — стенограмма Законодательного собрания Тамилнада с меткой `one` (онейда, ирокезский язык).
- **105485, «C. Sallustii Crispi Opera»** — Саллюстий с английским подстрочником, метка `bil` (биле, Нигерия).

| Метка в корпусе | Документов | На самом деле | Доля в проверке | Уверенность | Пример документа |
|---|---:|---|---:|---|---|
| `sco` Scots | 533 | `sga` Early Irish | — | проверено вручную | 997948: Die Wiederauffindung der Táin Bó Cúalnge (Egerton 1782, fo. 87b) |
| `esg` Aheri Gondi | 57 | `osp` Old Spanish | — | проверено вручную | староиспанская поэзия — «Serranillas, canciones y decires», «Cantica de los clérigos de Ta |
| `kac` Southern Jinghpaw | 49 | `brx` Bodo | — | проверено вручную | 2121026: Collection of Kachari Folk-Tales and Rhymes, in Tended as a Supplement to Reveren |
| `zhn` Nong Zhuang | 43 | `trv` Seediq | — | проверено вручную | 917273: Toda Seediq Language Elementary Teaching Material of Daily Life |
| `okg` Koko Babangk | 37 | `fla` Kalispel-Pend d'Oreille | 84% | проверено вручную | 93356: Book 2 - A Beginning Course in Salish & Pend d’Oreille Dialect: Lesson 40 Horses an |
| `atq` Aralle-Tabulahan | 29 | `atj` Atikamekw | 83% | проверено вручную | 1091444: Pipikorikic |
| `unk` Enawené-Nawé | 19 | `crk` Plains Cree | — | проверено вручную | 1092559: Otcikaci |
| `moq` Mor (Bomberai Peninsula) | 16 | `moe` Innu (Montagnais) | 88% | проверено вручную | 2122083: Dictionnaire français-montagnais |
| `sax` Sa | 14 | `stq` Saterfriesisch | — | проверено вручную | 2133323: Vokalsystem |
| `slb` Kahumamahon Saluan | 13 | `slv` Slovenian | 54% | проверено вручную | 1044062: Večna pratika od gospodarstva |
| `myg` Manta | 13 | `omn` Minoan (Linear A) | 100% | проверено вручную | 2934259: Dictionary of Minoan (Fragment) |
| `ali` Amaimon | 7 | `ttt` Muslim Tat | — | проверено вручную | 841961: Talesi Tati Dictionary |
| `one` Oneida | 4 | `tam` Tamil | 25% | проверено вручную | 694296: TNLA-DB-05-1972-4-17-2-QH24 (1972-03-09) |
| `aar` Afar | 42 | `gaz` West Central Oromo | 76% | высокая | 1017967: Numbers (Oromo Translation) |
| `tcx` Toda | 16 | `tcy` Tulu | 100% | высокая | 897905: Tulu-English and English-Tulu dictionary |
| `yao` Yao | 14 | `tao` Yami | 71% | высокая | 848354: 雅美語學習手冊 第５階 Yami Tao Language Level 5. Students book |
| `sgs`  | 14 | `gle` Irish | 93% | высокая | 997984: Early Irish Lemmatizer Dictionary Updates (upd_28.05.txt) |
| `myn`  | 13 | `omn` Minoan (Linear A) | 77% | высокая | 2934356: Lexicon of Minoan Linear A (Excerpt) |
| `njo` Ao Naga | 13 | `njy` Njyem | 85% | высокая | 7821: Français — Njyem Dictionary |
| `euq`  | 9 | `eus` Basque | 89% | высокая | 1199221: Okzitaniako udalerri bat (Hérault) |
| `luh` Leizhou Chinese | 8 | `luo` Dholuo | 88% | высокая | 1017874: Ezra (Dholuo translation) |
| `naq` Nama (Namibia) | 7 | `nau` Nauru | 71% | высокая | 897530: Nuwawin Anea Evangelist Ngea Lucas |
| `bvu` Bukit Malay | 7 | `bzi` Bisu | 86% | высокая | 89705: Basaa-French Finderlist |
| `rkh` Rakahanga-Manihiki | 7 | `dru` Rukai | 100% | высокая | 820821: 東魯凱語學習手冊 第8階 (Taromak Rukai Language Learning Handbook Level 8) |
| `snb`  | 6 | `sna` Shona | 100% | высокая | 1093391: Zvinotungamirira Mukusarudza Zvido: Bhuku Rekushandisa Kudzidzisa Madzimai |
| `pae` Pagibete | 6 | `pbb` Páez | 100% | высокая | 83718: ¿Cómo Se Dice En Páez? Gramática Pedagógica Páez - Castellano |
| `ruq` Megleno-Romanian | 6 | `dru` Rukai | 100% | высокая | 820828: Taromak Rukai Language Elementary Teaching Material of Dail |
| `myc`  | 6 | `omn` Minoan (Linear A) | 100% | высокая | 2934114: Minoan Dictionary Entry: duty phyle |
| `afz` Obokuitai | 5 | `afr` Afrikaans | 80% | высокая | 67468: Soebatsfontein (Excerpt) |
| `onr` Northern One | 5 | `ono` Onondaga | 80% | высокая | 849077: Zeisberger's Indian dictionary, English, German, Iroquois--the Onondaga and Algonq |
| `cmk`  | 5 | `ccp` Chakma | 80% | высокая | 927901: Chakma meghulo-debar-ahji |
| `ota`  | 123 | `sgh` Shughni (Bartangi) | 33% | средняя | 1006638: Unknown (Fragment from Bartangi Corpus) |
| `avx`  | 69 | `tab` Tabasaran | — | средняя | 1191106: Вузари чпин ляхин манзилнаъди давам апIиди |
| `sah` Sakha | 17 | `fla` Kalispel-Pend d'Oreille | 35% | средняя | 93360: Seliš Sm̓im̓iʔ 2: A Beginning Course in Salish & Pend d’Oreille Dialect, Level 2 S |
| `nhe` Eastern Huasteca Nahuatl | 17 | `nez` Perce | 41% | средняя | 2112981: The Gift of Knowledge / Ttnúwit Átawish Nch'inch'imamí: Reflections on Sahaptin W |
| `ber`  | 16 | `sgh` Shughni (Bartangi) | 44% | средняя | 1006583: Unknown (Fragment from Bartangi Corpus) |
| `zhg`  | 15 | `mnc` Manchu | 40% | средняя | 841329: Xin bian fan yi Qing yu |
| `bfa` Bari | 13 | `sgh` Shughni (Bartangi) | 31% | средняя | 1006600: Unknown (Fragment from Bartangi Corpus) |
| `pqu`  | 13 | `poc` Poqomam | 69% | средняя | 108181: Sa rich’eet ak’ach chije’ la mama’ ak’ach |
| `khw` Khowar | 12 | `kas` Kashmiri | 42% | средняя | 770048: Keshav Prakash (Radha Swayamvar) |
| `zha`  | 12 | `txg` Tangut | 33% | средняя | 103389: Xixia Wen Dictionary |
| `sme` North Saami | 11 | `smj` Lule Saami | 36% | средняя | 943512: UD North Sami Giella Training Data (Fragment) |
| `tly` North-Central Talysh | 10 | `tcy` Tulu | 60% | средняя | 897910: Tulu-English Dictionary |
| `sks` Maia | 10 | `san` Sanskrit | 30% | средняя | 770935: Suttagame: Ekara Sangasaju (Part of the Jaina Sutragama) |
| `heo`  | 10 | `xpr` Parthian | 50% | средняя | 897461: Inscriptional Parthian Script (250 B.C.E.) with Hebrew Reading |
| `del`  | 10 | `ono` Onondaga | 40% | средняя | 849077: Zeisberger's Indian dictionary, English, German, Iroquois--the Onondaga and Algonq |
| `osx` Old Saxon | 10 | `osa` Osage | 40% | средняя | 1092524: Unknown (Fragment) |
| `aca` Achagua | 8 | `acr` Achi | 50% | средняя | 110324: Neologismos en Idioma Achi: Propuesta de palabras Creadas en el Idioma Maya Achi |
| `sck` Sadri | 8 | `pra` Prakrit | 38% | средняя | 783373: Suttagame |
| `zgh`  | 6 | `shi` Tachelhit | 50% | средняя | 853380: Tachelhit New Testament |
| `xal` Oirad-Kalmyk-Darkhat | 6 | `sgh` Shughni (Bartangi) | 33% | средняя | 1005184: Unknown (Fragment from Bartangi Corpus Project) |
| `mif` Mofu-Gudur | 6 | `miq` Miskito | 33% | средняя | 998808: Baibil stady ka kum (Bible Study) |
| `huz` Hunzib | 5 | `hch` Huichol | 60% | средняя | 849407: Glosario Wixarika |
| `guc` Wayuu | 5 | `yrl` Nhengatu | 40% | средняя | 22412: Dicionário Tupi-Guarani / Português |
| `amb` Ambo | 5 | `tpi` Tok Pisin | 60% | средняя | 2122661: Ambulas-Wosera-Mamu Dictionary: Wosera-Mamu, Tok Pisin, English |
| `bax` Bamun | 5 | `sgh` Shughni (Bartangi) | 60% | средняя | 1006611: Unknown (Fragment from Bartangi Corpus) |
| `lez` Lezgian | 5 | `tly` North-Central Talysh | 40% | средняя | 14858: Bir xalçanın rəngləriyik: Azərbaycan'da yaşayan xalqların ədəbiyyat antologiyası |
| `chx` Chantyal | 5 | `cic` Chickasaw | 60% | средняя | 2932766: A Dictionary of the Chickasaw Language (Excerpt) |
| `nvk`  | 5 | `gwi` Gwich'in | 40% | средняя | 43924: Athabaskan Language Studies (Excerpt on Gwich'in Modality) |
| `brx` Bodo-Mech | 5 | `brh` Brahui | 40% | средняя | 2108222: Brahui Texts: Glossed and Translated Short Stories and Folktales |
| `srr` Sereer | 5 | `sba` Ngambay | 60% | средняя | 72834: 50 Lessons in Sara-Ngambay, Volume 3: Final Report |
| `crl` Northern East Cree | 5 | `dri` C'lela | 60% | средняя | 73323: Rikoto Bulus Doro: Illustrated C'lela - English - Hausa Dictionary (Appendices) |
| `lil` Lillooet | 5 | `lis` Lisu | 40% | средняя | 90088: Lisu Het Kethuaddu (傈汉词典) |
| `pau` Palauan | 5 | `fuc` Pulaar | 40% | средняя | 841997: Pulaar Language Manual |
| `lun` Lunda | 5 | `unm` Unami | 40% | средняя | 92318: The Lenape / English Dictionary |
| `nuk` Nuu-chah-nulth | 4 | `noo` Nootka | 50% | средняя | 850911: A Short Cathechism and Hymnal Adapted to the Use of the Indians in the Language of |
| `ieo`  | 4 | `ile` Interlingue (Occidental) | 75% | средняя | 2122532: Li Lunatico: Su Paráboles e Poemas De Khalil Gibran Traductet in Interlingue (Occ |
| `syx` Osamayi | 4 | `shs` Shuswap | 75% | средняя | 2630: English - Shuswap Dictionary Version 2 |
| `sgh` Shughni | 4 | `gle` Irish | 75% | средняя | 997716: Gein Branduib maic Echach ocus Aedáin maic Gabráin |
| `omi` Omi | 4 | `oji` Ojibwe | 50% | средняя | 1092470: Omitcimiwoc (Fragment) |
| `aam` Aramanik | 4 | `gaz` West Central Oromo | 75% | средняя | 1017682: Yaa obboloota ko! (Fragment) |
| `abz` Abui | 4 | `ady` West Circassian | 50% | средняя | 626217: Nart Sagas from the Caucasus: Myths and Legends from the Circassians, Abazas, Abkh |
| `nax` Nakwi | 4 | `gld` Nanai | 50% | средняя | 70309: Impersonal Participle in Nanai |
| `onq`  | 4 | `ono` Onondaga | 75% | средняя | 849064: A French-Onondaga dictionary : from a manuscript of the seventeenth century |
| `bjd` Bandjigali | 4 | `bej` Beja | 100% | средняя | 944154: Beja Text (UD Corpus) |
| `fon` Fon | 4 | `ajg` Benin | 50% | средняя | 815979: Guide d'apprentissage en Fon |
| `bej` Beja | 4 | `bel` Belarusian | 50% | средняя | 2124283: Bielaruskaja hramatyka dla skol |
| `tdd` Tai Nüa | 4 | `tcx` Toda | 50% | средняя | 2112998: Toda Songs |
| `chb` Chibcha | 4 | `cay` Cayuga | 50% | средняя | 816927: A Glossary of Special Gayogohǫ:nǫˀ (Cayuga) Words and Particles, Thematically-Orga |
| `kic` Kickapoo | 4 | `oji` Ojibwe | 50% | средняя | 1092050: Pron kotc part_sub otci matce kicepwac... |
| `mvc` Mam, Central | 4 | `mnc` Manchu | 100% | средняя | 816193: A Concise Manchu-English Lexicon |
| `jdo`  | 4 | `lad` Ladino | 75% | средняя | 2133412: Kurso de Djudeo-Espanyol (Ladino) para Prinsipiantes / Course in Judeo-Spanish (L |
| `mwr`  | 3 | `vie` Vietnamese | 67% | средняя | 24532: Muong-Vietnamese-English Lexicon |
| `shw` Shwai | 3 | `shh` Shoshoni | 100% | средняя | 21365: Western Shoshoni Grammar |
| `sli` Lower Silesian | 3 | `stq` Saterfriesisch | 67% | средняя | 2133129: Seeltersk - Kurs (Saterfriesisch Course) |
| `gor` Gorontalo | 3 | `hac` Gawraǰūyī | 33% | средняя | 388270: The Gorani language of Gawraǰū, a village of West Iran: Texts, grammar, and lexico |
| `jeh` Jeh | 3 | `khm` Central Khmer | 33% | средняя | 851964: Jeh Vocabulary |
| `jpx`  | 3 | `jpn` Japanese | 100% | средняя | 2098684: The Eastern Old Japanese Corpus and Dictionary |
| `saw` Sawi | 3 | `sac` Sauk | 33% | средняя | 103852: A Concise Dictionary of the Sauk Language |
| `sxt`  | 3 | `frr` Northern Frisian | 100% | средняя | 2133324: Vokalsystem |
| `luy`  | 3 | `lwg` Wanga | 33% | средняя | 39701: Wanga-English Dictionary |
| `tka` Truká | 3 | `eme` Teko | 33% | средняя | 944114: Teko Popor Ho (Narrative Text) |
| `kbp` Kabiyé | 3 | `arr` Karo | 67% | средняя | 944079: Karo UD Corpus Text (Fragment) |
| `akl` Aklanon | 3 | `knj` Akateko | 33% | средняя | 106215: Vocabulario de flora y fauna Akateko-Español |
| `tjr`  | 3 | `ssf` Thao | 100% | средняя | 839266: 邵語學習手冊 第３階 (Thao Language Level 3 Students Book) |
| `kam` Kamba (Kenya) | 3 | `kik` Kikuyu | 33% | средняя | 490259: Mein Kya kya Dikhai Deta (Mixed Religious and Social Media Texts) |
| `mrw` Maranao | 3 | `rmz` Marma | 67% | средняя | 106540: Upajatiyo Rupkotha Lokakahini Ebong Kingbodonti (Dwitiyo Khondo) |
| `ala` Alago | 3 | `moe` Innu (Montagnais) | 33% | средняя | 1090859: Mélissa Mollen-Dupuis |
| `efi` Efik | 3 | `ibo` Igbo | 33% | средняя | 72158: Ikpo Nsibidi-Igbo-English Dictionary |
| `nng` Maring Naga | 3 | `nnh` Ngiemboon | 33% | средняя | 7671: Dictionnaire Ngiemboon-Français |
| `esl` Egypt Sign Language | 3 | `ymh` Mili | 33% | средняя | 110081: Unknown (OCR corrupted) |
| `oto`  | 3 | `oji` Ojibwe | 33% | средняя | 1092551: Ototokon pisimw (Fragment) |
| `crw` Chrau | 3 | `cre` Cree | 33% | средняя | 1091796: Sasakamoose (Fragment) |
| `rar` Southern Cook Island Maori | 3 | `mrq` Marquesan | 33% | средняя | 388437: Grammaire et Dictionnaire de la Langue des Iles Marquises (Marquisien-Français) |
| `crm` Moose Cree | 3 | `oji` Ojibwe | 67% | средняя | 1092179: Mariette Niquay (Fragment) |
| `lfn` Lingua Franca Nova | 3 | `fur` Friulian | 33% | средняя | 2109003: Saggi ladini |
| `peu`  | 3 | `sgh` Shughni (Bartangi) | 100% | средняя | 1006648: Bartangi Corpus Project: Sentence 6538 |
| `snh` Shinabo | 3 | `sna` Shona | 100% | средняя | 1093390: Tsika dzaVaShona |
| `gax` Borana-Arsi-Guji Oromo | 3 | `grt` Garo | 67% | средняя | 2121819: The School Dictionary: Garo to English |
| `bjn` Banjar | 3 | `bbc` Batak Toba | 33% | средняя | 490311: NLLB_bjn.txt.gz (Fragmented Text Corpus) |
| `zht`  | 3 | `kho` Khotanese | 67% | средняя | 2108256: Khotanese Texts I-III |
| `gen` Geman Deng | 3 | `big` Biangai | 67% | средняя | 108256: Biangai Genesis Translation |
| `sav` Saafi-Saafi | 3 | `tel` Telugu | 67% | средняя | 850149: Telugu-Savara Dictionary |
| `isg` Irish Sign Language | 3 | `isl` Icelandic | 100% | средняя | 2098203: An Icelandic Primer with Grammar Notes and Glossary |
| `skx` Seko Padang | 3 | `skb` Saek | 67% | средняя | 848890: The Saek Language: Glossary, Texts, and Translations |
| `zlm` Central Malay | 3 | `tvk` Southeast | 33% | средняя | 1004868: patišyṓn |
| `mme` Tirax | 3 | `mqy` Manggarai | 100% | средняя | 924420: Kamus Manggarai II: Indonesia - Manggarai |
| `blc` Bella Coola | 3 | `nut` Tày-Nùng | 33% | средняя | 73012: Từ điển Tày-Nùng - Việt |
| `yap` Yapese | 3 | `tao` Yami | 67% | средняя | 848355: 雅美語學習手冊 第９階 Yami Tao Language Level 9. Students book |
| `ahk` Akha | 3 | `mar` Marathi | 33% | средняя | 850154: Ahirani Dhol (Issue 1, 1998) |
| `ick`  | 3 | `cad` Caddo | 33% | средняя | 1091837: Ickwatem Text Fragment |
| `dga` Central Dagaare | 3 | `kuu` Upper Kuskokwim | 33% | средняя | 38527: Dinak'i - English Dictionary |
| `nde` Zimbabwean Ndebele | 3 | `nnb` Kinande | 33% | средняя | 8217: Kinande-Konzo-English Dictionary with an English Kinande-Konzo Index |
| `twr` Southwestern Tarahumara | 3 | `tya` Tauya | 33% | средняя | 2108362: A Dictionary of Tauya |
| `nhi` Zacatlán-Ahuacatlán-Tepetzintla Nahuatl | 3 | `cre` Cree | 33% | средняя | 1092348: Nehiroaski |

## 3. Перепутаны родственные или соседние языки

Здесь модель путает языки, которые часто встречаются вместе или близки по письму:

- **дари ↔ пушту**: у ~500 из 974 документов с меткой `prs` (дари) аннотация говорит о пушту. Та же картина у `fas` и `pes` (по ~15–20%).
- **цоциль ↔ цутухиль** (`tzo`, `tzu` → `tzj`), **киче ↔ какчикель / кекчи**;
- **«Muslim Tat» ↔ татарский** (`ttt` → `tat`): это татарские тексты, а татский — иранский язык;
- **макроязык ↔ отдельный язык**: `aym` → `ayc`, `rom` → `rmy`.
- **`avx`**: аннотации модели называют аварский, но по словоформам (*апIиди*, *ляхин*) тексты похожи на табасаранский. Это пример того, что и аннотации могут ошибаться, поэтому код оставлен на ручную проверку.

| Метка в корпусе | Документов | На самом деле | Доля в проверке | Уверенность | Пример документа |
|---|---:|---|---:|---|---|
| `prs` Dari | 974 | `pus` Pashto | 50% | средняя | 998787: زما ژوند، لیکوالي او شاعري (My Life, Writing and Poetry) |
| `ttt` Muslim Tat | 102 | `tat` Tatar | 57% | средняя | 1098378: Гошалалар |
| `tzo` Tzotzil | 31 | `tzj` Tz'utujil | 55% | средняя | 109414: Jugando con sonidos y palabras: Tz’ajneem ruk’iin taq qulaaj k’in taq tziij (3.º G |

## 4. Не та историческая стадия языка

Код указывает на другую эпоху того же языка или на исторический язык вместо современного:

- `goh` (древневерхненемецкий, 750–1050 гг.) — немецкие стихи и проза XVI–XVII веков, 251 из 344 документов;
- `grc` (древнегреческий) — треть документов посвящена минойскому линейному письму A;
- `ang` (древнеанглийский) и `sco` (скотс) — ирландские саги (*Táin Bó Cúalnge*, *Tromdámh Guaire*);
- `peo` (древнеперсидский) — фрагменты Bartangi Corpus и новоперсидские тексты;
- в описываемых языках: «Old Javanese (Kawi)» под кодом `jav` вместо `kaw`, «Old Hindi» под `hin`, «Old Western Rajasthani» под `guj`.

| Метка в корпусе | Документов | На самом деле | Доля в проверке | Уверенность | Пример документа |
|---|---:|---|---:|---|---|
| `goh` Old High German (ca. 750-1050) | 344 | `deu` German | — | проверено вручную | ранненововерхненемецкие тексты XVI–XVII вв. — 251 из 344 аннотаций: немецкий; «Gedichte…», |
| `peo` Old Persian (ca. 600-400 B.C.) | 148 | `sgh` Shughni (Bartangi) | — | проверено вручную | фрагменты Bartangi Corpus и персидские тексты — 143 из 148 аннотаций: персидский; примеры  |
| `grc` Ionic-Attic Ancient Greek | 404 | `omn` Minoan (Linear A) | 33% | средняя | 2934442: Unknown Fragment (Minoan/Linear A context) |
| `ang` Old English (ca. 450-1100) | 102 | `gle` Irish | 53% | средняя | 997949: Wiederauffindung der Táin Bó Cúalnge (RIA MS D42, fo. 49b2) |

## 5. Выдуманное название языка (Described)

На одном источнике (файлы `PREPROCESSED_*.txt` со списками слов и тегами `part_sub`, `part_quan`) модель берёт слово из названия файла, объявляет его языком и сама придумывает, к какой группе он относится. Таких языков нет ни в Glottolog, ни в ISO 639-3.

| Документ | «Язык» по модели | Объяснение модели | Код Described | Код Written in | Что это, вероятно |
|---|---|---|---|---|---|
| 1092259 «Mikoapi Lexical Data» | Mikoapi | «язык Mikoapi» | `chr` (чероки) | `eng` | фрагмент словаря атикамек или кри |
| 1092646 «Pickowan Vocabulary List» | Pickowan | «диалект оджибве» | `otw` | `eng` | то же |
| 1092411 «PREPROCESSED_Ocacamekw.txt» | Ocacamekw | «диалект микмак» | `mic` | `ocm` (древнечамский) | то же |
| 1091720 «Patak Mantcoc» | Mantoc / Patak Mantcoc | «разновидность Pamagong» (такого языка тоже нет) | `mnc` (маньчжурский) | `pam` (капампанган) | то же |
| 1091710 «Cikotai Grammar Data» | Cikotai | «язык Cikotai» | `cic` (чикасо) | `eng` | то же |

Сами тексты я не открывала. Вывод «вероятно, атикамек или кри» сделан по соседним файлам того же источника, которые размечены как `atj`, `crj` и `crk`.

## 6. Название и код описываемого языка расходятся (Described)

В списке описываемых языков пара «glottocode / ISO» не совпадает с названием, которое пишет модель. Это та же ошибка с кодами, что в п. 1–3, но в поле Described.

| Код | Язык по коду (ISO 639-3) | Название, написанное моделью | Что, вероятно, имелось в виду |
|---|---|---|---|
| `dba` | бангиме (изолят) | Dogon | догонские языки |
| `wne` | ванеци | Pashto | пушту (`pus`) |
| `slq` | салчук | Azerbaijani | азербайджанский (`azj`) |
| `crh` | крымскотатарский | Meskhetian Turkish | месхетинско-турецкий |
| `ojs` | северноболотный оджибве | Cree | кри |
| `kxm` | северокхмерский | Khmer | кхмерский (`khm`) |
| `kic` | кикапу | Oto | отоэ (`iow`) |
| `ikw` | икверре | Ik | ик (`ikx`) |
| `bss` | акосе | Basaa | баса (`bas`) |
| `lkt` | лакота | Nakota | накота (`asb`) |
| `yao` | яо (Малави) | Yao'an Lolo | яоань-лоло (лолойские языки) |
| `hns` | карибский хиндустани | Hindustani | хиндустани / хинди-урду |
| `chr` | чероки | Mikoapi | выдуманный язык, см. п. 5 |
| `sna` | шона | Tebela | ндебеле (Tebele) |
| `kab` | кабильский | Zenatia (Mzab, Ouargla, Oued-Rir dialects) | зенатские берберские языки |
| `shi` | ташельхит | Tashelhit (Aokas dialect) | аокас — кабильский говор |

Сюда же относится документ **845046, «Dictionary of the Tebele & Shuna languages»**. Как описываемый язык там записан «Tebela» с кодом `sna`, что близко к правде. Но в «Written in» стоят `tbe` (танимбили, Соломоновы острова) и `shn` (шанский, Мьянма). На самом деле словарь ндебеле (`nde`) и шона (`sna`).

## 7. Несколько языков слиты в одно название (Described)

Модель пишет в поле одного описываемого языка сразу несколько, а код берёт по первому. Остальные языки при этом теряются.

| Код | Название, записанное моделью |
|---|---|
| `spa` | Spanish; Portuguese; Italian; French |
| `tam` | Tamil, Sinhala |
| `sin` | Sinhala, Tamil |
| `amh` | Amharic, Arabic |
| `tur` | Turkish, Armenian, English |
| `kat` | Georgian, Megrelian, Laz, Svan |
| `mal` | Malayalam, English, Telugu |
| `hil` | Kinaray-a, Hiligaynon, Aklanon, Capiznon, Ilonggo, Loocnon, Odionganon, Romblom |
| `ben` | Gaurian languages (including Bengali, Assamese, Oriya, etc.) |
| `osc` | Sabellic languages (Oscan, Umbrian, South Picene) |

## 8. Второстепенный язык засчитан как язык документа

В «Written in» перечислены все языки документа, и каждый из них увеличивает счётчик своего языка. Обычно основной язык указан правильно, но в выборку по языку попадают учебники, грамматики и словари, где этот язык встречается только в примерах. Пример — **2111086, «Introduction to Hindi Grammar»**: `eng: 0.95`, `hin: 0.05`, документ при этом считается хинди. Полная таблица — в [`data/inflated_counts.csv`](data/inflated_counts.csv), ниже первые 30 строк.

| Код | Язык | Документов в счётчике | Язык основной | Оценка «настоящих» | Основной язык у остальных |
|---|---|---:|---:|---:|---|
| `eng` | English | 409970 | 38% | 155789 | rus:473 deu:39 por:27 ukr:23 |
| `rus` | Russian | 43373 | 78% | 33831 | tyv:215 lat:2 kaa:1 tat:1 |
| `tam` | Tamil | 50867 | 84% | 42728 | eng:156 |
| `guj` | Gujarati | 33900 | 88% | 29832 | eng:120 peo:1 |
| `hin` | Hindi | 8106 | 58% | 4701 | san:279 eng:113 urd:6 pli:4 |
| `fra` | French | 4983 | 65% | 3239 | eng:167 rus:48 deu:24 por:18 |
| `spa` | Spanish | 7524 | 88% | 6621 | por:17 eng:11 eus:10 que:5 |
| `lat` | Latin | 2549 | 70% | 1784 | eng:64 slv:31 ang:26 sga:26 |
| `gwi` | Gwich'in | 820 | 52% | 426 | eng:394 lat:1 |
| `heb` | Modern Hebrew | 356 | 24% | 85 | yid:177 eng:79 kor:4 spa:3 |
| `zho` |  | 594 | 56% | 333 | eng:151 puy:12 ami:10 fra:8 |
| `ita` | Italian | 1288 | 83% | 1069 | eng:74 san:16 rus:13 deu:10 |
| `fas` |  | 458 | 56% | 256 | prs:116 eng:46 peo:9 san:9 |
| `bod` | Tibetan | 294 | 40% | 118 | eng:133 san:34 zho:4 deu:2 |
| `mar` | Marathi | 717 | 79% | 566 | san:99 eng:47 guj:1 kan:1 |
| `ind` | Standard Indonesian | 539 | 73% | 393 | eng:117 ace:4 min:3 tet:3 |
| `jpn` | Japanese | 368 | 64% | 236 | eng:97 deu:6 spa:6 rus:3 |
| `ben` | Bengali | 468 | 72% | 337 | eng:59 san:58 hin:6 ara:4 |
| `nld` | Dutch | 467 | 72% | 336 | eng:37 fry:11 fra:11 sax:9 |
| `tsg` | Tausug | 325 | 60% | 195 | eng:126 khm:2 zho:1 |
| `cmn` | Mandarin Chinese | 342 | 63% | 215 | eng:110 fra:4 rus:3 jpn:1 |
| `chc` | Catawba | 479 | 75% | 359 | eng:119 spa:2 |
| `pes` | Western Farsi | 195 | 43% | 84 | prs:87 eng:14 rus:3 kmr:2 |
| `tur` | Turkish | 602 | 82% | 494 | eng:50 deu:10 rus:9 aze:9 |
| `pol` | Polish | 936 | 89% | 833 | eng:54 lit:9 deu:8 ukr:7 |
| `tel` | Telugu | 461 | 78% | 360 | eng:63 san:32 gon:2 fra:1 |
| `grc` | Ionic-Attic Ancient Greek | 404 | 75% | 303 | eng:52 deu:14 fra:9 lat:8 |
| `nep` |  | 400 | 75% | 300 | eng:77 san:16 dan:2 ben:1 |
| `urd` | Urdu | 888 | 89% | 790 | eng:49 san:13 hin:12 fas:3 |
| `syr` |  | 129 | 25% | 32 | eng:85 ara:3 sam:3 lat:1 |

## 9. Коды не нормализованы

| Вид кода | Примеры | Что делать |
|---|---|---|
| ISO 639-2/B вместо 639-3 | `ger` (2 056), `dut`, `rum`, `chi`, `tib`, `bur`, `arm`, `alb`, `mac`, `geo`, `baq` | заменить на `deu`, `nld`, `ron`, `zho`, `bod`, `mya`, `hye`, `sqi`, `mkd`, `kat`, `eus` |
| Коды семей и групп (ISO 639-5) | `inc`, `sla`, `nah`, `ber`, `nub`, `myn`, `sai`, `kar`, `alg`, `apa`, `bat` … (39 кодов) | разметить вручную до конкретного языка |
| Частные коды `qaa–qtz` | `qan`, `qeq`, `qpa` | `qan` → `kjb` (канхобаль), `qeq` → `kek` (кекчи), `qpa` — разметить вручную |
| Служебные | `und` (33 265), `mis`, `mul`, `zxx` | `und` — в основном PDF без извлечённого текста, их надо переизвлечь |
| Макроязык рядом с отдельным языком | `ara`/`arb`, `zho`/`cmn`, `fas`/`pes`, `msa`/`zsm`, `nep`/`npi`, `aze`/`azj`, `est`, `yid` | выбрать один уровень (лучше отдельный язык) |

## 10. Язык приписан не-тексту или битому тексту

| Код | Проблема | Масштаб |
|---|---|---|
| `und` | PDF из коллекции грамматик, из которых не извлёкся текст | 33 265 документов |
| `gwi` | GIF-картинки | 749 из 820 |
| `udm` | битая кодировка (cp1251, прочитанная как latin-1) | 10 из 25 проверенных TXT |
| `ady` | списки слов с POS-тегами вместо связного текста | все проверенные TXT |
| `tyv`, `ukr` | нижний регистр без пунктуации (выгрузки из Википедии) | `ukr`: 22 из 25 TXT |

## 11. Доли языков — округлённые прикидки

Поле `share` у многоязычных документов почти всегда принимает одно из немногих значений: 0.8 / 0.2, 0.95 / 0.05, 0.5 / 0.5, реже 0.4 / 0.4 / 0.2. По нему можно отличить основной язык от второстепенного, но посчитать реальный объём текста на языке нельзя.

---

## CSV с предлагаемыми исправлениями

**[`data/proposed_corrections_by_code.csv`](data/proposed_corrections_by_code.csv)** — одна строка на подозрительный код (997 кодов):

| Колонка | Что значит |
|---|---|
| `label_code`, `label_name` | метка в корпусе и официальное название этого кода |
| `docs_in_catalogue`, `docs_checked` | сколько документов с меткой и сколько проверено (до 2000) |
| `label_confirmed_pct` | доля документов, где название или аннотация называет язык метки |
| `other_language_pct` | доля документов, где назван только другой язык |
| `proposed_code`, `proposed_name`, `proposed_share_pct` | предлагаемый код и доля документов, за которые он «голосует» |
| `error_type` | тип ошибки из этого файла |
| `confidence` | `verified` — проверено вручную, `high` — ≥ 70% документов за одну замену и ≥ 5 документов, `medium` — ≥ 30%, `low` — замену не предлагаем |
| `other_candidates`, `example`, `manual_note` | другие кандидаты, пример документа, заметка ручной проверки |

**[`data/proposed_corrections_by_document.csv`](data/proposed_corrections_by_document.csv)** — одна строка на документ из подозрительных кодов (9 036 документов). Здесь `proposed_written_languages` — новый список языков документа: неверная метка заменена, остальные языки сохранены. Колонка `confidence`:

- `keep` — метка подтверждается, менять не надо;
- `high` — в аннотации назван другой язык, и он же предложен для всего кода с высокой уверенностью;
- `medium` — в аннотации назван другой язык;
- `low (by code)` — в аннотации язык не назван, замена взята из исправления для всего кода;
- `review` — нужна ручная проверка.

Предложения сделаны по названию и аннотации, которые писала та же модель. Это подсказки для ручной правки, а не готовая разметка. Тексты документов автоматически не проверялись.
