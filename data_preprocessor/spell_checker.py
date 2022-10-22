from autocorrect import Speller

speller = Speller('ru')


def fix_typos(text):
    return speller(text)

