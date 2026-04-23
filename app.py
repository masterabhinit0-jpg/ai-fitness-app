import streamlit as st
import os
import re
import random
from bhagavad_gita_data import CHAPTER_THEMES, GITA_TOPICS, GITA_ADVICE

# Define GITA_QUOTE_PROMPTS since it's missing in data
GITA_QUOTE_PROMPTS = [
    "Karmanye Vadhikaraste Ma Phaleshu Kadachana",
    "Yogah Karmasu Kaushalam",
    "Sarva Dharman Parityajya Mam Ekam Sharanam Vraja",
    "Vasamsi Jirnani Yatha Vihaaya Navani Grihnati",
    "Uddharet Atmanatmanam Na Atmanam Avasedayet",
    "Man Mana Bhava Mad Bhakto Mad Yaji Mam Namaskuru",
    "Sukha Duhkhe Same Kritva Labhalabhau Jayajayau",
    "Tasmad Asaktah Satatam Karyam Karma Samachara",
    "Paritranaya Sadhunam Vinashaya Cha Dushkritam",
    "Dharmaksetre Kuruksetre Samaveta Yuyutsavah"
]

BHAGAVAD_GITA_FILE = os.path.join(os.path.dirname(__file__), 'bhagavad_gita.txt')
VOWELS = set('AEIOUY')
LETTER_MAP = {
    'A': 1, 'J': 1, 'S': 1,
    'B': 2, 'K': 2, 'T': 2,
    'C': 3, 'L': 3, 'U': 3,
    'D': 4, 'M': 4, 'V': 4,
    'E': 5, 'N': 5, 'W': 5,
    'F': 6, 'O': 6, 'X': 6,
    'G': 7, 'P': 7, 'Y': 7,
    'H': 8, 'Q': 8, 'Z': 8,
    'I': 9, 'R': 9,
}

def reduce_number(value):
    while value > 9 and value not in (11, 22, 33):
        value = sum(int(digit) for digit in str(value))
    return value

def letter_value(letter):
    return LETTER_MAP.get(letter.upper(), 0)

def normalize_gender(answer):
    answer = answer.strip().lower()
    if answer in ('ladki', 'girl', 'female', 'f', 'woman'):
        return 'ladki'
    return 'ladka'

def calculate_numerology(full_name):
    letters = [ch for ch in full_name.upper() if ch.isalpha()]
    expression = sum(letter_value(ch) for ch in letters)
    soul = sum(letter_value(ch) for ch in letters if ch in VOWELS)
    personality = sum(letter_value(ch) for ch in letters if ch not in VOWELS)
    return {
        'expression': reduce_number(expression) if expression else None,
        'soul': reduce_number(soul) if soul else None,
        'personality': reduce_number(personality) if personality else None,
        'expression_raw': expression,
        'soul_raw': soul,
        'personality_raw': personality,
    }

def calculate_life_path(birthdate):
    digits = [int(ch) for ch in birthdate if ch.isdigit()]
    if len(digits) < 6:
        return None
    return reduce_number(sum(digits))

def calculate_maturity(life_path, expression):
    if life_path is None or expression is None:
        return None
    return reduce_number(life_path + expression)

def missing_karmic_numbers(full_name):
    values = {reduce_number(letter_value(ch)) for ch in full_name.upper() if ch.isalpha()}
    missing = [str(num) for num in range(1, 10) if num not in values]
    return missing

