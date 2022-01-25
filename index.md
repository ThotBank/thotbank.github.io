# ThotBank

```yaml remark
type: primary
text: This website and the related database are under development
```

ThotBank, a part of the Madùwwe project, is a dataset of Coptic words for which an Egyptian etymology has been suggested. The datased provides the Coptic form in unicode, and automatically generated trascription, translation based on the [Comprehensive Coptic Lexicon](http://coptic-dictionary.org/about.cgi) project, the suggested Egyptian etymology with references, a translation of the Egyptian form based on the [Thesaurus Linguae Aegyptiae](http://aaew.bbaw.de/tla/index.html) project, and additional related Coptic and Egyptian words.

Dialectal variants of the Coptic forms will be added soon.

The project is currently in developement, and new entries and new references are added regularly.

```yaml package
descriptor: https://raw.githubusercontent.com/ThotBank/ThotBank/main/data/thotbank.package.yaml
```

## Header 1

Lorem ipsum

```yaml table
data: data/root.tsv
width: 600
order:
  - [3, 'desc']
columns:
  - data: root_form
  - data: root_meaning_en
  - data: tla_root_form
  - data: tla_root_id
  - data: tla_root_meaning_en
  - data: tla_root_meaning_de
```

## Header 2

Lorem ipsum

## Script

Testing Python script

```python script
print("Hello, World!")
```
