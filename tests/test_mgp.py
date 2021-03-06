from copy import deepcopy
from unittest import TestCase

from models.conversion_log import ConversionLog
from models.lyrics import Type, Word
from web.mgp import replace_lyrics_jap, get_titles, filter_invalid_furigana


class Test(TestCase):
    def test_replace_lyrics_jap(self):
        lyrics = "自分より下手くそな人{{ruby|别管我|べぐあんを}}あああ"
        words = [Word("自分", Type.KANJI, hiragana="じぶん"),
                 Word("下手", Type.KANJI, hiragana="へた"),
                 Word("人", Type.KANJI, hiragana="ひと"),
                 Word("别管我", Type.KANJI, hiragana="あ")]
        expected = "{{photrans|自分|じぶん}}より{{photrans|下手|へた}}くそな{{photrans|人|ひと}}{{ruby|别管我|べぐあんを}}あああ"
        self.assertEqual(expected,
                         replace_lyrics_jap(lyrics, words, ConversionLog()))
        lyrics = "自分より{{photrans|下手|へた}}くそな人{{ruby|别管我|べぐあんを}}あああ"
        words.append(Word("啊", Type.KANJI, hiragana="あ"))
        self.assertEqual(expected,
                         replace_lyrics_jap(lyrics, words, ConversionLog()))

    def test_get_titles(self):
        text = "|歌曲名称 = Test1 <br>{{lj|私}}  <br /> <span class=\"something\">{{lang|jap|Test2}}</span>\n|P主="
        existing = []
        self.assertEqual({"Test1", "私", "Test2"}, set(get_titles(text, existing)))

    def test_filter_invalid_furigana(self):
        w1 = Word(surface="空", type=Type.KANJI, hiragana="そら")
        w2 = deepcopy(w1)
        w2.hiragana = "ぞら"
        res = filter_invalid_furigana(
            [Word(surface="空", type=Type.KANJI, hiragana="ぞら")],
            [(w1, w2)]
        )
        print(res)