def numerology_description(number):
    descriptions = {
        1: 'Tum ek prerna dene wale neta ho. nayi shuruaat aur nirdeshan tumhari pehchan hai.',
        2: 'Tum bandhutva aur sahayog ke vyakti ho. tum samjhota aur saanjh mein vishwas karte ho.',
        3: 'Tumhara abhivyakti kaushal tej hai. rachnatmakta aur anand tumhari pehchan hai.',
        4: 'Tum sangathan aur mehnat se kaam karne wale ho. tumhari buniyad mazboot hai.',
        5: 'Tum badlav ke shaukeen ho. azaadi aur anyaay se ladne ki shakti tumhare andar hai.',
        6: 'Tum prem, seva aur zimmedari mein vishwas rakhte ho. parivar aur samaj tumhare liye mahatvapurn hai.',
        7: 'Tum gahan sochne wale ho. gyaan aur aadhyatmik khoj tumhari adhikaansh ruchi hai.',
        8: 'Tum mein udyam aur prabhavshali drishti hai. dhan aur adhikar tumhe kheenchte hain.',
        9: 'Tum ek bade uddeshya wale ho. dayalu, pehchaan yogya aur manav seva tumhara lakshya ho sakta hai.',
        11: 'Tum ek prabhaavshali aur adhyatmik soch rakhne wale ho. tum chhote se bada sapna poora kar sakte ho.',
        22: 'Tum ek brihat adyatan nirmaata ho. bade lakshyon ko vyavaharik roop dene ki kshamata tum mein hai.',
        33: 'Tum ek sachche shikshak ho. logon ko prem aur gyaan dena tumhari khasiyat hai.',
    }
    return descriptions.get(number, 'Yeh number tumhari vyaktitva yatra ko aur majboot banata hai.')

def get_gita_advice(challenge, ambition):
    text = (challenge + ' ' + ambition).lower()
    if any(keyword in text for keyword in ('dar', 'doubt', 'kise', 'asha')):
        return GITA_ADVICE['fear']
    if any(keyword in text for keyword in ('career', 'job', 'kaam', 'paisa', 'business')):
        return GITA_ADVICE['career']
    if any(keyword in text for keyword in ('pyaar', 'prema', 'love')):
        return GITA_ADVICE['love']
    if any(keyword in text for keyword in ('tanaav', 'stress', 'pressure', 'chinta')):
        return GITA_ADVICE['stress']
    if any(keyword in text for keyword in ('swasthya', 'health', 'sharir', 'bimari')):
        return GITA_ADVICE['health']
    if any(keyword in text for keyword in ('rishta', 'relationship', 'parivar', 'dosti')):
        return GITA_ADVICE['relationships']
    if any(keyword in text for keyword in ('aadhyatmik', 'spirituality', 'gyaan', 'bhakti', 'ishwar')):
        return GITA_ADVICE['spirituality']
    if any(keyword in text for keyword in ('safalta', 'success', 'jay', 'vijay')):
        return GITA_ADVICE['success']
    if any(keyword in text for keyword in ('asafalta', 'failure', 'haar', 'nakaam')):
        return GITA_ADVICE['failure']
    if any(keyword in text for keyword in ('krodh', 'anger', 'gussa')):
        return GITA_ADVICE['anger']
    if any(keyword in text for keyword in ('lobh', 'greed', 'lalach')):
        return GITA_ADVICE['greed']
    if any(keyword in text for keyword in ('irsha', 'jealousy', 'jaln')):
        return GITA_ADVICE['jealousy']
    if any(keyword in text for keyword in ('kshama', 'forgiveness', 'maaf')):
        return GITA_ADVICE['forgiveness']
    if any(keyword in text for keyword in ('dhairya', 'patience', 'sabar')):
        return GITA_ADVICE['patience']
    if any(keyword in text for keyword in ('netritva', 'leadership', 'leader')):
        return GITA_ADVICE['leadership']
    if any(keyword in text for keyword in ('dhan', 'wealth', 'paise', 'rich')):
        return GITA_ADVICE['wealth']
    if any(keyword in text for keyword in ('padhai', 'education', 'study', 'gyaan')):
        return GITA_ADVICE['education']
    if any(keyword in text for keyword in ('parivar', 'family', 'ghar')):
        return GITA_ADVICE['family']
    if any(keyword in text for keyword in ('dosti', 'friendship', 'mitra')):
        return GITA_ADVICE['friendship']
    if any(keyword in text for keyword in ('akela', 'loneliness', 'alone')):
        return GITA_ADVICE['loneliness']
    return 'Gita ka mool tatva: apne kartavya ko nishkaam bhav se karo aur man ko shaant rakho.'

