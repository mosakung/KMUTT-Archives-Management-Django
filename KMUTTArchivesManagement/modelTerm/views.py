from django.db.models import Max, F, OuterRef, Subquery, Q, Count
from datetime import datetime
import math
from django.shortcuts import render

from modelTerm.models import *
from modelTerm.serializers import *

from modelDocument.models import Document
from modelDocument.serializers import DocumentSerializer


class TermFrequency():
    def __init__(self, words, **kwargs):
        super().__init__(**kwargs)
        self.words = words

    def unique(self):
        corpus = []

        for word in self.words:
            if word not in corpus:
                corpus.append(word)

        return corpus

    def generateFrame(self):
        corpus = self.unique()
        frame = dict.fromkeys(corpus, 0)
        for word in self.words:
            frame[word] += 1
        return frame

    def calculate(self):
        frame = self.generateFrame()
        tfDict = {}
        for word, count in frame.items():
            if count == 0:
                tfDict[word] = 0
            else:
                tfDict[word] = math.log10(1 + count)
        return tfDict


class TermwordController():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def whatnew(self, tf):
        all_terms = tf.keys()
        old_terms = Term_word.objects.filter(
            term__in=all_terms
        ).values_list('term', flat=True).distinct()
        new_terms = list(set(all_terms) - set(old_terms))
        return new_terms

    def insertTermword(self, word):
        insertData = {
            'term': word,
            'frequency': 1,
            'score_idf': None,
        }
        serializer = TermWordSerializer(data=insertData)
        if serializer.is_valid():
            serializer.save()
            result = serializer.data
            return result.get('term_word_id')
        print(serializer.errors)
        return False

    def updateTermword(self, word):
        try:
            term = Term_word.objects.get(
                term=word
            )
            insertData = {
                'term': term.term,
                'frequency': term.frequency + 1,
                'rec_modified_at': datetime.now()
            }
            serializer = TermWordSerializer(
                term, data=insertData, partial=True)
            if serializer.is_valid():
                serializer.save()
                result = serializer.data
                return result.get('term_word_id')
            print(serializer.errors)
            return False
        except Term_word.DoesNotExist:
            return self.insertTermword(word)
        except Term_word.MultipleObjectsReturned:
            return False

    def patch_IDF_score(self, pkTerms):
        N = Document.objects.filter(
            status_process_document=5
        ).count() + 1

        for pk in pkTerms:
            try:
                row = Term_word.objects.get(
                    pk=pk
                )
                insertData = {
                    'term': row.term,
                    'score_idf': float("%.4f" % math.log10(N / row.frequency)),
                    'rec_modified_at': datetime.now()
                }
                serializer = TermWordSerializer(row, insertData, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
                    print("<ERROR> new patch IDF score (serializer errors)")
                    return False
            except Term_word.DoesNotExist:
                print("<ERROR> new patch IDF score (DoesNotExist)")
                return False
            except Term_word.MultipleObjectsReturned:
                print("<ERROR> new patch IDF score (MultipleObjectsReturned)")
                return False

        return True


class ScoreController():
    def __init__(self, documentId, **kwargs):
        super().__init__(**kwargs)
        self.documentId = documentId

    def insertScore(self, score, termId):
        insertData = {
            'score_tf': float("%.4f" % score),
            'score_tf_idf': None,
            'index_term_word_id': termId,
            'index_document_id': self.documentId,
            'generate_by': 'init-system'
        }
        serializer = ScoreSerializer(data=insertData)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        print(serializer.errors)
        return False

    def getPkTermInScore(self):
        rows = Score.objects.filter(index_document_id=self.documentId)
        serializer = ScoreSerializer(rows, many=True)
        result = serializer.data
        pkTerms = list(map(lambda x: x.get('index_term_word_id'), result))
        pkTerms.sort()
        return pkTerms

    def patch_TFIDF_score(self):
        rows = Score.objects.filter(
            ~Q(generate_by="init-user"),
            index_document_id=self.documentId
        )
        rows.update(
            score_tf_idf=F('score_tf') * Subquery(
                Term_word.objects.filter(
                    term_word_id=OuterRef('index_term_word_id')
                ).values('score_idf')
            ),
            generate_by="init-system"
        )
        return True


class TfIdf(TermFrequency, TermwordController, ScoreController):
    def __init__(self, words, documentId):
        self.documentId = documentId
        super().__init__(
            words=words,
            documentId=documentId
        )

    def done(self, status):
        try:
            document = Document.objects.get(pk=self.documentId)
            insertData = {
                'name': document.name,
                'status_process_document': status
            }
            serializer = DocumentSerializer(
                document, data=insertData, partial=True)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            print(serializer.errors)
            return False
        except Document.DoesNotExist:
            print("<EXCEPT> Document DoesNotExist")
            return False
        except Document.MultipleObjectsReturned:
            print("<EXCEPT> Document MultipleObjectsReturned")
            return False

    def manage(self):
        tf = self.calculate()

        for term, TFscore in tf.items():
            pkTermword = self.updateTermword(term)
            self.insertScore(TFscore, pkTermword)

        pkTerms = self.getPkTermInScore()
        self.patch_IDF_score(pkTerms)
        self.patch_TFIDF_score()
