import requests
import json

def get_word(word):
    url = "https://relatedwords.org/api/related?term=" + word
    res = requests.get(url)

    release = res.json()

    val = []
    
    # score 기반으로 단어를 추출   
    for i in release:
        if i['score'] is None:
            continue
        elif i['score']>=0.5:
            val.append(i['word'])
    
    return val

# 기본 단어
category = ["child porn", "hosting", "bitcoin", "drug", "counterfeit", "murder", "hack", "weapon"]
category_word = {}

for item in category:
    category_word[item] = get_word(item)

# 영어
enC = {
    'child porn': ['child sexual abuse', 'child', 'interpol', 'united states department of justice', 'pornography', 'video', 'sound recording', 
                    'minor', 'pedophilia', 'child grooming', 'european commission', 'internet watch foundation', 'united states reports', 'law', 
                    'photograph', 'sculpture', 'drawing', 'photography', 'painting', 'animation', 'coercion', 'censorship', 'clothing', 'lolicon', 
                    'nudity', 'camera', 'massachusetts', 'recording'],

    'hosting': ['hostess', 'emcee', 'legion', 'hospitality', 'master of ceremonies', 'guest', 'compere', 'server', 'innkeeper', 'horde', 'army', 
                'entertain', 'multitude', 'entertainer', 'recipient', 'organization', 'receiver', 'venue', 'presenter', 'series', 'boniface', 'bread', 
                'junket', 'feast', 'banquet', 'ringmaster', 'sullivan', 'medicine', 'being', 'computing', 'organism', 'adult', 'computer', 'victualler', 
                'concourse', 'throng', 'organisation', 'padrone', 'toastmaster', 'patron', 'hosts', 'hosting', 'hosted', 'breadstuff', 'symposiarch', 
                'grownup', 'quizmaster', 'victualer', 'sabaoth', 'friendly', 'conference', 'event', 'upcoming', 'weekend'],

    'bitcoin': ['blockchain', 'currency', 'bitcoin network', 'cryptography', 'node', 'satoshi nakamoto', 'open-source software', 'cryptocurrency wallet', 
                'cryptocurrency exchange', 'cryptocurrency', 'public-key cryptography', 'ethereum', 'qt', 'central bank', 'distributed ledger', 
                'university of cambridge', 'nobel memorial prize in economic sciences', 'gavin andresen', 'silk road', 'youtube', 'segwit', 'kraken', 
                'ledger', 'financial crimes enforcement network', 'forth', 'double-spending', 'lightning network', 'bitcoin cash', 'unit of account', 
                'digital signature', 'cryptographic hash', 'megabyte', 'winklevoss twins', 'synchronization', 'bitcoin xt', 'baidu', 'proof-of-concept', 
                'cve', 'leveldb', 'nyse', 'micropayment', 'openssl', 'andreas antonopoulos', 'bitinstant', 'unicode', 'broadcasting', 'banknote', 'malleability'],

    'drug': ['medicine', 'dope', 'psychoactive drug', 'medication', 'dose', 'stimulant', 'narcotic', 'injectable', 'pharmaceutical', 'pharmacy', 'analgesic', 
            'prescription', 'prescription drug', 'alcohol', 'drop', 'absorption', 'antisyphilitic', 'abortifacient', 'medicate', 'addiction', 'medicament', 
            'aspirin', 'tobacco', 'cannabis', 'fertility drug', 'narcotize', 'pharmaceutical drug', 'smoking', 'magic bullet', 'generic', 'antiviral', 'pharmacist', 
            'preventive medicine', 'physician', 'benzodiazepine', 'do drugs', 'anticonvulsant', 'antidrug', 'generic drug', 'antiemetic', 'probenecid', 'antidepressant', 
            'antibiotic', 'illegal', 'cocaine', 'marijuana', 'psychoactive substance', 'opiate', 'narcotics', 'heroin', 'amphetamine', 'methamphetamine', 'drug class',
            'pills', 'medicines', 'chemical structure', 'mechanism of action', 'caffeine', 'vaccine', 'steroids', 'mode of action', 'cancer',
            'anatomical therapeutic chemical classification system', 'atc code', 'biopharmaceutics classification system', 'hallucinogen', 'drug addiction',
            'recreational drug use', 'single convention on narcotic drugs', 'who', 'over-the-counter drug', 'ingestion', 'substance', 'druggist', 'pharmacology',
            'antihistamine', 'organism', 'codeine', 'anticholinergic', 'antibacterial', 'anticoagulant', 'biomedicine', 'chronic', 'immunology', 'prodrug',
            'paregoric', 'food', 'apc', 'oncology', 'therapeutic', 'rheumatology', 'gastroenterology', 'anesthesiology', 'placebo', 'radiotherapy', 'insufflation',
            'hypnotic', 'agent', 'relaxant', 'arsenical', 'pharmacopoeia', 'diuretic', 'botanical', 'overdose', 'orally', 'agonist', 'anaphylaxis', 'antagonist',
            'anesthetic', 'trip', 'anaesthetic', 'excitant', 'soporific', 'poison', 'base', 'use', 'inject', 'snort', 'nephrology', 'drugs', 'purgative', 'palliative',
            'neurology', 'nonspecific', 'panacea', 'therapy', 'pcp', 'clinician', 'laxative', 'urology', 'penicillin', 'curative', 'nostrum', 'remedy', 'medical',
            'virology', 'dermatology', 'pediatrics', 'catatonic', 'psychiatry', 'gynecology', 'medic', 'nondrug', 'peptic', 'insulin', 'sedation', 'paracetamol',
            'refractory', 'dispensary', 'pharmaceutic', 'neurologist', 'allopurinol', 'tiamulin', 'antidiabetic', 'acyclovir', 'opium', 'disulfiram', 'pentylenetetrazol',
            'antispasmodic', 'carminative', 'gemfibrozil', 'antidiarrheal', 'decongestant', 'antiprotozoal', 'expectorant', 'md', 'splint', 'premedication', 'antitussive',
            'pharmacon', 'physostigmine', 'psychotic', 'isoproterenol', 'medicinal', 'isosorbide', 'amrinone', 'antiarrhythmic', 'potentiation', 'perception',
            'immunosuppressant', 'fever', 'clofibrate', 'medicative', 'vermifuge', 'antipyretic', 'sucralfate', 'antihypertensive', 'psychomedicine', 'anticholinesterase',
            'mood', 'neurotropic', 'postdrug', 'parenteral', 'premedical', 'neuropsychiatry', 'clonic', 'azathioprine', 'aesculapian', 'venesect', 'traumatology',
            'nonprescription', 'urinalysis', 'vermicide', 'penicillamine', 'proctology', 'consciousness', 'lorfan', 'anaesthetize', 'anaesthetise', 'free-base', 'anesthetize',
            'uninjectable', 'habituate', 'narcotise', 'potentiate', 'aborticide', 'synergist', 'suppressant', 'dilator', 'feosol', 'fergon', 'o.d.', 'intoxicant', 'trental',
            'levallorphan', 'pentoxifylline', 'mydriatic', 'myotic', 'miotic', 'anesthetise', 'podiatry', 'papaverine', 'hematinic', 'leechcraft', 'counterirritant', 'ethanol',
            'ethnomedicine', 'suppository', 'mfm', 'pseudomedical', 'iatrophysics', 'polychrest', 'nonmedical', 'noninvasive', 'antidiuretic', 'infection', 'depressant',
            'nosology', 'wonderdrug', 'pulmonology', 'bronchodilator', 'panpharmacon', 'nicotine', 'nanomedicine', 'trafficking', 'achromia', 'vasoconstrictor', 'oxytocic',
            'phytomedicine', 'succedaneum', 'unguent', 'traffickers', 'digitalize', 'cases', 'zymosis', 'mercurialist', 'rubefacient', 'otology', 'treatment', 'hiv',
            'tylenol', 'medications', 'aids', 'linked', 'smuggling'],
    
    'counterfeit': ['fake', 'false', 'phony', 'bogus', 'forgery', 'spurious', 'sham', 'pseudo', 'imitation', 'scam', 'fraud', 'fictitious', 'forged', 'phoney',
                    'identity theft', 'unreal', 'insincere', 'handbags', 'forge', 'imitative', 'illegal', 'base', 'bastard', 'fictive', 'mock', 'synthetic', 'assumed',
                    'pretended', 'pinchbeck', 'bad', 'ostensible', 'fraudulent', 'unauthentic', 'inauthentic', 'ostensive', 'pirated', 'contraband', 'smuggled', 'put on',
                    'confiscated', 'heroin', 'printing', 'forgeries', 'stolen', 'cocaine', 'illicit', 'counterfeiters', 'banknotes', 'methamphetamine', 'theft', 'jewelry',
                    'illegally', 'marijuana', 'coins', 'narcotics', 'jewellery', 'knockoffs', 'united states secret service', 'sale', 'currency', 'document', 'clothing',
                    'shoes', 'falsely', 'falsification', 'pharmaceutical', 'artificial', 'falsity', 'manufacture', 'falseness', 'deception', 'mendacious', 'watch',
                    'deceit', 'falsify', 'imposture', 'dishonesty', 'untruthful', 'falsehood', 'mendacity', 'charlatan', 'untruth', 'electronics', 'feign', 'delusive',
                    'untrue', 'mislead', 'deceitful', 'deceiver', 'deceive', 'delude', 'imposter', 'deceptive', 'software', 'delusion', 'hoax', 'misrepresentation',
                    'trickery', 'fib', 'swindle', 'duplicity', 'dupe', 'liar', 'impostor', 'misrepresent', 'lig', 'art', 'lie', 'defraud', 'cozen', 'chicanery', 'perjure',
                    'bilk', 'humbug', 'subterfuge', 'forger', 'bask', 'ingenuine', 'cheat', 'deceptively', 'toys', 're-create', 'jugglery', 'pretense', 'trickster', 'guile',
                    'bamboozle', 'faithlessness', 'swindler', 'falsifier', 'belie', 'fallacious', 'movies', 'insincerity', 'dissimulate', 'perjury', 'amuser', 'unfaithful',
                    'hocus', 'cheater', 'gullible', 'trick', 'fraudulence', 'shlenter', 'fraudster', 'logos', 'blench', 'mendaciously', 'beguile', 'treacherous',
                    'embezzlement', 'counterfeiting', 'waylay', 'fakery', 'flimflam', 'whopper', 'brands', 'pretender', 'deceptiveness', 'laity', 'layoff', 'fibbery',
                    'prevarication', 'hoodwink', 'falsifiable', 'decipiency', 'mislie', 'unlying', 'blag', 'perjurer', 'adulterous', 'counterfeits', 'falsificationism',
                    'gull', 'rort', 'fool', 'dupery', 'importing', 'forlay', 'finagler', 'copying', 'overreach', 'chouse', 'prevaricate', 'forlie', 
                    'imported', 'befool', 'fakes', 'import', 'hornswoggle', 'blesh', 'undeceive', 'belirt'],
    
    'murder': ['homicide', 'manslaughter', 'assassination', 'infanticide', 'suicide', 'crime', 'slay', 'slaying', 'kill', 'common law', 'hit', 'bump off', 'dispatch',
                'revenge', 'massacre', 'parricide', 'murderer', 'filicide', 'killer', 'thuggee', 'genocide', 'california', 'mutilate', 'remove', 'mangle', 'slaughter', 
                'mariticide', 'carnage', 'regicide', 'fratricide', 'jurisdiction', 'tyrannicide', 'bloodshed', 'uxoricide', 'execution', 'butchery', 'polish off', 'burke',
                'mass murder', 'murderess', 'execute', 'felony', 'victim', 'lynching', 'decapitation', 'patricide', 'kidnapping', 'robbery', 'canada', 'serial killer',
                'matricide', 'criminal', 'first degree murder', 'arrest', 'strangulation', 'death', 'abduction', 'conspiracy', 'accomplice', 'conviction', 'killing',
                'molestation', 'suspects', 'strangler', 'arson', 'prosecution', 'sentence', 'treason', 'imprisonment', 'disappearance', 'burglary', 'prosecutors', 'extortion',
                'assault', 'united states', 'defendant', 'malice aforethought', 'self defense', 'country', 'aggravation', 'off', 'person', 'justification', 'excuse',
                'assassinate', 'homicidal', 'slayer', 'assassin', 'murderous', 'deterrence', 'rehabilitation', 'law', 'bloodbath', 'oppression', 'cide', 'decimate', 'slaughterer', 'lynch', 'liquidation', 'distort', 'gore', 'elimination', 'falsify', 'warp', 'exterminator', 'saber', 'poisoner', 'murderee', 'slaught', 'killingly', 'unslain', 'euthanasia', 'murdersome', 'electrocute', 'killbot', 'combatants', 'instakill', 'murderable', 'poison', 'criminalization', 'killable', 'fetus', 'lethal', 'murders', 'vagina', 'electrocution', 'horizontalize', 'accident', 'convicted', 'teamkill', 'guilty', 'obliterable', 'nonkilling', 'manslaying', 'proto-indo-european', 'exterminate', 'garble', 'dry-gulching', 'shoot-down', 'bane', 'anglo-saxon', 'lethality', 'trial', 'sororicide', 'sentenced', 'acquitted', 'pleaded', 'magistricide', 'eradication', 'decimation', 'avenge', 'charged', 'alleged', 'charges', 'butcher', 'poisoning', 'insanity', 'killings', 'crimes', 'murdering', 'self-defence', 'executioner', 'photokilling', 'killjoy', 'confessed', 'invincible', 'non-combatants', 'vengeance', 'winterkill', 'suspect', 'counts', 'precedent', 'killers', 'maniac', 'arrested', 'case', 'codification', 'killology', 'legal', 'democide', 'slaughterhouse', 'cadaver', 'witness', 'innocent', 'stabbing', 'organism', 'murdered', 'theft', 'indictment', 'jail', 'toxin', 'custody', 'femicide', 'simpson', 'slaughterman', 'indicted', 'butch', 'venom', 'involvement', 'poisonous', 'abuse', 'defendants', 'attempted', 'sex', 'adultery', 'suspicion', 'amok'],
    
    'hack': ['cut', 'hacker', 'horse', 'drudge', 'nag', 'foul', 'chop', 'plug', 'whoop', 'jade', 'cab', 'taxi', 'taxicab', 'equus caballus', 'ward-heeler',
            'machine politician', 'literary hack', 'hack writer', 'hack on', 'cut up', 'political hack', 'edit', 'saddle horse', 'axe', 'steal', 'fleet', 'manage',
            'grapple', 'machine', 'car', 'automobile', 'auto', 'deal', 'mount', 'rugby', 'programme', 'cope', 'program', 'contend', 'cough', 'politico', 'politician',
            'ax', 'pol', 'writer', 'author', 'hoops', 'basketball', 'tool', 'motorcar', 'minicab', 'plodder', 'slogger', 'redact', 'rugger', 'dobbin'],
    
    'weapon': ['sword', 'gun', 'missile', 'spear', 'firearm', 'ammunition', 'artillery', 'projectile', 'rifle', 'pistol', 'bomb', 'bow', 'weaponry', 'arm', 'arms', 
                'knife', 'munition', 'cannon', 'guns', 'shotgun', 'tool', 'gunpowder', 'rocket', 'weapon system', 'world war ii', 'military', 'hunting', 'instrument', 
                'pike', 'bronze age', 'firearms', 'tank', 'war', 'machine gun', 'animal', 'fire ship', 'warfare', 'warhead', 'rock', 'armor', 'weapons', 'explosive',
                'intercontinental ballistic missile', 'biological warfare', 'device', 'enemy', 'deterrent', 'sidearm', 'machine', 'caliber', 'firing', 'element', 'type',
                'threat', 'target', 'dangerous', 'vehicle', 'warship', 'army', 'fire', 'weapon of mass destruction', 'ammo', 'power', 'armour', 'siege weapon',
                'technology during world war i', 'injury', 'crime', 'club', 'teeth', 'axe', 'claw', 'tusk', 'knuckles', 'flamethrower', 'slasher', 'sling', 'lance',
                'shaft', 'blade', 'brand', 'steel', 'hatchet', 'tomahawk', 'wmd', 'persuasion', 'suasion', 'stone', 'self-defense', 'hominids', 'bc', 'obsidian',
                'neolithic', 'copper', 'metal', 'cyberweapon', 'knucks', 'w.m.d.', 'fortifications', 'catapult', 'spoke', 'chariot', 'china', 'cavalry', 'assault', 
                'handgun', 'europe', 'capable', 'explosives', 'trireme', 'possessing', 'arsenal', 'bombs', 'missiles', 'lethal', 'capability', 'revolver', 'knights',
                'conventional', 'carry', 'nuclear', 'battery', 'ballistic', 'infantry', 'using']
    }

koC = {
    "아동 포르노": ["아동 성학대, 아동, 인터폴, 미국 법무부, 포르노, 비디오, 녹음, 미성년자, 소아성애, 그루밍, 유럽 위원회, 인터넷 워치 재단,\
                    미국 보고서, 법률, 사진, 조각, 드로잉, 사진, 그림, 그림, 애니메이션, 강제, 검열, 옷, 롤리콘, 누드, 카메라, 매사추세츠 주의, 녹음"],
    "호스팅": [""]
    "비트코인"
    "마약"
    "위조"
    "살인"
    "해킹"
    "무기"
}

jaC = {
    "児童ポルノ"
    "ホスティング"
    "ビットコイン"
    "麻薬"
    "偽造"
    "殺人"
    "ハッキング"
    "武器"
}

chC = {
    "儿童色情"
    "主机"
    "比特币"
    "毒品"
    "假冒"
    "谋杀"
    "黑客"
    "武器"
}

raC = {
    "детская порнография"
    "хостинг"
    "биткойн"
    "наркотики"
    "контрафактные"
    "убийства"
    "хак"
    "оружие"
}