def load_chapter_previews(limit=5):
    if not os.path.exists(BHAGAVAD_GITA_FILE):
        return {}
    previews = {}
    with open(BHAGAVAD_GITA_FILE, 'r', encoding='utf-8', errors='replace') as f:
        lines = [line.rstrip('\n') for line in f]
    current_chapter = None
    buffer = []
    for line in lines:
        match = re.match(r'^CHAPTER\s+([IVXLCDM]+)$', line)
        if match:
            roman = match.group(1)
            if roman not in previews:
                current_chapter = roman
                buffer = []
            continue
        if current_chapter and len(buffer) < 4 and line.strip():
            buffer.append(line.strip())
            if len(buffer) == 4:
                previews[current_chapter] = buffer[:]
                current_chapter = None
    return previews

def format_chapter_preview(roman, lines):
    chapter_number = {
        'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6,
        'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12,
        'XIII': 13, 'XIV': 14, 'XV': 15, 'XVI': 16, 'XVII': 17, 'XVIII': 18,
    }.get(roman, roman)
    title = CHAPTER_THEMES.get(chapter_number, 'Bhagavad Gita Chapter')
    result = [f'Chapter {chapter_number}: {title}']
    result.extend(lines)
    return result

def style_summary(name, age, gender, ambition, favorite_color, challenge, career_goal):
    ambition = ambition.lower()
    if 'santushti' in ambition or 'shaanti' in ambition or 'dhyaan' in ambition:
        return 'You should keep calm, use patience, and stay focused on your inner purpose.'
    if 'safalta' in ambition or 'samriddhi' in ambition or 'kamai' in ambition:
        return 'You should use your energy with discipline and aim for steady progress toward success.'
    if 'seva' in ambition or 'madad' in ambition or 'duniya' in ambition:
        return 'You should use your strength in service and lead with compassion for others.'
    if 'kalakar' in ambition or 'artist' in ambition or 'creative' in ambition:
        return 'You should express your creativity and bring your ideas into action.'
    return f'You should follow your passion for {career_goal} while keeping a positive attitude like {favorite_color}.'

def profile_summary(full_name, age, gender, city, ambition, favorite_color, challenge, career_goal):
    gender_label = normalize_gender(gender)
    style = style_summary(full_name, age, gender_label, ambition, favorite_color, challenge, career_goal)
    power = power_message(age)
    time_desc = time_message(age)

    return [
        f"Name: {full_name}",
        f"Gender: {gender_label}.",
        f"Location: {city}.",
        f"Age: {age}.",
        f"Main ambition: {ambition}.",
        f"Career focus: {career_goal}.",
        f"Current challenge: {challenge}.",
        f"Insight: {style}",
        f"Strength: {power}",
        f"Timing: {time_desc}",
        "Action 1: Start with one clear step toward your goal today.",
        "Action 2: Keep your mind calm and avoid overthinking every choice.",
        "Action 3: Use your energy in disciplined effort, not scattered activity.",
        "Action 4: Stay consistent for at least 21 days to build new habits.",
        "Action 5: Trust your sense of duty and make decisions from purpose, not fear.",
    ]

def power_message(age):
    if age < 16:
        return 'This is the time to awaken your inner power and start building your confidence.'
    if age < 30:
        return 'Your power is growing fast now, and you should use your energy with courage.'
    if age < 45:
        return 'Your power is ready, and you should use it wisely for your goals.'
    return 'Your true power comes from your experience, and you can still reach new heights.'

def time_message(age):
    if age < 16:
        return 'Your time to rise is just beginning; the next years will be very useful for you.'
    if age < 30:
        return 'Your time is coming now. With hard work and strong focus, this period can define you.'
    if age < 45:
        return 'Your real rise is starting. This can change your future if you stay determined.'
    return 'You still have time. Use your experience to create new opportunities.'

def get_topic_tagline(ambition, challenge):
    text = (ambition + ' ' + challenge).lower()
    if 'safalta' in text or 'career' in text or 'paisa' in text:
        return 'Karma Yoga: karya par dhyaan do, phal se anasaakta raho.'
    if 'shaanti' in text or 'dhyaan' in text or 'stress' in text:
        return 'Dhyana Yoga: man ko ekagrata aur shaanti mein laane ka marg.'
    if 'seva' in text or 'madad' in text or 'log' in text:
        return 'Bhakti Yoga: prem, shraddha aur seva se jeevan turn hota hai.'
    return 'Jnana Yoga: gyaan aur apne swabhav ko pehchaan kar jeevan ko sudhaaren.'

def main():
    st.title("Bhagavad Gita + Numerology Profile App")
    st.write("I will ask a few questions so your profile becomes more meaningful and useful.")

    with st.form("profile_form"):
        full_name = st.text_input('Tumhara poora naam kya hai?', value='Mitra Sharma')
        age = st.number_input('Tumhari umr kitni hai?', min_value=1, max_value=120, value=20)
        gender = st.selectbox('Tum ladka ho ya ladki?', ['ladka', 'ladki'])
        city = st.text_input('Tum kis sheher se ho?', value='apna sheher')
        ambition = st.text_input('Tumhara sapna ya ichha kya hai?', value='safalta paana')
        favorite_color = st.text_input('Tumhara pasandida rang kaun sa hai?', value='neela')
        challenge = st.text_input('Aaj tumhari sabse badi chunauti kya hai?', value='naya mauka dhundhna')
        career_goal = st.text_input('Tum kis kshetra mein kaam karna chahte ho?', value='apna vyavasaay')
        birthdate = st.text_input('Tumhari janam tithi kya hai? (DDMMYYYY ya blank)', value='')

        submitted = st.form_submit_button("Profile Generate Karo")

    if submitted:
        st.header("Your Vishleshan")

        for item in profile_summary(full_name, age, gender, city, ambition, favorite_color, challenge, career_goal):
            st.markdown(f"- {item}")

        numbers = calculate_numerology(full_name)
        life_path = calculate_life_path(birthdate) if birthdate else None
        maturity = calculate_maturity(life_path, numbers['expression']) if life_path else None
        missing = missing_karmic_numbers(full_name)

        st.header("Numerology Summary")
        if numbers['expression'] is not None:
            st.write(f"Expression/Destiny number: {numbers['expression']} - {numerology_description(numbers['expression'])}")
        if numbers['soul'] is not None:
            st.write(f"Soul urge number: {numbers['soul']} - {numerology_description(numbers['soul'])}")
        if numbers['personality'] is not None:
            st.write(f"Personality number: {numbers['personality']} - {numerology_description(numbers['personality'])}")
        if life_path is not None:
            st.write(f"Life path number: {life_path} - {numerology_description(life_path)}")
        if maturity is not None:
            st.write(f"Maturity number: {maturity} - {numerology_description(maturity)}")
        st.write(f"Karmic lesson numbers missing in your name: {', '.join(missing) if missing else 'None - sabhi numbers majood hain.'}")

        st.header("Bhagavad Gita Insights")
        st.write(get_gita_advice(challenge, ambition))
        st.write(get_topic_tagline(ambition, challenge))
        st.write('Quote suggestion: ' + random.choice(GITA_QUOTE_PROMPTS))

        st.header("Bhagavad Gita ke pramukh vishay")
        for topic in GITA_TOPICS:
            st.write('-', topic)

        st.header("Bhagavad Gita chapter themes")
        for number, theme in CHAPTER_THEMES.items():
            st.write(f'Chapter {number}: {theme}')

        previews = load_chapter_previews(limit=3)
        if previews:
            st.header("Bhagavad Gita chapter preview")
            for roman, lines in list(previews.items())[:3]:
                for line in format_chapter_preview(roman, lines):
                    st.write(line)
        else:
            st.write('Bhagavad Gita file is not available or it is not in the correct format.')

        st.write('\nDhanyavaad! You can run this app again for a deeper Gita and numerology profile.')

if __name__ == '__main__':
    main()